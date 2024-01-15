from pathlib import Path
import ubuntu_data
import time
# from matchers.eager_step import EagerStep

from matchers_facade import  MatchersFacade
from pipeline import simplify_test
from data import FILE_COL

#'''Misplaced Result -> É o inverso de misplaced action'''

ubuntu = ubuntu_data.UbuntuSmellsData()


facade = MatchersFacade()

files_index = list(range(len(ubuntu.tests_catalog[FILE_COL])))
files = (ubuntu.by_catalog_index(file_index) for file_index in files_index)

for tests in files:
    for test in tests:
        facade(test)
        print('rodou')
