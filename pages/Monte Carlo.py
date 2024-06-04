import streamlit as st, pages.GUI.GUI_functions as GUI, pandas as pd, numpy as np
from Data.DefaultData import probability_distributions

class Monte_Carlo_standAlone:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            on_MCSA_information = st.toggle("Show me information on how to use Monte Carlo Analysis", value=False, label_visibility="visible")
            if on_MCSA_information:
                st.write("""A Monte Carlo Analysis is run with the input data. Change the inputs by double pressing the cells. P1 should be less than P50 which should be 
                        less than P99. 
                        The rows should be addable. Number of rows in the table can be chosen from the dropdown menu below. For instance all the rows should be
                        time [Hours] or cost [1E06 USD].
                        Uncertainties will be run on each variable according to the probability distribution for that row, P1 (Min), P99 (Max),
                        and P50 (ML) if applicable for the distribution chosen. They will then be added together to give a final/total probability distribution.
                        A different probability distribution than the pert (default) can be considered. Other available distributions 
                        are 'triangular', 'uniform', 'normal', 'lognormal' and 'exponential'. They can be chosen from a dropdown menu by double pressing the cell.
                        The Monte Carlo Analysis Parameters can be adjusted to obtain a smoother output probability distribution
                        according to the needs by adjusting the table below to the right. For most basic applications, the default values should be sufficient. 
                        If needed, the number of random numbers (simulations) and number of bins can be adjusted. Higher numbers are more computational costly.
                        """)
            default_message = st.warning("Default values/distributions below. Change to desired values and distributions")


        col18, col19 = st.columns(2)
        col16, col17 = st.columns(2)
        my_list = []
        for i in range(1, 101):
            my_list.append(i)
        with col16:
            self.__rows = st.selectbox(label='Number of rows', options = my_list, index=2)
        row_table_obj = self.Add_row_table(self.__rows)
        with col18:
            st.markdown("**Uncertainty in variables and probability distribution**")
            self._edited_MC_table = row_table_obj.display_table()
            from Data.DefaultData import default_MC_SA
            if self._edited_MC_table['P1'].to_list() != default_MC_SA()[1]:
                default_message.empty()
            elif self._edited_MC_table['P50'].to_list() != default_MC_SA()[2]:
                default_message.empty()
            elif self._edited_MC_table['P99'].to_list() != default_MC_SA()[3]:
                default_message.empty()
            elif self._edited_MC_table['P Dist'].to_list() != ['pert (default)', 'pert (default)', 'pert (default)']:
                default_message.empty()




      


        with col19:
            st.markdown("**Monte Carlo Analysis parameters (optional optimization)**")
            self._Nr_random_num, self._Nr_bins = GUI.display_table_Monte_Carlo_param2()

        colR, colR2 = st.columns(2)
        with col16:
            MC = st.button(label = "Run Monte Carlo-Analysis", use_container_width=True)
            if MC:
                from Modules.MONTE_CARLO.Monte_carlo_standAlone import RandomNumbers_with_Distribution_consideration
                list_of_arrays = RandomNumbers_with_Distribution_consideration(df = self._edited_MC_table, size = self._Nr_random_num)
                results_array = np.sum(list_of_arrays, axis=0)
                from Modules.MONTE_CARLO.Monte_carlo_standAlone import Monte_Carlo_Simulation
                fig_pdf, fig_cdf, table = Monte_Carlo_Simulation(self._Nr_bins, results_array, self._Nr_random_num, title_xaxis="addable input")
                with colR:
                    st.plotly_chart(fig_pdf, use_container_width=True)
                    st.dataframe(table, hide_index=True, use_container_width=True)
                with colR2:
                    st.plotly_chart(fig_cdf, use_container_width=True)


    class Add_row_table:
        def __init__(self, rows):
            from Data.DefaultData import default_MC_SA, probability_distributions
            list1, list2, list3, list4 = default_MC_SA()
            p_dists = probability_distributions()
            df = pd.DataFrame({
                                    'Input': list1,
                                    'P1': list2,
                                    'P50': list3,
                                    'P99': list4,
                                    'P Dist' : [p_dists[0] for el in list1]
                                })
            list1 = list(df['Input'])
            list2 = list(df['P1'])
            list3 = list(df['P50']) 
            list4 = list(df['P99'])

            if rows < 3:
                for i in range((len(list1)-rows)):
                    list1 =  list1[:-1]
                    list2 =  list2[:-1]
                    list3 =  list3[:-1]
                    list4 = list4[:-1]

            else:
                for i in range(rows-(len(list1))):
                    list1.append("New Input")
                    list2.append(1)
                    list3.append(2)
                    list4.append(3)

            from Data.DefaultData import probability_distributions
            p_dists = probability_distributions()

            self.__df_table = pd.DataFrame({
                'Input': list1,
                'P1': list2,
                'P50': list3,
                'P99': list4,
                'P Dist' : [p_dists[0] for el in list1]
            })
        def display_table(self):
            p_dists = probability_distributions()
            edited_table = st.data_editor(
                self.__df_table,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "P Dist": st.column_config.SelectboxColumn(
                        label="Prob dist",
                        help="Probability distribution of the input variable",
                        width="small",
                        options=p_dists,
                        required=True
                    ),
                    "P1": st.column_config.NumberColumn(
                        label="P1",
                        help="1% probability for variable to be below input"
                    ),
                    "P50": st.column_config.NumberColumn(
                        label="P50",
                        help="Most Likely value / Median value (50% probability)"
                    ),
                    "P99": st.column_config.NumberColumn(
                        label="P99",
                        help="99% probability for variable to be below input"
                    )
                }
            )
            return edited_table
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
st.title('Monte Carlo Analysis')
MC = Monte_Carlo_standAlone()