import pandas as pd
from Data.Storage.Cache import SessionState
import pages.GUI.GUI_functions as GUI
from Data.DefaultData import default_FD_data
import streamlit as st
import numpy as np
import time
import math

class DryGasAnalysis():
    def __init__(self, session_id:str, inputs:list = [], method:str = None, precision:str = None, field:str = 'No field chosen'):
        self.__parameters:list = inputs
        self._method = method
        self._precision = precision
        self.__field = field
        self.__session_id = session_id
        self.__result = pd.DataFrame()
        self.__state = SessionState.get(id=session_id, result=[], method=[], precision=[], field=[])      
    
    def updateFromDropdown(self, method, precision):
            self._method, self._precision = method, precision
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
        list1 = ['Target Rate [Sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [Sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]', 'Build-up period [years]']
        self.__parameters = (GUI.display_FD_variables_table(list1=list1, list2=default_FD_data(), edible=True))
        def validate_parameters(list1 = self.__parameters):
            if list1[0] <= 0:
                st.error("Target Rate [sm3/d] must be greater than 0")
                st.stop()            
            if list1[1] <= 0:
                st.error("Initial Reservoir Pressure [bare] must be greater than 0")
                st.stop()
            if list1[2] <= 0:
                st.error('Rate of Abandonment [sm3/d] must be greater than 0')
                st.stop()
            if list1[3] < -273.15:
                st.error("'Reservoir Temperature can not be lower than -273.15 degree C'")
                st.stop()
            if list1[4] <= 0:
                st.error('Gas Molecular Weight [g/mol] must greater than 0')
                st.stop()  
            if list1[7] <= 0:
                st.error('Number of Templates must be greater than 0')
                st.stop()  
            if list1[8] <= 0:
                st.error('Number of Wells per Template must be greater than 0')
                st.stop()  
            if list1[9] <= 0:
                st.error('Uptime [days] must be greater than 0')
                st.stop()
            if list1[9] > 365:
                st.error('Uptime [days] must be less than or equal 365 days')
                st.stop()  
            if list1[14] <= 0:
                st.error('Seperator Pressure [Bara] must be greater than 0')
                st.stop() 
            if list1[15] <= 0:
                st.error('Initial Gas in Place [sm3] must be greater than 0]')
                st.stop()  
            if list1[16] <= 0:
                st.error('Build-up period [years] must be greater than 0')
                st.stop()
            if isinstance(list1[16], float):
                if list1[16].is_integer():
                    pass
                else:
                    st.error('Build-up period [years] must be a whole number')
                    st.stop()
            if isinstance(list1[7], float):
                if list1[7].is_integer():
                    pass
                else:
                    st.error('Number of Templates must be a whole number')
                    st.stop()
            if isinstance(list1[8], float):
                if list1[8].is_integer():
                    pass
                else:
                    st.error('Number of Wells per Template must be a whole number')
                    st.stop()  
            if isinstance(list1[9], float):
                if list1[9].is_integer():
                    pass
                else:
                    st.error('Uptime [days] must be a whole number')
                    st.stop()
        validate_parameters()
        return self.__parameters

    def run(self):
        self.append_method(self._method)
        self.append_precision(self._precision)
        self.append_field(self.__field)
        self.append_parameters(self.__parameters)

        if self._method == 'IPR':
            from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
            df = IPRAnalysis(self._precision, self.__parameters)
        elif self._method == "NODAL":
            from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
            df = NodalAnalysis(self._precision, self.__parameters)
        else:
            st.error("An error has occured, method is not NODAL or IPR")
        self.__result = df
        return df
    
    def run_field(self, field):
        self.append_method(self._method)
        self.append_precision(self._precision)
        self.append_field(field)
        self.append_parameters(self.__parameters)

        if self.__method == 'IPR':
            from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
            df = IPRAnalysis(self._precision, self.__parameters)
        else:
            from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
            df = NodalAnalysis(self._precision, self.__parameters)
        import Data.dataProcessing as dP
        df = dP.addActualProdYtoDF(field, df, upTime=int(self.__parameters[9]))
        df = dP.addProducedYears(field, df)
        return df
        
    def plot(self, comp=False):
        res = self.getResult()
        if comp == False:
            for i in reversed(range(len(res))):
                if isinstance(res[i], pd.DataFrame):
                    field = self.getField()
                    method = self.getMethod()
                    prec = self.getPrecision()

                    st.header('Production Profile ' + str(i + 1), divider='red')
                    tab1, tab2 = st.tabs(["Plot", "Variables"])
                    if field[i] != 'No field chosen':
                        with tab2:        
                            st.write(method[i], prec[i], field[i])
                        with tab1:
                            GUI.multi_plot([res[i]], addProduced=True)
                    else:
                        with tab2:
                            st.write(method[i], prec[i])
                        with tab1:
                            GUI.multi_plot([res[i]], addAll=False)
                with tab2:
                    from pages.GUI.GUI_functions import display_FD_variables_table2
                    display_FD_variables_table2(list2=self.getParameters()[i])
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            st.header('Compared models', divider='red')
            GUI.multi_plot(dfs, addAll=False)
    
    def getParameters(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'parameters', pd.DataFrame())
    
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
    
    def getField(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'field', pd.DataFrame())

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state

    def get_production_profile(self, opt) -> list:
        Fr = self.getResult()[opt]['Field rates [sm3/d]'].to_list()
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
    #from Modules.FIELD_DEVELOPMENT.Artificial_lift import artificial_lift_class
    def __init__(self):
        super().__init__(session_id='DryGasAnalysis')
        self._CAPEX = []
        self._OPEX = []
        self._NPV_variables = []
        self._sheet = []
        self._data_For_NPV_sheet = []
        #self._production_profile = Analysis.get_production_profile(opt = opt)
   
        #const_NPV_toggle = st.toggle("constant Gas Price and Discount rate ", value=True, label_visibility="visible")


        #self.__sheet.display_table_NPV_Sheet()
        #NPV_str = str("Final NPV: " + str(self.__sheet.get_final_NPV().round(1)) + ' 1E6 USD')
        #st.title(NPV_str)

