import logging
import re
from collections import abc
from functools import singledispatch
from pathlib import Path, PosixPath

log = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from rich import print
from scipy.spatial import distance

import data
from data import SmellsData
from pipeline import Step, Test, nlp


class UbuntuSmellsData(SmellsData):
    '''This class keeps the Ubuntu tests'''

    def __init__(self, tests_catalog_file:str='ubuntu_files.csv'):
        return super().__init__(tests_catalog_file)

    def by_acronym(self, smell_acronym:str) -> abc.Container:
        filepaths = super().by_acronym(smell_acronym)[data.FILE_COL]
        result = list()
        for path in filepaths:
            tests_in_path = [test for test in self._split_tests(path.read_text(encoding='utf-8'), path)]  # retorna todos os testes de um path
            result.append(tests_in_path)
        log.debug('End of ubuntu retrieving')
        return result

    def pipeline(self, text: str) -> str:
        result = self._remove_html(text)
        log.debug('Running spacy through text')
        return nlp(result)

    def _erase_split(self, text: str, erase: str, split: str):
        return [chunk for chunk in text.replace(erase, '').split(split) if chunk]

    def _extract_texts(self, text: str, filepath: str) -> abc.Container:
        """
        Gets the raw text from the filepath as well the filepath as a string and returns a list containing the parsed
        raw texts from the tests.
        """
        spaces = r'\s{2,}'
        breaks = r'\n'
        trailing_whitespace = r'> '

        test_title = r'(?<=<strong>)(.+?)(?=</strong>)'
        test_header = r'(?<=^)(.+?)(?=<dl>)|(?<=</dl>)(.+?)(?=<dl>)'  # it's the title and the preconditions
        comments = r'(?<=<!--)(.+?)(?=-->)'
        tags = r'(?<=<dl>)(.+?)(?=</dl>)'
        dls = r'(<dl>)(.+?)(?=</dl>)'

        language_disclaimer = r'(?<=<em>)(.+?)(?=</em>)'

        text = re.sub(re.compile(language_disclaimer), '', text)
        text = re.sub(re.compile(comments), ' ', text)
        text = re.sub(re.compile(spaces), ' ', text)
        text = re.sub(re.compile(breaks), ' ', text)
        text = re.sub(re.compile(trailing_whitespace), '>', text)

        mid_header = r'(?<=<\/dl>)(.+?)(?=<dl>)'
        init_header = r'(?<=^)(.+?)(?=<dl>)'

        if text.strip().startswith('<dl>'):
            headers1 = ''
        else:
            headers1 = list(re.findall(init_header, text))
        headers2 = list(re.findall(mid_header, text))
        headers = [self._remove_html(sentence) for sentence in re.sub(dls,'<<REPLACEME>>', text).split('<<REPLACEME>>')][0:-1]

        tests = list(re.findall(tags, text))  # textão único, juntando tudo que tá dentro de <dl>
        tests = [self._erase_split(text=r, erase='</dt>', split='<dt>') for r in tests]  # se tiver mais de um caso de teste por arquivo, retorna todos os casos de teste separados
        return tests, headers


    def _remove_html(self, text: str):
        remove_html = re.compile('<.*?>')
        result = re.sub(remove_html, '', text)
        return result

    def _split_tests_steps(self, tests):
        result = []
        for test in tests:
            test = [self._erase_split(t, '</dd>', '<dd>') for t in test]
            test = [Step(self.pipeline(action), [self.pipeline(reaction) for reaction in reactions])
                    for action, *reactions in test
                    ]
            result.append(test)
        return result

if __name__ == '__main__':
    tests = UbuntuSmellsData('ubuntu_files.csv') #files.csv contains ubuntu files
    tests.by_catalog_index(1)