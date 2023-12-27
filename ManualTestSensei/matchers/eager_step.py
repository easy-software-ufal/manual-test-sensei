from pipeline import Test, Step, nlp
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
import smells_names
import itertools
from spacy.util import filter_spans


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

            try:
                action_matches = matcher(st.action, as_spans=True)
            except ValueError as _:
                action_matches = matcher(st.action)
                action_matches = [st.action[start:end] for (_, start, end) in action_matches]
            action_matches = list(filter_spans(action_matches))
            action_matches = [(-1,span.start, span.end) for span in action_matches]
            amount_matches = len(action_matches)
            # action_matches = [match for (_, start, end) in action_matches if not st.action[start:end]]
            if amount_matches > 1:
                new_steps = self.increase_new_steps(action_matches, st, amount_matches, step_index, new_steps, all_steps)
                test.steps = test.steps[0:step_index] + new_steps + test.steps[step_index+1::] #what happens if step_index = ultimo?
                break
        if amount_matches>1:
            return self.__call__(test)
        return [test]

    def increase_new_steps(self, action_matches, st:Step, amount_matches, step_index, new_steps, all_steps) -> list[Step]:
        action_matches = [(start, end) for (_, start, end) in action_matches]
        old_reactions = list()
        if st.reactions:
            old_reactions = st.reactions
        new_steps = list()

        action_matches = [start for (start, _) in action_matches]
        action_matches[0] = 0
        action_matches.append(len(st.action)+1)
        _starts = list(action_matches)
        _starts.pop()
        _ends = list(action_matches)
        _ends.pop(0)
        action_matches = list(zip(_starts, _ends))
        for (match_index, (start, end)) in enumerate(action_matches):
            action = self.extract_action_from_match(st.action, start, end)
            if match_index == len(action_matches) - 1:
                new_step = Step(action, old_reactions)
            else:
                new_step = Step(action, [nlp('[FILL_VERIFICATION]')])
            new_step.add_flag(VISITED)
            new_steps.append(new_step)
        return new_steps
    # helpers._store_smell(st, self.smell, 'dependent clause', 'verification', st.action[start:end])


    def extract_action_from_match(self, action, start:int, end:int):
        span = action[start:end]
        if span[0].pos_ == 'CCONJ':
            span = span[1::]
        span = nlp(str(span).capitalize())
        return span