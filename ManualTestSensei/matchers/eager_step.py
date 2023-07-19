from pipeline import Test
import smells_names
from matchers_factory import MatchersFactory
from matchers import helpers
import smells_names

class EagerStep:
    smell:str = smells_names.EAGER_STEP

    def __call__(self, test: Test):
        """
        More than one action (imperative verbs not preceded by particles because this construction shows intent) per step.
        """
        matcher = MatchersFactory.eager_step_matcher()
        for step in test.steps:
            action_matches = matcher(step.action)
            if len(action_matches) > 1: # TODO: Isso aqui é > 1 mesmo? "ao menos dois elementos?"
                _, start, end = action_matches[0]
                helpers._store_smell(step, self.smell, 'dependent clause', 'verification', step.action[start:end])