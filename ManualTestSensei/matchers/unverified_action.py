from pipeline import Test, nlp
import smells_names
from matchers import helpers
from transformation import transformator

class UnverifiedAction:
    smell:str = smells_names.UNVERIFIED_ACTION

    def __call__(self, test: Test):
        '''
        Missing verification step
        '''
        steps = test.steps
        unverified_actions = [step for step in steps if len(step.reactions) == 0]
        for st in unverified_actions:
            st = transformator.unverified_action(st)
            helpers._store_smell(st, self.smell, '', 'action', st.action)
    
    