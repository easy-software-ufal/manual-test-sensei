import copy
from pipeline import Test, nlp
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
from itertools import product
import smells_names

_OPERATIONS = (_REMOVE := 0, _REFACTOR := 1)


class AmbiguousTest:
    smell: str = smells_names.AMBIGUOUS_TEST
    matcher_comparative_adverbs = MatchersFactory.ambiguous_test_comparative_adverbs_matcher()
    matcher_manner = MatchersFactory.ambiguous_test_adverbs_of_manner_matcher()
    matcher_adjective = MatchersFactory.ambiguous_test_adjectives_matcher()
    matcher_indef_det = MatchersFactory.ambiguous_test_indefinite_determiners_matcher()
    matcher_indef_pron = MatchersFactory.ambiguous_test_indefinite_pronouns_matcher()
    matchers = [matcher_comparative_adverbs, matcher_manner,
                matcher_adjective, matcher_indef_det, matcher_indef_pron]

    def process_matches_action(self, step, matcher, smell_type, attribute, additional_action=None):
        matches = matcher(step.action)
        for _, start, end in matches:
            span = step.action[start:end]
            if additional_action:
                additional_action(step, self.smell, smell_type, attribute, span, step.action)
            else:
                helpers._store_smell(step, self.smell, smell_type, attribute, span)

    def process_reaction_matches(self, step, matcher, smell_type, attribute, filter_definite_det=False, additional_action=None):
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for _, start, end in reaction_matches:
                span = reaction[start:end]
                if filter_definite_det and "Definite=Def" in str(span[-1].morph):
                    helpers._store_smell(
                                step, self.smell, 'verb + indefinite determiner', 'verification', span, reaction)
                    print(step, self.smell, 'verb + indefinite determiner', 'verification', span, reaction)

                helpers._store_smell(step, self.smell, smell_type, attribute, span, reaction)


    def process_indefinite_determiner_action(self, step):
        matches = self.matcher_indef_det(step.action)
        for _, start, end in matches:
            span = step.action[start:end]
            # spaCy recognizes definite determiners, which we don't want
            if "Definite=Def" not in str(span[-1].morph):
                self.process_matches_action(step, self.matcher_indef_det, 'verb + indefinite determiner', 'action')

    def process_action(self, step_number, step):
        self.process_matches_action(step.action, self.matcher_comparative_adverbs, 'comparative adverb', 'action')
        self.process_matches_action(step.action, self.matcher_adjective, 'adjective', 'action', additional_action=helpers._store_smell)
        self.process_matches_action(step.action, self.matcher_manner, 'adverb of manner', 'action')
        self.process_matches_action(step.action, self.matcher_indef_pron, 'indefinite pronoun', 'action')
        self.process_indefinite_determiner_action(step)
        print(step_number,step.action)

    def process_reaction(self, step_number, step):
        for reaction in step.reactions:
            self.process_reaction_matches(reaction, self.matcher_comparative_adverbs, 'comparative adverb', 'verification')
            self.process_reaction_matches(reaction, self.matcher_manner, 'adverb of manner', 'verification')
            self.process_reaction_matches(reaction, self.matcher_adjective, 'adjective', 'verification')
            self.process_reaction_matches(reaction, self.matcher_indef_pron, 'indefinite pronoun', 'verification')
            self.process_reaction_matches(reaction, self.matcher_indef_det, 'verb + indefinite determiner', 'verification', filter_definite_det=True)
        print(step_number,step.reactions)

    def __call__(self, test: Test) -> Test:  # TODO: Muito código repetido. Refazer
        """
            Comparative adverbs (RBR)
            Comparative and superlative adjectives (JJR, JJS)

            Adverbs of manner(RB) --> excluir token do adverbio de modo
            Indefinite pronouns (PRON) --> meter um asterisco e mandar o usuario resolver o problema

        """

        test_copy = copy.deepcopy(test)

        # for (step_number, step) in enumerate(test.steps):
        #     self.process_matches_action(step, self.matcher_comparative_adverbs, 'comparative adverb', 'action')
        #     self.process_matches_action(step, self.matcher_adjective, 'adjective', 'action', additional_action=helpers._store_smell)
        #     self.process_matches_action(step, self.matcher_manner, 'adverb of manner', 'action')
        #     self.process_matches_action(step, self.matcher_indef_pron, 'indefinite pronoun', 'action')
        #     self.process_indefinite_determiner_action(step)

        for (step_number, step) in enumerate(test.steps):
                    self.process_action(step_number, step)
                    self.process_reaction(step_number, step)

        # # Actions
        # for (step_number, step) in enumerate(test.steps):
        #     action_matches = matcher_comparative_adverbs(step.action)
        #     for _, start, end in action_matches:
        #         span = step.action[start:end]  # The matched span of tokens
        #         helpers._store_smell(
        #             step, self.smell, 'comparative adverb', 'action', span)

        #     action_matches = matcher_manner(step.action)
        #     for _, start, end in action_matches:
        #         span = step.action[start:end]
        #         helpers._store_smell(
        #             step, self.smell, 'adverb of manner', 'action', span)

        #     action_matches = matcher_adjective(step.action)
        #     for _, start, end in action_matches:
        #         span = step.action[start:end]
        #         helpers._store_smell(
        #             step, self.smell, 'adjective', 'action', span, step.action)

        #     action_matches = matcher_indef_det(step.action)
        #     for _, start, end in action_matches:
        #         span = step.action[start:end]
        #         # spaCy recognizes definite determiners, which we don't want
        #         if "Definite=Def" not in str(span[-1].morph):
        #             helpers._store_smell(
        #                 step, self.smell, 'verb + indefinite determiner', 'action', span, step.action)

        #     action_matches = matcher_indef_pron(step.action)
        #     for _, start, end in action_matches:
        #         span = step.action[start:end]
        #         helpers._store_smell(
        #             step, self.smell, 'indefinite pronoun', 'action', span, step.action)

        #     for reaction in step.reactions:
        #         reaction_matches = matcher_comparative_adverbs(reaction)
        #         for _, start, end in reaction_matches:
        #             span = reaction[start:end]  # The matched span of tokens
        #             helpers._store_smell(
        #                 step, self.smell, 'comparative adverb', 'verification', span)

        #     for reaction in step.reactions:
        #         reaction_matches = matcher_manner(reaction)
        #         for _, start, end in reaction_matches:
        #             span = reaction[start:end]
        #             helpers._store_smell(
        #                 step, self.smell, 'comparative adverb', 'verification', span)

        #     for reaction in step.reactions:
        #         reaction_matches = matcher_adjective(reaction)
        #         for _, start, end in reaction_matches:
        #             span = reaction[start:end]
        #             helpers._store_smell(
        #                 step, self.smell, 'adjective', 'verification', span, reaction)

        #     for reaction in step.reactions:
        #         reaction_matches = matcher_indef_det(reaction)
        #         for _, start, end in reaction_matches:
        #             span = reaction[start:end]
        #             if "Definite=Def" not in str(
        #                     span[-1].morph):  # spaCy recognizes definite determiners, which we don't want
        #                 helpers._store_smell(
        #                     step, self.smell, 'verb + indefinite determiner', 'verification', span, reaction)

        #     for reaction in step.reactions:
        #         reaction_matches = matcher_indef_pron(reaction)
        #         for _, start, end in reaction_matches:
        #             span = reaction[start:end]
        #             helpers._store_smell(
        #                 step, self.smell, 'indefinite pronoun', 'verification', span, reaction)

        return [test,]

    def _map_smelly_steps(self, test: Test) -> list:
        '''
        Returns the truth table where each row indicates wheter a step will be removed or refactored.
        '''
        step_smells_map = list()
        for (index, st) in enumerate(test.steps):
            action_matches = self._matcher(st.action)
            if action_matches:
                step_smells_map.append(True)
            else:
                step_smells_map.append(False)
        step_smells_map = [index for (index, has_smell) in enumerate(
            step_smells_map) if has_smell]

        operations_truth_table = list(
            product((_REMOVE, _REFACTOR), repeat=len(step_smells_map)))
        operations_truth_table = [
            list(zip(step_smells_map, row)) for row in operations_truth_table]
        return operations_truth_table
