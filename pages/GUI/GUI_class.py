import streamlit as st
import pages.GUI.GUI_functions as display
import time
import Data.getData as get
import os
from Data.dataProcessing import get_field_list_inc_No_field_chosen
from Data.ManualData import manualData_RP
fieldnames = get_field_list_inc_No_field_chosen()
class main_page_GUI(): 
    def __init__(self):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col5:
            load = st.button('Load New Data from Sodir',  'sodir')
        if load:
            from Data.getData import deleteAndLoadNewDataFromNPD
            deleteAndLoadNewDataFromNPD()
            timestamp = time.ctime()
            alert00 = st.warning('Data downloaded from sodir ' + timestamp)
            time.sleep(5)
            alert00.empty() 
    #opt = display.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'NPD DATA'], labelVisibility='visible')   
    #if opt == "NO OPTION CHOSEN":
        st.title('Simulation and Modeling of Integrated Petroleum Production Systems')
        st.write(" ")
        st.write(" ")
        col1, col2 = st.columns(2)
        with col1:
            my_path = os.path.join('Data', 'Storage', 'Morten_front_page.png')
            st.image(my_path)
        with col2:
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
            
            on_more_about = st.toggle("Show me more information about the specialization project", value=False, label_visibility="visible")
            if on_more_about:
                st.write("""Integrated petroleum production systems are typically modeled and simulated using Excel spread-
                        sheets, or specialized software. As part of my specialization project the following application was made in an attempt to 
                        make a platform for computational routines for the Simulation and Modeling of Integrated Petroleum Production Systems.The
                        web-application has been built in Python, utilizing the Streamlit library. The application is free for everyone to use.
                        See the report for more information. 
                        """)
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write('Specialization project by Morten Simensen, supervised by associate professor Milan Stanko')

        #elif opt == 'FIELD DEVELOPMENT':
            #self.field_development = FIELD_DEVELOPMENT(parent=GUI)
        #elif opt == 'RESERVOIR PRESSURE FROM PRODUCTION DATA':
             #self.reservoir_pressure_from_production_data = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(self)
        #elif opt == 'NPD DATA':
             #self.NPD_DATA = NPD_DATA(GUI)           

