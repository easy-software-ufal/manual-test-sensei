import sys
import logging.config
import argparse
import spacy
import pandas as pd
from collections import namedtuple
import detector_main
from transformation import transformation_main
from transformation import transformation_data
from transformation import transformator

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)

Test = namedtuple('Test', ['file', 'header', 'steps'])
Step = namedtuple('Step', ['action', 'reactions'])

def no_test_left_to_transform(df):
    return len(df) == transformator.skipped_tests

def run_code(mode):
    # log.info(f'spaCy model: {model_name[0]}')
    #nlp = create_pipeline(str(model_name[0]))
    
    if mode == 'all' or mode == 'detect' or mode == 'd':
        detector_main.detection_runner(log, "d")

    if mode == 'all' or mode == 'transform' or mode =='t':
        #detector_main.detection_runner(log, "d")
        log.info('Starting transformation...')
        count = 0
        #while True:
        file = transformation_data.get_csv_path()
        df = pd.read_csv(file)
        
        transformation_main.transformation_runner(log)
        #detector_main.detection_runner(log, "d")
            # if count > 0:
            #     detector_main.detection_runner(log, "t")
            # else:
            #     detector_main.detection_runner(log, "d")
            
            
            # if no_test_left_to_transform(df):
            #     break
            # count += 1
        
        log.info('FINISHED TRANSFORMATION.')


# def create_pipeline(model_name):
#     # breakpoint()
#     nlp = spacy.load(model_name)
#     lang = nlp.meta['lang']
#     name = nlp.meta['name']
#     model_name = lang + '_' + name
#     # log.info(f'spaCy model: {model_name}')
#     return nlp
#

#TODO: #1 tries to fix this argparse. it's so elegant...
# parser = argparse.ArgumentParser()
# # parser.add_argument('--model', choices=['en_core_web_lg', 'en_core_web_trf', 'en_core_web_sm'], default='en_core_web_lg', nargs=1, help='Choose the model name')
# parser.add_argument('--mode', choices=['all', 'transform', 'detect'], default='transform', nargs=1, help='Choose the mode of execution')
mode = sys.argv[2]
nlp = run_code(mode)
model_name = mode



#use python controller.py <model> <mode>
#where model needs to be one of ['trf','sm','lg']
#where mode needs to be one of ['all','transform','detect']