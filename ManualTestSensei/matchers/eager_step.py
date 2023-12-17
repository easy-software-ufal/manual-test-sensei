from pipeline import Test, Step, nlp
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
import smells_names
import itertools


VISITED = 'EAGER_ACTION_VISITED'
class EagerStep:
    smell:str = smells_names.EAGER_STEP


    def __call__(self, test: Test) -> list[Test]:
        '''More than one action (imperative verbs not preceded by particles because this construction shows intent) per step.'''
        matcher = MatchersFactory.eager_step_matcher()
        all_steps = list(enumerate(test.steps))
        new_steps = dict()
        amount_matches = 0
        for (step_index, st) in all_steps:
            if st.has_flag(VISITED):
                continue
            action_matches = matcher(st.action)
            amount_matches = len(action_matches)
            # action_matches = [match for (_, start, end) in action_matches if not st.action[start:end]]
            if amount_matches > 1:
                new_steps = self.increase_new_steps(action_matches, st, amount_matches, step_index, new_steps, all_steps)
                test.steps = test.steps[0:step_index] + new_steps + test.steps[step_index+1::]
                break
        if amount_matches>1:
            return self.__call__(test)
        return [test]

    def increase_new_steps(self, action_matches, st, amount_matches, step_index, new_steps, all_steps) -> list[Step]:
        new_steps = list()
        for (match_index, (_, start, end)) in enumerate(action_matches):
            action = self.extract_action_from_match(match_index, action_matches, st, amount_matches, start)
            new_step = Step(action, [nlp('[FILL_VERIFICATION]')])
            new_step.add_flag(VISITED)
            new_steps.append(new_step)
        return new_steps

    # helpers._store_smell(st, self.smell, 'dependent clause', 'verification', st.action[start:end])
    def extract_action_from_match(self, match_index:int, action_matches:tuple, st:Step, amount_matches:int, start:int):
        if match_index == 0: # first
            (_, next_start, _) = action_matches[match_index+1]
            action = st.action[0:next_start]
        else:
            action = st.action[start::]



        if action[0].pos_ == 'CCONJ':
            action = action[1::]
        action = nlp(str(action).capitalize())
        return action