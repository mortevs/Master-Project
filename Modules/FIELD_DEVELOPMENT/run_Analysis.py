import pandas as pd
from Data.Storage.Cache import SessionState
import pages.GUI.GUI_functions as GUI
from Data.DefaultData import default_FD_data
import streamlit as st
import numpy as np
import math
from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis

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
        return self.__parameters

    def validate_parameters(self, list1):
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

        if self._method == 'IPR':
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
                    if method[i] == "IPR":
                        st.write("Reservoir pressure assumed constant during build-up period")
                    tab1, tab2 = st.tabs(["Plot", "Variables"])
                    if field[i] != 'No field chosen':
                        with tab2:        
                            st.write(method[i], prec[i], field[i])
                        with tab1:
                            st.write("Converted actual produced rates from yearly volumes to Sm3/d with input uptime = ", int(self.__parameters[9]))
                            GUI.multi_plot([res[i]], addProduced=True, num=i+1)
                    else:
                        with tab2:
                            st.write(method[i], prec[i])
                        with tab1:
                            GUI.multi_plot([res[i]], addAll=False, num=i+1)
                with tab2:
                    from pages.GUI.GUI_functions import display_FD_variables_table2
                    display_FD_variables_table2(list2=self.getParameters()[i])
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            st.header('Compared models', divider='red')
            GUI.multi_plot(dfs, addAll=False, comp = True)
    
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
        Fr = self.getResult()[opt]['Field Rates [Sm3/d]'].to_list()
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
    def __init__(self):
        super().__init__(session_id='DryGasAnalysis')
        self._CAPEX = []
        self._OPEX = []
        self._NPV_variables = []
        self._sheet = []
        self._data_For_NPV_sheet = []

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
        self._OPEX_cost = float(self.__OPEX[0])
        self._N_temp = self.__field_variables[7]
        self._N_Wells_per_Temp = self.__field_variables[8]
        self._buildUp_length = int(self.__field_variables[16])

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

        from Data.DefaultData import default_well_distribution, default_template_distribution
        self._end_prod = int(len(self._production_profile)+ (self._CAPEX_period_prior-1))
        self._years = []         
        for i in range(self._end_prod):
            self._years.append(i)    

        self._def_well_list  = default_well_distribution(self._N_temp, self._N_Wells_per_Temp, self._end_prod, self._Max_Well_per_year_nr)
        self._templ_list = default_template_distribution(self._def_well_list, self._N_temp, self._N_Wells_per_Temp, self._end_prod)
        
        self._Well_Cost = self.__CAPEX[0]
        self._p_u = self.__CAPEX[1]
        self._p_u_list = [self._p_u/2, self._p_u/2]
        for i in range(2, self._end_prod):
            self._p_u_list.append(0)
        
        self._temp_cost = self.__CAPEX[2]

        self._LNG_plant_per_Sm3 = self.__CAPEX[3]
        self._LNG_cost_per_vessel = self.__CAPEX[4]
        import math 
        number_of_LNG_vessels = (math.ceil(self._plateau_rate*self._uptime/((86000000*22)))) 
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
        self._yearly_gas_offtake = [0 for i in range (self._CAPEX_period_prior)] + [(self._production_profile[i-1]+self._production_profile[i])/2 * self._uptime for i in range(1, len(self._production_profile))]

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
    
    def run_grid_NPV(self, edited_df, prod_profiles, i):
        production_profile = prod_profiles[i][0].copy()
        wells=prod_profiles[i][1]
        rate = prod_profiles[i][2]
        yearly_gas_offtake = [0 for i in range (self._CAPEX_period_prior)] + [(production_profile[i-1]+production_profile[i])/2 * self._uptime for i in range(1, len(production_profile))]
        end_prod = len(yearly_gas_offtake)
        revenue = [offtake/(1000000) * self._Gas_Price for offtake in yearly_gas_offtake]
        years = []         
        for j in range(end_prod):
            years.append(j)

        from Data.DefaultData import default_template_distribution, default_well_distribution
        
        well_list  = default_well_distribution(wells/self._N_Wells_per_Temp, self._N_Wells_per_Temp, end_prod, self._Max_Well_per_year_nr)
        templ_list = default_template_distribution(well_list, wells/self._N_Wells_per_Temp, self._N_Wells_per_Temp, end_prod)

        DRILLEX = [element * self._Well_Cost for element in well_list]   #DRILLEX [1E6 USD]
        TEMPLATES = [element * self._temp_cost for element in templ_list]
        
        LNG_p = edited_df['LNG Plant [1E6 USD]'].to_list()
        LNG_v = edited_df['LNG Vessels [1E6 USD]'].to_list()
        LNG_p = np.array([element / sum(LNG_p) if sum(LNG_p) != 0 else 0 for element in LNG_p]) * rate * self._LNG_plant_per_Sm3 / 1e6
        LNG_v = np.array([element / sum(LNG_v) if sum(LNG_v) != 0 else 0 for element in LNG_v]) * (math.ceil(rate*self._uptime/((86000000*22))))*self._LNG_cost_per_vessel


        TOTAL_CAPEX = [sum(x) for x in zip(DRILLEX, edited_df['Pipeline & Umbilicals [1E6 USD]'], TEMPLATES, LNG_p, LNG_v)] #'TOTAL CAPEX [1E6 USD]'
        CASH_FLOW = [sum(x) for x in zip(revenue, np.negative(TOTAL_CAPEX), np.negative(edited_df['OPEX [1E6 USD]']))] #'Cash Flow [1E6 USD]'
        DISCOUNTED_CASH_FLOW =  [cf/(1+self._discount_rate/100)**year for cf, year in zip(CASH_FLOW, years)] #'Discounted Cash Flow [1E6 USD]'        
        my_dict = {}
        for k in range(self._CAPEX_period_prior, len(DISCOUNTED_CASH_FLOW)):
            NPV = float(sum(DISCOUNTED_CASH_FLOW[:k+1]))
            my_dict[NPV] = (wells, rate, (yearly_gas_offtake[k]/self._uptime))
        return my_dict
    
    def update_grid_variables(self, df):
        self._minPlat = float(df["Min"][0])
        self._minWells = float(df["Min"][1])
        self._minROA = float(df["Min"][2])

        self._maxPlat = int(df["Max"][0])
        self._maxWells = int(df["Max"][1])
        
        self._platSteps = int(df["Steps"][0])

    def validate_grid_variables(self, df, params):
        minPlat = float(df["Min"][0])
        minWells = float(df["Min"][1])
        minROA = float(df["Min"][2])
        maxPlat = float(df["Max"][0])
        maxWells = float(df["Max"][1])
        platSteps = float(df["Steps"][0])
        WellSteps = float(df["Steps"][1])

        if minPlat<=0:
            st.error("Minimum plateau rate must be greater than 0")
            st.stop()
        if minWells<=0:
            st.error("Minimum Nr Wells must be greater than 0")
            st.stop()
        if minWells%params[8]!=0:
            errormesg = f"Min Nr Wells must be {int(params[8])}, {int(params[8]*2)}, {int(params[8]*3)}, etc due to assumption that all templates and wells are equal. (Number of Wells per Template = {int(params[8])}, specified in the table at the top)"
            st.error(errormesg)
            st.stop()

        if platSteps<2:
            st.error("Minimum plateau rate steps must be greater than 2")
            st.stop()


        if isinstance(minWells, float):
            if minWells.is_integer():
                pass
            else:
                st.error('Min Nr Wells must be a whole number')
                st.stop()

        if isinstance((maxWells), float):
            if maxWells.is_integer():
                pass
            else:
                st.error('Max Nr Wells must be a whole number')
                st.stop()


        # if isinstance(WellSteps, float):
        #     if WellSteps.is_integer():
        #         pass
        #     else:
        #         st.error('Nr Wells step must be a whole number')
        #         st.stop()

        if isinstance(platSteps, float):
            if platSteps.is_integer():
                pass
            else:
                st.error('Plateau rate steps must be a whole number')
                st.stop()

        if minROA<=0:
            st.error("Minimum rate of abandonment must be greater than 0")
            st.stop()
        
        if platSteps>20:
            st.warning("Number of steps is high. Be patient when running grid search")
        return True

    def get_grid_plateau_variables(self):
        return self._minPlat, self._maxPlat, self._platSteps
    
    def get_grid_well_variables(self):
        return self._minWells, self._maxWells
    
    def get_ROA_variables(self):
        return self._minROA
    
    def get_inital_MC_variables(self):
        self.__IGIP_input = self.__field_variables[15]
        return self._Gas_Price, self.__IGIP_input, self._LNG_plant_per_Sm3, self._OPEX_cost, self._Well_Cost, self._p_u, self._temp_cost, self._LNG_cost_per_vessel
    
    def grid_production_profiles(self, rates, minROA, W):
        self.__minROA = minROA
        pp_list = []
        stepping_field_variables = self.getParameters()[self._opt].copy()
        nWpT = stepping_field_variables.copy()[8]
        stepping_field_variables[2] = self.__minROA  
        method = self.getMethod()[self._opt]
        precision = self.getPrecision()[self._opt]
        from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
        from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
        for rate in rates:
            stepping_field_variables[0] = rate
            for wells in W:
                stepping_field_variables[7] = wells/nWpT
                if method == 'IPR':
                    new_df = IPRAnalysis(precision, stepping_field_variables)
                    pp_list.append([(new_df['Field Rates [Sm3/d]'].to_list()), wells, rate])
                    #pp_list.append(df[])

                elif method == "NODAL":
                    new_df = NodalAnalysis(precision, stepping_field_variables)
                    pp_list.append([(new_df['Field Rates [Sm3/d]'].to_list()), wells, rate])
                else:
                    st.error("Error, method and precision is:", self._method, self._precision)     
        return pp_list
   
    def Tornado_production_profiles(self, dfMC, minROA):
        self._minIGIP =dfMC["P1"][1]*1e9
        self._maxIGIP =dfMC["P99"][1]*1e9
        pp__tornado_list = []
        stepping_field_variables = self.getParameters()[self._opt].copy()
        self.__IGIP_input = stepping_field_variables[15]

        stepping_field_variables[2] = minROA
        IGIP_list = [self.__IGIP_input, self._minIGIP, self._maxIGIP]
        precision = self.getPrecision()[self._opt]
        method = self.getMethod()[self._opt]
        from Modules.FIELD_DEVELOPMENT.IPR.IPRAnalysis import IPRAnalysis
        from Modules.FIELD_DEVELOPMENT.Nodal.NodalAnalysis import NodalAnalysis
        for ele in IGIP_list:
            stepping_field_variables[15] = ele
            if method == 'IPR':
                new_df = IPRAnalysis(precision, stepping_field_variables)
                pp__tornado_list.append(new_df['Field Rates [Sm3/d]'].to_list())
            elif method == "NODAL":
                new_df = NodalAnalysis(precision, stepping_field_variables)
                pp__tornado_list.append(new_df['Field Rates [Sm3/d]'].to_list())
            else:
                st.error("Error, method and precision is:", self._method, self._precision)   
        return pp__tornado_list

    def NPV_calculation_Uncertainty(self, df, gas_price, LNG_p_vari, yGofftake, opex_cost, well_cost, PU_cost, temp_cost, carrier_cost):
            yearly_gas_offtake = [0 for i in range (self._CAPEX_period_prior)] + [(yGofftake[i-1]+yGofftake[i])/2 * self._uptime for i in range(1, len(yGofftake))]
            end_prod = len(yearly_gas_offtake)
            revenue = [offtake/(1000000) * gas_price for offtake in yearly_gas_offtake]
            years = []         
            for j in range(end_prod):
                years.append(j)
            
            well_list = df['Nr Wells'].to_list()
            templ_list = df['Nr Templates'].to_list()
            DRILLEX = [element * well_cost for element in well_list]   #DRILLEX [1E6 USD]
            TEMPLATES = [element * temp_cost for element in templ_list]
            LNG_p = df['LNG Plant [1E6 USD]'].to_list()
            LNG_v = df['LNG Vessels [1E6 USD]'].to_list()
            LNG_p = np.array([element / sum(LNG_p) if sum(LNG_p) != 0 else 0 for element in LNG_p]) * self._plateau_rate * LNG_p_vari / 1e6
            LNG_v = np.array([element / sum(LNG_v) if sum(LNG_v) != 0 else 0 for element in LNG_v]) * (math.ceil(self._plateau_rate*self._uptime/((86000000*22))))*carrier_cost
            OPEX = df['OPEX [1E6 USD]']
            OPEX = [element * opex_cost / self._OPEX_cost for element in OPEX]
            

            PU = df['Pipeline & Umbilicals [1E6 USD]']
            PU = np.array([element / sum(PU) if sum(PU) != 0 else 0 for element in PU]) * PU_cost

            TOTAL_CAPEX = [sum(x) for x in zip(DRILLEX, PU, TEMPLATES, LNG_p, LNG_v)] #'TOTAL CAPEX [1E6 USD]'
            CASH_FLOW = [sum(x) for x in zip(revenue, np.negative(TOTAL_CAPEX), np.negative(OPEX))] #'Cash Flow [1E6 USD]'
            DISCOUNTED_CASH_FLOW =  [cf/(1+self._discount_rate/100)**year for cf, year in zip(CASH_FLOW, years)] #'Discounted Cash Flow [1E6 USD]'        
            NPV_list=[]
            for k in range(self._CAPEX_period_prior, len(DISCOUNTED_CASH_FLOW)):
                NPV = float(sum(DISCOUNTED_CASH_FLOW[:k+1]))
                NPV_list.append(NPV)
            maxNPV = round(max(NPV_list),1)  
            return maxNPV

    def getNPVsforTornado(self, dfMC, NPV_edited_df, prod_profiles):
        self._minGasPrice = dfMC["P1"][0]
        self._maxGasPrice =dfMC["P99"][0]
        self._minLNGPlant =dfMC["P1"][2]
        self._maxLNGPlant = dfMC["P99"][2]
        self._minOPEX =dfMC["P1"][3]
        self._maxOPEX = dfMC["P99"][3]

        self._minOPEX =dfMC["P1"][3]
        self._maxOPEX = dfMC["P99"][3]

        self._minWell_ =dfMC["P1"][4]
        self._maxWell_ = dfMC["P99"][4]

        self._minPU_ =dfMC["P1"][5]
        self._maxPU_ = dfMC["P99"][5]

        self._minTemp_ =dfMC["P1"][6]
        self._maxTemp_ = dfMC["P99"][6]

        self._minCarrier_ =dfMC["P1"][7]
        self._maxCarrier_ = dfMC["P99"][7]



        IGIPyGofftake = prod_profiles[0]
        initial_NPV=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost,  well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        minIGIPyGofftake = prod_profiles[1]
        maxIGIPyGofftake = prod_profiles[2]
        NPVgaspricemin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._minGasPrice, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPVgaspricemax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._maxGasPrice, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        LNGPlantMin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._minLNGPlant, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        LNGPlantMax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._maxLNGPlant, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPV_IGIPmin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = minIGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPV_IGIPmax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = maxIGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPV_OPEXmin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._minOPEX, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPV_OPEXmax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._maxOPEX, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        
        NPV_Wellmax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._maxWell_, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPV_Wellmin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._minWell_, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)

        NPV_PUmax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._maxPU_, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)
        NPV_PUmin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._minPU_, temp_cost = self._temp_cost, carrier_cost = self._LNG_cost_per_vessel)

        NPV_tempmax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._maxTemp_, carrier_cost = self._LNG_cost_per_vessel)
        NPV_tempmin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._minTemp_, carrier_cost = self._LNG_cost_per_vessel)

        NPV_Carriermax=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._maxCarrier_)
        NPV_Carriermin=self.NPV_calculation_Uncertainty(df = NPV_edited_df, gas_price = self._Gas_Price, LNG_p_vari = self._LNG_plant_per_Sm3, yGofftake = IGIPyGofftake, opex_cost=self._OPEX_cost, well_cost = self._Well_Cost, PU_cost = self._p_u, temp_cost = self._temp_cost, carrier_cost = self._minCarrier_)

        
        return initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, NPV_OPEXmax, NPV_OPEXmin, NPV_Wellmax, NPV_Wellmin, NPV_PUmax, NPV_PUmin, NPV_tempmax, NPV_tempmin, NPV_Carriermax, NPV_Carriermin
    
    def Monte_Carlo_production_profiles(self, minROA, IGIP_array):
        stepping_field_variables = self.getParameters()[self._opt].copy()
        stepping_field_variables[2] = minROA
        precision = self.getPrecision()[self._opt]
        method = self.getMethod()[self._opt]       
        pp_MC_dict = {}        
        pp_MC_dict = {ele: (
            IPRAnalysis(precision, stepping_field_variables).get('Field Rates [Sm3/d]') if method == 'IPR'
            else NodalAnalysis(precision, stepping_field_variables).get('Field Rates [Sm3/d]') if method == 'NODAL'
            else None).to_numpy() for ele in IGIP_array}
        if method not in ['IPR', 'NODAL']:
            st.error("Error: Invalid method or precision:", self._method, self._precision)
        return pp_MC_dict

    def NPV_calculation_Monte_Carlo(self, df, gas_price, LNG_p_vari, pp, Opex_vari,  well_cost, PU_cost, temp_cost, carrier_cost):
            yearly_gas_offtake = [0 for i in range (self._CAPEX_period_prior)] + [(pp[i-1]+pp[i])/2 * self._uptime for i in range(1, len(pp))]
            end_prod = len(yearly_gas_offtake)
            revenue = [offtake/(1000000) * gas_price for offtake in yearly_gas_offtake]
            years = []         
            for j in range(end_prod):
                years.append(j)
            well_list = df['Nr Wells'].to_list()
            templ_list = df['Nr Templates'].to_list()
            DRILLEX = [element * self._Well_Cost for element in well_list]   #DRILLEX [1E6 USD]
            TEMPLATES = [element * self._temp_cost for element in templ_list]
            LNG_p = df['LNG Plant [1E6 USD]'].to_list()
            LNG_v = df['LNG Vessels [1E6 USD]'].to_list()
            OPEX = df['OPEX [1E6 USD]']
            OPEX = [element * Opex_vari / self._OPEX_cost for element in OPEX]
            LNG_p = np.array([element / sum(LNG_p) if sum(LNG_p) != 0 else 0 for element in LNG_p]) * self._plateau_rate * LNG_p_vari / 1e6
            LNG_v = np.array([element / sum(LNG_v) if sum(LNG_v) != 0 else 0 for element in LNG_v]) * (math.ceil(self._plateau_rate*self._uptime/((86000000*22))))*self._LNG_cost_per_vessel
            TOTAL_CAPEX = [sum(x) for x in zip(DRILLEX, df['Pipeline & Umbilicals [1E6 USD]'], TEMPLATES, LNG_p, LNG_v)] #'TOTAL CAPEX [1E6 USD]'
            CASH_FLOW = [sum(x) for x in zip(revenue, np.negative(TOTAL_CAPEX), np.negative(OPEX))] #'Cash Flow [1E6 USD]'
            DISCOUNTED_CASH_FLOW =  [cf/(1+self._discount_rate/100)**year for cf, year in zip(CASH_FLOW, years)] #'Discounted Cash Flow [1E6 USD]'        
            NPV_list=[]
            for k in range(self._CAPEX_period_prior, len(DISCOUNTED_CASH_FLOW)):
                NPV = float(sum(DISCOUNTED_CASH_FLOW[:k+1]))
                NPV_list.append(NPV)
            maxNPV = round(max(NPV_list),1)  
            return maxNPV

        

        

        