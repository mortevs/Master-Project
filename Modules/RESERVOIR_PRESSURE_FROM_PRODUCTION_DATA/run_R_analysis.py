import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
from Data.ManualData import manualData
import streamlit as st
from GUI.GUI_class import RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA
import Data.getData as get
class ReservoirPressureAnalysis(RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA):
    def __init__(self, parent, session_id:str, field:str = 'No field chosen', time: str = 'Yearly'):
        self.__production_data = []
        self.__field = field
        self.__time_frame = time
        self.__result = []
        self.__session_id = session_id
        self.__parameters = []
        self.__state = SessionState.get(id=session_id, result=[], time_frame=[], field=[], production_data=[])

    def updateFromDropDown(self, fieldName, time):
         self.__field, self.__time_frame = fieldName, time
    
    def update_from_upload(self, productionData):
        self.__production_data = productionData
    
    def updateParameterListfromTable(self):
        list1 = ['Initial Reservoir Pressure [bara]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Initial Gas in Place [sm3]']
        PRi = 276 #reservoir pressure bara . these parameters needs to be updated to fetch to the according field
        TR = 92 #reservoir temperature [C]
        gasMolecularWeight = 16 #[g/mol]
        IGIP = 270e9 #Initial gas in place
        self.__parameters.append(display.display_table_RESPRES(list1=list1, list2=[PRi, TR, gasMolecularWeight, IGIP], edible=True))
    

    def runY(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)
        gas = get.CSVProductionYearly(self.__field)[0]
        gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
        PRi = 276 #reservoir pressure bara
        TR = 92 #reservoir temperature [C]
        gasMolecularWeight = 16 #[g/mol]
        IGIP = 270e9 #Initial gas in place
    
        import Data.dataProcessing as dP
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.dry_gas_R_analysis import ResAnalysis
        df = ResAnalysis(gas, PRi, TR, gasMolecularWeight, IGIP)
        import Data.dataProcessing as dP
        df = dP.yearly_produced_DF(self.__field, df)
        df = dP.addProducedYears(self.__field, df)
        #new_row = [0, 0, PRi]
        #new_df = pd.DataFrame([new_row], columns=df.columns)
        #df = pd.concat([new_df, df], ignore_index=True)
        return df
    
    def runM(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)
        gas = get.CSVProductionMonthly(self.__field)[0]
        gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
        PRi = 276 #reservoir pressure bara
        TR = 92 #reservoir temperature [C]
        gasMolecularWeight = 16 #[g/mol]
        IGIP = 270e9 #Initial gas in place
    
        import Data.dataProcessing as dP
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.dry_gas_R_analysis import ResAnalysis
        df = ResAnalysis(gas, PRi, TR, gasMolecularWeight, IGIP)
        import Data.dataProcessing as dP
        df = dP.monthly_produced_DF(self.__field, df )
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
                    st.title('Reservoir pressure: ' + field[i])
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
        self.__state = SessionState.get(id=self.__session_id, result=[], time_frame=[], field=[], production_data=[])
    
    
    def get_current_time_frame(self):
        return self.__time_frame
    def get_current_field(self):
        return self.__field
    def get_current_result(self):
        return self.__result

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
        

