import Data.getData as gd
from Data.dataProcessing.dataProcessing import *
from Data.NPDgetURL import *
from Data.classPage import Page
import zipfile
import pandas as pd
from Data.Cache.Cache import *



def IGIP(field: str) -> float:
    """
    Initial free gas in place sm3
    """
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    a = (content.find("td", {"class":"a858c"}))
    a = a.text
    a = float(float(a))*1e9
    if a == 0:
        raise ValueError("No initial free gas in place") 
    return a


def remainingGas(field: str) -> float:
    """Remaing volumes sm3"""
    
    field = field.upper()
    page = CachePage(field)
    wellURLs = CacheWellURLs(field)
    content = page.getPageContent()
    a = (content.find("td", {"class":"a796c"}))
    a = a.text
    a = float(float(a))*1e9
    return a


def fieldName(field: str) -> str: 
    """get field name from discovery well page"""
    field = field.upper()
    page = CacheDiscovery(field)
    content = page.getPageContent()
    a = (content.find("td", {"class":"a889c r6"}))
    a = a.select("div")
    a = (a[1].text)
    return a
    
        #print("No field name was found")
        #return "field"


def producedRates(field: str) -> list:
    """
    yearly volumes sm3 
    """
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    
    ProducedRates = []
    rateList = (content.find_all("td", {"class":"a1223cr"}))
    for rate in rateList:
        rate=rate.text
        rate = float(float(rate))*1e9
        ProducedRates.append(rate)
    return ProducedRates

def productionStartup(field: str) -> str:
    
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()    
    
    a = (content.find("td", {"class":"a557c"}))
    a = str(str(a))
    a = a[30:40]
    return a

def producedYears(field: str):
    
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    
    producedYears= []
    yearlist = (content.find_all("td", {"rowspan":"1"},{"class":"a1173"}))
    for year in yearlist:
        producedYears.append(int(year.text))
    producedYears = list(dict.fromkeys(producedYears))
    return producedYears


def target(field: str, upTime = 355) -> float:
    """
    Target rate for field. Default uptime = 355
    """
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    
    from Data.dataProcessing.dataProcessing import ratesToTarget
    estimatedDaily = ratesToTarget(productionStartup(field), producedRates(field), producedYears(field), upTime)
    return (estimatedDaily)

def temperature(field: str) -> float:
    """
    temperature at bottom of discovery well in degree celsius
    """
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    
    try:
        a = (content.find("td", {"class":"a1321c r6"}))
        a = a.text
        a = float(float(a))
        return a
    except:
        print("Discovery well for "+fieldName(field)+" did not include temperature data. Using default value = 90 C")
        return 90
    
def TVD(field: str) -> float:
    """
    TVD m [RKB] from discovery well
    """
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    
    try:
        a = (content.find("td", {"class":"a1295c r6"}))
        a = a.text
        a = float(float(a))
        return a
    except:
        print("Discovery well for "+fieldName(field)+" did not include depth data. Using default value = 2500 m")
        return 2500


def gasDensity(field: str) -> float:
    """
    gas density kg / sm^3 from discovery well
    """
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    
    densities= []
    densityList = (content.find_all("td", {"class":"a2206c"}))
    if len(densityList) == 0:
        print ('No density data was found at NPD for '+fieldName(field)+'. Using default value 16 g/mol')
        return 16 #defaultDensity
                         
    for density in densityList:
        density2 = density.text
        density2 = (density2.strip())
        try:
            density2 = (float(density2))*28.967 #convertion from relative air density in NPD data to density
            densities.append(density2) 
        except:
            densities.append(0) 
    return sum(densities)/len(densities)

def casingSize(field: str):
    """
    data from discovery well in Inches
    """
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    
    casingDiameters= []
    diameterData = (content.find_all("td", {"class":"a2312c"}))
    if len(diameterData) == 0:
        print ('No size data was found at NPD for this field')
        return False
    for el in diameterData:
        size = el.text
        if " " in size:
            try:
                num = float(size.split()[0])
                fraction = (size.split()[1])
                numerator =float(fraction.split("/")[0])
                denominator = float(fraction.split("/")[1])
                size = num + numerator/denominator
            except:
                pass
        try:
            size = (float(size))
            casingDiameters.append(size) 
        except:
            pass
    
    return casingDiameters


def depthSettings(field: str):
    """
    data from discovery well in m
    """
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    
    DepthSettings= []
    depthData = (content.find_all("td", {"class":"a2316c"}))    
    if len(depthData) == 0:
        print ('Depth setting data was not found at NPD for this field ')
        return False
                         
    for el in depthData:
        size = el.text
        size = size.strip()
        try:
            size = (float(size))
            DepthSettings.append(size) 
        except:
            pass
    return DepthSettings

def holeSize(field: str):
    """
    data from discovery well in inches
    """  
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    holeDiameters= []
    holeData = (content.find_all("td", {"class":"a2320c"}))
    if len(holeData) == 0:
        print ('No hole data was found at NPD for this field')
        return False                 
    for el in holeData:
        size = el.text
        if " " in size:
            try:
                num = float(size.split()[0])
                fraction = (size.split()[1])
                numerator =float(fraction.split("/")[0])
                denominator = float(fraction.split("/")[1])
                size = num + numerator/denominator
            except:
                pass
        try:
            size = (float(size))
            holeDiameters.append(size) 
        except:
            pass
    return holeDiameters
    
    
