from pathlib import Path, PosixPath
import logging
log = logging.getLogger(__name__)
import pandas as pd




DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'

class SmellsData:
    def __init__(self, tests_catalog_file:str):
        self.tests_catalog_file = tests_catalog_file
        self.tests_catalog = None
        self._load_tests_catalog()


    def by_aconym(self, smell_acronym: str) -> pd.DataFrame:
        """
        Will return every filepath that has the smell_acronym. If no acronym is passed, returns all.
        """
        if smell_acronym != '':
            return self.tests_catalog.loc[self.tests_catalog[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(drop=True)  # this is a df of paths
        return self.tests_catalog.reset_index(drop=True)

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
        self.tests_catalog =df



if __name__ == '__main__':
    data = SmellsData('ubuntu_files.csv') #files.csv contains ubuntu files