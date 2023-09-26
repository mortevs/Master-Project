from Data.ManualData import manualData
import Data.getData as get 
import Data.dataProcessing.dataProcessing as dP
import streamlit as st
import Plotting.plotFunc as Plot
 
def NodalAnalysis(precision: str, field:str = None):
    
    """
   
    precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems. 
   
    """
    if precision == 'Explicit':
        from Nodal.dfNodalExplicit import Nodal
    else:
        from Nodal.dfNodalImplicit import Nodal

    parameters = manualData()

    df = Nodal(*parameters)
    df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    qFieldTarget = parameters[0]
    abandonmentRate = parameters[2]
    ticker = 0
    if field != 'NO FIELD CHOSEN':
        df = dP.addActualProdYtoPlot(field, df)
        df = dP.addProducedYears(field, df)
        df2=df[['Field rates [sm3/d]', 'ActualProducedRatesSM3perday']].copy()
        Plot.multi_plot(df2)
    Plot.multi_plot(df)
    list1=['qFieldTarget', 'PRi', 'abandonmentRate', 'TR', 'gasMolecularWeight', 'C_R', 'n', 'N_temp', 'NWellsPerTemplate', 'upTime', 'C_t', 'S', 'C_FL', 'C_PL', 'P_sep', 'IGIP']
    Plot.display_table(list1, manualData())
    return df

    # for i in range (df.shape[0]):
    #     if (df.iloc[i, 0] < qFieldTarget and ticker == 0):
    #         print("Plateau length estimated to end in year ", i)
    #         ticker = 1
    #     if (df.iloc[i, 0]) <= abandonmentRate:
    #         print ("Abandonment rates estimated to be reached in year ", i)
    #         #multi_plot(df, title=precision + " Nodal analysis")
    #         #if field != None:
    #             #multi_plot(df2, title=precision + " Nodal analysis")

    #         return df  
    #     elif i == (df.shape[0]-1):
    #         #multi_plot(df, title=precision + " Nodal analysis")
    #         #if field != None:
    #             #multi_plot(df2, title=precision + " Nodal analysis")
    #         return df
        

