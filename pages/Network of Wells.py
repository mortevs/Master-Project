import streamlit as st
from Modules.xtra.reservoirModel.reservoirModel import FlowSimulation
# sim = FlowSimulation(t=10000)
# pressure_fig = sim.get_pressure_plot()
# flow_fig = sim.get_flow_plot()

# st.pyplot(pressure_fig)
# st.pyplot(flow_fig)

from Modules.xtra.DryGasNetworks.noChoke import noChoke
from Data.DefaultData import default_network_of_wells
import pandas as pd
import streamlit
class Add_row_table:
        def __init__(self, rows):
            inputnames, list2, list3 = default_network_of_wells()

            df = pd.DataFrame({
                                    'Input': inputnames,
                                    'Well 1': list2,
                                    'Well 2': list3,
                                    'Well 3': list4,
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
            from Data.DefaultData import probability_distributions
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

