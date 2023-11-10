from collections import abc

from spacy.tokens import Doc

from csv_writter import resultsWritter
from matchers_factory import MatchersFactory


def find_conditional_test_logic(index: int, test: abc.Container):
    """
    Subordinate (dependent clauses). They start with a subordinating conjunction
    """
    matcher = MatchersFactory.conditional_test_matcher()
    for step in test.steps:
        # Actions
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            resultsWritter().write(
                [test.file, index, 'Conditional Test Logic', 'dependent clause', 'action', span, step.action])

        # Verifications
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                resultsWritter().write(
                    [test.file, index, 'Conditional Test Logic', 'dependent clause', 'verification', span, reaction])


def find_eager_step(index: int, test: abc.Container):
    """
    More than one action (imperative verbs not preceded by particles because this construction shows intent) per step.
    """
    matcher = MatchersFactory.eager_step_matcher()
    for step in test.steps:
        action_matches = matcher(step.action)
        if len(action_matches) > 1:
            span = []
            for match_id, start, end in action_matches:
                substring = step.action[start:end]
                span.append(str(substring))
            resultsWritter().write([test.file, index, 'Eager Action', 'multiple actions', 'action', span, step.action])


def find_unverified_step(index: int, test: abc.Container):
    """
    Missing verification step
    """
    steps = test.steps
    unverified_steps = [step for step in steps if len(step.reactions) == 0]
    for step in unverified_steps:
        resultsWritter().write([test.file, index, 'Unverified Action', '', 'action', '', step.action])


def find_misplaced_precondition(index: int, test: abc.Container):
    """
        The first action step declares the SUT state (e.g. 'wifi is turned off')
    """
    matcher = MatchersFactory.misplaced_precondition_matcher()
    
    step = test.steps[0]
    action_matches = matcher(step.action)
    for match_id, token_ids in action_matches:
        words = [step.action[token_id] for token_id in sorted(token_ids)]
        resultsWritter().write(
            [test.file, index, 'Misplaced Precondition', 'SUT state', 'action', words, step.action])

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
                span = reaction[start:end]
                resultsWritter().write([test.file, index, 'Misplaced Action', '', 'verification', span, reaction])


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
                resultsWritter().write(
                    [test.file, index, 'Misplaced Verification', 'verification performed', 'action', step.action[token_id], step.action])

        # Second test: Interrogative sentences as step
        for sentence in step.action.sents:
            if is_interrogative_sentence(sentence):
                resultsWritter().write(
                    [test.file, index, 'Misplaced Verification', 'question as step', 'action', '', sentence])

    # Third test: SUT state declaration after any action
    matcher = MatchersFactory.misplaced_result_affirmative_sentences()
    for step in test.steps[1:]:
        for sentence in step.action.sents:
            if not (is_interrogative_sentence(sentence) or is_imperative_sentence(sentence)):
                action_matches = matcher(sentence)
                for match_id, token_ids in action_matches:
                    words = [sentence[token_id] for token_id in sorted(token_ids)]
                    resultsWritter().write(
                        [test.file, index, 'Misplaced Verification', 'SUT state declaration', 'action', words, sentence])


def find_ambiguous_test(index: int, test: abc.Container):
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
            resultsWritter().write(
                [test.file, index, 'Ambiguous Test', 'comparative adverb', 'action', span, step.action])

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]  # The matched span of tokens
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'comparative adverb', 'verification', span, reaction])

    # Adverbs of manner(RB)
    matcher = MatchersFactory.ambiguous_test_adverbs_of_manner_matcher()

    # Actions
    for step in test.steps:
        action_matches = matcher(step.action)
        for match_id, start, end in action_matches:
            span = step.action[start:end]
            resultsWritter().write(
                [test.file, index, 'Ambiguous Test', 'adverb of manner', 'action', span, step.action])

    # Verifications
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                span = reaction[start:end]
                resultsWritter().write(
                    [test.file, index, 'Ambiguous Test', 'adverb of manner', 'verification', span, reaction])

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
