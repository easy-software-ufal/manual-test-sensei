from matchers import (ambiguous_test, conditional_test_logic, eager_step,
                      misplaced_precondition, unverified_action, misplaced_result)
from ubuntu_data import UbuntuSmellsData
from pipeline import Test

class MatchersFacade:
    '''This class is responsible for applying the smells detections of any smell. It contains an instance of each matcher.'''

    condition_test_logic = conditional_test_logic.ConditionalTestLogic()
    eager_step = eager_step.EagerStep()
    # ambiguous_test = ambiguous_test.AmbiguousTest() # TODO: Fix this test
    misplaced_precondition = misplaced_precondition.MisplacedPrecondition()
    unverified_action = unverified_action.UnverifiedAction()
    misplaced_result = misplaced_result.MisplacedResult()

    def __call__(self, test:Test) -> bool:
        pipeline = (getattr(MatchersFacade,m) for m in self.pipeline_tostr())
        for pipe in pipeline:
            pipe(test)
        return True

    def pipeline_tostr(self) ->list[str]:
        pipeline = [m for m in dir(MatchersFacade) if not m.startswith('_')] # Ignores dunders and private attributes.
        return pipeline

if __name__ == '__main__':
    facade = MatchersFacade()
    tests = UbuntuSmellsData('ubuntu_files.csv') #files.csv contains ubuntu files
    test = tests.by_catalog_index(2)[0]
    facade(test)