import streamlit as st
import pandas as pd

import ubuntu_data
from pipeline import simplify_test
from matchers import find_conditional_test_logic
st.set_page_config(layout='wide')


ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)

header = ''
header_new = ''
for test in file_tests:
  find_conditional_test_logic(1, test) # TODO: Remover essa execução do interface.py
  simplified_test = simplify_test(test)
  header_new = '\n'.join(test.header)
  if header_new != header:
    st.write(header_new)
    header = header_new
  with st.container(): # Test container
    df = pd.DataFrame(simplified_test)
    df = df.drop(columns='where')
    st.table(df)