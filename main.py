if __name__ == "__main__":
    import streamlit as st
    # import Plotting.plotFunc as Plot
    # opt = Plot.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING'], labelVisibility='visible')
    # if opt == 'FIELD DEVELOPMENT':
    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis

    Analysis = DryGasAnalysis()
    st.title('Production profile modelling')
    Analysis.updateFromDropdown()
    Analysis.run()


    
    #file_name = 'productionProfile.xlsx'
    #df.to_excel(file_name)
    #import Data.getData as get 
    #print(get.CSVProductionYearly("Snøhvit"))


    


    