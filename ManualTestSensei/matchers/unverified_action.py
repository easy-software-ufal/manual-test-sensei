from pipeline import Test, nlp
import smells_names
from matchers import helpers
from transformation import transformator
from itertools import product

_OPERATIONS = (_REMOVE:=0, _REFACTOR:=1)


class UnverifiedAction:
    smell:str = smells_names.UNVERIFIED_ACTION

    def __call__(self, test: Test):
        '''
        Missing verification step
        '''
        steps = test.steps
        unverified_actions = [step for step in steps if len(step.reactions) == 0]
        tests = list()
        if unverified_actions:
            breakpoint()
        for st in unverified_actions:
            st = transformator.unverified_action(st)
            helpers._store_smell(st, self.smell, '', 'action', st.action)

        return unverified_actions
    def _matcher(doc)
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
