from pipeline import Test
import smells_names
from matchers_factory import MatchersFactory
# from helpers import _store_smell
from itertools import product
import copy

_OPERATIONS = (_REMOVE:=0, _REFACTOR:=1)

class MisplacedPrecondition:
    smell:str = smells_names.MISPLACED_PRECONDITION
    _matcher = MatchersFactory.misplaced_precondition_matcher()

    def __call__(self, test: Test):
        """
            The first action step declares the SUT state (e.g. 'wifi is turned off')
        """
        # step = test.steps[0]
        # action_matches = matcher(step.action)
        # for match_id, token_ids in action_matches:
        #     words = [step.action[token_id] for token_id in sorted(token_ids)]
        #     _store_smell(step, self.smell, 'SUT state', 'action', words)
        truth_table = self._map_smelly_steps(test)
        tests = list()
        for row in truth_table:
            test_copy = copy.deepcopy(test)
            for (step_index, operation) in row:
                if operation == _REMOVE:
                    test_copy = self._mark_step_to_deletion(test_copy, step_index)
                elif operation == _REFACTOR:
                    test_copy = self._refactor_test(test_copy, step_index)
            test_copy.steps =  [step for step in test_copy.steps if step is not None]
            tests.append(test_copy)
        return tests

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
            # if action_matches:
            #     breakpoint()
            # print(f'action_matches:{action_matches}')

            #172 é um problemático
            if action_matches:
                step_smells_map.append(True)
            else:
                step_smells_map.append(False)
        step_smells_map = [index for (index, has_smell) in enumerate(step_smells_map) if has_smell]

        operations_truth_table = list(product((_REMOVE, _REFACTOR), repeat=len(step_smells_map)))
        operations_truth_table = [list(zip(step_smells_map, row)) for row in operations_truth_table]
        return operations_truth_table


    def _refactor_test(self, test:Test, step_index:int) -> Test:
        st = test.steps[step_index]
        action_matches = self._matcher(st.action)
        if action_matches:
            new_header = st.action
            test.header.append(new_header.text)
        return test