class FIELD_DEVELOPMENT():
    def __init__(self):
        from Modules.FIELD_DEVELOPMENT.run_Analysis import DryGasAnalysis
        Analysis = DryGasAnalysis(parent = FIELD_DEVELOPMENT, session_id='DryGasAnalysis')
        on_information = st.toggle("Show me information on how to use the field development feature", value=False, label_visibility="visible")
        if on_information:
            st.write("""The table below on the right side contains default values for 16 parameters, in which the production profile estimation
                     is based upon. The values can be changed as the user sees fit. For example, if the user wants to run with a pressure of 
                     250 bara, and a different temperature, click the values in the table and change them to the desired values directly.""")
            st.write(""" 
                    The production profile is estimated with the values in the table when the user clicks <Run Analysis>. 
                    The first production profile will display as Prod-profile 1. The parameters used for each Prod-profile are stored. The
                    user can change the parameters and click <Run Analysis> again. This will display a second prod-profile.
                    The user can create as many production profiles as desired.""")
                     
            st.write("""The <Compare different models> button
                     will create a new plot, where all the production profiles are compared in one plot.""")
            st.write( 
                    """Each production profile plot contains a dropdown menu. From the dropdown menu, sub-calculations for the production profile can be displayed 
                    instead of the production profile. This includes among other, Recovery Factor, Z-factor, Reservoir pressure and choke pressure.""")
            
            st.write("""
                    Clicking the <Clear output> button will remove all the plots and stored parameters. You will start over creating 
                    production profile 1 again after clicking this button.""")
                     
            st.write("""The feature has a <Choose field to compare with> dropdown menu. By choosing a field from NPD, 
                     instead of default "No Field Chosen", the daily average SM^3 volumes of water, oil, gas and condensate rates for that particular field are possible to 
                     display for the user.""")
            st.write("""
                     There is also two options the user can choose from to run different models. 
                     These options decide the mathematical method for obtaining the production profile. 
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
        if plot_comp == True:
            Analysis.plot(comp = True)
        Analysis.plot()
        self.parent = parent
        
        opts = []
        i = 1
        production_profiles = Analysis.getResult()
        for production_profile in production_profiles:
            opts.append(i)
            i += 1
        makeNPV = st.button('Make Net-Present-Value analysis', 'make NPV')       
        if makeNPV and len(production_profiles) != 0:
            col0, col1, col2 = st.columns(3)
            with col0:
                opt = display.dropdown(label = 'Choose which production profile to run the NPV-analysis with',options = opts, labelVisibility="visible")
            from Modules.FIELD_DEVELOPMENT.run_Analysis import NPVAnalysis
            NPV = NPVAnalysis(parent = FIELD_DEVELOPMENT, session_id='DryGasAnalysis', prod_prof = production_profiles[opt-1]['Field rates [sm3/d]'])
            NPV.updateParameterListfromTable()
            runNPV = st.button('Run Net-Present-Value analysis', 'Run NPV')
            if runNPV:
                pass
        elif makeNPV and len(production_profiles) == 0:
            alert = st.warning("You must create a production profile first")
            time.sleep(5)
            alert.empty()
  
class RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA():
    def __init__(self):
        self.place_holder = 1
        on_information = st.toggle("Show me information on how to use the reservoir pressure from production data feature", value=False, label_visibility="visible")
        if on_information:
            st.write(""" The user has some options for running the model. As per now only one equation is available, but the user can choose to fetch
                     monthly or yearly rates from NPD using the dropdownmenu below on the left side""")

            st.write(""" Choose production data from an NCS-field from the dropdown menu below, or upload data. Use the following format when uploading: 
                     column 0 - gas produced in sm3, column 1 - date (year/ year-month). use ; as seperator""")
            
            st.write("""Click <Run Analysis> to estimate the reservoir pressure for a field chosen, or for the uploaded data.
                      The numbers in the table below on the right side will be used for the estimation. The user can change these numbers before
                     clicking <Run Analysis>""")
            
            st.write("""An alternative to clicking <Run Analysis> is to click <Get NPD-data for field>. The IGIP and Reservoir pressure will be 
                     fetched from NPD and an analysis wil be run with this data. """)

                     
            st.write("""Click <Clear output> to remove all the plots and start over again""")

        uploaded = st.file_uploader(label = "Upload a CSV file")
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
        with col1:
            col2, col3, col4, col5= st.columns(4)
            with col2:   
                run = st.button('Run Analysis', 'Run RP')
            with col4:   
                SODIR_button = st.button('Get Sodir-data', 'get SODIR data into table')
            with col5: 
                clear = st.button('Clear output', 'clear RESPRES')
        
        if SODIR_button and field == 'No field chosen':
            alert3 = st.warning('Choose a field')
            time.sleep(1.5)
            alert3.empty()

        if run and field == 'No field chosen' and uploaded == None:
            alert3 = st.warning('Choose a field or upload data')
            time.sleep(1.5)
            alert3.empty()

        elif SODIR_button and field != 'No field chosen':
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

        RES_Analysis.plot()
        self.parent = parent
        
class SODIR_feature():
    def __init__(self):
        on_information = st.toggle("Show me information on how to use the SODIR data feature", value=False, label_visibility="visible")
        if on_information:
            st.write(""" To compare fields follow these steps, 'Step 1 - Choose a field, Step 2- Click Plot production profile, Step 3 - 
                     Repeat step 1 and 2, Step 4 - Click Compare fields'""")
            
            st.write(""" Click clear output to remove all the plots and start over again'""")

            st.write("""" Click Plot reservoir area to plot a polygon of the reservor area with the production wells marked""")

        from Modules.SODIR_DATA.Sodir_data import Sodir_prod
        sodir_obj = Sodir_prod(parent = SODIR_feature, session_id='sodir_prod', field = 'No field chosen')
        col4, col5  = st.columns(2)
        with col4:
            field = display.dropdown(label = 'Choose a field', options = fieldnames, labelVisibility="visible")
        with col5:
            time = display.dropdown(label = 'Time frame of interest', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        
        sodir_obj.updateFromDropDown(fieldName = field, time = time)
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
            result = sodir_obj.runY()
            sodir_obj.append_result(result)

        elif run and time == 'Monthly':
            result = sodir_obj.runM()
            sodir_obj.append_result(result)

        if clear:
            sodir_obj.clear_output()

        if comp:
            sodir_obj.plot(comp = True)
        sodir_obj.plot()
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
            from Modules.SODIR_DATA.Sodir_data import makePlot
            makePlot(field)
        show_more_prod = st.toggle(label = "Show me more information about the producing wells on this field")    
        if show_more_prod:
            st.dataframe(get.producing_wlb(field))
        show_more_inj = st.toggle(label = "Show me more information about the injection wells on this field") 
        if show_more_inj:
            st.dataframe(get.injecting_wlb(field))
        
        show_more_closed = st.toggle(label = "Show me more information about the closed wells on this field") 
        if show_more_closed:
            st.dataframe(get.closed_wlb(field))
        show_more_PA = st.toggle(label = "Show me more information about the P&A wells on this field") 
        if show_more_PA:
            st.dataframe(get.PA_wlb(field))


