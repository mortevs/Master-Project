import streamlit as st, time, os

class main_page_GUI:
    def __init__(self):
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
        col1, col2, col3, col4, col5 = st.columns(5)
        with col5:
            load = st.button('Load New Data from Sodir',  'sodir')
        if load:
            from Data.getData import deleteAndLoadNewDataFromNPD
            deleteAndLoadNewDataFromNPD()
            timestamp = time.ctime()
            alert00 = st.warning('Data downloaded from Sodir ' + timestamp)
            time.sleep(5)
            alert00.empty()
        st.title('Simulation and Modeling of Integrated Petroleum Production Systems')
        st.write(" ")
        st.write(" ")
        col1, col2 = st.columns(2)
        with col1:
            my_path = os.path.join('Data', 'Storage', 'Morten_front_page.png')
            st.image(my_path)
        with col2:
            on_more_about = st.toggle("Show me more information about the Master project", value=False, label_visibility="visible")
            on_information = st.toggle("Show me more information on how to use the application", value=False, label_visibility="visible")
            if on_information:
                st.write(
                            """The application is connected to Sodir (https://www.sodir.no/). Data can automatically be pulled from Sodirs open data sources,
                        before being used in the application. The data includes field, well and production data. The data is stored
                        in the application. The button in the top right corner <Load New Data from Sodir> deletes the stored data, and fetches the latest data
                        at Sodir. Sodir data are updated every night. During this time, Sodir's services and portals are unavailable, and the user will not be able
                        fetch data.""")
                st.write("""The application has several features available through different pages. The user can navigate between the pages in the menu to the left. The features per December 2023 are Field Development,
                            Reservoir Pressure From Production Data, and SODIR Data Investigation. The user can switch back and forth among the pages. The resulting plots
                            will be stored/cached while the application is running.""")

                st.write("""The field development feature can be used for estimating production profiles for dry-gas fields.
                            The reservoir pressure from production data feature can be used for estimating the decline in pressure for a dry-gas reservoir when the produced gas rates are known.
                            The Sodir data feature can be used for NCS field investigation. The feature offers a service that lets you compare production volumes
                            from different fields and plot the reservoir area (polygon) with well locations.""")

            if on_more_about:
                st.write("""Integrated petroleum production systems are typically modeled and simulated using Excel spread-
                        sheets, or specialized software. As part of my specialization and master project the following application was made in an attempt to
                        make a platform for computational routines for the Simulation and Modeling of Integrated Petroleum Production Systems.The
                        web-application has been built in Python, utilizing the Streamlit library. The application is free for everyone to use.
                        See the report for more information.
                        """)
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write('Master project by Morten Simensen, supervised by associate professor Milan Stanko')
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("BY USING THIS WEB SITE YOU UNDERSTAND AND AGREE THAT YOUR USE OF THIS WEB SITE AND ANY SERVICES OR CONTENT PROVIDED IS MADE AVAILABLE AND PROVIDED TO YOU AT YOUR OWN RISK. IT IS PROVIDED TO YOU AS IS AND SMIPPS EXPRESSLY DISCLAIM ALL WARRANTIES OF ANY KIND.")

        #elif opt == 'FIELD DEVELOPMENT':
            #self.field_development = FIELD_DEVELOPMENT(parent=GUI)
        #elif opt == 'RESERVOIR PRESSURE FROM PRODUCTION DATA':
             #self.reservoir_pressure_from_production_data = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(self)
        #elif opt == 'NPD DATA':
             #self.NPD_DATA = NPD_DATA(GUI)














