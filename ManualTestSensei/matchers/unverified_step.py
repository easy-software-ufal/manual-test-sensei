from pipeline import Test
import smells_names
from matchers import helpers

class UnverifiedStep:
    smell:str = smells_names.UNVERIFIED_STEP

    def __call__(self, test: Test):
        """
        Missing verification step
        """
        steps = test.steps
        unverified_steps = [step for step in steps if len(step.reactions) == 0]
        for step in unverified_steps:
            helpers._store_smell(step, self.smell, '', 'action', step.action)