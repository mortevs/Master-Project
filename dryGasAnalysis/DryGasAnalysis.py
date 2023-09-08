
def runAnalysis(method: str, precision: str, field:str, file_id: str):
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
        return IPRAnalysis(precision, field, file_id)
    elif method.lower() == 'nodal':
        from Nodal.NodalAnalysis import NodalAnalysis
        return NodalAnalysis(precision, field, file_id)
    
    else:
        from Nodal.NodalAnalysis import NodalAnalysis
        return NodalAnalysis("implicit", field, file_id)


class DryGasAnalysis:
    __method = "nodal"
    __precision = "implicit"
    __field = "fieldname"
    __file_id = None

    def __init__(self, method="nodal", precision="implicit", field = "fieldname", file_id = None):
        self.__method=method
        self.__precision=precision 
        self.__field=field
        self.__file_id=file_id
        

    def runAnalysis(self):
        return runAnalysis(self.__method, self.__precision, self.__field, self.__file_id)
    