import pandas as pd
import streamlit as st
import ubuntu_data
from matchers import find_conditional_test_logic
from pipeline import simplify_test

st.set_page_config(layout='wide')

ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)

for (test_index, test) in enumerate(file_tests):
    find_conditional_test_logic(test) # TODO: Remover essa execução do interface.py
    simplified_test = simplify_test(test)
    try:
        header = test.header[test_index]
        st.write(header)
    except:
        pass
    with st.container(): # Test container
        df = pd.DataFrame(simplified_test)
        df = df.drop(columns='where')
        st.table(df)