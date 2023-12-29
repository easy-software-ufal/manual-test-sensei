# https://docs.google.com/spreadsheets/d/19KgJ6MgGvAVZrh80dEa-ha-KUTUEVupemmBalWi3ZVM/edit#gid=523400574
from pathlib import Path
import pandas as pd
import streamlit as st
import ubuntu_data
import time
import pygame
# from matchers.eager_step import EagerStep

from matchers.ambiguous_test import AmbiguousTest
from matchers.misplaced_result import MisplacedResult
from matchers_facade import  MatchersFacade
from pipeline import simplify_test
from datetime import datetime as dt
from pipeline import nlp

#'''Misplaced Result -> É o inverso de misplaced action'''

st.set_page_config(layout='wide', page_title='Manual Test Alchemist', page_icon=':alembic:')
st.write('# :alembic: Manual Test *Alchemist* :alembic:')
st.write('*Transforming your tests into better ones!* ')
ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, file_name = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)
all_tests_indexes = [index for index, value in enumerate(file_tests)]
test_index = st.selectbox('Select the test', all_tests_indexes)

start_time = time.time()  # Record the start time
# print(start_time)
elapsed_time_element = st.empty()

# matcher = EagerStep()
matcher = MisplacedResult()
facade = MatchersFacade()

submit_button = st.button(label='Transform :sparkles:')

test = file_tests[test_index] #seleciona um único teste

if submit_button:
    formatted_start_time = dt.fromtimestamp(start_time).strftime('%d-%m-%Y %H:%M:%S')
    print(f'{formatted_start_time} | Processing: {file_name} - {test_index} ')

    initial_test = simplify_test(test)
    refactored_tests = facade(test)

    end_time = time.time()  # Record the end time
    formatted_end_time = dt.fromtimestamp(end_time).strftime('%d-%m-%Y %H:%M:%S')

    print(f'{formatted_end_time} | Done.')
    # print(end_time)
    deltatime = end_time - start_time
    print(f'{dt.now().strftime("%d-%m-%Y %H:%M:%S")} | Total time elapsed: {deltatime}')
    elapsed_time_element.write(f"Total time taken for transformation: {deltatime:.2f} seconds")

    pygame.mixer.init()
    pygame.mixer.music.load("sound.wav")
    pygame.mixer.music.play()

    # Wait for the sound to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    if refactored_tests:
        refactored_tests = [simplify_test(test) for test in refactored_tests]
    tabs = ['Initial', 'Refactored']
    # tabs = st.tabs(tabs)

    # Initial test
    # with tabs[0]:
    header, test = initial_test
    st.markdown('# Original Test')
    st.markdown('\n'.join(header))
    with st.container():
        df = pd.DataFrame(test)
        st.table(df)
    st.divider()
    st.markdown('# Transformed Test(s)')
    # Refactored tests
    # with tabs[1]:
    if refactored_tests:
        for test in refactored_tests:
            header, test = test
            st.markdown('\n'.join(header))
            with st.container():
                df = pd.DataFrame(test)
                st.table(df)
    else:
        st.table(df)    