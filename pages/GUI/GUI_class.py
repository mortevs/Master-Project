import streamlit as st
import pages.GUI.GUI_functions as display
import time
import Data.getData as get
import os
from Data.dataProcessing import get_field_list_inc_No_field_chosen
from Data.DefaultData import manualData_RP
fieldnames = get_field_list_inc_No_field_chosen()

class main_page_GUI: 
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

class FIELD_DEVELOPMENT:
    def __init__(self):
        m = st.markdown("""<style>
        div.stButton > button:first-child {
        background-color: rgb(204, 49, 49);
        }
        </style>""", unsafe_allow_html=True)
        from Modules.FIELD_DEVELOPMENT.run_Analysis import DryGasAnalysis
        Analysis = DryGasAnalysis(session_id='DryGasAnalysis')
        on_pp_information = st.toggle("Show me information on how to estimate dry gas production profiles", value=False, label_visibility="visible")
        if on_pp_information:
            st.write("""The following feature allows for modeling of the production profile for a dry gas field. 
                     The table below on the right side contains default values for 17 variables, for which the production profile estimation
                     is based upon. The values can be changed as the user sees fit. For example, if the user wants to run with a Target Rate of 15 1E6 Sm3, a pressure of 
                     250 bara, and a build-up period of 5 years, these changes may directly be applied in the table below to the right.""")
            st.write(""" 
                    The production profile is estimated with the values in the table when the user clicks <Run Analysis>. 
                    If desireable, the user can create multiple production profiles with different sets of variables. The first production profile will display as Production Profile 1, the second as Production Profile 2, the third as Production Profile 3, and so on.
                    For each production profile the corresponding variables are available for the user to see in the Variables tab under the Production Profile title.
                    """) 
            st.write( 
                    """Each resulting Production Profile contains a dropdown menu.
                    From the dropdown menu sub-calculations for the present production profile can be displayed.
                    These sub-calculations include the estimated yearly gas of take, cumulative gas of take,
                    recovery factor, Z-factor, reservoir pressure, rates per well, bottomhole pressure, wellhead pressure,
                    template pressure, PLEM pressure, seperator pressure, rates per template, choke pressure,
                    ratio of template pressure to wellhead pressure, and the production potential.""")
            st.write("""The <Compare Profiles> button will create a new plot, where all the current production profiles are compared in the same plot.""")
            
            st.write("""
                    The production profiles and corresponding variables are stored in session-states in the application.
                    Even if the application is closed, the production profiles and variables are stored. Pressing the <Clear Output> button will remove all the resulting production profiles.
                    If the user wants to retrieve the default table values, refresh the page.""")
                     
            st.write("""The feature also has an experimental <Choose field to compare with> dropdown option. The user can choose a field from the Norwegian Continental Shelf.
                    By choosing a field from the dropdown menu, instead of the default "No Field Chosen", the average daily rates (Sm3/day) of gas 
                    for that field can be displayed for the user after pressing <Run Analysis>. The average daily rates of NGL, oil, condensate, oil-equivalents, and water 
                    are also available for the user to display from the dropdown menu.
                    The average rates are calculated based on yearly produced volumes for the field (fetched from SODIR) and the upTime variable in the table.
                    The  <Choose field to compare with> is an experimental option. By providing an option for the user to
                    quickly compare estimated gas rates with produced gas rates for a chosen field, it intends to give the user insight
                    into wheter the estimates are somewhat realistic or not.
                    """)
            
            st.write("""
                     There is two dropdown menus from which the user can choose to run different mathematical models. 
                     These options decide the mathematical method for obtaining the production profile. 
                     By default the production profile is estimated using the implicit Nodal approach. 
                     From the two dropdown menu, the user can choose IPR instead of Nodal, and explicit instead of implicit. 
                     Nodal implicit is the most accurate method, but 
                     also the most computational costly. If Nodal Implicit fails to find a solution,
                     the user has the option to run the analysis using a simpler, but less computational costly method.
                     IPR explicit is the method with the lowest computational cost. 
                     For more details on the IPR, Nodal, Explicit and Implcit methods, see my Masters report. 
                     """)
        col0, col1 = st.columns(2)
        plot_comp = False
        with col0:
            method, precision = display.columnDisplay2(list1=[['NODAL', 'IPR'], ['IMPLICIT', 'EXPLICIT']])
            col4, col5 = st.columns(2)
            with col4:
                run = st.button('Run Analysis', 'Run DG')
            with col5: 
                if st.button('Compare Profiles', 'Compare'):
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
        
        opts = []
        production_profiles = Analysis.getResult()
        i = len(production_profiles)
        for pp in reversed(production_profiles):
            opts.append(i)
            i -= 1
        st.write('------------------------')
        if len(production_profiles) != 0:
            on_NPV_information = st.toggle("Show me information on how to generate NPV estimates ", value=False, label_visibility="visible", key = "")
            if on_NPV_information:
                st.write("""The following feature allows for automatic modeling of the Net-Present-Value of a project. The NPV is based on a  
                         production profile and corresponding field-variables from the production profile section above, together with key economic variables found in the tables below. 
                        The tables below contain default variables, for which the NPV estimation
                        is based upon. The values can be changed as the user sees fit. For example, if the user wants to run with a discount rate
                        of 7% , a CAPEX period (period without income from production) of 3 years and a well cost of 150 1E6 USD, these changes may directly be applied in the 
                        tables below.""")
                st.write(""" From the dropdown menu below, the user can choose which production profile to make the NPV analysis for. The
                        NPV-analysis will take the field-variables corresponding to the chosen production profile into consideration. By default,
                         the latest production profile generated will be utilized.""")
                st.write(""" 
                        The NPV is estimated utilizing variables from the table above in the production profile section, and the tables below.
                        Well costs in the NPV analysis will be distributed according to the number of wells (numer of templates and well per templates), and Max Wells Drilled per year automaticly.
                        The template distribution will be distributed to match so that a new template is only installed when there are no available slots. As an example,
                        if max 1 well is to be drilled every year, number of templates is 3,  number of wells per template is 3, cost for a new template will be 
                        covered the first, fourth and seventh year. The user can choose to change the automated distribution of costs. Wells, templates, pipeline & Umbilical, LNG Plant, LNG Vessels and OPEX cost may be adjustes to the users preference
                        in the editable dataframe below.
                         
                        The edible dataframe is generated based on the three variable tables. By changing the OPEX value or Well Cost in the variable tables below, the editable dataframe will automaticly be
                         updated. The edible dataframe may be adjusted by changing the variables, or may be customized direcly in the Editable dataframe. Based on the editable dataframe
                         a Non-editable table is generated that displays the DRILLEX, Templates, Total Capex and ultimately the NPV for each year.
                         
                        The cost of LNG plant and LNG Vessels scale with the plateau rate. 
                         
                        Keep in mind that the number of wells (Number of templates and wells per template) will affect the production profile, in addition to 
                        having a cost per well. To study how the number of wells affect the NPV, generate for instance two production profiles,
                        with different nummber of templates. Switch from the drop-down option mentioned above between 2 and 1 to see the NPV difference.
                        """
                         
                       ) 
            col0, col1, col2 = st.columns(3)
            with col0:
                opt = display.dropdown(label = 'Choose production profile for NPV-analysis',options = opts, labelVisibility="visible")

            from Modules.FIELD_DEVELOPMENT.run_Analysis import NPV_dry_gas, NPVAnalysis
            opt = opt-1
            dry_gas_NPV = NPV_dry_gas(parent = NPVAnalysis, Analysis = Analysis, opt = opt)
            dry_gas_NPV.NPV_gas_field_update_edible_tables()
            edible_df = dry_gas_NPV.dry_gas_NPV_calc_sheet()
            col0, col1 = st.columns(2)
            with col0:
                st.markdown("**Editable**")
                edible_df = st.data_editor(edible_df, hide_index=True, use_container_width=True, height=350)

            def make_pretty(styler):
                styler.set_properties(subset = None, **{'color': 'red'})
                return styler
            
            red_df = dry_gas_NPV.update_dry_gas_NPV_calc_sheet(edible_df)
        
            final_NPV_value = str(dry_gas_NPV.get_final_NPV())
            font_size = "64px"  # You can adjust the size as needed
            NPV_str = f"<div style='font-size:{font_size};'>Final NPV of Project: <span style='color:red;'>{final_NPV_value}</span> 1E6 USD</div>"
            st.markdown(NPV_str, unsafe_allow_html=True)
            with col1:
                st.markdown("**Non-editable**")
                st.dataframe(red_df.style.format("{:.0f}").pipe(make_pretty), hide_index=True, use_container_width=True, height=350)
            optimize_NPV = st.button(label = "Optimize NPV with grid search")
            parameters = Analysis.getParameters()[opt]
            plataeu = parameters[0]
            nr_temps =parameters[8]
            pertemp = parameters[0]
            import pages.GUI.GUI_functions as GUI
            list1 = ['Plateau rate [Sm3/d]', 'Nr Templates', 'Nr Wells per Template']
            list2 = [plataeu/2,nr_temps/nr_temps,pertemp/pertemp] 
            list3 = [plataeu*2,nr_temps/nr_temps*5,pertemp/pertemp*5] 
            list4 = [5,5,5] 

            col9, co10 = st.columns(2)
            with col9:
                GUI.display_table_grid_search(list1, list2, list3, list4, edible=True, key = "grid")



  
class RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA:
    def __init__(self):
        m = st.markdown("""<style>
        div.stButton > button:first-child {
        background-color: rgb(204, 49, 49);
        }
        </style>""", unsafe_allow_html=True)
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
        #self.parent = parent
        
class SODIR_feature:
    m = st.markdown("""<style>
        div.stButton > button:first-child {
        background-color: rgb(204, 49, 49);
        }
        </style>""", unsafe_allow_html=True)
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
        #self.parent = parent

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
