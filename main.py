
if __name__ == "__main__":
    from dryGasAnalysis.DryGasAnalysis import DryGasAnalysis
    results = DryGasAnalysis(method = 'IPR', precision = 'explicit', field = "my data").runAnalysis()
    
    file_name = 'productionProfile.xlsx'
    results.to_excel(file_name)
    #import Data.getData as get
    #print(get.productionStartup("aasta hansteen"))
    #print(get.gasDensity("aasta hansteen"))
    #print(get.temperature("ormen lange"))
    # print(get.wellsPurpose("brage"))
    # print(get.wellsContent("gimle"))
    # print(get.producedYears("ivar aasen"))
    # print(get.casingSize("sleipner vest"))
    # print(get.depthSettings("solveig"))
    # print(get.holeSize("oseberg"))
    # print(get.producedMonthlyRates("troll"))
    # print(get.fieldNames())
    # print(get.fieldStatus("johan sverdrup"))
    # print(get.mainArea("goliat"))
    # print(get.fldMainSupplyBase("johan sverdrup"))
    # print(get.CSVwellsStatus("snøhvit"))