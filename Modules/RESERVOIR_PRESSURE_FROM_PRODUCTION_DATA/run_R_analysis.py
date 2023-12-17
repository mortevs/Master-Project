import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
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
        self.edible_df = None
        self.__state = SessionState.get(id=session_id, result=[], time_frame=[], field=[], production_data=[], parameters = [])

    def updateFromDropDown(self, fieldName, time):
         self.__field, self.__time_frame = fieldName, time
    
    def update_from_upload(self, productionData):
        self.__production_data = productionData
    
    def updateParameterListfromTable(self, list2):
        list1 = ['Initial Reservoir Pressure [bara]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Initial Gas in Place [sm3]']
        self.__parameters = (display.display_table_RESPRES(list1=list1, list2=list2, edible=True))



    def get__PR_NPD_data(self):
        PRi = get.initial_reservoir_pressure(self.__field)
        T_R = get.Temp(self.__field)        
        gasMolecularWeight = get.gas_molecular_weight(self.__field)
        IGIP = get.IGIP(self.__field)
        return PRi, T_R, gasMolecularWeight, IGIP

    def runY(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)
        self.append_parameters(self.__parameters)
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.dry_gas_R_analysis import ResAnalysis
        gas = get.CSVProductionYearly(self.__field)[0]
        gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
        import Data.dataProcessing as dP
        df = ResAnalysis(gas, self.__parameters)
        import Data.dataProcessing as dP
        df = dP.yearly_produced_DF(self.__field, df)
        df = dP.addProducedYears(self.__field, df)
        return df
    
    def run_uploaded(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)
        self.append_parameters(self.__parameters)
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.dry_gas_R_analysis import ResAnalysis
        uploaded = self.get_current_production_data()
        self.__field = "No field chosen"
        if uploaded.type == "text/csv":
            try:
                data = pd.read_csv(uploaded, sep=";", skip_blank_lines=True)
                data = data.dropna(how='all')
                gas = data.iloc[:,0].to_list()
                df = ResAnalysis(gas, self.__parameters)
                df.index = df.iloc[:,1].to_list()
                return df
            except:
                (st.warning("an error occured with uploaded file, try a new file"))
        else:
            import time as ti
            alert10 = st.warning("You have not uploaded a CSV file")
            ti.sleep(3)
            alert10.empty()

    
    def runM(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)
        self.append_parameters(self.__parameters)
        gas = get.CSVProductionMonthly(self.__field)[0]
        gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3    
        import Data.dataProcessing as dP
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.dry_gas_R_analysis import ResAnalysis
        df = ResAnalysis(gas, self.__parameters)
        import Data.dataProcessing as dP
        df = dP.monthly_produced_DF(self.__field, df )
        df = dP.addProducedMonths(self.__field, df)
        return df
    

    def plot(self, comp=False):
        import streamlit as st
        from pandas import DataFrame
        res = self.getResult()
        field = self.getField()
        if comp == False:
            for i in range(len(res)):
                if isinstance(res[i], DataFrame):
                    header_ = 'Est Res-pressure ' + str(i+1)
                    st.header(header_, divider='red')
                    if field[i] != "No field chosen":
                        st.write(field[i][0]+field[i][1:].lower())
                        st.write("$P_R$ = " + str(self.getParameters()[i][0]) + " Bar")
                        st.write("T = " + str(self.getParameters()[i][1]) + " $^{\circ}$C")
                        st.write("Gas Molecular Wieght = " + str(self.getParameters()[i][2]) + " g/mol")
                        st.write("IGIP = " + str((self.getParameters()[i][3]/1e9)) + " billion $sm^3$")

                    else:
                        st.write('Uploaded data')
                        st.write("$P_R$ = " + str(self.getParameters()[i][0]) + " Bar")
                        st.write("T = " + str(self.getParameters()[i][1]) + " $^{\circ}$C")
                        st.write("Gas Molecular Wieght = " + str(self.getParameters()[i][2]) + " g/mol")
                        st.write("IGIP = " + str((self.getParameters()[i][3]/1e9)) + " billion $sm^3$")
                    display.multi_plot_PR([res[i]], addAll= False)
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            display.multi_plot(dfs, addAll=False)

    def clear_output(self):
        from Data.Storage.Cache import SessionState
        SessionState.delete(id = self.__session_id)
        self.__state = SessionState.get(id=self.__session_id, result=[], time_frame=[], field=[], production_data=[], parameters = [])
    
    
    def get_current_time_frame(self):
        return self.__time_frame
    def get_current_field(self):
        return self.__field
    def get_current_result(self):
        return self.__result
    def get_current_parameters(self):
        return self.__parameters
    def get_current_production_data(self):
        return self.__production_data

    def getResult(self) -> list:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'result', [])

    def get_time_frame(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'time_frame', pd.DataFrame())
    
    def getField(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'field', pd.DataFrame())
    
    def getParameters(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'parameters', pd.DataFrame())

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state
    
    def delParameters(self):
        del self.__parameters
    
    
    def append_time_frame(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'time_frame', value = item)

    def append_result(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'result', value = item)
    
    def append_field(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'field', value = item)
        
    def append_parameters(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'parameters', value = item)
    
    def append_production_data(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'production_data', value = item)

    def get_edible_df(self):
        return self.__edible_df
    
    def update_edible_df(self, list2):
        self.__edible_df.update_table(list2)
        #self.__edible_df = display.edible_df(list2)
        #self.__parameters =self.__edible_df.get_parameters()
        #self.__edible_df = self.__edible_df, self.__parameters = (display.display_table_RESPRES(list1=list1, list2=list2, edible=True))