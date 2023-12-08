from spacy.tokens import Doc
from pipeline import Test,Step, Smell, nlp
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
from itertools import product
import smells_names

_OPERATIONS = (_REMOVE := 0, _REFACTOR := 1)


class AmbiguousTest:
    smell: str = smells_names.AMBIGUOUS_TEST
    # matcher_comparative_adverbs = MatchersFactory.ambiguous_test_comparative_adverbs_matcher()
    # matcher_adjective = MatchersFactory.ambiguous_test_adjectives_matcher()


    matcher_indef_det = MatchersFactory.ambiguous_test_indefinite_determiners_matcher()
    matcher_indef_pron = MatchersFactory.ambiguous_test_indefinite_pronouns_matcher()

    def __call__(self, test: Test) -> Test:  # TODO: Muito código repetido. Refazer
        '''
            Comparative adverbs (RBR)
            Comparative and superlative adjectives (JJR, JJS)

            Indefinite pronouns (PRON) --> meter um asterisco e mandar o usuario resolver o problema
            Adverbs of manner(RB) --> excluir token do adverbio de modo
        '''
        for (step_index, st) in enumerate(test.steps):
            mode_adverbs_smells = self._apply_mode_adverbs(st)

            indefinite_determinant_smells = self._apply_indefinite_determinant(st, self.matcher_indef_det)
            if indefinite_determinant_smells:
                st.smells = st.smells+indefinite_determinant_smells
            indefinite_pronouns_smells = self._apply_indefinite_determinant(st, self.matcher_indef_pron)
            if indefinite_pronouns_smells:
                st.smells = st.smells+indefinite_pronouns_smells
        return [test,]

    def _apply_mode_adverbs(self, st:Step) -> Step:
        def refactor(doc:Doc) -> Doc:
            matcher = MatchersFactory.ambiguous_test_adverbs_of_manner_matcher()
            matches = matcher(doc)
            new_text = doc.text
            for (_, start, end) in matches:
                new_text = new_text.replace(doc[start:end].text, '')
            if new_text == doc.text:
                return None
            return nlp(new_text)

        new_doc = refactor(st.action)
        if new_doc:
            st.action = new_doc

        for (reaction_index, reaction) in enumerate(st.reactions):
            new_doc = refactor(reaction)
            if new_doc:
                st.reactions[reaction_index] = new_doc
        return st

    def _apply_indefinite_determinant(self, st:Step, matcher) -> Smell:
        def refactor(doc:Doc, location:str, matcher) -> list[Smell]:
            matches = matcher(doc)
            smells = list()
            if matches:
                for (_, start, end) in matches:
                    smell = Smell(self.smell, doc[start:end].text, f'Define this for the {location}')
                    smells.append(smell)
            return smells
        action_smells = refactor(st.action, 'action', matcher)
        reaction_smells = list()
        for reaction in st.reactions:
            reaction_smells = reaction_smells + refactor(reaction, 'verification', matcher)
        smells = action_smells + reaction_smells
        return smells

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
                if filter_definite_det and 'Definite=Def' in str(span[-1].morph):
                    helpers._store_smell(
                                step, self.smell, 'verb + indefinite determiner', 'verification', span, reaction)
                    print(step, self.smell, 'verb + indefinite determiner', 'verification', span, reaction)

                helpers._store_smell(step, self.smell, smell_type, attribute, span, reaction)


    def process_indefinite_determiner_action(self, step):
        matches = self.matcher_indef_det(step.action)
        for _, start, end in matches:
            span = step.action[start:end]
            # spaCy recognizes definite determiners, which we don't want
            if 'Definite=Def' not in str(span[-1].morph):
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
