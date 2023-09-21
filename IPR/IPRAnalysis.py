import Plotting.plotFunc as Plot
from Data.ManualData import manualData
import Data.dataProcessing.dataProcessing as dP 

def IPRAnalysis(precision: str, field:str = None):
    
    """
   
    precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems. 
   
    """
    if precision.lower() == 'implicit':
        from IPR.dfIPRImplicit import IPROnly
    elif precision.lower() == 'explicit':
        from IPR.dfIPRExplicit import IPROnly
    else: 
        raise ValueError('you chose ', precision, " precision, but the only options are implicit and explicit.")
    
    #if field.lower() == "manual data" or field.lower() == "manualdata":
    parameters = manualData()
    #elif file_id is None:
    #    parameters = pullData(field)
        
    def swapColumns(df, col1, col2):
        col_list = list(df.columns)
        x, y = col_list.index(col1), col_list.index(col2)
        col_list[y], col_list[x] = col_list[x], col_list[y]
        df = df[col_list]
        return df

    df = IPROnly(*parameters)
    df.columns=('QFieldTarget [sm3/d]', 'qWellTarget[sm3/d]', 'Reservoir pressure [bara]', 'Z-factor', ' Minimum bottomhole pressure [bara]', 'Potential rates per well [sm3/d]', 'Potential field rates [sm3/d]', 'Field rates [sm3/d]', 'Well production rates [sm3/d]', 'yearly gas offtake [sm3]', 'Cumulative gas offtake [sm3]', 'Recovery Factor', 'Bottomhole pressure [bara]')
    qFieldTarget = parameters[0]
    abandonmentRate = parameters[2]
    df = swapColumns(df, 'QFieldTarget [sm3/d]', 'Field rates [sm3/d]')
    ticker = 0
    if field != None:
        df = dP.addActualProdYtoPlot(field, df)
        df = dP.addProducedYears(field, df)
        df2=df[['Field rates [sm3/d]', 'ActualProducedRatesSM3perday']].copy()
        Plot.multi_plot(df2, title=precision + " IPR analysis")
    Plot.multi_plot(df, title=precision + " IPR analysis")
    #Plot.display_table(list1, list2)
    return df

    # for i in range (len(df.index)):
    #     if (df.iloc[i, 0] < qFieldTarget and ticker == 0):
    #         print("Plateau length estimated to end in year ", i)
    #         ticker = 1
    #     if (df.iloc[i, 0]) <= abandonmentRate:
    #         print ("Abandonment rates estimated to be reached in year ", i)
    #         multi_plot(df, title=precision + " IPR analysis")
    #         if field != None:
    #             multi_plot(df2, title=precision + " IPR analysis")

    #         return df
    #     elif i == (df.shape[0]-1):
    #         multi_plot(df, title=precision + " IPR analysis")
    #         if field != None:
    #             multi_plot(df2, title=precision + " IPR analysis")
    #         return df
     

      




      


