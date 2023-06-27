import sys
import logging.config
import argparse
import spacy
from collections import namedtuple
import detector_main
from transformation import transformation_main as transformation



logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)

Test = namedtuple('Test', ['file', 'header', 'steps'])
Step = namedtuple('Step', ['action', 'reactions'])

def run_code(mode):
    # log.info(f'spaCy model: {model_name[0]}')
    #nlp = create_pipeline(str(model_name[0]))
    if mode == 'all' or mode == 'detect':
        detector_main.detection_runner(log)

    if mode == 'all' or mode == 'transform':
        log.info('Starting transformation...')
        transformation.transformation_runner(log)
        log.info('FINISHED TRANSFORMATION.')


    # breakpoint()


# def create_pipeline(model_name):
#     # breakpoint()
#     nlp = spacy.load(model_name)
#     lang = nlp.meta['lang']
#     name = nlp.meta['name']
#     model_name = lang + '_' + name
#     # log.info(f'spaCy model: {model_name}')
#     return nlp

parser = argparse.ArgumentParser()
# parser.add_argument('--model', choices=['en_core_web_lg', 'en_core_web_trf', 'en_core_web_sm'], default='en_core_web_lg', nargs=1, help='Choose the model name')
parser.add_argument('--mode', choices=['all', 'transform', 'detect'], default='transform', nargs=1, help='Choose the mode of execution')
mode = sys.argv[2]
nlp = run_code(mode)
model_name = mode



