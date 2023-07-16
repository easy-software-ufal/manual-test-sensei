import streamlit as st
import pandas as pd

import data

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

file = st.selectbox('Select the files containing the tests', data.get_files()[data.FILE_COL])
st.write(str(type(file)))
