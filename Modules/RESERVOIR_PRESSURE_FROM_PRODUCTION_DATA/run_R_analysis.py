import pandas as pd, pages.GUI.GUI_functions as display, streamlit as st, Data.getData as get
from Data.Storage.Cache import SessionState

class ReservoirPressureAnalysis(): 
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
        list1 = ['Initial Reservoir Pressure [bara]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Initial Gas in Place [Sm3]']
        self.__parameters = (display.display_table_RESPRES(list1=list1, list2=list2, edible=True))
        return self.__parameters

    def get_Sodir_data_Res_Pres(self):
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
        import pandas as pd
        df = df.drop("Produced Gas [Sm3]", axis = 1)
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
                self.uploaded_data = data.dropna(how='all')
                gas = data.iloc[:,1].to_list()
                gas = [el*1e9 for el in gas]
                df = ResAnalysis(gas, self.__parameters)
                df.index = data.iloc[:,0].to_list()
                return df
            except:
                (st.warning("An error occured with the uploaded file"))
        else:
            import time as ti
            alert10 = st.warning("The format of the uploaded file must be CSV")
            ti.sleep(5)
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
        df = df.drop("Produced Gas [Sm3]", axis = 1)
        import Data.dataProcessing as dP
        df = dP.monthly_produced_DF(self.__field, df )
        df = dP.addProducedMonths(self.__field, df)
    
        return df
    
    def plot(self):
        res = self.getResult()
        field = self.getField()
        time_frame = self.get_time_frame()
        for i in reversed(range(len(res))):
            if isinstance(res[i], pd.DataFrame):
                header_ = 'Estimated Reservoir Pressure ' + str(i+1)
                st.header(header_, divider='red')
                tab1, tab2 = st.tabs(["Plot", "Data"])
                with tab2:
                    st.write("$P_R$ = " + str(self.getParameters()[i][0]) + " bara")
                    st.write("T = " + str(self.getParameters()[i][1]) + " $^{\circ}$C")
                    st.write("Gas Molecular Weight = " + str(self.getParameters()[i][2]) + " g/mol")
                    st.write("IGIP = " + str((self.getParameters()[i][3]/1e9)) + " 1E09 $Sm^3$")
                    if field[i] != "No field chosen":
                        st.write('Production data from Sodir ', field[i][0]+field[i][1:].lower(), ' used for analysis')
                    else:
                        st.write('Uploaded production data used for analysis')
                        try:
                            st.dataframe(self.uploaded_data, use_container_width=True, hide_index=True)
                        except AttributeError:
                            pass                                

                with tab1:
                    st.write("The model assumes gas filled reservoir and does not account for injection volumes or reservoir geometry")
                    display.multi_plot_PR([res[i]], addAll= False, time_frame=time_frame[i])

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
