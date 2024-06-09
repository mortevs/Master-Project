import streamlit as st
import pages.GUI.GUI_functions as GUI
import numpy as np
from Data.dataProcessing import get_field_list_inc_No_field_chosen
import math
import pandas as pd
from bisect import bisect_left
from Data.DefaultData import default_FD_data


class FIELD_DEVELOPMENT:
    def __init__(self):
        st.title('Field Development')
        def make_pretty(styler):
            styler.set_properties(subset = None, **{'color': 'red'})
            return styler
        
        try:
            self.__fieldnames = get_field_list_inc_No_field_chosen()
        except Exception as e:
            st.write(e)
            st.warning("could not get list of fieldnames from SODIR")
            self.__fieldnames = ["None"]


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
                    For the Nodal method, these sub-calculations include the estimated yearly gas of take, cumulative gas of take,
                    recovery factor, Z-factor, reservoir pressure, rates per well, bottomhole pressure, wellhead pressure,
                    template pressure, PLEM pressure, seperator pressure, rates per template, choke pressure,
                    ratio of template pressure to wellhead pressure, and the production potential. For the IPR method the sub-calculations that can 
                    be displayed are Qwelltarget, reservoir pressure, z-factor, minimum bottom-hole pressure, potential rates per well, qfield target, 
                    well production rates, yearly gas offtake, cumulative gas offtake, recovery factor, and bottom-hole pressure. """)
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
                field = GUI.dropdown(label = 'Choose a field to compare with', options = self.__fieldnames, labelVisibility="visible")
                Analysis.updateField(field)
        with col1:
            Analysis.updateFromDropdown(method = self._method, precision=self._precision)
            params = Analysis.updateParameterListfromTable()
            if params != default_FD_data():
                default_message.empty()
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
                        with different number of templates. Switch from the drop-down option mentioned above between 2 and 1 to see the NPV difference.
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
            st.write("The NPV does not take consideration to applicable taxes/royalties")
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

                w_string = f"""The NPV does not take consideration to taxes and royalties. All templates and wells are assumed equal. Therefore number of wells in grid seach follows
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
                  default distributed (as we are optimizing on number of wells, a cost distribution must be assumed).
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
            st.title("Uncertainty Analysis")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            col16, col17 = st.columns(2)
            col18, col19 = st.columns(2)

            with col16:
                st.markdown("**Uncertainty in variables**")
                Gas_Price, IGIP_input, LNG_plant_per_Sm3, OPEX_variable, well_cost, PU_cost, temp_cost, LNG_carrier  = dry_gas_NPV.get_inital_MC_variables()
                self.__edited_uncertainity_table = GUI.display_uncertainty_table(Gas_Price, IGIP_input, LNG_plant_per_Sm3, OPEX_variable, well_cost, PU_cost, temp_cost, LNG_carrier)

                #edited_df = self.__edited_df, prod_profiles = prodProfiles_to_NPV, i = i)

                #st.write(NPVsMC)
            with col17:
                st.markdown("**Monte Carlo Analysis parameters (optional optimization)**")
                self._Nr_random_num, self._Nr_bins, self._Nr_Production_profiles = GUI.display_table_Monte_Carlo_param()
            with col18:
                UC = st.button(label = "Run uncertainity Analysis", use_container_width=True)
            if UC:
                prodProfiles_to_Tornado = dry_gas_NPV.Tornado_production_profiles(self.__edited_uncertainity_table, minROA=self.__minROA)
                initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, NPV_OPEXmax, NPV_OPEXmin, NPV_Wellmax, NPV_Wellmin, NPV_PUmax, NPV_PUmin, NPV_tempmax, NPV_tempmin, NPV_Carriermax, NPV_Carriermin = dry_gas_NPV.getNPVsforTornado(dfMC = self.__edited_uncertainity_table, NPV_edited_df=self.__edited_df, prod_profiles= prodProfiles_to_Tornado)
                
                GUI.tornadoPlot(initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, Gas_Price, IGIP_input, LNG_plant_per_Sm3, NPV_OPEXmax, NPV_OPEXmin, OPEX_variable, NPV_Wellmax, NPV_Wellmin, NPV_PUmax, NPV_PUmin, NPV_tempmax, NPV_tempmin, NPV_Carriermax, NPV_Carriermin, well_cost, PU_cost, temp_cost, LNG_carrier)
                GUI.tornadoPlotSensitivity(NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, NPV_OPEXmax, NPV_OPEXmin, NPV_Wellmax, NPV_Wellmin, NPV_PUmax, NPV_PUmin, NPV_tempmax, NPV_tempmin, NPV_Carriermax, NPV_Carriermin,)
                wait_msg = st.warning("Monte Carlo simulation running. Have some patience.")
                from Modules.MONTE_CARLO.Monte_carlo_standAlone import RandomNumbers_with_Distribution_consideration
                GP_array, IGIP_array, LNG_array, OPEX_array, wellcost_array, PUCost_array, tempcost_array, vesselcost_array = RandomNumbers_with_Distribution_consideration(df = self.__edited_uncertainity_table, size = self._Nr_random_num)
                IGIP_P1 = self.__edited_uncertainity_table['P1'][1]
                IGIP_P99 = self.__edited_uncertainity_table['P99'][1]
                IGIP_smart_array = np.linspace(IGIP_P1, IGIP_P99, self._Nr_Production_profiles)
                def find_closest_numbers(a_list, b_list):
                    def closest_number(target):
                        pos = bisect_left(a_list, target)
                        if pos == 0:
                            return a_list[0]
                        if pos == len(a_list):
                            return a_list[-1]
                        before = a_list[pos - 1]
                        after = a_list[pos]
                        if abs(after - target) < abs(before - target):
                            return after
                        else:
                            return before
                    closest_numbers = []

                    for b in b_list:
                        closest = closest_number(b)
                        closest_numbers.append(closest)

                    return closest_numbers
                closest_IGIP_array = find_closest_numbers(IGIP_smart_array, IGIP_array)
                pp_MC_pre_defined_dict = dry_gas_NPV.Monte_Carlo_production_profiles(self.__minROA, IGIP_smart_array)
                PP_MC_assigned_array = np.array(([np.array(pp_MC_pre_defined_dict.get(key)) for key in closest_IGIP_array]), dtype=object)
                results = [dry_gas_NPV.NPV_calculation_Uncertainty(df=self.__edited_df, gas_price=gas_price,
                                                   LNG_p_vari=LNG_p_vari, yGofftake=pp, opex_cost = opexx, well_cost= wc, PU_cost= puc, temp_cost= tempc, carrier_cost=vesc)
                                                for gas_price, LNG_p_vari, pp, opexx, wc, puc, tempc, vesc in zip(GP_array, LNG_array, PP_MC_assigned_array, OPEX_array, wellcost_array, PUCost_array, tempcost_array, vesselcost_array)]

                results_array = np.array(results)
                from Modules.MONTE_CARLO.Monte_carlo_standAlone import Monte_Carlo_Simulation
                fig_pdf, fig_cdf, table = Monte_Carlo_Simulation(self._Nr_bins, results_array, self._Nr_random_num)
                col20, col21 = st.columns(2)
                with col20:
                    st.plotly_chart(fig_pdf, use_container_width=True)
                    st.dataframe(table, hide_index=True, use_container_width=True)
                with col21:
                    st.plotly_chart(fig_cdf, use_container_width=True)
                wait_msg.empty()
                st.warning("""
                           Nr production profiles (20 by default) are simulated for IGIPs between P1 and P99 IGIP with fixed spacing. 
                           A random IGIP number is chosen between P1 and P99 Nr random Samples times (100 000 times by default).
                           Instead of simulating 100 000 production profiles, the simulated production profile generated for the IGIP closest to the random IGIP is used.
                           This is an approximation, because generating 100 000 production profiles would be too computational costly. If the IGIP sensitivity
                           is low, this approximation should be fine. Alternatively, Nr production profiles can be increased. 
                            NOTE that optimized number of templates and plateau rate are not automatically used. If you would like to
                            use the optimized variables for the Monte Carlo Analyis, you would have to generate a new production profile with the optimized
                            variables that were found. All NPVs found in the Monte Carlo Analysis are found for the optimized rate of abandonment for those variables (assuming it occurs above the
                            minimum Rate of Abandonment treshhold specified above). As the gas price variable, OPEX, and the other variables are randomly chosen (following the distribution), the 
                           optimum abandonment rate changes. Therefore, an analysis done to find the optimum abandonmentrate, so that it is always the highest NPV for all
                           configurations that are considered. 
                            The Monte Carlo Analysis considers the editable NPV table above. Any changes to the editable table
                           will be considered in the Monte Carlo analysis, as the fractions with time from the cost distribution is considered for all variables).
                    """)




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
    'About': "# Master project by Morten Vier Simensen"}
    )
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(264, 49, 49);
}
</style>""", unsafe_allow_html=True)
field_development = FIELD_DEVELOPMENT()



