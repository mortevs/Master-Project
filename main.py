if __name__ == "__main__":
    import pandas as pd
    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
    Analysis = DryGasAnalysis()
    import streamlit as st
    st.markdown('''
    :green[Specialization Project by Morten Vier Simensen, supervised by Prof. Milan Stanko]''')
    import streamlit as st, Plotting.plotFunc as Plot
    opt = Plot.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')   
    if opt == 'FIELD DEVELOPMENT':
        Analysis.updateFromDropdown()
        Analysis.updateParameterListfromTable()   
        col4, col5, col6 = st.columns(3)
        with col4:     
            if st.button('Run Analysis', 'Run'):
                Analysis.getResult().append(Analysis.run())
        with col6: 
            if st.button('Compare different models', 'Compare'):
                with col4:
                    Analysis.plot(comp = True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Restart', 'Restart'):
                from Data.Cache.Cache import clear_state
                clear_state(Analysis.getState())
        with col3:
            if st.button('Load New Data from NPD',  'NPD'):
                from Data.Cache.Cache import delete_files
                delete_files()  
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



    


    