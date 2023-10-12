if __name__ == "__main__":
    import pandas as pd
    def plotDf(df:pd.DataFrame)->None:
        import Plotting.plotFunc as Plot, streamlit as st
        from pandas import DataFrame
        if isinstance(df, DataFrame):
            st.title('Production profile: ')
            Plot.multi_plot(df, addAll=False)

    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
    Analysis = DryGasAnalysis()
    import streamlit as st
    st.markdown('''
    :green[Specialization Project by Morten Vier Simensen, supervised by Prof. Milan Stanko]''')
    col1, col2, col3 = st.columns(3)
    with col1:
        from Plotting.plotFunc import dropdown
        if st.button('Restart Application', 'Restart'):
            from Data.Cache.Cache import clear_state, delete_files
            clear_state(Analysis.getState())
    with col3:
        if st.button('Load New Data from NPD',  'NPD'):
            delete_files()


            
    import streamlit as st, Plotting.plotFunc as Plot
    opt = Plot.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')
         
    if opt == 'FIELD DEVELOPMENT':
        Analysis.updateFromDropdown()
        Analysis.updateParameterListfromTable()        
        if st.button('Run Analysis'):
            Analysis.getResult().append(Analysis.run())
        Analysis.plot()
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
    #file_name = 'productionProfile.xlsx'
    #df.to_excel(file_name)
    #import Data.getData as get 
    #print(get.CSVProductionYearly("Snøhvit"))



    


    