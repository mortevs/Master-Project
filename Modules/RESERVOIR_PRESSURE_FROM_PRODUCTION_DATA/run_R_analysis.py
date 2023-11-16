import pandas as pd, streamlit as st, time

class ReservoirPressureAnalysis:
    def __init__(self, productionData : list = None, field:str = 'No field chosen', time: str = 'yearly'):
        import pandas as pd
        self.__production_data = [productionData]
        self.__field = [field]
        self.__time_frame = [time]
        self.__results = []
        from Data.Storage.Cache import SessionState
        self.__state = SessionState.get(production_data=[], field = [], time_frame = [], results = [])


    def updateFromDropdown(self, field, time_frame):
        self.__field.append(field)
        self.__time_frame.append(time_frame)


    def updateParameterListfromTable(self):
        import GUI.GUI_functions as display
        from Data.ManualData import manualData
        list1=['Target Rate [sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]']
        self.__parameters.append(display.display_table(list1 = list1, list2 = manualData(), edible=True))

    def reset_lists(self):
        self.__production_data = []
        self.__field = ['No field chosen']
        self.__time_frame = ['Yearly']
    
    def run(self, selected_field, selected_time, df_prod):
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.build_analysis import ResAnalysis
        if df_prod != None:
            st.write('Data upload will be impplemented')
        elif selected_field != "No field chosen":
            self.__results.append(ResAnalysis())


    
    def plot(self, comp = False):
        import GUI.GUI_functions as display, streamlit as st
        from pandas import DataFrame
        if comp == False:
            for i in range (len(self.__state.result)):
                if isinstance(self.__state.result[i], DataFrame):
                    st.title('Production profile: '+str(i+1))
                    st.write(self.__state.method[i], self.__state.precision[i])
                    display.multi_plot([self.__state.result[i]], addAll=False)
        else:
            display.multi_plot(self.__state.result, addAll=False)

            
    def get_field(self) -> str:
        return self.__field[-1]
    
    def get_time_frame(self) -> str:
        return self.__time_frame[-1]
    
    def get_prod_data(self) -> str:
        return self.__production_data[-1]
