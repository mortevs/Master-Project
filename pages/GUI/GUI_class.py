import streamlit as st
import pages.GUI.GUI_functions as GUI
import time
import Data.getData as get
import os
from Data.dataProcessing import get_field_list_inc_No_field_chosen
import math
import pandas as pd
try:
    fieldnames = get_field_list_inc_No_field_chosen()
except Exception as e:
    st.write(e)
    st.warning("could not get list of fieldnames from SODIR")


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
            time.sleep(3)
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
            
            on_more_about = st.toggle("Show me more information about the Master project", value=False, label_visibility="visible")
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

def make_pretty(styler):
    styler.set_properties(subset = None, **{'color': 'red'})
    return styler
class FIELD_DEVELOPMENT:
    def __init__(self):
        m = st.markdown("""<style>
        div.stButton > button:first-child {
        background-color: rgb(204, 49, 49);
        }
        </style>""", unsafe_allow_html=True)
        from Modules.FIELD_DEVELOPMENT.run_Analysis import DryGasAnalysis
        Analysis = DryGasAnalysis(session_id='DryGasAnalysis')
        colA, colB = st.columns(2)
        with colA:
            on_pp_information = st.toggle("Show me information on how to estimate dry gas production profiles", value=False, label_visibility="visible")
        with colB:
            default_message = st.warning("Default values below. Change to desired values")
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
            self._method, self._precision = GUI.columnDisplay2(list1=[['NODAL', 'IPR'], ['IMPLICIT', 'EXPLICIT']])
            col4, col5 = st.columns(2)
            with col4:
                run = st.button('Run Analysis', use_container_width=True)
            with col5: 
                if st.button('Compare Profiles', use_container_width=True):
                        plot_comp = True
            col7, col8 = st.columns(2)
            with col7:
                clear =  st.button('Clear Output', use_container_width=True)
            with col8: 
                field = GUI.dropdown(label = 'Choose a field to compare with', options = fieldnames, labelVisibility="visible")
                Analysis.updateField(field)
        with col1:  
            Analysis.updateFromDropdown(method = self._method, precision=self._precision)
            params = Analysis.updateParameterListfromTable()
            Analysis.validate_parameters(params)
        if clear:
            Analysis.clear_output()
        field_name = Analysis.get_current_field()
        if run and field_name == 'No field chosen':
            result = Analysis.run()
            Analysis.append_result(result)

        elif run and field_name != 'No field chosen':
            result = Analysis.run_field(field)
            Analysis.append_result(result)

        if plot_comp and len(Analysis.getResult()) == 0:
            st.error("""No profiles to compare. Press Run Analysis (with the desired field charateristics in the table above to the right). Then change the field charateristics, 
                     and press Run Analysis once again. THEN press compare fields to compare the two (or more) production 
                     profiles.""")
        elif plot_comp == True:
            Analysis.plot(comp = True)
        Analysis.plot()
        production_profiles = Analysis.getResult()
        i = len(production_profiles)
        opts = []
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
                opt = GUI.dropdown(label = 'Choose production profile for NPV-analysis',options = opts, labelVisibility="visible")

            from Modules.FIELD_DEVELOPMENT.run_Analysis import NPV_dry_gas
            opt = opt-1
            #variables=Analysis.getParameters()[opt]
            dry_gas_NPV = NPV_dry_gas(opt)
            dry_gas_NPV.NPV_gas_field_update_edible_tables()
            self.__editable_df = dry_gas_NPV.dry_gas_NPV_calc_sheet()
            col0, col1 = st.columns(2)
            with col0:
                st.markdown("**Editable**")
                self.__edited_df = st.data_editor(self.__editable_df, hide_index=True, use_container_width=True, height=350)

            
            self.__ned_df = dry_gas_NPV.update_dry_gas_NPV_calc_sheet(self.__edited_df)
        
            final_NPV_value = str(dry_gas_NPV.get_final_NPV())
            font_size = "44px"  
            NPV_str = f"<div style='font-size:{font_size};'>NPV of project: <span style='color:red;'>{final_NPV_value}</span> 1E6 USD</div>"
            st.markdown(NPV_str, unsafe_allow_html=True)
            with col1:
                st.markdown("**Non-editable**")
                st.dataframe(self.__ned_df.style.format("{:.0f}").pipe(make_pretty), hide_index=True, use_container_width=True, height=350)

            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write("-------------------------")
            st.markdown("**Field-variable optimization**")            
            col9, co10 = st.columns(2)
            with col9:
                edited_grid = GUI.display_table_grid_search(Analysis.getParameters()[opt])
                self.__minROA = float(edited_grid["Min"][2])
                dry_gas_NPV.validate_grid_variables(edited_grid, Analysis.getParameters()[opt])
                optimize_NPV = st.button(label = "Optimize NPV with grid search", use_container_width=True)
             
            if optimize_NPV:
                dry_gas_NPV.update_grid_variables(edited_grid)
                minP, maxP, pStep = dry_gas_NPV.get_grid_plateau_variables()
                minW, maxW = dry_gas_NPV.get_grid_well_variables()
                self.__minROA = dry_gas_NPV.get_ROA_variables()
                rates = []
                for i in range(pStep):
                    rates.append(minP + (maxP-minP)/(pStep-1)*i)
                
                W = [minW]
                while W[-1]<maxW:
                    W.append(W[-1]+Analysis.getParameters()[opt][8])

                prodProfiles_to_NPV = dry_gas_NPV.grid_production_profiles(rates, self.__minROA, W)

                NPV_dict = {}
                for i in range(len(prodProfiles_to_NPV)):
                    part_ = dry_gas_NPV.run_grid_NPV(edited_df = self.__edited_df, prod_profiles = prodProfiles_to_NPV, i = i)
                    NPV_dict.update(part_)
                optimized_NPV = max(NPV_dict)
                optimized_Nr_Wells = NPV_dict[optimized_NPV][0]
                optimized_rate = NPV_dict[optimized_NPV][1]
                optimized_ROA = math.floor(NPV_dict[optimized_NPV][2])

                w_string = f"""All templates and wells are assumed equal. Therefore number of wells in grid seach follows 
                stepsize of "Number of Wells per Template" = {Analysis.getParameters()[opt][8]}. (In other words
                only "full templates" are considered). The editable table above was used as basis in the grid search analysis. 
                The Pipeline & umbilical and OPEX columns in the table remain unchanged throughout the grid search.
                  The LNG plant and LNG vessel columns change with rate, but the cost proportions 
                  remain the same as they are in the table (by default 50 % of the cost the first 
                  year, and 50 % of the cost the second year, however this can be changed). 
                Note that Wells and templates are distributed by a default distribution algorithm. 
                The distribution algorithm distrubtes wells and templates with consideration to number of wells, 
                Max Wells Drilled p/year and number of Wells per template. Template cost and well cost is then
                  estimated with well cost and template cost variables in the CAPEX table above. Changes to the Nr Wells and Nr Templates 
                  column in the editable table above are not considered by the grid search optimization, well ands templates needs to be 
                  default distributed (as we are optimizing on number of wells, a cost distibution must be assumed). 
                  """
                st.warning(w_string)


                #optimized_ROA = math.ceil((prodProfiles_to_NPV[NPV_dict[optimized_NPV][0]][NPV_dict[optimized_NPV][2]])/1000)*1000
                
                opt_NPV_str = f"<div style='font-size:{font_size};'>Optimized NPV: <span style='color:red;'>{round(optimized_NPV,1)}</span> 1E6 USD</div>"
                st.markdown(opt_NPV_str, unsafe_allow_html=True)
                
                optimized_data = {
                    "Input": ["Plateau rate [Sm3/d]", "Rate of Abandonment [Sm3/d]",  "Number of Wells [-]"],
                    "Value": [int(optimized_rate), int(optimized_ROA), int(optimized_Nr_Wells)]
                }
                df = pd.DataFrame(optimized_data)
                col11, col12, col13 = st.columns(3)
                with col11:
                    st.markdown("**Achieved with the following variables:**")
                    st.dataframe(df.style.pipe(make_pretty), hide_index=True, use_container_width=True)
                
            #     #for i in range(3):
            # col14, col15 = st.columns(2)
            # with col14:
            #     optimize_wells = st.button(label = "Optimize Templates and wells", use_container_width=True)
            # if optimize_wells:
            #     dry_gas_NPV.grid_production_profiles2()
            #variables=Analysis.getParameters()[opt]
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.title("Uncertainity Analysis")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            col16, col17 = st.columns(2)
            col18, col19 = st.columns(2)
            
            with col16:
                st.markdown("**Uncertainty in variables**")
                Gas_Price, IGIP_input, LNG_plant_per_Sm3 = dry_gas_NPV.get_inital_MC_variables()
                self.__edited_MC_table = GUI.display_uncertainty_table(Gas_Price, IGIP_input, LNG_plant_per_Sm3)
                
                #edited_df = self.__edited_df, prod_profiles = prodProfiles_to_NPV, i = i)
                
                #st.write(NPVsMC)
            with col17:
                st.markdown("**Monte Carlo Analysis parameters**")
                self._Nr_random_num, self._Nr_bins = GUI.display_table_Monte_Carlo_param()
            with col18:
                MC = st.button(label = "Run uncertainity Analysis", use_container_width=True)
            
            if MC:
                prodProfiles_to_MC = dry_gas_NPV.Monte_Carlo_production_profiles(self.__edited_MC_table, minROA=self.__minROA)
                initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax = dry_gas_NPV.getNPVsforMonteCarlo(dfMC = self.__edited_MC_table, NPV_edited_df=self.__edited_df, prod_profiles= prodProfiles_to_MC)
                #st.write( NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax)
                GUI.tornadoPlot(initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, Gas_Price, IGIP_input, LNG_plant_per_Sm3)    
                GUI.tornadoPlotSensitivity(NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax)                        
                
                from Modules.FIELD_DEVELOPMENT.Monte_Carlo import Monte_Carlo_FD
                MC = Monte_Carlo_FD(parent = self, df = self.__edited_MC_table)
                pdf_fig, cdf_fig, tab, std = MC.getResults()
                col20, col21 = st.columns(2)
                with col20:
                    st.plotly_chart(pdf_fig, use_container_width=True)
                    st.dataframe(tab, hide_index=True, use_container_width=True)
                    st.write("std:", round(std,1))
                with col21:                      
                    st.plotly_chart(cdf_fig, use_container_width=True)
                st.warning("""The Monte Carlo Analysis is based on the active production profile (chosen from the dropdown menu) and the editable NPV table.
                            NOTE that optimized number of templates and plateau rate are not automaticly used. If you would like to 
                            use the optimized variables for the Monte Carlo Analyis, you would have to generate a new production profile with the optimized
                            variables that were found. The optimized rate of abandonment (assuming it occurs above the 
                            minimum Rate of Abandonment) is considered by considering the highest NPV found until the rates
                            reach abandonment rates.
                    """)

