from pipeline import Test
import smells_names
from matchers_factory import MatchersFactory

class MisplacedPrecondition:
    smell:str = smells_names.MISPLACED_PRECONDITION

    def __call__(self, test: Test):
        """
            The first action step declares the SUT state (e.g. 'wifi is turned off')
        """
        matcher = MatchersFactory.misplaced_precondition_matcher()
        step = test.steps[0]
        action_matches = matcher(step.action)
        for match_id, token_ids in action_matches:
            words = [step.action[token_id] for token_id in sorted(token_ids)]
            _store_smell(step, self.smell, 'SUT state', 'action', words)