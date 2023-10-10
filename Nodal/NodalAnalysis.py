from Data.ManualData import manualData
import Data.getData as get 
import Data.dataProcessing.dataProcessing as dP
import streamlit as st
import Plotting.plotFunc as Plot
import pandas as pd

def NodalAnalysis(precision: str, field:str = None, Parameters: list = manualData(), i = '1'):
    """precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems."""
    if precision == 'Explicit':
        from Nodal.dfNodalExplicit import Nodal
    else:
        from Nodal.dfNodalImplicit import Nodal
    #df = Nodal(*inputParameters)
    #df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    #list1=['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
    #st.title('Production profile:'+ i)
    df = Nodal(*Parameters)
    df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    if field != 'NO FIELD CHOSEN':
        df = dP.addActualProdYtoDF(field, df)
        df = dP.addProducedYears(field, df)
    return df

        #Plot.multi_plot(df, addProduced=True)
    #else:
        #Plot.multi_plot(df, addAll = False)

        #df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
        #Plot.multi_plot(df, addAll=False)
    