def sectionDepths(field: str): 
    """
    data from discovery well in m
    """
    field = field.upper()
    discovery = CacheDiscovery(field)
    content = discovery.getPageContent()
    WellDepths= []
    wellDepthData = (content.find_all("td", {"class":"a2324c"}))
    if len(wellDepthData) == 0:
        print ('No well depth data was found at NPD for this field')
        return False                 
    for el in wellDepthData:
        size = el.text
        size = size.strip()
        try:
            size = (float(size)) 
            WellDepths.append(size) 
        except:
            pass
    return WellDepths 
       

def gasProducingWells(field: str) -> int:
    """
    takes in status, purpose and content of wells as three lists in a list and returns gas producing producion wells. 
    """
    field = field.upper()
    #status = CacheStatus(field) #if requst method then comment out the one below
    status = CSVwellsStatus(field)
    purpose = wellsPurpose(field)
    content = wellsContent(field)
    from Data.dataProcessing.dataProcessing import producingGassWells
    return producingGassWells(status, purpose, content)
    

def reservoirPressure(field: str) -> float:
    """
    returns estimated reservoir pressure based on TVD from discovery well [Bara]
    """
    field = field.upper()
    depth = TVD(field)
    
    from Data.dataProcessing.dataProcessing import estimatedReservoirPressure
    return estimatedReservoirPressure(depth)


def wellsStatus(field: str):
    field = field.upper()
    status = CacheStatus(field)
    return status 

def wellsPurpose(field: str):
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    purposes = (content.find_all("td", {"class":"a1506c"}))
    purposeList = []
    for purpose in purposes:
        try:
            a = (str(purpose.text))
            a = a.strip()
            if a == "":
                purposeList.append("NO DATA")
            else:
                purposeList.append(a)
        except:
            purposeList.append("NO DATA")
    return purposeList

def wellsContent(field: str):
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    data = (content.find_all("td", {"class":"a1514c"}))
    contentList = []
    for el in data:
        try:
            a = (str(el.text))
            a = a.strip()
            if a == "":
                contentList.append("NO DATA")
            else:
                contentList.append(a)
        except:
            contentList.append("NO DATA")
    return contentList

def wellboreName(field: str):
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    data = (content.find_all("td", {"class":"a1494cl"}))
    wellborelist = []
    for el in data:
        try:
            a = el.select("div")
            a = (a[1].text)
            if a == "":
                wellborelist.append("NO DATA")
            else:
                wellborelist.append(a)
        except:
            wellborelist.append("NO DATA")
    return wellborelist



def producedMonthlyRates(field: str) -> dict:
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    
    myDict = dict()
    startup = (content.find("td", {"class":"a557c"}))
    startup = str(str(startup))
    startup = startup[36:40]
    producedMonths = []
    producedMonthlyRates = []
    monthDict = {1:"Jan", 2:"Feb", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
    monthList = (content.find_all("td", {"class":"a1259cr"}))
    monthlyRateList = (content.find_all("td", {"class":"a1267cr"}))
    yearlist = (content.find_all("td", {"rowspan":"1"},{"class":"a1173"}))
    producedYears= []
    for year in yearlist:
        producedYears.append(int(year.text))
    producedYears = list(dict.fromkeys(producedYears))
    
    for month in monthList:
        month=month.text
        month = int(int(month))
        producedMonths.append(month)
        
    for rate in monthlyRateList:
        rate=rate.text
        rate = float(float(rate))
        producedMonthlyRates.append(rate)
    year = 0
    for i in range (len(producedMonths)):
        month = monthDict[producedMonths[i]]
        if i > 0:
            temp = producedMonths[i-1]
            temp2 = producedMonths[i]
            if temp2 < temp :
                year -= 1  
        myDict[month+" "+str(producedYears[0]+year)] = producedMonthlyRates[i]              
    return myDict


def initialLiquidInPlace(field: str) -> float:
    field = field.upper()
    page = CachePage(field)
    content = page.getPageContent()
    a = (content.find("td", {"class":"a850c"}))
    a = a.text
    a = float(float(a))*1e6
    return a



#CSV files

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
    return (list(df["fldName"]))



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

def CSVwellsStatus(fieldName: str) -> str:
    df = CacheDF("fldArea")
    mylist = df['wlbWellboreName'].tolist()
    mylist2 = df['wlbStatus'].tolist()
    wbs = wellboreName(fieldName)
    statusList = []
    for el in wbs:
        try:
            i = mylist.index(el)
            statusList.append(mylist2[i])
        except:
            statusList.append("NO DATA")
    return statusList

# def CSVProductionMonthly(fieldName: str) -> list:
#     zipFileUrl = "https://hotell.difi.no/download/npd/field/production-monthly-by-field"
#     zf = CacheZip("productionMonthly", zipFileUrl)
#     csvName = zf.namelist()[0]
#     wbs = wellboreName(fieldName)
#     df = pd.read_csv(zf.open(csvName), low_memory=False)
#     mylist = df['prfPrdGasNetBillSm3'].tolist()
#     mylist2 = df['wlbStatus'].tolist()
#     wbs = wellboreName(fieldName)
#     index = fieldList.index(fieldName.upper())
#     area = df['fldMainArea'].values[index]
#     statusList = []
#     return statusList

def CSVProductionYearly(fieldName: str) -> str:
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        csvURL = "https://hotell.difi.no/download/npd/field/production-yearly-by-field"
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


