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

            indefinite_determinant_smells = self._apply_indefinite_matcher(st, self.matcher_indef_det)
            if indefinite_determinant_smells:
                st.smells = st.smells+indefinite_determinant_smells
            indefinite_pronouns_smells = self._apply_indefinite_matcher(st, self.matcher_indef_pron)
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

    def _apply_indefinite_matcher(self, st:Step, matcher) -> Smell:
        def refactor(doc:Doc, location:str, matcher) -> list[Smell]:
            matches = matcher(doc)
            smells = list()
            if matches:
                for (_, start, end) in matches:
                    smell = Smell(self.smell, doc[start:end].text, f'Define the following for the {location}')
                    smells.append(smell)
            return smells
        action_smells = refactor(st.action, 'action', matcher)
        reaction_smells = list()
        for reaction in st.reactions:
            reaction_smells = reaction_smells + refactor(reaction, 'verification', matcher)
        smells = action_smells + reaction_smells
        return smells