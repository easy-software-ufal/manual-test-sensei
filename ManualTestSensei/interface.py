import pandas as pd
import streamlit as st
import ubuntu_data
from matchers.conditional_test_logic import ConditionalTestLogic
from matchers_facade import MatchersFacade
from pipeline import simplify_test
from pipeline import nlp

st.set_page_config(layout='wide')

ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)

conditional_test_logic = ConditionalTestLogic()
matchers = MatchersFacade()



for (test_index, test) in enumerate(file_tests):
    test.take_snapshot()
    test.steps[0].action = nlp('Fazer algo bonito')
    snapshots = [t for t in test.rollback_all()]
    tabs = [f'T_{i}' for (i, _) in enumerate(snapshots)]
    tabs = st.tabs(tabs)
    data = zip(tabs, snapshots)
    for (tab, snapshot) in data:
        with tab:
            conditional_test_logic(snapshot) # TODO: Remover essa execução do interface.py
            simplified_test = simplify_test(snapshot)
            try:
                header = test.header[test_index]
                st.write(header)
            except:
                pass
            with st.container(): # Test container
                df = pd.DataFrame(simplified_test)
                st.table(df)