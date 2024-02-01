import streamlit as st
st.set_page_config(
    page_title="Smipps",
    layout="wide"
    )
from GUI.GUI_class import FIELD_DEVELOPMENT
st.title('Field Development')
field_development = FIELD_DEVELOPMENT()