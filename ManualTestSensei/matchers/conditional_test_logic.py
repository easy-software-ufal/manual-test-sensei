from collections import abc
from pipeline import nlp
import copy
from itertools import product


import smells_names
import spacy
from matchers_factory import MatchersFactory
from pipeline import Test
from matchers import helpers
import smells_names

_OPERATIONS = (_REMOVE:=0, _REFACTOR:=1)

class ConditionalTestLogic:
    smell = smells_names.CONDITIONAL_TEST_LOGIC
    _matcher = MatchersFactory.conditional_test_matcher()

    def __call__(self, test: Test) -> list[Test]:
        '''
        Subordinate (dependent clauses). They start with a subordinating conjunction
        '''

        truth_table = self._map_smelly_steps(test)
        tests = list()
        for row in truth_table:
            # Actions
            test_copy = copy.deepcopy(test)
            for (step_index, operation) in row:
                if operation == _REMOVE:
                    test_copy = self._mark_step_to_deletion(test_copy, step_index)
                elif operation == _REFACTOR:
                    test_copy = self._refactor_test(test_copy, step_index)
            test_copy.steps =  [step for step in test_copy.steps if step is not None]
            tests.append(test_copy)
                # for (match_id, start, end) in action_matches:
                #     helpers._store_smell(st, self.smell, 'dependent clause', 'verification', st.action[start:end])
        if len(tests) == 1:
            return [test, ]
        return tests

    def _refactor_test(self, test:Test, step_index:int) -> Test:
        st = test.steps[step_index]
        action_matches = self._matcher(st.action)
        if action_matches:
            doc = st.action
            first_subtree = [tuple(tkn.subtree)[1::] for tkn in doc if tkn.pos_ == 'VERB']
            if first_subtree:
                first_subtree = first_subtree[0]
                text = ' '.join([tkn.text for tkn in first_subtree])
                st.action = nlp(doc[1::].text.capitalize())
                text = 'Ensure' + ' ' + ' '.join([tkn.text for tkn in first_subtree])
                test.header = [text] + test.header
        return test

    def _mark_step_to_deletion(self, test:Test, step_index:int) -> Test:
        test.steps[step_index] = None
        return test


    def _map_smelly_steps(self, test : Test) -> list:
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
        step_smells_map = [index for (index, has_smell) in enumerate(step_smells_map) if has_smell]

        operations_truth_table = list(product((_REMOVE, _REFACTOR), repeat=len(step_smells_map)))
        operations_truth_table = [list(zip(step_smells_map, row)) for row in operations_truth_table]
        return operations_truth_table







            # #Reactions
            # for reaction in st.reactions:
            #     reaction_matches = matcher(reaction)
            #     for match_id, start, end in reaction_matches:
            #         helpers._store_smell(st, self.smell, 'dependent clause', 'verification', reaction[start:end])