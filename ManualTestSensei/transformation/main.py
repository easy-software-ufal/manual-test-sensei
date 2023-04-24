import data
import transformation
import logging, logging.config

logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)
log = logging.getLogger(__name__)
if __name__ == '__main__':
    log.info('Initializing transformations...')
    data.data_closure()
    breakpoint()