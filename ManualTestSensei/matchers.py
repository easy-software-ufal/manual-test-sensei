from collections import abc

import spacy
from spacy.tokens import Doc

import smells_names
from csv_writter import resultsWritter
from matchers_factory import MatchersFactory
from pipeline import Step, Test, Smell


def find_conditional_test_logic(index: int, test: abc.Container):
    """
    Subordinate (dependent clauses). They start with a subordinating conjunction
    """
    matcher = MatchersFactory.conditional_test_matcher()
    for step in test.steps:
        # Actions
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            _store_smell(step, smells_names.CONDITIONAL_TEST_LOGIC, 'dependent clause', 'verification', step.action[start:end])
        #Reactions
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                _store_smell(step, smells_names.CONDITIONAL_TEST_LOGIC, 'dependent clause', 'verification', reaction[start:end])

# def find_eager_step(index: int, test: abc.Container):
#     """
#     More than one action (imperative verbs not preceded by particles because this construction shows intent) per step.
#     """
#     matcher = MatchersFactory.eager_step_matcher()
#     for step in test.steps:
#         action_matches = matcher(step.action)
#         if len(action_matches) > 1: # TODO: Isso aqui é > 1 mesmo? "ao menos dois elementos?"
#             span = [step.action[start:end] for match_id, start, end in action_matches]
#             _fill_step_or_test(step, smells_names.EAGER_STEP, 'dependent clause', 'verification', step.action[start:end])
#             breakpoint()


def find_unverified_step(index: int, test: abc.Container):
    """
    Missing verification step
    """
    steps = test.steps
    unverified_steps = [step for step in steps if len(step.reactions) == 0]
    for step in unverified_steps:
        _store_smell(step, smells_names.UNVERIFIED_ACTION, '', 'action', step.action)


def find_misplaced_precondition(index: int, test: abc.Container):
    """
        The first action step declares the SUT state (e.g. 'wifi is turned off')
    """
    matcher = MatchersFactory.misplaced_precondition_matcher()
    step = test.steps[0]
    action_matches = matcher(step.action)
    for match_id, token_ids in action_matches:
        words = [step.action[token_id] for token_id in sorted(token_ids)]
        _store_smell(step, smells_names.MISPLACED_PRECONDITION, 'SUT state', 'action', words)

def find_misplaced_step(index: int, test: abc.Container):
    """
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    """
    matcher = MatchersFactory.misplaced_step_matcher()
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                _store_smell(step, smells_names.MISPLACED_STEP, '', 'verification', reaction[start:end])


def find_misplaced_result(index: int, test: abc.Container):
    """
    A verification verb (check, verify, observe, recheck) in the step description
    Interrogative sentences as steps
    SUT state declaration after any action
    """

    def get_root(doc: Doc) -> list:
        return [token for token in doc if token.dep_ == 'ROOT']

    def is_imperative_sentence(sent: Doc) -> bool:
        root = get_root(sent)
        if root and root[0].pos_ == 'VERB' and 'VerbForm=Inf' in str(root[0].morph):
            return True
        else:
            return False

    def is_interrogative_sentence(sent: Doc) -> bool:
        return sent[-1].text == '?'

    matcher = MatchersFactory.misplaced_result_verification_matcher()
    for step in test.steps:
        # First test: A verification verb in the step description
        action_matches = matcher(step.action)
        for match_id, token_ids in action_matches:
            for token_id in token_ids:
                _store_smell(step, smells_names.MISPLACED_VERIFICATION, 'verification performed', 'action', step.action[token_id])

        # Second test: Interrogative sentences as step
        for sentence in step.action.sents:
            if is_interrogative_sentence(sentence):
                _store_smell(step, smells_names.MISPLACED_VERIFICATION, 'question as step', 'action', sentence)

    # Third test: SUT state declaration after any action
    matcher = MatchersFactory.misplaced_result_affirmative_sentences()
    for step in test.steps[1:]:
        for sentence in step.action.sents:
            if not (is_interrogative_sentence(sentence) or is_imperative_sentence(sentence)):
                action_matches = matcher(sentence)
                for match_id, token_ids in action_matches:
                    words = [sentence[token_id] for token_id in sorted(token_ids)]
                    _store_smell(step, smells_names.MISPLACED_VERIFICATION, 'SUT state declaration', 'action', sentence)


def find_ambiguous_test(index: int, test: abc.Container): # TODO: Muito código repetido. Refazer
    """
        Comparative adverbs (RBR)
        Adverbs of manner(RB)
        Comparative and superlative adjectives (JJR, JJS)
        Indefinite pronouns (PRON)
    """
    # Comparative adverbs (RBR)
    matcher = MatchersFactory.ambiguous_test_comparative_adverbs_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]  # The matched span of tokens
            _store_smell(step, smells_names.AMBIGUOUS_TEST, 'comparative adverb', 'action', span)

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]  # The matched span of tokens
                _store_smell(step, smells_names.AMBIGUOUS_TEST, 'comparative adverb', 'verification', span)

    # Adverbs of manner(RB)
    matcher = MatchersFactory.ambiguous_test_adverbs_of_manner_matcher()
    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            _store_smell(step, smells_names.AMBIGUOUS_TEST, 'adverb of manner', 'action', span)

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                _store_smell(step, smells_names.AMBIGUOUS_TEST, 'comparative adverb', 'verification', span)

    # Adjectives
    matcher = MatchersFactory.ambiguous_test_adjectives_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            resultsWritter().write([test.file, index, 'Ambiguous Test', 'adjective', 'action', span, step.action])

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'adjective', 'verification', span, reaction])

    # Verb + indefinite determiner
    matcher = MatchersFactory.ambiguous_test_indefinite_determiners_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            if "Definite=Def" not in str(span[-1].morph):  # spaCy recognizes definite determiners, which we don't want
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'verb + indefinite determiner', 'action', span, step.action])

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                if "Definite=Def" not in str(
                        span[-1].morph):  # spaCy recognizes definite determiners, which we don't want
                    resultsWritter().write(
                        [test.file, index, 'Ambiguous Test', 'verb + indefinite determiner', 'verification', span, reaction])

    # Indefinite pronouns
    matcher = MatchersFactory.ambiguous_test_indefinite_pronouns_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            resultsWritter().write(
                [test.file, index, 'Ambiguous Test', 'indefinite pronoun', 'action', span, step.action])

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'indefinite pronoun', 'verification', span, reaction])


def _store_smell(container: Test|Step, smell_name:str, hint:str, where:str, term:spacy.tokens.Span) -> None:
    smell = Smell(smell_name, where, hint, term)
    container.smells.append(smell)
    return None