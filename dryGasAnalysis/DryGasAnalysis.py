
def runAnalysis(method: str, precision: str, field:str):
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    """
    Runs dry gas field analysis provided method, precision and field.
    method = IPR or Nodal, precision = implicit or explicit. Implicit has higher precision, but may fail due to error in root-finding. 
    field = field with data avaiable at NPD. 
    
    """    
    #
    # fetch production data from NPD should be inserted here
    #
    if method.lower() == 'ipr':
        from IPR.IPRAnalysis import IPRAnalysis
        return IPRAnalysis(precision, field)
    elif method.lower() == 'nodal':
        from Nodal.NodalAnalysis import NodalAnalysis
        return NodalAnalysis(precision, field)
    
    else:
        from Nodal.NodalAnalysis import NodalAnalysis
        return NodalAnalysis("implicit", field)


class DryGasAnalysis:
    __method = "nodal"
    __precision = "implicit"
    __field = None


    def __init__(self, method="nodal", precision="implicit", field = None):
        self.__method=method
        self.__precision=precision 
        self.__field=field
        

    def runAnalysis(self):
        return runAnalysis(self.__method, self.__precision, self.__field)
    