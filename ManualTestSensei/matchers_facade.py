from matchers import (ambiguous_test, conditional_test_logic, eager_step,
                      misplaced_precondition, unverified_action, misplaced_result, misplaced_action)
from ubuntu_data import UbuntuSmellsData
from pipeline import Test

class MatchersFacade:
    '''This class is responsible for applying the smells detections of any smell. It contains an instance of each matcher.'''
    multiplicative_pipeline = (conditional_test_logic.ConditionalTestLogic(),)
    non_multiplicative_pipeline =  (
        misplaced_action.MisplacedAction(), # Extract Actions
        eager_step.EagerStep(), # Separate Actions
        misplaced_result.MisplacedResult(), # Extract Verifications
        ambiguous_test.AmbiguousTest(), # Extract Ambiguities
        misplaced_precondition.MisplacedPrecondition(), # Extract Preconditions
        unverified_action.UnverifiedAction(), # Fill Verifications
    )

    def __call__(self, tests:Test|list[Test]) -> list[Test]:
        result = list()
        if isinstance(tests, Test):
            tests = [tests]
        tests = self._call_multiplicative_pipeline(tests)
        for pipe in self.non_multiplicative_pipeline:
            for test in tests:
                result = result+pipe(test)
        return list(set(result))

    def _call_multiplicative_pipeline(self, tests:Test|list[Test]) -> list[Test]:
        initial_size = len(tests)
        result = list()
        for pipe in self.multiplicative_pipeline:
            for test in tests:
                result = result+pipe(test)
        if len(result) == initial_size:
            return result
        return self._call_multiplicative_pipeline(result)


    def _pipeline_tostr(self) ->list[str]:
        pipeline = [m for m in dir(MatchersFacade) if not m.startswith('_')] # Ignores dunders and private attributes.
        return pipeline

if __name__ == '__main__':
    facade = MatchersFacade()
    tests = UbuntuSmellsData('ubuntu_files.csv') #files.csv contains ubuntu files
    test = tests.by_catalog_index(2)[0]
    facade(test)


