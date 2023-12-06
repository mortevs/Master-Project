import streamlit as st
import GUI.GUI_functions as display
import time
import Data.getData as get
import pandas as pd
from Data.dataProcessing import get_field_list_inc_No_field_chosen
from Data.ManualData import manualData_RP
fieldnames = get_field_list_inc_No_field_chosen()
class GUI():
    def __init__(self):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col5:
            load = st.button('Load New Data from NPD',  'NPD')
            if load:
                from Data.getData import deleteAndloadNewDatafromNPD
                deleteAndloadNewDatafromNPD()
                timestamp = time.ctime()
                alert00 = st.warning('Data downloaded from NPD ' + timestamp)
                time.sleep(5)
                alert00.empty() 

        opt = display.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'NPD DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')   
        if opt == "NO OPTION CHOSEN":
            st.title('Computational Routines For The Simulation and Modeling of Integrated Petroleum Production Systems')
            st.write(" ")
            st.write(" ")
            # Path to your JPG file
            import os
            image_path = os.path.join(os.getcwd(), "Data/Storage/stanko_front_page.png")

            # Display the image using st.image
            col1, col2 = st.columns(2)
            with col1:
                st.image("Data\Storage\stanko_front_page.png",width=650)
            with col2:
                on_information = st.toggle("Show me more information on how to use the application", value=False, label_visibility="visible")
                if on_information:
                    st.write("""The application has several features it can be used for. The features per December 5. 2023 is field development, production forecasting, 
                             reservoir pressure from production, and NPD data. The field development feature is for estimating production profiles for dry-gas fields.
                             The reservoir pressure from production data feature is for estimating the decline in pressure for a dry-gas reservoir when producing. 
                             The NPD data feature is for displaying open public data at NPD. This feature makes it possible to compare rates, and to plot the
                             reservoir Area, with well locations. The user can switch back and forth among the features. The resulting plots will be stored/cached while the application is running.""")
                on_more_about = st.toggle("Show me more information about the specialization project", value=False, label_visibility="visible")
                if on_more_about:
                    st.write("""Integrated petroleum production systems are typically modeled and simulated using Excel spread-
                            sheets, or specialized software. In the following specialization project, computational routines
                            have been developed for simulating and modeling integrated petroleum production systems. The
                            web-application has been built in Python, utilizing the Streamlit library. The application will be free for everyone to use.
                            """)
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.markdown('<p style="color: lightgreen;">Specialization project Morten Simensen, supervised by associate professor Milan Stanko.</p>', unsafe_allow_html=True)

        elif opt == 'FIELD DEVELOPMENT':
            self.field_development = FIELD_DEVELOPMENT(parent=GUI)
        elif opt == 'RESERVOIR PRESSURE FROM PRODUCTION DATA':
             self.reservoir_pressure_from_production_data = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(self)
        elif opt == 'NPD DATA':
             self.NPD_DATA = NPD_DATA(GUI)           

class FIELD_DEVELOPMENT(GUI):
    def __init__(self, parent):
        from Modules.FIELD_DEVELOPMENT.run_Analysis import DryGasAnalysis
        Analysis = DryGasAnalysis(parent = FIELD_DEVELOPMENT, session_id='DryGasAnalysis')
        on_information = st.toggle("Show me information on how to use the field development feature", value=False, label_visibility="visible")
        if on_information:
            st.write("""The table below on the right side contains default values for 16 parameters, in which the production profile calculation
                     is based upon. The values can be changed as the user sees fit. For example, if the user wants to run with a pressure of 
                     250 bara, and a different temperature, that can be changed in the table. 
                     With a set of desired parameters, the calculation of the production profile for those parameters
                     is performed when the user clicks <Run Analysis>. The production profile will display as Production profile 1.
                     The user can then change (optimize) the parameters and run a new analysis by clicking <Run Analysis> again. This
                     will produce a second production profile plot. The user can create as many production profiles as desired. The <Compare different models> button
                     will create a new plot, where all the production profiles are compared in one plot. 
                    Each production profile plot contains a dropdown menu. From the dropdown menu, sub-calculations for the production profile can be displayed 
                    instead of the production profile. This includes among other, Recovery Factor, Z-factor, Reservoir pressure and choke pressure.
                    Furthermore there is a <Clear output button>. Clicking this button will remove all the plots, and you will start over creating 
                     production profile 1 again. The feature also has a <Choose field to compare with> dropdown menu. By choosing a field from NPD, 
                     instead of default "No Field Chosen", the (daily average) water, oil, gas and condensate rates for that particular field are possible to 
                     display for the user. There is also two options the user can choose from to run different models. 
                     These options decide the mathimatical method for obtaining the production profile. 
                     By default the production profile is estimated using implicit Nodal approach. However, from the two dropdown menu, the user can choose 
                    IPR instead of Nodal, and explicit instead of implicit. Nodal implicit is the most accurate method, but 
                     also the most computational costly. For more details see the report. 
                     """)

        col0, col1 = st.columns(2)
        plot_comp = False
        with col0:
            method, precision = display.columnDisplay2(list1=[['NODAL', 'IPR'], ['IMPLICIT', 'EXPLICIT']])
            col4, col5 = st.columns(2)
            with col4:
                run = st.button('Run Analysis', 'Run DG')
            with col5: 
                if st.button('Compare different models', 'Compare'):
                        plot_comp = True
            col7, col8 = st.columns(2)
            with col7:
                clear =  st.button('Clear output', 'clear FD')
            with col8: 
                field = display.dropdown(label = 'Choose a field to compare with', options = fieldnames, labelVisibility="visible")
                Analysis.updateField(field)
        with col1:  
            Analysis.updateFromDropdown(method = method, precision=precision)
            Analysis.updateParameterListfromTable() 
        
        if clear:
            Analysis.clear_output()

        field_name = Analysis.get_current_field()
        if run and field_name == 'No field chosen':
            result = Analysis.run()
            Analysis.append_result(result)

        elif run and field_name != 'No field chosen':
            result = Analysis.run_field(field)
            Analysis.append_result(result)
        col10, col11, col12, col13, col14 = st.columns(5)
        with col11:
            if plot_comp == True:
                Analysis.plot(comp = True)
            Analysis.plot()
            self.parent = parent

class RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(GUI):
    def __init__(self, parent):
        self.place_holder = 1
        on_information = st.toggle("Show me information on how to use the reservoir pressure from production data feature", value=False, label_visibility="visible")
        if on_information:
            st.write(""" Choose production data from NPD from the dropdown menu below, or upload data. use the following format when uploading: 
                     column 1- year-(month), column 2 - sm3.
                     Click <Run Analysis>. Click <Clear output> for removing all the plots and starting over again
                     """)
        uploaded = st.file_uploader(label = "Upload a CSV/Excel file with production data here")
        col0, col1 = st.columns(2)
        with col0:
            eq = display.dropdown(label = 'What equation do you want to use?', options = ['Material balance with Z-factor calculation'], labelVisibility="visible")
            if eq == 'Backpressure equation':
                pass     
            field = display.dropdown(label = 'Get gas production data from the following field:', options = fieldnames, labelVisibility="visible")
            selected_time = display.dropdown(label = 'Choose yearly or monthly producted volumes', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.run_R_analysis import ReservoirPressureAnalysis
        RES_Analysis = ReservoirPressureAnalysis(parent = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA, session_id='ReservoirPressureAnalysis')
        RES_Analysis.updateFromDropDown(fieldName= field, time = selected_time)
        RES_Analysis.update_from_upload(uploaded)
            #RES_Analysis.updateParameterListfromTable(list2 = manualData_RP())

        #st.write("The following data for " + field[0]+field[1:].lower() + " was found at NPD. Run analysis with these data or change them as you see fit" )
        with col1:
            col2, col3, col4, col5= st.columns(4)
            with col2:   
                run = st.button('Run Analysis', 'Run RP')
            with col4:   
                NPD_button = st.button('Get NPD-data for field', 'get NPD data into table')
            with col5: 
                clear = st.button('Clear output', 'clear RESPRES')
        
        
        if NPD_button and field == 'No field chosen':
            alert3 = st.warning('Choose a field')
            time.sleep(1.5)
            alert3.empty()

        if run and field == 'No field chosen' and uploaded == None:
            alert3 = st.warning('Choose a field or upload data')
            time.sleep(1.5)
            alert3.empty()

        elif NPD_button and field != 'No field chosen':
            self.place_holder = 2
        
        with col1:
            if self.place_holder == 1:
                RES_Analysis.updateParameterListfromTable(list2 = manualData_RP())

            elif self.place_holder ==2:
                PRi = 276 #reservoir pressure bara #default value
                gasMolecularWeight = 16 #[g/mol] default value
                PRi, T, gasMolecularWeight, IGIP = RES_Analysis.get__PR_NPD_data()
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
        col6, col7, col8, col9, col10 = st.columns(5)
        with col7:
            RES_Analysis.plot()
        self.parent = parent
        
class NPD_DATA(GUI):
    def __init__(self, parent):
        on_information = st.toggle("Show me information on how to use the NPD data feature", value=False, label_visibility="visible")
        if on_information:
            st.write(""" To compare fields follow these steps, 'Step 1 - Choose a field, Step 2- Click Plot production profile, Step 3 - 
                     Repeat step 1 and 2, Step 4 - Click Compare fields'""")
        from Modules.NPD_DATA.npd_data import npd_prod
        npd_obj = npd_prod(parent = NPD_DATA, session_id='npd_prod', field = 'No field chosen')
        col4, col5  = st.columns(2)
        with col4:
            field = display.dropdown(label = 'Choose a field', options = fieldnames, labelVisibility="visible")
        with col5:
            time = display.dropdown(label = 'Time frame of interest', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        
        npd_obj.updateFromDropDown(fieldName = field, time = time)
        col6, col7, col8 = st.columns(3)
        with col6:
            run = st.button('Plot production profile', 'Show produced volumes')
        with col7:
            comp = st.button('Compare fields', 'Compare')
        with col8: 
            clear =  st.button('Clear output', 'clear FD')
        
        if run and field == 'No field chosen':
            import time as t
            alert3 = st.warning('Choose a field first')
            t.sleep(1.5)
            alert3.empty()
        
        elif run and time == 'Yearly':
            result = npd_obj.runY()
            npd_obj.append_result(result)

        elif run and time == 'Monthly':
            result = npd_obj.runM()
            npd_obj.append_result(result)

        if clear:
            npd_obj.clear_output()

        if comp:
            npd_obj.plot(comp = True)
        npd_obj.plot()
        self.parent = parent

        st.write(' ')
        st.write(' ')
        st.write(' ')

        poly_button = st.button('Plot reservoir area', 'polygon plotter', use_container_width=True)
        if poly_button and field == 'No field chosen':
            import time
            alert4 = st.warning('Choose a field first')
            time.sleep(1.5)
            alert4.empty()
        elif poly_button and field != 'No field chosen':
            from Modules.NPD_DATA.npd_data import makePlot
            makePlot(field)