from Plotting.multi_plot import multi_plot
from Data.pullData import pullData
from Data.ManualData import manualData
import Data.getData as get 
import Data.dataProcessing.dataProcessing as dP 

 
def NodalAnalysis(precision: str, field:str = None):
    
    """
   
    precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems. 
   
    """
    if precision.lower() == 'implicit':
        from Nodal.dfNodalImplicit import Nodal
    elif precision.lower() == 'explicit':
        from Nodal.dfNodalExplicit import Nodal
    else: 
        raise ValueError('you chose ', precision, " precision, but the only options are implicit and explicit.")  
    #if field.lower() == "manual data" or field.lower() == "manualdata":
    parameters = manualData()
    #elif file_id is None:
        #parameters = pullData(field)
    df = Nodal(*parameters)
    df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    qFieldTarget = parameters[0]
    abandonmentRate = parameters[2]
    ticker = 0
    if field != None:
        df = dP.addActualProdYtoPlot(field, df)
        df = dP.addProducedYears(field, df)
        df2=df[['Field rates [sm3/d]', 'ActualProducedRatesSM3perday']].copy()
    for i in range (df.shape[0]):
        if (df.iloc[i, 0] < qFieldTarget and ticker == 0):
            print("Plateau length estimated to end in year ", i)
            ticker = 1
        if (df.iloc[i, 0]) <= abandonmentRate:
            print ("Abandonment rates estimated to be reached in year ", i)
            multi_plot(df, title=precision + " Nodal analysis")
            if field != None:
                multi_plot(df2, title=precision + " Nodal analysis")

            return df  
        elif i == (df.shape[0]-1):
            multi_plot(df, title=precision + " Nodal analysis")
            if field != None:
                multi_plot(df2, title=precision + " Nodal analysis")
            return df
        

