import csv
import time
from pipeline import model_name
import logging
log = logging.getLogger(__name__)

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class resultsWritter(metaclass=SingletonMeta):

    csv_writer = ''

    def __init__(self):
        log.debug('Starting resultsWritter.')
        csv_header = ['Test file', 'Test index', 'Smell', 'Hint', 'Where', 'Term', 'Sentence']
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = 'results-' + timestr +'-'+model_name+'.csv'
        file = open(filename, 'w', encoding="UTF8", newline='')
        self.csv_writer = csv.writer(file)
        self.csv_writer.writerow(csv_header)

    def write(self, row: []):
        self.csv_writer.writerow(row)
