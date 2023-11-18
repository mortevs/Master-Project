import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
from Data.ManualData import manualData

class DryGasAnalysis:
    def __init__(self, session_id:str, inputs:list = [], method:str = None, precision:str = None, field:str = None):
        self.__parameters:list = inputs
        self.__method = method
        self.__precision = precision
        self.__field = field
        self.__session_id = session_id
        self.__state = SessionState.get(id=session_id, result=[], method=[], precision=[], field=[])

    def updateFromDropdown(self):
        (self.__method, self.__precision) = display.columnDisplay2(list1=[['NODAL', 'IPR'], ['IMPLICIT', 'EXPLICIT']])

    def updateParameterListfromTable(self):
        list1 = ['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
        self.__parameters.append(display.display_table(list1=list1, list2=manualData(), edible=True))

    def run(self):
        self.__state.method.append(self.__method)
        self.__state.precision.append(self.__precision)
        self.__state.field.append(self.__field)
        if self.__method == 'IPR':
            from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
            return IPRAnalysis(self.__precision, self.__parameters[-1])
        else:
            from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
            return NodalAnalysis(self.__precision, self.__parameters[-1])

    def plot(self, comp=False):
        import streamlit as st
        from pandas import DataFrame
        if comp == False:
            for i in range(len(self.__state.result)):
                if isinstance(self.__state.result[i], DataFrame):
                    st.title('Production profile: ' + str(i + 1))
                    st.write(self.__state.method[i], self.__state.precision[i])
                    display.multi_plot([self.__state.result[i]], addAll=False)
        else:
            display.multi_plot(self.__state.result, addAll=False)

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

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state
