def ZiptoDF(zipname = 'fldArea.zip', zipFileUrl='https://factpages.npd.no/downloads/csv/fldArea.zip'):
    import pandas as pd, zipfile, wget,os, requests, streamlit as st, time
    if os.path.exists(zipname):
        zf = zipfile.ZipFile(zipname)
    else:
        response = requests.get(zipFileUrl)
        if response.status_code == 200:
            zf = zipfile.ZipFile(wget.download(zipFileUrl))
            timestamp =  time.ctime()
            alert = st.warning("Data downloaded from NPD " + timestamp) # Display the alert
            time.sleep(5)
            alert.empty() 
        else:
            st.write(f"Failed to get data from NPD, status code: {response.status_code}")
    df = pd.read_csv(zf.open(zf.namelist()[0]))
    zf.close()
    return df

def fieldNames():
    """
    Returns a list with all fieldnames listed at NPD
    """
    import pandas as pd, streamlit as st, Data.getData as gd, Data.Cache.Cache as c

    fldData = c.CacheDF(df = ZiptoDF(), key = "fldArea")
    field_names = list(fldData["fldName"])
    return field_names

def CSVProductionMonthly(fieldName: str):
    df = None
    import pandas as pd, Data.getData as gd, zipfile, wget, Data.Cache.Cache as c,os, requests, streamlit as st    
    if c.checkKeyinDict("monthlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-monthly-by-field"
        response = requests.get(csvURL)
        if response.status_code == 200:
            df = c.csvURLtoDF(csvURL)
        else:
            st.write(f"Failed to get data from NPD, status code: {response.status_code}")

    df = c.CacheDF(df, 'monthlyProduction')  
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    gas = df['prfPrdGasNetBillSm3'].tolist()
    NGL = df['prfPrdNGLNetMillSm3'].tolist()
    oil = df['prfPrdOilNetMillSm3'].tolist()
    cond = df['prfPrdCondensateNetMillSm3'].tolist()
    Oe = df['prfPrdOeNetMillSm3'].tolist()
    w = df['prfPrdProducedWaterInFieldMillSm3'].tolist()
    return gas, NGL, oil, cond, Oe, w

def CSVProductionYearly(fieldName: str):
    import pandas as pd, Data.getData as gd, zipfile, wget, Data.Cache.Cache as c,os, requests, streamlit as st  
    df = None
    if c.checkKeyinDict("yearlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
        response = requests.get(csvURL)
        if response.status_code == 200:
            df = c.csvURLtoDF(csvURL)
        else:
            st.write(f"Failed to get data from NPD, status code: {response.status_code}")

    df = c.CacheDF(df, 'yearlyProduction')  
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
    import pandas as pd, Data.getData as gd, zipfile, wget, Data.Cache.Cache as c,os, requests, streamlit as st    
    if c.checkKeyinDict("yearlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
        response = requests.get(csvURL)
        if response.status_code == 200:
            df = c.csvURLtoDF(csvURL)
        else:
            st.write(f"Failed to get data from NPD, status code: {response.status_code}")
    df = c.CacheDF(df, "yearlyProduction")
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    years = df['prfYear'].tolist()
    return years

def CSVProducedMonths(fieldName: str) -> list:
    df = None
    import pandas as pd, Data.getData as gd, zipfile, wget, Data.Cache.Cache as c,os, requests, streamlit as st
    if c.checkKeyinDict("monthlyProduction") == 0:
        csvURL = "https://hotell.difi.no/download/npd/field/production-monthly-by-field"
        response = requests.get(csvURL)
        if response.status_code == 200:
            df = c.csvURLtoDF(csvURL)
        else:
            st.write(f"Failed to get data from NPD, status code: {response.status_code}")
    df = c.CacheDF(df, "monthlyProduction")
    df.drop(df[df['prfInformationCarrier'] != fieldName.upper()].index, inplace = True)
    years = df['prfYear'].tolist()
    months = df['prfMonth'].tolist()
    return years, months

def deleteAndloadNewDatafromNPD():
    from Data.Cache.Cache import delete_files
    delete_files()
    ZiptoDF()


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


