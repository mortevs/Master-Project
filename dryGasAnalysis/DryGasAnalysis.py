class DryGasAnalysis:
    import pandas as pd
    def __init__(self):
        import pandas as pd
        self.__result:pd.DataFrame = None
        self.__method = None
        self.__precision = None
        self.__field = None

    def updateFromDropdown(self):
        import Data.getData as get
        import Plotting.plotFunc as Plot
        self.__method=Plot.dropdown(['Nodal', 'IPR'])
        self.__precision=Plot.dropdown(['Implicit', 'Explicit'])
        self.__field=Plot.dropdown(get.fieldNames(), index = 1)

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

            
            

                    # import warnings
        # warnings.filterwarnings("ignore", category=DeprecationWarning)
        # """
        # Runs dry gas field analysis provided method, precision and field.
        # method = IPR or Nodal, precision = implicit or explicit. Implicit has higher precision, but may fail due to error in root-finding. 
        # field = field with data avaiable at NPD. 
        
        # """ 


    