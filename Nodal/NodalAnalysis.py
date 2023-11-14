from Data.ManualData import manualData
import Data.dataProcessing as dP
def NodalAnalysis(precision: str, field:str = None, Parameters: list = manualData(), i = '1'):
    """precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems."""
    if precision == 'Explicit':
        from Nodal.dfNodalExplicit import Nodal
    else:
        from Nodal.dfNodalImplicit import Nodal
    df = Nodal(*Parameters)
    df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    if field != 'NO FIELD CHOSEN':
        df = dP.addActualProdYtoDF(field, df)
        df = dP.addProducedYears(field, df)
    return df
    

