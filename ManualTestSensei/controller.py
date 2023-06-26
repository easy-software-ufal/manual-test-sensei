import sys
import detector_main
from transformation import transformation_main as transformation
import logging, logging.config
from pipeline import model_name
# from rich import print

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.info(f'spaCy model: {model_name}')
    try:
        if sys.argv[2] == 'all':
            detector_main.detection_runner(log)
            log.info(f'Starting transformation...')
            transformation.transformation_runner(log)
            log.info(f'FINISHED TRANSFORMATION.')
        if sys.argv[2] == 't':
            log.info(f'Starting transformation...')
            transformation.transformation_runner(log)
            log.info(f'FINISHED TRANSFORMATION.')
        if sys.argv[2] == 'd':
            detector_main.detection_runner(log)
    except:
        detector_main.detection_runner(log)
        log.info(f'Starting transformation...')
        transformation.transformation_runner(log)
        log.info(f'FINISHED TRANSFORMATION.')