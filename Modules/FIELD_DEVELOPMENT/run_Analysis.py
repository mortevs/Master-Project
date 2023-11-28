import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
from Data.ManualData import manualData
from GUI.GUI_class import FIELD_DEVELOPMENT

class DryGasAnalysis(FIELD_DEVELOPMENT):
    def __init__(self, parent, session_id:str, inputs:list = [], method:str = None, precision:str = None, field:str = 'No field chosen'):
        self.__parameters:list = inputs
        self.__method = method
        self.__precision = precision
        self.__field = field
        self.__session_id = session_id
        self.__result = pd.DataFrame()
        self.__state = SessionState.get(id=session_id, result=[], method=[], precision=[], field=[])
        self.parent  = parent

    def updateFromDropdown(self, method, precision):
            self.__method, self.__precision = method, precision

    def updateField(self, fieldName):
         self.__field = fieldName
    
    def get_current_field(self):
        return self.__field
    def get_current_method(self):
        return self.__method
    def get_current_precision(self):
        return self.__precision
    def get_current_result(self):
        return self.__result


    def updateParameterListfromTable(self):
        list1 = ['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
        self.__parameters.append(display.display_table(list1=list1, list2=manualData(), edible=True))

    def run(self):
        self.append_method(self.__method)
        self.append_precision(self.__precision)
        self.append_field(self.__field)
        if self.__method == 'IPR':
            from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
            df = IPRAnalysis(self.__precision, self.__parameters[-1])
        else:
            from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
            df = NodalAnalysis(self.__precision, self.__parameters[-1])
        self.__result = df
        return df
    
    def run_field(self, field):
        self.append_method(self.__method)
        self.append_precision(self.__precision)
        self.append_field(field)

        if self.__method == 'IPR':
            from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
            df = IPRAnalysis(self.__precision, self.__parameters[-1])
        else:
            from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
            df = NodalAnalysis(self.__precision, self.__parameters[-1])
        import Data.dataProcessing as dP
        df = dP.addActualProdYtoDF(field, df)
        df = dP.addProducedYears(field, df)
        return df
    
    def plot(self, comp=False):
        import streamlit as st
        from pandas import DataFrame
        res = self.getResult()
        if comp == False:
            for i in range(len(res)):
                if isinstance(res[i], DataFrame):
                    field = self.getField()
                    method = self.getMethod()
                    prec = self.getPrecision()
                    st.title('Production profile: ' + str(i + 1))
                    if field[i] != 'No field chosen':
                        st.write(method[i], prec[i], field[i])
                        display.multi_plot([res[i]], addProduced=True)
                    else:
                        st.write(method[i], prec[i])
                        display.multi_plot([res[i]], addAll=False)
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            display.multi_plot(dfs, addAll=False)

    def clear_output(self):
        from Data.Storage.Cache import SessionState
        SessionState.delete(id = 'DryGasAnalysis')
        self.__state = SessionState.get(self.__session_id, result=[], method=[], precision=[], field=[])
    

    def getMethod(self) -> str:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'method', None)

    def getPrecision(self) -> str:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'precision', None)

    def getResult(self) -> list:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'result', [])

    def getParameters(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'parameters', pd.DataFrame())
    
    def getField(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'field', pd.DataFrame())

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state
    
    def append_method(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'method', value = item)

    def append_precision(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'precision', value = item)

    def append_result(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'result', value = item)

    def append_parameters(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'parameter', value = item)
    
    def append_field(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'field', value = item)
        
