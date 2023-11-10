import pandas as pd
import streamlit as st
import ubuntu_data
from matchers.conditional_test_logic import ConditionalTestLogic
from matchers.unverified_action import  UnverifiedAction
from matchers_facade import MatchersFacade
from pipeline import simplify_test
from pipeline import nlp

st.set_page_config(layout='wide')

ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)
all_tests_indexes = [index for index, value in enumerate(file_tests)]
test_index = st.selectbox('Select the test', all_tests_indexes)

conditional_test_logic = ConditionalTestLogic()
unverified_action = UnverifiedAction()
matchers = MatchersFacade()


test = file_tests[test_index]
initial_state = simplify_test(test)
unverified_action(test)
test = simplify_test(test)

snapshots = [initial_state, test]
tabs = [f'T_{i}' for (i, _) in enumerate(snapshots)]
tabs = st.tabs(tabs)
data = zip(tabs, snapshots)

for (tab, snapshot) in data:
    with tab:
        try:
            header = test.header[test_index]
            st.write(header)
        except:
            pass
        with st.container(): # Test container
            df = pd.DataFrame(snapshot)
            st.table(df)