class NPV_dry_gas(NPVAnalysis):
    def __init__(self, opt):
        self._opt = opt
        super().__init__()
        self.__field_variables = self.getParameters()[self._opt]
              
    def NPV_gas_field_update_edible_tables(self):
        from Data.DefaultData import default_data_NPV, default_data_NPV_CAPEX, default_data_NPV_OPEX
        NPV = ['Gas Price [USD/Sm3]', 'Discount Rate [%]', 'Max Wells Drilled p/ Year', 'CAPEX Period [Years]']
        CAPEX = ["Well Cost [1E6 USD]", 'Pipe & Umbilical [1E6 USD]', 'Template [1E6 USD]', 'LNG Plant [USD/ Sm3/d]', 'Cost per LNG Carrier [1E6 USD] ']
        OPEX = ["OPEX [1E6 USD]"]
        self._plateau_rate = self.__field_variables[0]
        self._uptime = self.__field_variables[9]
        col0, col1, col2 = st.columns(3)
        with col0:
            st.markdown("**NPV variables**")
            self.__NPV_variables = (GUI.display_table_NPV(list1=NPV, list2=default_data_NPV(), edible=True, key = 'df_table_editor_NPV'))
        with col1:
            st.markdown('**CAPEX variables**')
            self.__CAPEX = (GUI.display_table_NPV(list1=CAPEX, list2=default_data_NPV_CAPEX(), edible=True, key = 'df_table_editor2_CAPEX'))
        with col2:
            st.markdown('**OPEX variables**')
            self.__OPEX = (GUI.display_table_NPV(list1=OPEX, list2=default_data_NPV_OPEX(), edible=True, key = 'df_table_editor2_OPEX'))
            
        
    def dry_gas_NPV_calc_sheet(self):
        #field development parameters
        self._OPEX_cost = float(self.__OPEX[0])
        self._N_temp = self.__field_variables[7]
        self._N_Wells_per_Temp = self.__field_variables[8]
        self._buildUp_length = int(self.__field_variables[16])

        #NPV table 
        self._Gas_Price = self.__NPV_variables[0]
        self._discount_rate = self.__NPV_variables[1]
        self._Max_Well_per_year_nr = int(self.__NPV_variables[2])
        self._production_profile = self.get_production_profile(self._opt)
        if self._Max_Well_per_year_nr <= 0:
            st.error("Max Number of Wels Drilled per Year must be greater than 0")
            st.stop()
        self._CAPEX_period_prior = int(self.__NPV_variables[3])
        if self._CAPEX_period_prior < 1:
            st.error("CAPEX Period Prior to Production Startup must be greater than 0")
            st.stop()


        #CAPEX table 
        from Data.DefaultData import default_well_distribution, default_template_distribution
        self._end_prod = int(len(self._production_profile)+ (self._CAPEX_period_prior-1))
        self._years = []         
        for i in range(self._end_prod):
            self._years.append(i)    

        self._def_well_list  = default_well_distribution(self._N_temp, self._N_Wells_per_Temp, self._end_prod, self._Max_Well_per_year_nr)
        self._templ_list = default_template_distribution(self._def_well_list, self._N_temp, self._N_Wells_per_Temp, self._end_prod)
        
        self._Well_Cost = self.__CAPEX[0]
        self._p_u = self.__CAPEX[1]
        self._p_u_list = [self._p_u, self._p_u]
        for i in range(2, self._end_prod):
            self._p_u_list.append(0)
        
        self._temp_cost = self.__CAPEX[2]

        self._LNG_plant_per_Sm3 = self.__CAPEX[3]
        self._LNG_cost_per_vessel = self.__CAPEX[4]
        import math #HERE IS THE PROBLEM. I DONT THINK SELF._PLATEAU_RATE IS UPDATING DURING GRID
        number_of_LNG_vessels = (math.ceil(self._plateau_rate*self._uptime/((86000000*22)))) #rough estimation
        self._LNG_plant = self._plateau_rate * self._LNG_plant_per_Sm3 / 1e6
        self._LNG_vessels = self._LNG_cost_per_vessel*number_of_LNG_vessels

        self._LNG_plant_list = [self._LNG_plant/2, self._LNG_plant/2]
        self._LNG_vessels_list = [self._LNG_vessels/2, self._LNG_vessels/2]
        for i in range(2, self._end_prod):
            self._LNG_plant_list.append(0)
            self._LNG_vessels_list.append(0)

        self._OPEX_list = [0 for i in range (self._CAPEX_period_prior)] +  [self._OPEX_cost for i in range (int(len(self._production_profile)-1))]
        
        self.__df_table = pd.DataFrame({
            'Year': self._years,
            'Nr Wells': self._def_well_list,
            'Nr Templates': self._templ_list,
            'Pipeline & Umbilicals [1E6 USD]': self._p_u_list,
            'LNG Plant [1E6 USD]' : self._LNG_plant_list,
            'LNG Vessels [1E6 USD]' : self._LNG_vessels_list,
            'OPEX [1E6 USD]': self._OPEX_list,
        })
        return self.__df_table
    

    def update_dry_gas_NPV_calc_sheet(self, edited_df):
        def validate_edited_df(edited_df):
            self.__edited_dataframe = edited_df
            N_wells = self._N_Wells_per_Temp*self._N_temp
            if sum(edited_df["Nr Wells"]) != N_wells:
                error_str = "The sum of wells in the Nr Wells column needs to be (" + str(int(N_wells)) + ") because the number of templates is ("+ str(int(self._N_temp)) + ") and the number of wells per template is (" + str(int(self._N_Wells_per_Temp)) + "). You need to change the N Wells columns so that the sum of the Nr Wells columns matches (" + str(int(N_wells)) + "). Current sum is (" + str(sum(edited_df["Nr Wells"])) +"). The reason for this is that changing the number of wells will affect the production profile directly, and not just the NPV. If desired then create a new production profile with the desired amount of wells by changing Number of Templates and Number of Wells per Template in the table at the top right."
                st.error(error_str)
                st.stop()
        validate_edited_df(edited_df)
        self._yearly_gas_offtake = [0 for i in range (self._CAPEX_period_prior-1)] + [element * self._uptime for element in self._production_profile]
        self._NPV_prod_profile = [0 for i in range (self._CAPEX_period_prior-1)] + self._production_profile
        self._revenue = [offtake/(1000000) * self._Gas_Price for offtake in self._yearly_gas_offtake]
        
        self._years = []         
        for i in range(self._end_prod):
            self._years.append(i)            

        
        self.__df_table2 = pd.DataFrame({
            'Year': self._years,
            'DRILLEX [1E6 USD]': [element * self._Well_Cost for element in edited_df['Nr Wells']],
            'Templates [1E6 USD]': [element * self._temp_cost for element in edited_df['Nr Templates']],
            'TOTAL CAPEX [1E6 USD]': self._years,
            'Daily gas rate [sm3/d]':self._NPV_prod_profile,
            'Yearly gas offtake [sm3]': self._yearly_gas_offtake,
            'Revenue [1E6 USD]': self._revenue,
            'Cash Flow [1E6 USD]': self._years,
            'Discounted Cash Flow [1E6 USD]': self._years,
            'NPV [1E6 USD]': self._years,
        })
        
        self.__df_table2[ 'TOTAL CAPEX [1E6 USD]'] = [sum(x) for x in zip(self.__df_table2['DRILLEX [1E6 USD]'], edited_df['Pipeline & Umbilicals [1E6 USD]'], self.__df_table2['Templates [1E6 USD]'], edited_df['LNG Plant [1E6 USD]'], edited_df['LNG Vessels [1E6 USD]'])]
        self.__df_table2['Cash Flow [1E6 USD]'] = [sum(x) for x in zip(self._revenue, np.negative(self.__df_table2['TOTAL CAPEX [1E6 USD]']), np.negative(edited_df['OPEX [1E6 USD]']))]
        self.__df_table2['Discounted Cash Flow [1E6 USD]'] = self.__df_table2['Cash Flow [1E6 USD]']/(1+self._discount_rate/100)** self.__df_table2['Year']
        self.__df_table2['NPV [1E6 USD]'] = [sum(self.__df_table2['Discounted Cash Flow [1E6 USD]'][0:(i+1)]) for i in range(self._end_prod)]
        return self.__df_table2


    def get_final_NPV(self):
        self.__final_NPV = self.__df_table2['NPV [1E6 USD]'].to_list()[-1]
        return round(self.__final_NPV, 1)
    
    def optimize_Rate_of_Abandonment(self):
        pass


    
    def run_grid_NPV(self, edited_df, production_profile, rate):
        yearly_gas_offtake = [0 for i in range (self._CAPEX_period_prior-1)] + [element * self._uptime for element in production_profile]
        end_prod = len(yearly_gas_offtake)
        revenue = [offtake/(1000000) * self._Gas_Price for offtake in yearly_gas_offtake]
        
        years = []         
        for i in range(end_prod):
            years.append(i)            

        
        DRILLEX = [element * self._Well_Cost for element in edited_df['Nr Wells']]   #DRILLEX [1E6 USD]
        TEMPLATES = [element * self._temp_cost for element in edited_df['Nr Templates']]

        
        LNG_p = edited_df['LNG Plant [1E6 USD]'].to_list()
        LNG_v = edited_df['LNG Vessels [1E6 USD]'].to_list()
        
        
        LNG_p = np.array([element / sum(LNG_p) if sum(LNG_p) != 0 else 0 for element in LNG_p]) * rate * self._LNG_plant_per_Sm3 / 1e6
        LNG_v = np.array([element / sum(LNG_v) if sum(LNG_v) != 0 else 0 for element in LNG_v]) * (math.ceil(rate*self._uptime/((86000000*22))))*self._LNG_cost_per_vessel


        TOTAL_CAPEX = [sum(x) for x in zip(DRILLEX, edited_df['Pipeline & Umbilicals [1E6 USD]'], TEMPLATES, LNG_p, LNG_v)] #'TOTAL CAPEX [1E6 USD]'
        CASH_FLOW = [sum(x) for x in zip(revenue, np.negative(TOTAL_CAPEX), np.negative(edited_df['OPEX [1E6 USD]']))] #'Cash Flow [1E6 USD]'
        DISCOUNTED_CASH_FLOW =  [cf/(1+self._discount_rate/100)** year for cf, year in zip(CASH_FLOW, years)] #'Discounted Cash Flow [1E6 USD]'        
        FINAL_NPV = sum(DISCOUNTED_CASH_FLOW) #[1E6 USD]
        return round(FINAL_NPV, 1)
    
    def update_grid_variables(self, df):
        self._minPlat = int(df["Min"][0])
        self._minNrTemp = int(df["Min"][1])
        self._minWellspTemp = int(df["Min"][2])
        self._minROA = int(df["Min"][3])

        self._maxPlat = int(df["Max"][0])
        self._maxNrTemp = int(df["Max"][1])
        self._maxWellspTemp = int(df["Max"][2])
        
        self._platSteps = int(df["Steps"][0])
        self._tempStep = int(df["Steps"][1])
        self._wellspTempStep = int(df["Steps"][2])


    def get_grid_plateau_variables(self):
        return self._minPlat, self._maxPlat, self._platSteps
    def get_grid_temp_variables(self):
        return self._minNrTemp, self._maxNrTemp, self._tempStep
    def get_grid_well_variables(self):
        return self._minWellspTemp, self._maxWellspTemp, self._wellspTempStep
    def get_ROA_variables(self):
        return self._minROA

    def grid_production_profiles2(self, rates=40000000, minROA=1000000):
        pp_list = []
        temp_well_optimization = self.getParameters()[self._opt].copy()
        temp_well_optimization[2] = minROA
        temp_well_optimization[7] = 4
        temp_well_optimization[8] = 4
        st.write(temp_well_optimization)


    def grid_production_profiles(self, rates, minROA):
        pp_list = []
        stepping_field_variables = self.getParameters()[self._opt].copy()
        for i in range(len(rates)):
            stepping_field_variables[0] = rates[i]
            stepping_field_variables[2] = minROA
            if self.getMethod()[self._opt] == 'IPR':
                from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
                new_df = IPRAnalysis(self.getPrecision()[self._opt], stepping_field_variables)
                #pp_list.append(df[])

            elif self.getMethod()[self._opt] == "NODAL":
                from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
                new_df = NodalAnalysis(self.getPrecision()[self._opt], stepping_field_variables)
            else:
                st.write("this is not supposed to happen, method and precision is:", self._method, self._precision)
            pp_list.append((new_df['Field rates [sm3/d]'].to_list()))
        return pp_list
    
def getNPVforMonteCarlo(table):
    pass

        




