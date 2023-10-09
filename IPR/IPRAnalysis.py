import Plotting.plotFunc as Plot
from Data.ManualData import manualData
import Data.dataProcessing.dataProcessing as dP 

def IPRAnalysis(precision: str, field:str = None, parameters: list = manualData()):
    if precision == 'Explicit':
        from IPR.dfIPRExplicit import IPROnly
    else: 
        from IPR.dfIPRImplicit import IPROnly
    def swapColumns(df, col1, col2):
        col_list = list(df.columns)
        x, y = col_list.index(col1), col_list.index(col2)
        col_list[y], col_list[x] = col_list[x], col_list[y]
        df = df[col_list]
        return df
    df = IPROnly(*parameters)
    df.columns=('QFieldTarget [sm3/d]', 'qWellTarget[sm3/d]', 'Reservoir pressure [bara]', 'Z-factor', ' Minimum bottomhole pressure [bara]', 'Potential rates per well [sm3/d]', 'Potential field rates [sm3/d]', 'Field rates [sm3/d]', 'Well production rates [sm3/d]', 'yearly gas offtake [sm3]', 'Cumulative gas offtake [sm3]', 'Recovery Factor', 'Bottomhole pressure [bara]')
    df = swapColumns(df, 'QFieldTarget [sm3/d]', 'Field rates [sm3/d]')
    ticker = 0
    list1=['qFieldTarget', 'PRi', 'abandonmentRate', 'TR', 'gasMolecularWeight', 'C_R', 'n', 'N_temp', 'NWellsPerTemplate', 'upTime', 'C_t', 'S', 'C_FL', 'C_PL', 'P_sep', 'IGIP']
    updatedParameters = Plot.display_table(list1, manualData(), method = 'IPR', precision = precision, edible=True)
    if field != 'NO FIELD CHOSEN':
        df = dP.addActualProdYtoDF(field, df)
        df = dP.addProducedYears(field, df)
        #df2=df[['Field rates [sm3/d]', 'gasSM3perday', 'oilSM3perday', 'condensateSM3perday', 'OilEquivalentsSM3perday', 'WaterSM3perday']].copy()
        #Plot.multi_plot(df2)
        Plot.multi_plot(df, addProduced=True)
    if field == 'NO FIELD CHOSEN':
        Plot.multi_plot(df, addAll = False)
    if updatedParameters != False:
        df2 = IPROnly(*updatedParameters)
        df2.columns=('QFieldTarget [sm3/d]', 'qWellTarget[sm3/d]', 'Reservoir pressure [bara]', 'Z-factor', ' Minimum bottomhole pressure [bara]', 'Potential rates per well [sm3/d]', 'Potential field rates [sm3/d]', 'Field rates [sm3/d]', 'Well production rates [sm3/d]', 'yearly gas offtake [sm3]', 'Cumulative gas offtake [sm3]', 'Recovery Factor', 'Bottomhole pressure [bara]')
        df2 = swapColumns(df2, 'QFieldTarget [sm3/d]', 'Field rates [sm3/d]')

        Plot.multi_plot(df2, addAll = False)
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
     

      




      


