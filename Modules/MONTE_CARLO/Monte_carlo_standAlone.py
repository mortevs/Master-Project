import numpy as np
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
class Monte_Carlo():
    def __init__(self, parent, df):
        self.__P10_GP = df['P10'][0]
        self.__P10_IGIP = df['P10'][1]
        self.__P10_LNG = df['P10'][2]
        
        self.__P50_GP = df['P50'][0]
        self.__P50_IGIP = df['P50'][1]
        self.__P50_LNG = df['P50'][2]

        self.__P90_GP = df['P90'][0]
        self.__P90_IGIP = df['P90'][1]
        self.__P90_LNG = df['P90'][2]

        self.__Dist_GP = df['P Dist'][0]
        self.__Dist_IGIP = df['P Dist'][1]
        self.__Dist_LNG = df['P Dist'][2]

        prob_dists_dict = {}


        NPV_gas_v = np.random.(NPVgaspricemin,NPVgaspricemax, parent._Nr_random_num)
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