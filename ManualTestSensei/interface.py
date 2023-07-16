import streamlit as st
import pandas as pd

import ubuntu_data
from pipeline import simplify_test
st.set_page_config(layout='wide')


ubuntu = ubuntu_data.UbuntuSmellsData()

file_index, _ = st.selectbox('Select the files containing the tests', ubuntu.list_files())
file_tests = ubuntu.by_catalog_index(file_index)

for test in file_tests:
  simplified_test = simplify_test(test)
  with st.container(): # Test container
    df = pd.DataFrame(simplified_test)
    st.table(df)