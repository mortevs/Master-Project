class DryGasAnalysis:
    import pandas as pd
    def __init__(self, inputs:list = [], method:str = None, precision:str = None, field:str = None):
        import pandas as pd
        self.__parameters:list = inputs
        self.__method = method
        self.__precision = precision
        self.__field = field
        from Data.Storage.Cache import SessionState
        self.__state = SessionState.get(result=[], method = [], precision = [], field = [])

    def updateFromDropdown(self):
        import Data.getData as get, GUI.GUI_functions as display
        fieldnames = get.fieldNames()
        fieldnames.insert(0, 'NO FIELD CHOSEN')
        (self.__method, self.__precision, self.__field) = (display.columnDisplay(list1=[['NODAL', 'IPR'],['IMPLICIT', 'EXPLICIT'], fieldnames]))


    def updateParameterListfromTable(self):
        import GUI.GUI_functions as display
        from Data.ManualData import manualData
        list1=['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
        self.__parameters.append(display.display_table(list1 = list1, list2 = manualData(), edible=True))

    def run(self):
        (self.__state.method).append(self.__method)
        (self.__state.precision).append(self.__precision)
        (self.__state.field).append(self.__field)
        if self.__method == 'IPR':
            from IPR.IPRAnalysis import IPRAnalysis
            return IPRAnalysis(self.__precision, self.__field, self.__parameters[-1])
        else:
            from Nodal.NodalAnalysis import NodalAnalysis
            return NodalAnalysis(self.__precision, self.__field, self.__parameters[-1])
    
    def plot(self, comp = False):
        import GUI.GUI_functions as display, streamlit as st
        from pandas import DataFrame
        if comp == False:
            for i in range (len(self.__state.result)):
                if isinstance(self.__state.result[i], DataFrame):
                    st.title('Production profile: '+str(i+1))
                    if self.__state.field[i] != 'NO FIELD CHOSEN':
                        st.write(self.__state.method[i], self.__state.precision[i], self.__state.field[i])
                        display.multi_plot([self.__state.result[i]], addProduced=True)
                    else:
                        st.write(self.__state.method[i], self.__state.precision[i])
                        display.multi_plot([self.__state.result[i]], addAll=False)
        else:
            display.multi_plot(self.__state.result, addAll=False)

            
    def getMethod(self) -> str:
        return self.__state.method
    def getPrecision(self) -> str:
        return self.__state.precision
    def getResult(self) -> list:
        return self.__state.result
    def getParameters(self) -> pd.DataFrame:
        return self.__state.parameters
    def getState(self) -> pd.DataFrame:
            return self.__state

            
        


    