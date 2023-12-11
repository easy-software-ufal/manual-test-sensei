from pipeline import Test, Step, nlp
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
import smells_names

TINY_NUMBER = 0.00005 # HackUsed to sort the substeps

class EagerStep:
    smell:str = smells_names.EAGER_STEP


    def __call__(self, test: Test) -> list[Test]:
        '''More than one action (imperative verbs not preceded by particles because this construction shows intent) per step.'''
        matcher = MatchersFactory.eager_step_matcher()
        all_steps = list(enumerate(test.steps))
        new_steps = dict()
        for (step_index, st) in all_steps:
            action_matches = matcher(st.action)
            amount_matches = len(action_matches)
            if amount_matches > 1:
                new_steps = self.increase_new_steps(action_matches, st, amount_matches, step_index, new_steps, all_steps)
        all_steps = sorted(all_steps, key=lambda x: x[0])
        all_steps = [step for (index, step) in all_steps if index not in new_steps]
        test.steps = all_steps
        return [test]

    def increase_new_steps(self, action_matches, st, amount_matches, step_index, new_steps, all_steps) -> list[Step]:
        for (match_index, (_, start, end)) in enumerate(action_matches):
            action = self.extract_action_from_match(match_index, action_matches, st, amount_matches, start)

            new_step = Step(action, [nlp('[FILL_VERIFICATION]')])
            if step_index in new_steps:
                position = (step_index + (len(new_steps[step_index]) * TINY_NUMBER))
                new_step = (position, new_step)
                new_steps[step_index] = new_step
                all_steps.append(new_step)
            else:
                new_steps[step_index] = list()
                new_step = (step_index + TINY_NUMBER, new_step)
                new_steps[step_index].append(new_step)
                all_steps.append(new_step)
        try:
            (_, st) = all_steps[step_index]
        except:
            st = [st for st in all_steps if step_index == st[0]][0][1]
        all_steps[-1][-1].reactions = st.reactions
        return new_steps

    # helpers._store_smell(st, self.smell, 'dependent clause', 'verification', st.action[start:end])
    def extract_action_from_match(self, index:int, action_matches:tuple, st:Step, amount_matches:int, start:int):
        if index == 0: # first
            (_, next_start, _) = action_matches[index+1]
            action = st.action[0:next_start]
        elif index+1 == amount_matches: #last
            action = st.action[start::]
        else:
            (_, _, previous_end) = action_matches[index-1]
            action = st.action[previous_end::]
        if action[0].pos_ == 'CCONJ':
            action = action[1::]
        action = nlp(str(action).capitalize())
        return action