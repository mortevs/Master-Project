from Data.Cache.Cache import *
def ZiptoDF(zipFileUrl):
    zf = CacheZip('fldArea', zipFileUrl)
    df = pd.read_csv(zf.open(zf.namelist()[0]))
    return df

def fieldNames():
    """
    Returns a list with all fieldnames listed at NPD
    """
    if checkKeyinDict("fldArea") == 0:
        df = gd.ZiptoDF(zipFileUrl = "https://factpages.npd.no/downloads/csv/fldArea.zip")
    else:
        df = loadDict("fldArea")
    CacheDF(df, "fldArea")
    
    # Get the list of field names
    field_names = list(df["fldName"])
    
    # Add 'NO FIELD CHOSEN' at the beginning of the list
    field_names.insert(0, 'NO FIELD CHOSEN')
    
    return field_names


def fieldStatus(fieldName: str) -> str:
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        zipFileUrl = "https://factpages.npd.no/downloads/csv/fldArea.zip"
        index = fieldList.index(fieldName.upper())
        df = CacheDF("fldArea")
        status = df['fldCurrentActivitySatus'].values[index]
        return status
    raise ValueError("No field with name ", fieldName, " at NPD")
    
def mainArea(fieldName: str) -> str:        
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        df = CacheDF("fldArea")
        index = fieldList.index(fieldName.upper())
        area = df['fldMainArea'].values[index]
        return area
    raise ValueError("No field with name ", fieldName, " at NPD")
    
def fldMainSupplyBase(fieldName: str) -> str:        
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        df = CacheDF("fldArea")
        index = fieldList.index(fieldName.upper())
        base = df['fldMainSupplyBase'].values[index]
        return base
    raise ValueError("No field with name ", fieldName, " at NPD")

def CSVProductionMonthly(fieldName: str) -> list:
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        csvURL = "https://hotell.difi.no/download/npd/field/production-monthly-by-field"
        df = csvURLtoDF("monthlyProduction", csvURL)
        prfIC = df['prfInformationCarrier'].tolist()
        gas = df['prfPrdGasNetBillSm3'].tolist()
        NGL = df['prfPrdNGLNetMillSm3'].tolist()
        oil = df['prfPrdOilNetMillSm3'].tolist()
        cond = df['prfPrdCondensateNetMillSm3'].tolist()
        Oe = df['prfPrdOeNetMillSm3'].tolist()
        w = df['prfPrdProducedWaterInFieldMillSm3'].tolist()
        return gas
    raise ValueError("No field with name ", fieldName, " at NPD")

def CSVProductionYearly(fieldName: str) -> list:
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
        df = csvURLtoDF("yearlyProduction", csvURL)
        df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
        gas = df['prfPrdGasNetBillSm3'].tolist()
        # NGL = df['prfPrdNGLNetMillSm3'].tolist()
        # oil = df['prfPrdOilNetMillSm3'].tolist()
        # cond = df['prfPrdCondensateNetMillSm3'].tolist()
        # Oe = df['prfPrdOeNetMillSm3'].tolist()
        # w = df['prfPrdProducedWaterInFieldMillSm3'].tolist()
        return gas
    raise ValueError("No field with name ", fieldName, " at NPD")

def CSVProducedYears(fieldName: str) -> list:
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
        df = csvURLtoDF("yearlyProduction", csvURL)
        df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
        years = df['prfYear'].tolist()
        return years
    raise ValueError("No field with name ", fieldName, " at NPD")




