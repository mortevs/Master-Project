import dataiku
def datasetToDict(inputDataSet):
    
    """
    Reads input dataset and stores data as dictionary that can be used for IPR and Nodal analysis. 
    The input dataset should be ordered as following:
    
    
    variableName1       variableName2       variableName3       ...           variableNameN
     
    value1              value2              value3              ...           valueN

    
    
    """
    data = dataiku.Dataset(inputDataSet)
    data_df = data.get_dataframe()
    dataDict = data_df.to_dict("list")
    return dataDict
