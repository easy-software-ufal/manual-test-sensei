import re
from collections import abc
from functools import singledispatch
from pathlib import Path, PosixPath
import logging
log = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from rich import print
from scipy.spatial import distance

import data
from data import SmellsData
from pipeline import Step, Test, nlp

# def _k_closest_words_closure():
#     vocab_ids = [x for x in nlp.vocab.vectors.keys()]
#     vocab_vectors = np.array([nlp.vocab.vectors[x] for x in vocab_ids])

#     def k_closest_words(input_word: str, k: int):
#         input_word_vector = np.array([nlp.vocab[input_word].vector])
#         # closest_indexes = distance.cdist(input_word_vector, vocab_vectors, metric='cosine').argsort()[0][:k]
#         closest_indexes = distance.cdist(input_word_vector, vocab_vectors).argsort()[0][:k]
#         return [nlp.vocab[vocab_ids[idx]].text for idx in closest_indexes]

#     return k_closest_words


# def _expand_words(words, k=5) -> tuple:
#     # TODO: FIX THIS FUNCTION WHEN number of words = 1
#     expanded_words = [k_closest_words(w, k) for w in words]
#     print(f'{words}:{expanded_words}\n')
#     return tuple(set([word.lower() for word_list in expanded_words for word in word_list]))




class UbuntuSmellsData(SmellsData):
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
        language_disclaimer = r'(?<=<em>)(.+?)(?=</em>)'

        text = re.sub(re.compile(language_disclaimer), '', text)
        text = re.sub(re.compile(comments), ' ', text)
        text = re.sub(re.compile(spaces), ' ', text)
        text = re.sub(re.compile(breaks), ' ', text)
        text = re.sub(re.compile(trailing_whitespace), '>', text)

        mid_header = r'(?<=<\/dl>)(.+?)(?=<dl>)'
        init_header = r'(?<=^)(.+?)(?=<dl>)'

        headers1 = list(re.findall(init_header, text))
        headers2 = list(re.findall(mid_header, text))

        headers = headers1 + headers2  # TODO  #17   #talvez seja necessário usar self.erase_split() em headers2 para que a gente consiga pegar o caso de >=3 testes no arquivo
        headers = [self.remove_html(header) for header in headers]

        tests = list(re.findall(tags, text))  # textão único, juntando tudo que tá dentro de <dl>
        tests = [self._erase_split(text=r, erase='</dt>', split='<dt>') for r in tests]  # se tiver mais de um caso de teste por arquivo, retorna todos os casos de teste separados
        # if len(tests)>1:
        #     breakpoint()
        return tests, headers

    def split_tests(self, text: str, filepath: str) -> list:
        tests, headers = self._extract_texts(text, filepath)
        tests = self.split_tests_steps(tests)

        result = []  # lista de testes para cada filepath
        for test in tests:
            temp = Test(file=filepath, header=[header for header in headers], steps=[steps for steps in test])
            result.append(temp)
        return result

    def pipeline(self, text: str) -> str:
        result = self.remove_html(text)
        log.debug('Running spacy through text')
        return nlp(result)

    def remove_html(self, text: str):
        remove_html = re.compile('<.*?>')
        result = re.sub(remove_html, '', text)
        return result

    def split_tests_steps(self, tests):
        result = []
        for test in tests:
            test = [self._erase_split(t, '</dd>', '<dd>') for t in test]
            test = [Step(self.pipeline(action), [self.pipeline(reaction) for reaction in reactions])
                    for action, *reactions in test
                    ]
            result.append(test)
        return result

    def by_acronym(self, smell_acronym: str):
        filepaths = super().by_aconym(smell_acronym)[data.FILE_COL]
        result = list()
        for path in filepaths:
            tests_in_path = [test for test in self.split_tests(path.read_text(encoding='utf-8'), path)]  # retorna todos os testes de um path
            result.append(tests_in_path)
        log.debug('End of ubuntu retrieving')
        return result

    def by_path(filepath: PosixPath):
        return split_tests(filepath.read_text(encoding='utf-8'), filepath)


if __name__ == '__main__':
    ubuntu = UbuntuSmellsData('ubuntu_files.csv')
    tests = ubuntu.by_acronym('US')