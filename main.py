if __name__ == "__main__":
    import streamlit as st
    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
    Analysis = DryGasAnalysis()
    Analysis.updateFromDropdown()
    Analysis.run()


    
    #file_name = 'productionProfile.xlsx'
    #df.to_excel(file_name)
    #import Data.getData as get 
    #print(get.CSVProductionYearly("Snøhvit"))


    


    