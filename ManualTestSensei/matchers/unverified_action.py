from pipeline import Test, nlp
import smells_names
from transformator import Transformator

class UnverifiedAction(Transformator):
    def __init__(self):
        self.smell = smells_names.UNVERIFIED_ACTION
        super().__init__()

    def __call__(self, test: Test) -> list[Test]:
        '''Missing verification step'''
        self.start_counting_time()
        for step in test.steps:
            if len(step.reactions) == 0:
                if len(step.action) == 0:
                    continue
                step.reactions = [nlp('[FILL_VERIFICATION]'), ]
                step.smells.append(self.smell)
        self.stop_counting_time()
        return [test, ]