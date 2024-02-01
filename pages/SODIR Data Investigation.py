import streamlit as st
st.set_page_config(
    page_title="Smipps",
    layout="wide"
    )
from GUI.GUI_class import SODIR_feature
st.title('Sodir Data Investigation')
NPD_DATA = SODIR_feature()
