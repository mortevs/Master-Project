from Data.Cache.Cache import delete_files
delete_files()
if __name__ == "__main__":
    import streamlit as st, Plotting.plotFunc as Plot
    opt = Plot.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')
    if opt == 'FIELD DEVELOPMENT':
        from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
        Analysis = DryGasAnalysis()
        Analysis.updateFromDropdown()
        Analysis.run()
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



    


    