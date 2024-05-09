import numpy as np
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
class Monte_Carlo():
    def __init__(self, parent, df):
        self.__rows = len(df.index)
        function_map = {'uniform': np.random.uniform, 'normal': np.random.normal}
        dist_dict = {'uniform': ['P1', 'P99'], 'pert (default)' : ['P1', 'P50', 'P99']}
        rand_variables = []
        for i in range(self.__rows):
            func = (function_map[df.iloc[i]['P Dist']])
            var = func(*df[dist_dict[df.iloc[i]['P Dist']]].loc[i].to_list(), 5)
            rand_variables.append(var)

        st.write(rand_variables)
            

            





        #NPV_gas_v = np.random.(NPVgaspricemin,NPVgaspricemax, parent._Nr_random_num)
    #     NPV_IGIP_v = np.random.uniform(NPV_IGIPmin ,NPV_IGIPmax, parent._Nr_random_num)
    #     NPV_CAPEX_v = np.random.uniform(LNGPlantMin ,LNGPlantMax, parent._Nr_random_num)
    #     NPV_v = NPV(NPV_gas_v,NPV_IGIP_v,NPV_CAPEX_v)
    #     nr_bins = parent._Nr_bins
    #     bins = np.linspace(NPV_v.min(),NPV_v.max(),nr_bins)
    #     counts = np.histogram(NPV_v,bins)[0]
    #     pdf = counts/parent._Nr_random_num
    #     bin_for_plotting = (bins[0:-1]+bins[1:])/2

    #     self._fig_pdf = go.Figure()
    #     self._fig_pdf.add_trace(go.Scatter(x=bin_for_plotting, y=pdf, mode='lines', name='pdf'))
    #     self._fig_pdf.update_layout(title='PDF', xaxis_title='NPV [1E06 USD]', yaxis_title='frequency', showlegend=True)
        
    #     # Calculate CDF
    #     cdf = np.cumsum(pdf)
    #     invcdf = 1 - cdf
    #     bins_cdfplot = bins[1:]

    #     # Create CDF plot
    #     self._fig_cdf = go.Figure()
    #     self._fig_cdf.add_trace(go.Scatter(x=bins_cdfplot, y=invcdf, mode='lines', name='ccdf'))
    #     self._fig_cdf.update_layout(title='CCPF', xaxis_title='NPV [1E06 USD]', yaxis_title='Complementary cumulative probability distribution', showlegend=True)

        
    #     self._table = pd.DataFrame({'Variable':['P90 [1E06 USD]','P50 [1E06 USD]','P10 [1E06 USD]'],
    #     'Value':[np.percentile(NPV_v,10),np.percentile(NPV_v,50),np.percentile(NPV_v,90)]})
    #     self._std = np.std(NPV_v)

    # def getResults(self):
    #     return self._fig_pdf, self._fig_cdf, self._table, self._std