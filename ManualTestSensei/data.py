from pathlib import Path, PosixPath
import logging
from collections import abc
log = logging.getLogger(__name__)
import pandas as pd
from pipeline import Step, Test, nlp


DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

class SmellsData:
    '''This `abstract` class is intended to be inherited by the classes containing the data of the tests. Example: Ubuntu Tests.'''
    def __init__(self, tests_catalog_file:str):
        self.tests_catalog_file = tests_catalog_file
        self.tests_catalog = None
        self._load_tests_catalog()


    def by_acronym(self, smell_acronym: str) -> pd.DataFrame:
        """
        Will return every filepath that has the smell_acronym. If no acronym is passed, returns all.
        """
        if smell_acronym != '':
            return self.tests_catalog.loc[self.tests_catalog[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True)  # this is a df of paths
        return self.tests_catalog.reset_index(drop=True)

    def by_path(self, filepath: PosixPath):
        return self._split_tests(filepath.read_text(encoding='utf-8'), filepath)

    def by_catalog_index(self, index:int) -> abc.Container:
        return self.by_path(self[index])

    def list_files(self) -> list:
        files = [(index, str(value.name)) for (index, value) in self.tests_catalog[FILE_COL].reset_index().values]
        return files

    def __getitem__(self, index:int) -> PosixPath:
        return self.tests_catalog.iloc[index][FILE_COL]

    def _split_tests(self, text: str, filepath: str) -> list:
        tests, headers = self._extract_texts(text, filepath)
        tests = self._split_tests_steps(tests)

        result = []  # lista de testes para cada filepath
        for (index, test) in enumerate(tests):
            temp = Test(file=filepath, header=[ headers[index] ], steps=[steps for steps in test])
            result.append(temp)
        return result

    def _load_tests_catalog(self):
        def file_exists(file) -> bool:
            if Path(file).exists():
                return True
            else:
                log.warning('Test file not found: ' + file)
                return False

        df = pd.read_csv(self.tests_catalog_file)
        df[SMELL_COL] = df[SMELL_COL].fillna('')
        df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
        df[FILE_COL] = df[DIR_COL] + df[FILE_COL]
        df = df[[FILE_COL, SMELL_COL]]
        df = df.loc[df[FILE_COL].apply(lambda x: file_exists(x))]
        df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))
        self.tests_catalog = df
