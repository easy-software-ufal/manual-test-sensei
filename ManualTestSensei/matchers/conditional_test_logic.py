from collections import abc
from pipeline import nlp

import smells_names
import spacy
from matchers_factory import MatchersFactory
from pipeline import Test
from matchers import helpers
import smells_names

class ConditionalTestLogic:
    smell = smells_names.CONDITIONAL_TEST_LOGIC

    def __call__(self, test: Test) -> list[Test]:
        '''
        Subordinate (dependent clauses). They start with a subordinating conjunction
        '''
        matcher = MatchersFactory.conditional_test_matcher()
        for (index, st) in enumerate(test.steps):
            # Actions
            action_matches = matcher(st.action)
            if action_matches:
                doc = st.action
                first_subtree = [tuple(tkn.subtree)[1::] for tkn in doc if tkn.pos_ == 'VERB']
                if first_subtree:
                    first_subtree = first_subtree[0]
                    text = ' '.join([tkn.text for tkn in first_subtree])
                    st.action = nlp(doc[1::].text.capitalize())
                    text = 'Ensure' + ' ' + ' '.join([tkn.text for tkn in first_subtree])
                    test.header = [text] + test.header
            for match_id, start, end in action_matches:
                helpers._store_smell(st, self.smell, 'dependent clause', 'verification', st.action[start:end])








            # #Reactions
            # for reaction in st.reactions:
            #     reaction_matches = matcher(reaction)
            #     for match_id, start, end in reaction_matches:
            #         helpers._store_smell(st, self.smell, 'dependent clause', 'verification', reaction[start:end])