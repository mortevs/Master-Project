from Data.ManualData import manualData
import Data.dataProcessing.dataProcessing as dP 

def IPRAnalysis(precision: str, field:str = None, parameters: list = manualData()):
    if precision == 'Explicit':
        from IPR.dfIPRExplicit import IPROnly
    else: 
        from IPR.dfIPRImplicit import IPROnly
    df = IPROnly(*parameters)
    df.columns=('QFieldTarget [sm3/d]', 'qWellTarget[sm3/d]', 'Reservoir pressure [bara]', 'Z-factor', ' Minimum bottomhole pressure [bara]', 'Potential rates per well [sm3/d]', 'Potential field rates [sm3/d]', 'Field rates [sm3/d]', 'Well production rates [sm3/d]', 'yearly gas offtake [sm3]', 'Cumulative gas offtake [sm3]', 'Recovery Factor', 'Bottomhole pressure [bara]')
    df = swapColumns(df, 'QFieldTarget [sm3/d]', 'Field rates [sm3/d]')
    if field != 'NO FIELD CHOSEN':
        df = dP.addActualProdYtoDF(field, df)
        df = dP.addProducedYears(field, df)
    return df

def swapColumns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df





      




      


