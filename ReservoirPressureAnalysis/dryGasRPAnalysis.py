class ReservoirPressureAnalysis:
    def __init__(self):
        import pandas as pd
        self.__productionData = list
        self.__field = 'NO FIELD CHOSEN'
        from Data.StreamlitUpload import upload 
        upload(text = "Upload a CSV file / Excel file with the following format or choose field from dropdown menu below")
        self.__timeframe = 'Yearly' 

    def updateFromDropdown(self):
        import Data.getData as get
        import Plotting.plotFunc as Plot
        fieldnames = get.fieldNames()
        fieldnames.insert(0, 'NO FIELD CHOSEN')
        import streamlit as st
        self.__field = Plot.dropdown(options = fieldnames)
        self.__timeframe = Plot.dropdown(options = ['Yearly', 'Monthly'])
    
    def run(self):
        if self.__field != 'NO FIELD CHOSEN':
            import Data.dataProcessing.dataProcessing as dP 
            import pandas as pd
            import streamlit as st
            import Data.getData as get
            if self.__timeframe == 'Yearly':
                self.__productionData = get.CSVProductionYearly(self.__field)[0]
                #self.__productionData = dP.addProducedYears(self.__field, self.__productionData)
            elif self.__timeframe == 'Monthly':
                self.__productionData = get.CSVProductionMonthly(self.__field)[0]
                #self.__productionData = dP.addProducedYears(self.__field, self.__productionData)
            st.dataframe(self.__productionData)
            from Data.ManualData import manualData
            inputParameters=manualData()
            prodGas = [20e6, 20e6, 20e6, 20e6, 20e6]
            #df = build(*inputParameters, self.__productionData)
            df = build(*inputParameters, prodGas)
            import Equations.DryGasFlowEquations as DGFE
            #a = st.write(DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6))
            #b = st.write(DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6), q_g=20e6 / N_temp))
            #c = st.write(DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6), q_g=20e6 / N_temp), q_g=20e6/NWells)+169)
            #d = st.write(DGFE.IPR_PR(C_R=C_R, n=n, p_wf=DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6), q_g=20e6 / N_temp), q_g=20e6/NWells)+169, q_g=20e6/NWells))
            # rate = [20e6, 20e6, 20e6, 20e6, 20e6,20e6]
            # for i in range (len(rate)):
            #     def GA(choke):
            #         return DGFE.IPR_PR(C_R=C_R, n=n, p_wf=DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = rate[i]), q_g=rate[i] / N_temp), q_g=rate[i]/NWells)+choke, q_g=rate[i]/NWells)-PRi
            #     from scipy.optimize import fsolve
            #     a = (fsolve(GA, 50))
            #     st.write(DGFE.IPR_PR(C_R=C_R, n=n, p_wf= a + DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = rate[i]), q_g=rate[i] / N_temp), q_g=rate[i]/NWells), q_g=rate[i]/NWells))

import pandas as pd
import numpy as np
from Equations.ZfacStanding import ZfacStanding
import Equations.DryGasFlowEquations as DGFE
from Equations.pWfMinEstimation import pWfMinEstimation
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF
from scipy.optimize import fsolve
from scipy.optimize import root
import matplotlib.pyplot as plt
def build(qFieldTarget: float, PRi: float, abandonmentRate: float, TR:float, gasMolecularWeight: float, C_R: float, n:float, N_temp: float, NWellsPerTemplate: float, upTime: int, C_t: float, S:float, C_FL:float, C_PL:float, P_sep: float, IGIP: float, gasProd: list) -> float: 
    import Equations.DryGasFlowEquations as DGFE, streamlit as st
    NWells = NWellsPerTemplate*N_temp
    a = st.write(DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6))
    b = st.write(DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6), q_g=20e6 / N_temp))
    c = st.write(DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6), q_g=20e6 / N_temp), q_g=20e6/NWells)+169)
    d = st.write(DGFE.IPR_PR(C_R=C_R, n=n, p_wf=DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = 20e6), q_g=20e6 / N_temp), q_g=20e6/NWells)+169, q_g=20e6/NWells))
    rate = [20e6, 20e6, 20e6, 20e6, 20e6,20e6]
    for i in range (len(rate)):
        def GA(choke):
            return DGFE.IPR_PR(C_R=C_R, n=n, p_wf=DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = rate[i]), q_g=rate[i] / N_temp), q_g=rate[i]/NWells)+choke, q_g=rate[i]/NWells)-PRi
        from scipy.optimize import fsolve
        a = (fsolve(GA, 50))
        st.write(DGFE.IPR_PR(C_R=C_R, n=n, p_wf= a + DGFE.Tubingp1(C_T=C_t, s=S, p2=DGFE.Linep1(C_FL=C_FL, p2=DGFE.Linep1(C_FL=C_PL, p2=P_sep, q_g = rate[i]), q_g=rate[i] / N_temp), q_g=rate[i]/NWells), q_g=rate[i]/NWells))

    


        




