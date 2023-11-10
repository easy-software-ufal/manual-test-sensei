import logging.config
from pathlib import Path
from data import get_tests
import matchers

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)

def detection_runner(log):
    csvs = sorted(Path('.').glob('*.csv'))
    csvs = [s for s, s in enumerate(csvs) if 'results' in str(s)]
    if len(csvs) == 0:
        log.info('Retrieving tests...')  # logging.info
        tests = get_tests('')  # lista com todos os testes originais
        log.info('Analyzing...')
        for (file_index, test_file) in enumerate(tests):
            for (test_index, test) in enumerate(test_file):
                #matchers.conditional_test_logic(test_index, test)
                # matchers.find_eager_step(test_index, test)
                # matchers.find_unverified_action(test_index, test)
                matchers.find_misplaced_precondition(test_index, test)
                # matchers.find_misplaced_step(test_index, test)
                # matchers.find_misplaced_result(test_index, test)
                #matchers.find_ambiguous_test(test_index, test)
        log.info('Analysis complete!')
    else: #after 1st detection, we get the tests from the transformed_testcases
        log.info('TODO: implement after 1st detection')

if __name__ == '__main__':
    log.info('Program started.')
    detection_runner(log)