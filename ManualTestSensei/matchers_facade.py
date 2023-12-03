from matchers import (ambiguous_test, conditional_test_logic, eager_step,
                      misplaced_precondition, unverified_action, misplaced_result)
from ubuntu_data import UbuntuSmellsData
from pipeline import Test

class MatchersFacade:
    '''This class is responsible for applying the smells detections of any smell. It contains an instance of each matcher.'''
    pipeline =  (
    eager_step.EagerStep(),
    misplaced_precondition.MisplacedPrecondition(),
    unverified_action.UnverifiedAction(),
    conditional_test_logic.ConditionalTestLogic(),
    # misplaced_result.MisplacedResult(),
    # ambiguous_test.AmbiguousTest()
    )

    def __call__(self, tests:Test|list[Test]) -> list[Test]:
        result = list()
        if isinstance(tests, Test):
            tests = [tests]
        for pipe in self.pipeline:
            for test in tests:
                result = result+pipe(test)
        return result

    def _pipeline_tostr(self) ->list[str]:
        pipeline = [m for m in dir(MatchersFacade) if not m.startswith('_')] # Ignores dunders and private attributes.
        return pipeline

if __name__ == '__main__':
    facade = MatchersFacade()
    tests = UbuntuSmellsData('ubuntu_files.csv') #files.csv contains ubuntu files
    test = tests.by_catalog_index(2)[0]
    facade(test)