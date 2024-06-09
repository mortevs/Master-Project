import streamlit as st
import pages.GUI.GUI_functions as GUI
import time
from Data.dataProcessing import get_field_list_inc_No_field_chosen
from Data.DefaultData import defaultData_RP


class RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA:
    def __init__(self):
        try:
            self.__fieldnames = get_field_list_inc_No_field_chosen()
        except Exception as e:
            st.write(e)
            st.warning("could not get list of fieldnames from SODIR")
            self.__fieldnames = ["None"]
            

        self.place_holder = 1
        on_information = st.toggle("Show me information on how to use the reservoir pressure from production data feature", value=False, label_visibility="visible")
        if on_information:
            st.write(""" The user has some options for running the model. As per now only one equation is available, but the user can choose to fetch
                     monthly or yearly production rates from Sodir using the dropdownmenu below on the left side""")

            st.write(""" Choose production data from an NCS-field from the dropdown menu below, or upload data in csv format with
                     column 0 - date (year/ year-month), column 1 - gas produced in 1E06 Sm3""")

            st.write("""Click <Run Analysis> to estimate the reservoir pressure for a field chosen, or for the uploaded data.
                      The numbers in the table below on the right side will be used for the estimation. The user can change these numbers before
                     clicking <Run Analysis>""")

            st.write("""An alternative to clicking <Run Analysis> is to click <Get NPD-data for field>. The IGIP and Reservoir pressure will be
                     fetched from NPD and an analysis wil be run with this data. """)


            st.write("""Click <Clear output> to remove all the plots and start over again""")

        uploaded = st.file_uploader(label = "Upload production data as CSV file, or choose field and time frame from drop-down menus below")
        col0, col1 = st.columns(2)
        with col0:
            eq = GUI.dropdown(label = 'What equation do you want to use?', options = ['Material balance with Z-factor calculation'], labelVisibility="visible")
            if eq == 'Backpressure equation':
                pass
            field = GUI.dropdown(label = 'Get gas production data from the following field:', options = self.__fieldnames, labelVisibility="visible")
            selected_time = GUI.dropdown(label = 'Choose yearly or monthly producted volumes', options = ['Yearly', 'Monthly'], labelVisibility="visible")

        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.run_R_analysis import ReservoirPressureAnalysis
        RES_Analysis = ReservoirPressureAnalysis(parent = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA, session_id='ReservoirPressureAnalysis')
        RES_Analysis.updateFromDropDown(fieldName= field, time = selected_time)
        RES_Analysis.update_from_upload(uploaded)
        with col1:
            col2, col3, col4= st.columns(3)
            with col2:
                run = st.button('Run Analysis', 'Run RP', use_container_width=True)
            with col3:
                clear = st.button('Clear output', 'clear RESPRES', use_container_width=True)
            with col4:
                SODIR_button = st.button('Get Sodir-data', 'get SODIR data into table', use_container_width=True)
            default_message = st.warning("Default values below. Change to desired values")
        if SODIR_button and field == 'No field chosen':
            alert3 = st.warning('Choose a field')
            time.sleep(3.5)
            alert3.empty()

        if run and field == 'No field chosen' and uploaded == None:
            alert3 = st.warning('Choose a field or upload data')
            time.sleep(3.5)
            alert3.empty()

        elif SODIR_button and field != 'No field chosen':
            parameters = []
            self.place_holder = 2

        with col1:
            if self.place_holder == 1:
                parameters = RES_Analysis.updateParameterListfromTable(list2 = defaultData_RP())

            elif self.place_holder ==2:
                PRi = 276 #reservoir pressure bara #default value
                gasMolecularWeight = 16 #[g/mol] default value
                PRi, T, gasMolecularWeight, IGIP = RES_Analysis.get_Sodir_data_Res_Pres()
                updated_list = [PRi, T, gasMolecularWeight, IGIP]
                RES_Analysis.updateParameterListfromTable(list2 = updated_list)
                alert4 = st.warning('Found estimates for IGIP and Temperature. Running Analysis with the data above')
                time.sleep(3)
                alert4.empty()
                if field != 'No field chosen' and selected_time == 'Yearly':
                    result = RES_Analysis.runY()
                    RES_Analysis.append_result(result)

                elif field != 'No field chosen' and selected_time == 'Monthly':
                    result = RES_Analysis.runM()
                    RES_Analysis.append_result(result)

        if run and field != 'No field chosen' and selected_time == 'Yearly':
            result = RES_Analysis.runY()
            RES_Analysis.append_result(result)

        elif run and field != 'No field chosen' and selected_time == 'Monthly':
            result = RES_Analysis.runM()
            RES_Analysis.append_result(result)

        elif run and uploaded != None:
            result = RES_Analysis.run_uploaded()
            RES_Analysis.append_result(result)

        if clear:
            RES_Analysis.clear_output()
        RES_Analysis.getParameters()
        if parameters != defaultData_RP():
            default_message.empty()
        RES_Analysis.plot()
email_address = "morten.viersi@gmail.com"
email_subject_Help = "Get help with the SMIPPS application"
email_body_Help = "Hi Morten, \n\n I need help with using the SMIPPS Application. I need help with the following: .........."
email_subject_BUG = "Report a SMIPPS Bug"
email_body_BUG = "Hi Morten, \n\n I'm sending you an email experiencing a bug while using the SMIPPS Application. I experienced the bug after performing the following steps .........."
email_link_Help = f"mailto:{email_address}?subject={email_subject_Help}&body={email_body_Help}"
email_link_BUG = f"mailto:{email_address}?subject={email_subject_BUG}&body={email_body_BUG}"

st.set_page_config(
    page_title="Smipps",
    layout="wide",
    page_icon=":wrench:",
    menu_items={'Get Help': email_link_Help,
    'Report a bug': email_link_BUG,
    'About': "# Master project by Morten Vier Simensen"
}
    )
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(264, 49, 49);
}
</style>""", unsafe_allow_html=True)
st.title('Reservoir Pressure from Production Data')
reservoir_pressure_from_production_data = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA()