class Monte_Carlo_standAlone:
    def __init__(self):
        on_MCSA_information = st.toggle("Show me information on how to use Monte Carlo Analysis", value=False, label_visibility="visible")
        if on_MCSA_information:
            st.write("""A Monte Carlo Analysis is run with the input data. 
                    The rows should be addable. For instance all the rows should be 
                     time [Hours] or cost [1E06 USD]. 
                     Uncertainties will be run on each variable according to Min, Max,
                     ML (if applicable) and the probability distribution for that row.
                     They will then be added together to give a final probability distribution. 
                     A different probability distribution than the default Uniform 
                     can the be chosen from a dropdown menu by double pressing the cell.
                     The Monte Carlo Analysis Parameters can be adjusted to obtain higher or lower resolution
                     according to the needs. Higher resolution is more computational costly.  
                     """)
        col16, col17 = st.columns(2)
        col18, col19 = st.columns(2)
        col20, col21 = st.columns(2)
        with col16:
            st.markdown("**Uncertainity in variables and probability distribution**")
            edited_MC_table = GUI.display_table_Monte_Carlo_SA()
            GUI.validate_MC_SA(edited_MC_table) #not configured yet
        with col17:
            st.markdown("**Monte Carlo Analysis parameters**")
            self._Nr_random_num, self._Nr_bins = GUI.display_table_Monte_Carlo_param()
        with col18:
            MC = st.button(label = "Run Monte Carlo-Analysis", use_container_width=True)
            if MC:
                from Modules.MONTE_CARLO import Monte_carlo_standAlone
                MC = Monte_carlo_standAlone(self, edited_MC_table)
                pdf_fig, cdf_fig, tab, std = MC.getResults()
                with col20:
                    st.plotly_chart(pdf_fig, use_container_width=True)
                    st.dataframe(tab, hide_index=True, use_container_width=True)
                    st.write("std:", round(std,1))
                with col21:                      
                    st.plotly_chart(cdf_fig, use_container_width=True)
 
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
                     monthly or yearly production rates from Sodir using the dropdownmenu below on the left side""")

            st.write(""" Choose production data from an NCS-field from the dropdown menu below, or upload data in csv format with 
                     column 0 - date (year/ year-month), column 2 - gas produced in 1E06 Sm3""")
            
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
            field = GUI.dropdown(label = 'Get gas production data from the following field:', options = fieldnames, labelVisibility="visible")
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
            default_message2 = st.warning("Default values below. Change to desired values")
        if SODIR_button and field == 'No field chosen':
            alert3 = st.warning('Choose a field')
            time.sleep(3.5)
            alert3.empty()

        if run and field == 'No field chosen' and uploaded == None:
            alert3 = st.warning('Choose a field or upload data')
            time.sleep(3.5)
            alert3.empty()

        elif SODIR_button and field != 'No field chosen':
            self.place_holder = 2
        
        with col1:
            if self.place_holder == 1:
                from Data.DefaultData import defaultData_RP
                RES_Analysis.updateParameterListfromTable(list2 = defaultData_RP())

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
            st.write(""" Choose a field from the NCS from the dropdown menu below. Choose a timeframe (yearly or montly) from the second
                     dropdown menu. Now press Plot production profile to display the produced volumes. By default, the gas volumes are
                     visualized, but from the plots dropdown menu the user can choose to display NGL, oil, condendsate, Oil equivilants and 
                     water volumes produced instead.""")
            st.write(""" To compare fields follow these steps: Step 1 - Choose a field, Step 2 - Press Plot production profile, Step 3 - 
                     choose a new field, Step 4 - press Plot production profile again, Step 5 - press Compare fields. Keep the same timeframe,
                     dont change between years and months when comparing multiple fields. Compare year with year or month by month, not year with month, it will
                     result in poor comparisons.
                     """)
            st.write("""Be aware that comparisons are made with reference from the fields produced volumes x number of years/months from startup, NOT the dates.
                     Comparisons between different field where one plot is displayed with regard to monthly produced
                     volumes, and the other yearly produced volumes, will result in poor comparisons. The compared fields should be
                     compared with the same timeframe""")
            
            st.write(""" Click clear output to remove all the plots and start over again""")

            st.write("""" Click Plot reservoir area to plot a polygon of the reservor area with the production wells marked""")

        from Modules.SODIR_DATA.Sodir_data import Sodir_prod
        sodir_obj = Sodir_prod(parent = SODIR_feature, session_id='sodir_prod', field = 'No field chosen')
        col4, col5  = st.columns(2)
        with col4:
            self.__field = GUI.dropdown(label = 'Choose a field', options = fieldnames, labelVisibility="visible")
        with col5:
            self.__time = GUI.dropdown(label = 'Time frame of interest', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        colA, colB, colC = st.columns(3)
        with colC:
            align = GUI.dropdown(label = 'Compare fields alignment', options = ['Compare from production startup', 'Compare by dates'], labelVisibility="visible")
        sodir_obj.updateFromDropDown(fieldName = self.__field, time = self.__time, align = align)
        col6, col7 = st.columns(2)
        with col6:
            run = st.button('Show Produced Volumes', 'Show produced volumes', use_container_width=True)
        with col7:
            comp = st.button('Compare Fields', 'Compare', use_container_width=True)
        col8, col9 = st.columns(2)
        with col8:
            poly_button = st.button('Show Reservoir Area', 'polygon plotter', use_container_width=True)
        with col9:
            clear =  st.button('Clear Output', 'clear sodir', use_container_width=True)
        if run and self.__field == 'No field chosen':
            import time as t
            alert3 = st.warning('Choose a field first')
            t.sleep(1.5)
            alert3.empty()
        
        elif run and self.__time == 'Yearly':
            result = sodir_obj.runY()
            sodir_obj.append_result(result)

        elif run and self.__time == 'Monthly':
            result = sodir_obj.runM()
            sodir_obj.append_result(result)

        if clear:
            sodir_obj.clear_output()

        if comp and len(sodir_obj.getResult()) == 0:
            st.error("""No fields to compare. Choose a field and press Plot production profile. Choose another field and then press
                     Plot production profile again. Then press compare fields.""")
        elif comp:
            st.title('Comparison of Produced Volumes')
            sodir_obj.plot(comp = True)
        sodir_obj.plot()

        st.write(' ')
        st.write(' ')
        st.write(' ')

        if poly_button and self.__field == 'No field chosen':
            import time
            alert4 = st.warning('Choose a field first')
            time.sleep(3)
            alert4.empty()
        elif poly_button and self.__field != 'No field chosen':
            from Modules.SODIR_DATA.Sodir_data import makePolyPlot
            sodir_obj.append_polyPlot(makePolyPlot(self.__field))

        from Modules.SODIR_DATA.Sodir_data import plotPolyPlot
        polyFig = sodir_obj.getPolyPlot()
        if len(polyFig) == 0:
            pass
        else:
            plotPolyPlot(polyFig[-1])

        show_more_prod = st.toggle(label = ("Show me more information about the producing wells on "+ self.__field))    
        if show_more_prod:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.producing_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)

        show_more_inj = st.toggle(label = ("Show me more information about the injection wells on  "+ self.__field))   
        if show_more_inj:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.injecting_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)
        
        show_more_closed = st.toggle(label = ("Show me more information about the closed wells on  "+ self.__field))   
        if show_more_closed:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.closed_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)
        show_more_PA = st.toggle(label = ("Show me more information about the P&A wells on  "+ self.__field))   
        if show_more_PA:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.PA_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)

        CF = self.Curve_fitting(sodir_obj)
    class Curve_fitting():
        def __init__(self, parent):
            self.parent = parent
            st.title("Forecasting")
            col0, col1 = st.columns(2)
            forecast_l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,35,36,37,38,39,4,41,42,43,44,45,46,47,48,49,50,51,52,52,54,55,56,57,58,59,60]
            with col0:    
                FC_length = GUI.dropdown(label="Forecast length (time frame of interst - Years/Months)", options = forecast_l, index = 2, labelVisibility='visible')
                CF_button = st.button('Forecast with Curve Fit Analysis', 'Curve fit', use_container_width=True)
            import Modules.SODIR_DATA.Curve_Fitting as CF
            import Data.dataProcessing as dP
            if CF_button:
                self.__fields = parent.getField()
                self.__time = parent.get_time_frame()
                self.__dfs = parent.getResult()
                if len(self.__dfs) == 0:
                    st.warning("""You must choose a field first and then click 'Show Produced Volumes'. 
                               Repeat for as many fields as desired. Then click
                               'Forecast with Curve Fit Analysis'.""")
                else:
                    st.write(self.__time)
                    if len(set(self.__time)) != 1:
                        st.error("""Forecasts will be made for all fields above. 
                                    Several fields require that the fields have the same 
                                    time frame. Clear Output. Then click Show Produced volumes 
                                    for each field desired, and do not change Time frame of interest between the fields""")
                    else:
                        #Curve_fitted_dfs = CF.Curve_fitting(self.__dfs)
                        Curve_fitted_dfs = (self.__dfs)
                        parent.plot_forecast(self.__dfs, self.__fields, self.__time)
                        






