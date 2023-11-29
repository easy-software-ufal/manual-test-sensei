from pipeline import Test
import smells_names
from matchers_factory import MatchersFactory
# from helpers import _store_smell
from itertools import product
import copy
from collections import Counter

_OPERATIONS = (_REMOVE:=0, _REFACTOR:=1)

class MisplacedPrecondition:
    smell:str = smells_names.MISPLACED_PRECONDITION
    _matcher = MatchersFactory.misplaced_precondition_matcher()

    def __call__(self, test: Test):
        """
            The first action step declares the SUT state (e.g. 'wifi is turned off')
        """

        number_of_steps_to_be_refactored = self.count_smelly_steps(test)
        tests = list()
        test_copy = copy.deepcopy(test)

        test_copy = self._refactor_test(test_copy, number_of_steps_to_be_refactored)
        test_copy = self._mark_step_to_deletion(test_copy, number_of_steps_to_be_refactored)

        test_copy.steps =  [step for step in test_copy.steps if step is not None]
        test_copy.header = [header for header in test_copy.header if header is not None]
        tests.append(test_copy)

        return tests

    def _mark_step_to_deletion(self, test:Test, number_of_steps:int) -> Test:
            for step_index in range(number_of_steps):
                test.steps[step_index] = None
            return test

    def count_smelly_steps(self, test : Test) -> int:
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

        counter = dict(Counter(step_smells_map))
        try:
            trues = counter[True]
        except KeyError:
            trues = 0

        return trues


    def _refactor_test(self, test:Test, number_of_steps:int) -> Test:
        for step_index in range(number_of_steps):
            st = test.steps[step_index]
            # breakpoint()
            action_matches = self._matcher(st.action)
            if action_matches:
                new_header = st.action
                test.header.append(new_header.text)
        return test