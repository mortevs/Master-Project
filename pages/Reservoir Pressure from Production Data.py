import streamlit as st
st.set_page_config(
    page_title="Smipps",
    layout="wide"
    )
from GUI.GUI_class import RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA
st.title('Reservoir Pressure from Production Data')
reservoir_pressure_from_production_data = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA()

