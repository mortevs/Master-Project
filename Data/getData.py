from Data.Cache.Cache import *
def ZiptoDF(zipFileUrl):
    import os
    #zf = CacheZip('fldArea', zipFileUrl) 
    zf = zipfile.ZipFile(wget.download(zipFileUrl)) 
    df = pd.read_csv(zf.open(zf.namelist()[0]))
    zf.close()
    os.remove('fldArea.zip')
    return df

def fieldNames():
    """
    Returns a list with all fieldnames listed at NPD
    """
    df=None
    if checkKeyinDict("fldArea") == 0:
        df = gd.ZiptoDF(zipFileUrl = "https://factpages.npd.no/downloads/csv/fldArea.zip")
    df = CacheDF(df, "fldArea")
    field_names = list(df["fldName"])
    return field_names

def CSVProductionMonthly(fieldName: str):
    df = None
    if checkKeyinDict("monthlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-monthly-by-field"
        df = csvURLtoDF(csvURL)
    df = CacheDF(df, 'monthlyProduction')  
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    gas = df['prfPrdGasNetBillSm3'].tolist()
    NGL = df['prfPrdNGLNetMillSm3'].tolist()
    oil = df['prfPrdOilNetMillSm3'].tolist()
    cond = df['prfPrdCondensateNetMillSm3'].tolist()
    Oe = df['prfPrdOeNetMillSm3'].tolist()
    w = df['prfPrdProducedWaterInFieldMillSm3'].tolist()
    return gas, NGL, oil, cond, Oe, w

def CSVProductionYearly(fieldName: str):
    df = None
    if checkKeyinDict("yearlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
        df = csvURLtoDF(csvURL)
    df = CacheDF(df, 'yearlyProduction')  
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    gas = df['prfPrdGasNetBillSm3'].tolist()
    NGL = df['prfPrdNGLNetMillSm3'].tolist()
    oil = df['prfPrdOilNetMillSm3'].tolist()
    cond = df['prfPrdCondensateNetMillSm3'].tolist()
    Oe = df['prfPrdOeNetMillSm3'].tolist()
    w = df['prfPrdProducedWaterInFieldMillSm3'].tolist()
    return gas, NGL, oil, cond, Oe, w

def CSVProducedYears(fieldName: str) -> list:
    df = None
    if checkKeyinDict("yearlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
        df = csvURLtoDF(csvURL)
    df = CacheDF(df, "yearlyProduction")
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    years = df['prfYear'].tolist()
    return years

def CSVProducedMonths(fieldName: str) -> list:
    df = None
    if checkKeyinDict("monthlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-monthly-by-field"
        df = csvURLtoDF(csvURL)
    df = CacheDF(df, "monthlyProduction")
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    years = df['prfYear'].tolist()
    months = df['prfMonth'].tolist()
    return years, months



# def fieldStatus(fieldName: str) -> str:
#     fieldList = fieldNames()
#     if fieldName.upper() in fieldList:
#         zipFileUrl = "https://factpages.npd.no/downloads/csv/fldArea.zip"
#         index = fieldList.index(fieldName.upper())
#         df = CacheDF("fldArea")
#         status = df['fldCurrentActivitySatus'].values[index]
#         return status
#     raise ValueError("No field with name ", fieldName, " at NPD")
    
# def mainArea(fieldName: str) -> str:        
#     fieldList = fieldNames()
#     if fieldName.upper() in fieldList:
#         df = CacheDF("fldArea")
#         index = fieldList.index(fieldName.upper())
#         area = df['fldMainArea'].values[index]
#         return area
#     raise ValueError("No field with name ", fieldName, " at NPD")
    
# def fldMainSupplyBase(fieldName: str) -> str:        
#     fieldList = fieldNames()
#     if fieldName.upper() in fieldList:
#         df = CacheDF("fldArea")
#         index = fieldList.index(fieldName.upper())
#         base = df['fldMainSupplyBase'].values[index]
#         return base
#     raise ValueError("No field with name ", fieldName, " at NPD")


