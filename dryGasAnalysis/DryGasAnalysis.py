class DryGasAnalysis:
    import pandas as pd
    def __init__(self):
        import pandas as pd
        self.__inputs:list = None
        self.__result:pd.DataFrame = None
        self.__method = None
        self.__precision = None
        self.__field = None

    def updateFromDropdown(self):
        import Data.getData as get, Plotting.plotFunc as Plot
        fieldnames = get.fieldNames()
        fieldnames.insert(0, 'NO FIELD CHOSEN')
        self.__method, self.__precision, self.__field = Plot.columnDisplay(list1=[['NODAL', 'IPR'],['IMPLICIT', 'EXPLICIT'], fieldnames])

    def run(self):
        if self.__method == 'IPR':
            from IPR.IPRAnalysis import IPRAnalysis
            self.__result = IPRAnalysis(self.__precision, self.__field)
        else:
            from Nodal.NodalAnalysis import NodalAnalysis
            self.__result = NodalAnalysis(self.__precision, self.__field)

    def getMethod(self) -> str:
        return self.__method
    def getPrecision(self) -> str:
        return self.__precision
    def getResult(self) -> pd.DataFrame:
        return self.__result

            
        


    