import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
from Data.ManualData import manualData
import streamlit as st

class ReservoirPressureAnalysis:
    def __init__(self, session_id:str, productionData:list = None, field:str = 'No field chosen', time: str = 'yearly'):
        self.__production_data = [productionData]
        self.__field = [field]
        self.__time_frame = [time]
        self.__result = []
        self.__session_id = session_id
        self.__state = SessionState.get(id=session_id, result=[], time_frame=[time], field=[field], production_data=[productionData])

    def updateFromDropdown(self, field, time_frame):
        self.__field = field
        self.__time_frame = time_frame

    def updateParameterListfromTable(self):
        list1 = ['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
        self.__parameters.append(display.display_table(list1=list1, list2=manualData(), edible=True))

    def reset_lists(self):
        self.__production_data = []
        self.__field = ['No field chosen']
        self.__time_frame = ['Yearly']

    def run(self, selected_field, selected_time, df_prod):
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.build_analysis import ResAnalysis
        if df_prod != None:
            st.write('Data upload will be implemented')
        elif selected_field != "No field chosen":
            #self.__state.field.append(self.__field)
            #self.__state.time_frame.append(self.__time_frame)
            #self.__state.production_data.append(self.__production_data)
            res = ResAnalysis()
            st.dataframe(res)
            return (res)


    def plot(self, comp=False):
        import GUI.GUI_functions as display
        from pandas import DataFrame
        if comp == False:
            for i in range(len(self.__state.result)):
                if isinstance(self.__state.result[i], DataFrame):
                    st.title('Production profile: ' + str(i + 1))
                    #st.write(self.__state.method[i], self.__state.precision[i])
                    display.multi_plot([self.__state.result[i]], addAll=False)
                else:
                    st.alert('Something is wrong..')
        else:
            display.multi_plot(self.__state.result, addAll=False)


    def getResult(self) -> list:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'result', [])

    def getState(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return session_state
