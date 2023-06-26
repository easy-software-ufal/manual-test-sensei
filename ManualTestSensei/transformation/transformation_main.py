# try:
from . import transformation_data
from . import transformator
# except:
#     import transformation_data
#     import transformator

import logging, logging.config

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)

def transformation_runner(log):
    log = logging.getLogger(__name__)
    log.info('Initializing transformations...')
    df = transformation_data.data_closure()
    df = transformator.transformation_closure(df)

if __name__ == '__main__':
    log = logging.getLogger(__name__)
    transformation_runner(log)