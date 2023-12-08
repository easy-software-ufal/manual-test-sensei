# https://docs.google.com/spreadsheets/d/19KgJ6MgGvAVZrh80dEa-ha-KUTUEVupemmBalWi3ZVM/edit#gid=523400574
import pandas as pd
import streamlit as st
import ubuntu_data
# from matchers.eager_step import EagerStep
from matchers.ambiguous_test import AmbiguousTest
from pipeline import simplify_test
from pipeline import nlp

st.set_page_config(layout='wide')

ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)
all_tests_indexes = [index for index, value in enumerate(file_tests)]
test_index = st.selectbox('Select the test', all_tests_indexes)

# matcher = EagerStep()
matcher = AmbiguousTest()

test = file_tests[test_index] #seleciona um único teste
initial_test = simplify_test(test)
refactored_tests = matcher(test)

if refactored_tests:
    refactored_tests = [simplify_test(test) for test in refactored_tests]
tabs = ['Initial', 'Refactored']
tabs = st.tabs(tabs)

# Initial test
with tabs[0]:
    header, test = initial_test
    st.markdown('\n'.join(header))
    with st.container():
        df = pd.DataFrame(test)
        st.table(df)

# Refactored tests
with tabs[1]:
    if refactored_tests:
        for test in refactored_tests:
            header, test = test
            st.markdown('\n'.join(header))
            with st.container():
                df = pd.DataFrame(test)
                st.table(df)
    else:
        st.table(df)