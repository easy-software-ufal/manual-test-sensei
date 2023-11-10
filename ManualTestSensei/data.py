import re
from pathlib import Path, PosixPath
from collections import abc
from functools import singledispatch
from rich import print
import logging

log = logging.getLogger(__name__)
import pandas as pd
import numpy as np
from scipy.spatial import distance

from pipeline import nlp
from pipeline import Test, Step

DIR_COL = 'DIRETÓRIO'
FILE_COL = 'NUMERO E NOME DO ARQUIVO'
SMELL_COL = 'QUAL SMELL?'


def smells_loader_closure(mode):
    def file_exists(file) -> bool:
        if Path(file).exists():
            return True
        else:
            log.warning('Test file not found: ' + file)
            return False


    df = pd.read_csv('files.csv') # lê o caminho dos dados
    df[SMELL_COL] = df[SMELL_COL].fillna('')
    df[SMELL_COL] = df[SMELL_COL].apply(lambda x: x.replace(' ', '').split(','))
    # df2 = pd.DataFrame(df[FILE_COL])
    # print(df2[FILE_COL])
    df[FILE_COL] = df[DIR_COL] + df[FILE_COL]
    df = df[[FILE_COL, SMELL_COL]]
    df = df.loc[df[FILE_COL].apply(lambda x: file_exists(x))]
    df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))

    def smells_loader(smell_acronym: str) -> pd.DataFrame:
        """
        Will return every filepath that has the smell_acronym. If no acronym is passed, returns all.
        """
        if smell_acronym != '':
            return df.loc[df[SMELL_COL].apply(lambda x: smell_acronym in x)].reset_index(
                drop=True)  # this is a df of paths
        return df.reset_index(drop=True)

    return smells_loader


# def smells_loader_closure_v2():
#     df = pd.read_csv('dirs.txt', header=None)
#     df.columns = [FILE_COL]
#     df = df.loc[df[FILE_COL].apply(lambda x: Path(x).exists())]
#     df[FILE_COL] = df[FILE_COL].apply(lambda x: Path(x))
#     print(df)
#     return df.reset_index(drop=True)


#smells_loader = smells_loader_closure()


def k_closest_words_closure():
    vocab_ids = [x for x in nlp.vocab.vectors.keys()]
    vocab_vectors = np.array([nlp.vocab.vectors[x] for x in vocab_ids])

    def k_closest_words(input_word: str, k: int):
        input_word_vector = np.array([nlp.vocab[input_word].vector])
        # closest_indexes = distance.cdist(input_word_vector, vocab_vectors, metric='cosine').argsort()[0][:k]
        closest_indexes = distance.cdist(input_word_vector, vocab_vectors).argsort()[0][:k]
        return [nlp.vocab[vocab_ids[idx]].text for idx in closest_indexes]

    return k_closest_words


def expand_words(words, k=5) -> tuple:
    # TODO: FIX THIS FUNCTION WHEN number of words = 1
    expanded_words = [k_closest_words(w, k) for w in words]
    print(f'{words}:{expanded_words}\n')
    return tuple(set([word.lower() for word_list in expanded_words for word in word_list]))


k_closest_words = k_closest_words_closure()


def erase_split(text: str, erase: str, split: str):
    return [chunk for chunk in text.replace(erase, '').split(split) if chunk]


@singledispatch
def split_tests(text, filepath: str):
    pass


def extract_texts(text: str, filepath: str) -> abc.Container:
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

    headers = headers1 + headers2  # TODO  #17   #talvez seja necessário usar erase_split() em headers2 para que a gente consiga pegar o caso de >=3 testes no arquivo
    headers = [remove_html(header) for header in headers]

    tests = list(re.findall(tags, text))  # textão único, juntando tudo que tá dentro de <dl>
    tests = [erase_split(text=r, erase='</dt>', split='<dt>') for r in
             tests]  # se tiver mais de um caso de teste por arquivo, retorna todos os casos de teste separados
    # if len(tests)>1:
    #     
    return tests, headers


def split_tests(text: str, filepath: str) -> list:
    tests, headers = extract_texts(text, filepath)
    tests = split_tests_steps(tests)

    result = []  # lista de testes para cada filepath
    for test in tests:
        temp = Test(file=filepath, header=[header for header in headers], steps=[steps for steps in test])
        result.append(temp)
    return result


def pipeline(text: str) -> str:
    result = remove_html(text)
    log.debug('Running spacy through text')
    return nlp(result)


def remove_html(text: str):
    remove_html = re.compile('<.*?>')
    result = re.sub(remove_html, '', text)
    return result


def split_tests_steps(tests):
    result = []
    for test in tests:
        test = [erase_split(t, '</dd>', '<dd>') for t in test]
        test = [Step(pipeline(action), [pipeline(reaction) for reaction in reactions])
                for action, *reactions in test
                ]
        result.append(test)
    return result


@singledispatch
def get_tests(arg):
    """
    Pass a str with the smell acronym to read all smells with that acronym;
    Pass a pathlib.PosixPath pointing to a smell file to read all smells within that file;
    """
    pass


@get_tests.register(str)
def _(smell_acronym: str, mode):
    language = 'english'
    if language == 'english':
        log.debug(f'Starting Ubuntu Retrieving...')
        ubuntu_tests = ubuntu_get_tests(smell_acronym, mode)
        sum_ubuntu_tests = 0
        for test_list in ubuntu_tests:
            sum_ubuntu_tests += len(test_list)
        log.info(f'{sum_ubuntu_tests} Ubuntu tests retrieved.')
        return ubuntu_tests 

def ubuntu_get_tests(smell_acronym, mode):
    smells_loader = smells_loader_closure(mode)
    filepaths = [path for path in smells_loader(smell_acronym)[FILE_COL]]
    result = list()
    for path in filepaths:
        tests_in_path = [test for test in
                         split_tests(path.read_text(encoding='utf-8'), path)]  # retorna todos os testes de um path
        result.append(tests_in_path)
    log.debug('End of ubuntu retrieving')
    return result


@get_tests.register(PosixPath)
def _(filepath: PosixPath):
    return split_tests(filepath.read_text(encoding='utf-8'), filepath)
