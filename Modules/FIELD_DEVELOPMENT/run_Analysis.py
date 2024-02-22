import pandas as pd
from Data.Storage.Cache import SessionState
import pages.GUI.GUI_functions as GUI
from Data.DefaultData import default_FD_data
import streamlit as st

class DryGasAnalysis():
    def __init__(self, session_id:str, inputs:list = [], method:str = None, precision:str = None, field:str = 'No field chosen'):
        self.__parameters:list = inputs
        self.__method = method
        self.__precision = precision
        self.__field = field
        self.__session_id = session_id
        self.__result = pd.DataFrame()
        self.__state = SessionState.get(id=session_id, result=[], method=[], precision=[], field=[])
       

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
        list1 = ['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]', 'build-up period [years]']
        self.__parameters = (GUI.display_FD_variables_table(list1=list1, list2=default_FD_data(), edible=True))



    def run(self):
        self.append_method(self.__method)
        self.append_precision(self.__precision)
        self.append_field(self.__field)
        self.append_parameters(self.__parameters)
        if self.__method == 'IPR':
            from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
            df = IPRAnalysis(self.__precision, self.__parameters)
        else:
            from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
            df = NodalAnalysis(self.__precision, self.__parameters)
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
            for i in reversed(range(len(res))):
                if isinstance(res[i], DataFrame):
                    field = self.getField()
                    method = self.getMethod()
                    prec = self.getPrecision()
                    st.header('Prod-profile: ' + str(i + 1), divider='red')
                    if field[i] != 'No field chosen':
                        st.write(method[i], prec[i], field[i])
                        GUI.multi_plot([res[i]], addProduced=True)
                    else:
                        st.write(method[i], prec[i])
                        GUI.multi_plot([res[i]], addAll=False)
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            st.header('Compared models', divider='red')
            GUI.multi_plot(dfs, addAll=False)
    
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

    def get_production_profile(self, opt) -> list:
        Fr = self.getResult()[opt-1]['Field rates [sm3/d]'].to_list()
        return Fr
       
    def append_method(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'method', value = item)

    def append_precision(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'precision', value = item)

    def append_result(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'result', value = item)

    def append_parameters(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'parameters', value = item)
    
    def append_field(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'field', value = item)

class NPVAnalysis(DryGasAnalysis):
    from Modules.FIELD_DEVELOPMENT.Artificial_lift import artificial_lift_class
    #a_l = artificial_lift_class()
    def __init__(self, parent, Analysis, opt):
        self.__Analysis = Analysis
        self.__opt = opt
        self.__CAPEX = []
        self.__OPEX = []
        self.__NPV_variables = []
        self.__sheet = []
        self.parent  = parent
        self.__data_For_NPV_sheet = []
        const_NPV_toggle = st.toggle("constant Gas Price and Discount rate ", value=True, label_visibility="visible")
        build_up_NPV_toggle =  st.toggle("Include build up period", value=True, label_visibility="visible")
        if build_up_NPV_toggle == 0:
            buildUp_length = 0
        self.__production_profile = Analysis.get_production_profile(opt = opt)

    def updateParameterListfromTable(self):
        from Data.DefaultData import manualData_NPV, manualData_NPV_CAPEX, manualData_NPV_OPEX
        CAPEX = ["Well Cost [MUSD]", 'Pipeline & Umbilicals [MUSD]', 'Subsea Manifold Cost [MUSD]', 'LNG Plant [MUSD]', 'LNG Vessels [MUSD]']
        OPEX = ["OPEX [MUSD]"]
        col0, col1, col2 = st.columns(3)
        with col0:
            st.title("NPV variables")
            self.__NPV_variables = (GUI.display_table_NPV(list1=['Gas Price [USD per Sm3]', 'Discount Rate [%]', 'Length of Build-up Period [years]', 'uptime [days]'], list2=manualData_NPV(), edible=True, key = 'df_table_editor_NPV'))
        with col1:
            st.title('CAPEX variables')
            self.__CAPEX = (GUI.display_table_NPV(list1=CAPEX, list2=manualData_NPV_CAPEX(), edible=True, key = 'df_table_editor2_CAPEX'))
        with col2:
            st.title('OPEX variables')
            self.__OPEX = (GUI.display_table_NPV(list1=OPEX, list2=manualData_NPV_OPEX(), edible=True, key = 'df_table_editor2_OPEX'))
        
        self.__data_For_NPV_sheet = [self.__NPV_variables, self.__CAPEX, self.__OPEX]
        self.__sheet = GUI.NPV_sheet(parent = NPVAnalysis, Analysis = self.__Analysis, opt = self.__opt, user_input = self.__data_For_NPV_sheet, key = 'df_table_sheet')
        NPV_str = str("Final NPV: " + str(self.__sheet.get_final_NPV().round(1)) + ' MUSD')
        st.title(NPV_str)


        #mylist2 =
        #self.__tot.append(display.display_table_NPV(list1=OPEX, list2=manualData_NPV_OPEX(), edible=True, key = 'df_table_editor2_OPEX'))



