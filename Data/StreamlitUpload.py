import streamlit as st
import pandas as pd
from io import StringIO
def upload(text ='Upload a file')->pd.DataFrame:
    uploaded_file = st.file_uploader(text)
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)
        string_data = stringio.read()
        st.write(string_data)
        dataframe = pd.read_csv(uploaded_file)
        return dataframe
