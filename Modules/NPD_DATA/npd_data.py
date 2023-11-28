import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
from GUI.GUI_class import NPD_DATA
import streamlit as st

class npd_prod(NPD_DATA):
    def __init__(self, parent, session_id:str, field:str = 'No field chosen'):
        self.__field = field
        self.__session_id = session_id
        self.__result = []
        self.__time_frame = []
        self.__state = SessionState.get(id=session_id, result=[], field=[], time_frame = [])
        self.parent  = parent

    def updateFromDropDown(self, fieldName, time):
         self.__field, self.__time_frame = fieldName, time
    
    def get_current_time_frame(self):
        return self.__time_frame
    def get_current_field(self):
        return self.__field
    def get_current_result(self):
        return self.__result

    def runY(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)  
        import Data.dataProcessing as dP
        df = dP.yearly_produced_DF(self.__field, df = pd.DataFrame())
        df = dP.addProducedYears(self.__field, df)
        return df
    
    def runM(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)  
        import Data.dataProcessing as dP
        df = dP.monthly_produced_DF(self.__field, df = pd.DataFrame())
        df = dP.addProducedMonths(self.__field, df)
        return df

    
    def plot(self, comp=False):
        import streamlit as st
        from pandas import DataFrame
        res = self.getResult()
        if comp == False:
            for i in range(len(res)):
                if isinstance(res[i], DataFrame):
                    field = self.getField()
                    st.title('Produced volumes: ' + field[i])
                    display.multi_plot([res[i]], addAll= False)
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            display.multi_plot(dfs, addAll=False)

    def clear_output(self):
        from Data.Storage.Cache import SessionState
        SessionState.delete(id = self.__session_id)
        self.__state = SessionState.get(id=self.__session_id, result=[], field=[], time_frame = [])
    

    def getResult(self) -> list:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'result', [])

    def get_time_frame(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'time_frame', pd.DataFrame())
    
    def getField(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'field', pd.DataFrame())

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state
    
    def append_time_frame(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'time_frame', value = item)

    def append_result(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'result', value = item)
    
    def append_field(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'field', value = item)
        
