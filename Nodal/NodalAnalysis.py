from Data.ManualData import manualData
import Data.getData as get 
import Data.dataProcessing.dataProcessing as dP
import streamlit as st
import Plotting.plotFunc as Plot
import pandas as pd

def NodalAnalysis(precision: str, field:str = None, inputParameters: list = manualData()):
    
    """
   
    precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems. 
   
    """
    if precision == 'Explicit':
        from Nodal.dfNodalExplicit import Nodal
    else:
        from Nodal.dfNodalImplicit import Nodal
    df = Nodal(*inputParameters)
    df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    qFieldTarget = inputParameters[0]
    abandonmentRate = inputParameters[2]
    ticker = 0
    list1=['qFieldTarget', 'PRi', 'abandonmentRate', 'TR', 'gasMolecularWeight', 'C_R', 'n', 'N_temp', 'NWellsPerTemplate', 'upTime', 'C_t', 'S', 'C_FL', 'C_PL', 'P_sep', 'IGIP']
    updatedParameters = Plot.display_table(list1, manualData(), method = 'IPR', precision = precision, edible=True)
    st.title('Estimated Production profile')
    if field != 'NO FIELD CHOSEN':
        df = dP.addActualProdYtoDF(field, df)
        df = dP.addProducedYears(field, df)
        df2=df[['Field rates [sm3/d]', 'gasSM3perday', 'oilSM3perday', 'condensateSM3perday', 'OilEquivalentsSM3perday', 'WaterSM3perday']].copy()
        Plot.multi_plot(df2)
        Plot.multi_plot(df, addProduced=True)
    if field == 'NO FIELD CHOSEN':
        Plot.multi_plot(df, addAll = False)
    
    if updatedParameters != False:
        df = Nodal(*updatedParameters)
        df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
        Plot.multi_plot(df, addAll=False)
    return df
    

