if __name__ == "__main__":
    
    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
    df = DryGasAnalysis(method = 'Nodal', field = "Snøhvit").runAnalysis()

    
    #file_name = 'productionProfile.xlsx'
    #df.to_excel(file_name)
    #import Data.getData as get 
    #print(get.CSVProductionYearly("Snøhvit"))


    


    