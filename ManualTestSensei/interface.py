# https://docs.google.com/spreadsheets/d/19KgJ6MgGvAVZrh80dEa-ha-KUTUEVupemmBalWi3ZVM/edit#gid=523400574
import pandas as pd
import streamlit as st
import ubuntu_data
from matchers.conditional_test_logic import  ConditionalTestLogic
from pipeline import simplify_test
from pipeline import nlp

st.set_page_config(layout='wide')

ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)
all_tests_indexes = [index for index, value in enumerate(file_tests)]
test_index = st.selectbox('Select the test', all_tests_indexes)

matcher = ConditionalTestLogic()


test = file_tests[test_index]
(initial_header, initial_state) = simplify_test(test)
matcher(test)
(header, simplified) = simplify_test(test)

snapshots = [(initial_header, initial_state), (header, simplified)]
tabs = [f'T_{i}' for (i, _) in enumerate(snapshots)]
tabs = st.tabs(tabs)
data = zip(tabs, snapshots)


for (tab, content) in data:
    header, snapshot = content
    with tab:
        st.write(header)
        with st.container(): # Test container
            df = pd.DataFrame(snapshot)
            st.table(df)