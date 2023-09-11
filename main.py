import shelve
if __name__ == "__main__":
    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
    # results = DryGasAnalysis(method = 'Nodal', precision = 'explicit', field = "manual data").runAnalysis()
    
    # file_name = 'productionProfile.xlsx'
    # results.to_excel(file_name)

    import Data.getData as get
    #print(get.fieldNames())
    print(get.CSVProductionYearly("Snøhvit"))



    


    