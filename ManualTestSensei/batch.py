# https://docs.google.com/spreadsheets/d/19KgJ6MgGvAVZrh80dEa-ha-KUTUEVupemmBalWi3ZVM/edit#gid=523400574
from pathlib import Path
import pandas as pd
import streamlit as st
import ubuntu_data
import time
# from matchers.eager_step import EagerStep

from matchers.ambiguous_test import AmbiguousTest
from matchers.misplaced_result import MisplacedResult
from matchers_facade import  MatchersFacade
from pipeline import simplify_test
from datetime import datetime as dt
from pipeline import nlp

#'''Misplaced Result -> É o inverso de misplaced action'''
# test_file, test_index, smells_found, smells_treated, n_smells_found, n_smells_treated
ubuntu = ubuntu_data.UbuntuSmellsData()
facade = MatchersFacade()

df = pd.DataFrame(columns=['test_file', 'test_index', 'smells_found', 'smells_treated', 'n_smells_found', 'n_smells_treated'])
#TODO: implement batch execution. it should not be too hard. make a singleton df and update it everytime a new pipe runs.
file_index, file_name = st.selectbox('Select the files containing the tests', ubuntu.list_files())
for file in file_index:
    file_tests = ubuntu.by_catalog_index(file_index)
    all_tests_indexes = [index for index, value in enumerate(file_tests)]
    for index in all_tests_indexes:
        test = file_tests[index]
        df = df.append({})
        refactored_tests = facade(test)

    if refactored_tests:
        refactored_tests = [simplify_test(test) for test in refactored_tests]