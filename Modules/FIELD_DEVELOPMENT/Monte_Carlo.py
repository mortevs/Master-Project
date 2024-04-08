import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def NPV(Gas_price, IGIP, CAPEX):
    NPV = (Gas_price+IGIP+CAPEX)/3
    return NPV

class Monte_Carlo():
    def __init__(self, parent, NPVgaspricemin = -2422, NPVgaspricemax=4810, NPV_IGIPmin=513, NPV_IGIPmax=1653, NPV_CAPEXmin=-853, NPV_CAPEXmax=3204):
        NPV_gas_v = np.random.uniform(NPVgaspricemin,NPVgaspricemax, parent._Nr_random_num)
        NPV_IGIP_v = np.random.uniform(NPV_IGIPmin ,NPV_IGIPmax, parent._Nr_random_num)
        NPV_CAPEX_v = np.random.uniform(NPV_CAPEXmin ,NPV_CAPEXmax, parent._Nr_random_num)
        NPV_v = NPV(NPV_gas_v,NPV_IGIP_v,NPV_CAPEX_v)
        nr_bins = parent._Nr_bins
        bins = np.linspace(NPV_v.min(),NPV_v.max(),nr_bins)
        counts = np.histogram(NPV_v,bins)[0]
        pdf = counts/parent._Nr_random_num
        bin_for_plotting = (bins[0:-1]+bins[1:])/2

        self._fig = plt.figure()
        plt.xlabel('NPV [1E06 USD]')
        plt.ylabel('frequency')
        plt.title('pdf')
        plt.plot(bin_for_plotting,pdf,'r',label = 'pdf')
        plt.legend()
        plt.grid()
        plt.show()

        cdf = np.cumsum(pdf)
        invcdf = 1- cdf
        bins_cdfplot = bins[1:]

        self._fig2 = plt.figure()
        plt.xlabel('NPV [1E06 USD]')
        plt.ylabel('Complementary cumulative probability distribution')
        plt.title('ccpf')
        plt.plot(bins_cdfplot,invcdf,label = 'ccdf')
        plt.legend()
        plt.grid()
        

        self._table = pd.DataFrame({'Variable':['P90 [1E06 USD]','P50 [1E06 USD]','P10 [1E06 USD]'],
        'Value':[np.percentile(NPV_v,10),np.percentile(NPV_v,50),np.percentile(NPV_v,90)]})
        self._std = np.std(NPV_v)
        
    def getResults(self):
        return self._fig, self._fig2, self._table, self._std