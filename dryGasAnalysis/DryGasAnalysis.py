class DryGasAnalysis:
    import pandas as pd
    def __init__(self, inputs:list = [], method:str = None, precision:str = None, field:str = None):
        import pandas as pd
        self.__parameters:list = inputs
        self.__method = method
        self.__precision = precision
        self.__field = field
        self.__result = []

    def updateFromDropdown(self):
        import Data.getData as get, Plotting.plotFunc as Plot
        import streamlit as st
        fieldnames = get.fieldNames()
        fieldnames.insert(0, 'NO FIELD CHOSEN')
        self.__method, self.__precision, self.__field = Plot.columnDisplay(list1=[['NODAL', 'IPR'],['IMPLICIT', 'EXPLICIT'], fieldnames])
    
    def updateParameterListfromTable(self):
        import Plotting.plotFunc as Plot
        from Data.ManualData import manualData
        list1=['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
        self.__parameters.append(Plot.display_table(list1 = list1, list2 = manualData(), edible=True))

    def run(self):
        if self.__method == 'IPR':
            from IPR.IPRAnalysis import IPRAnalysis
            return IPRAnalysis(self.__precision, self.__field, self.__parameters[-1])
        else:
            from Nodal.NodalAnalysis import NodalAnalysis
            return NodalAnalysis(self.__precision, self.__field, self.__parameters[-1])




        
        # if self.__field != 'NO FIELD CHOSEN':
        #     import Data.dataProcessing.dataProcessing as dP

        #     import Plotting.plotFunc as Plot
            #Plot.multi_plot(self.__result, addProduced=True)
    
    def plotDf(self)->None:
        import streamlit as st
        import Plotting.plotFunc as Plot
        from pandas import DataFrame
        for df in self.__result:
            if isinstance(df, DataFrame):
                Plot.multi_plot(df, addAll=False)

    def getMethod(self) -> str:
        return self.__method
    def getPrecision(self) -> str:
        return self.__precision
    def getResult(self) -> list:
        return self.__result
    def getParameters(self) -> pd.DataFrame:
        return self.__parameters

        



class analysisResult(DryGasAnalysis):
    def __init__(self):
        super().__init__()



import streamlit as st

# This is the SessionState implementation
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def get(**kwargs):
        # Get a SessionState object for the current session
        if not hasattr(st, '_session_state'):
            st._session_state = SessionState(**kwargs)
        return st._session_state


            
        


    