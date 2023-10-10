# from Data.Cache.Cache import delete_files
# delete_files()
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def get(**kwargs):
        # Get a SessionState object for the current session
        if not hasattr(st, '_session_state'):
            st._session_state = SessionState(**kwargs)
        return st._session_state
import pandas as pd
def plotDf(df:pd.DataFrame)->None:
    import streamlit as st
    import Plotting.plotFunc as Plot
    from pandas import DataFrame
    if isinstance(df, DataFrame):
        Plot.multi_plot(df, addAll=False)

if __name__ == "__main__":
    import streamlit as st, Plotting.plotFunc as Plot
    opt = Plot.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')
    if opt == 'FIELD DEVELOPMENT':
        from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
        Analysis = DryGasAnalysis()
        Analysis.updateFromDropdown()
        Analysis.updateParameterListfromTable()
        state = SessionState.get(my_list=[])
        if st.button('Run Analysis'):
            state.my_list.append(Analysis.run())
        
        for i in range (len(state.my_list)):
            st.title('Production profile:'+ str(i+1))
            plotDf(state.my_list[i])


            
        #Analysis.plotDf()
    elif opt == 'PRODUCTION FORECASTING':
        None
    elif opt == 'RESERVOIR PRESSURE FROM PRODUCTION DATA':
        from ReservoirPressureAnalysis.dryGasRPAnalysis import ReservoirPressureAnalysis
        st.title('Reservoir pressure modelling')
        Analysis = ReservoirPressureAnalysis()
        Analysis.updateFromDropdown()
        Analysis.run()

    
    elif opt == 'IPR TUNING':
        None
    elif opt == 'TPR TUNING':
        None



import streamlit as st

# This is the SessionState implementation



    
    #file_name = 'productionProfile.xlsx'
    #df.to_excel(file_name)
    #import Data.getData as get 
    #print(get.CSVProductionYearly("Snøhvit"))



    


    