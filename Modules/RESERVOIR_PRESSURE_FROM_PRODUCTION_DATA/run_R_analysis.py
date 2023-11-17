import pandas as pd, streamlit as st, time

class ReservoirPressureAnalysis:
    def __init__(self, productionData : list = None, field:str = 'No field chosen', time: str = 'yearly'):
        import pandas as pd
        self.__production_data = [productionData]
        self.__field = [field]
        self.__time_frame = [time]
        self.__result = []
        from Data.Storage.Cache import SessionState
        self.__stateRPA = SessionState.get(result=[], method = [], time_frame = [], field = [], production_data = [])

    def updateFromDropdown(self, field, time_frame):
        self.__field = field
        self.__time_frame = time_frame


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
            st.write('Data upload will be implemented')
        elif selected_field != "No field chosen":
            self.__field = selected_field
            self.__production_data = df_prod
            self.__time_frame = selected_time
            self.__result = ((ResAnalysis()))

            self.__stateRPA.production_data.append(self.__production_data)
            self.__stateRPA.field.append(self.__field)
            self.__stateRPA.time_frame.append(self.__time_frame)
            self.__stateRPA.result.append(self.__result)

    def plot(self, comp = False):
        import GUI.GUI_functions as display, streamlit as st
        from pandas import DataFrame
        if comp == False:
            for i in range (len(self.__stateRPA.result)):
                if isinstance(self.__stateRPA.result[i], DataFrame):
                    st.title('Production profile: '+str(i+1))
                    st.write(self.__stateRPA.method[i], self.__stateRPA.precision[i])
                    display.multi_plot([self.__stateRPA.result[i]], addAll=False)
                else:
                    st.alert('Something is wrong..')
        else:   
            display.multi_plot(self.__stateRPA.result, addAll=False)

            
    def getMethod(self) -> str:
        return self.__stateRPA.method
    def getPrecision(self) -> str:
        return self.__stateRPA.precision
    def getResult(self) -> list:
        return self.__stateRPA.result
    def getParameters(self) -> pd.DataFrame:
        return self.__stateRPA.parameters
    def getState(self) -> pd.DataFrame:
            return self.__stateRPA
