from pipeline import Test
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
import smells_names


class AmbiguousTest:
    smell:str = smells_names.AMBIGUOUS_TEST

    def __call__(self, test: Test): # TODO: Muito código repetido. Refazer
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
                helpers._store_smell(step, self.smell, 'comparative adverb', 'action', span)

        # Verifications
        for step in test.steps:
            for reaction in step.reactions:
                reaction_matches = matcher(reaction)
                for match_id, start, end in reaction_matches:
                    span = reaction[start:end]  # The matched span of tokens
                    helpers._store_smell(step, self.smell, 'comparative adverb', 'verification', span)

        # Adverbs of manner(RB)
        matcher = MatchersFactory.ambiguous_test_adverbs_of_manner_matcher()
        # Actions
        for step in test.steps:
            action_matches = matcher(step.action)
            for match_id, start, end in action_matches:
                span = step.action[start:end]
                helpers._store_smell(step, self.smell, 'adverb of manner', 'action', span)

        # Verifications
        for step in test.steps:
            for reaction in step.reactions:
                reaction_matches = matcher(reaction)
                for match_id, start, end in reaction_matches:
                    span = reaction[start:end]
                    helpers._store_smell(step, self.smell, 'comparative adverb', 'verification', span)

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
