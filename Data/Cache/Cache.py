import Data.getData as gd
from Data.dataProcessing.dataProcessing import *
from Data.NPDgetURL import *
from Data.classPage import Page
import zipfile, wget
import pandas as pd
import shelve

cacheURL = dict()
cachePage = dict()
cacheWellURLs = dict()
cacheDiscovery = dict()
cacheStatus = dict()
cacheZip = dict()
cacheCSV = dict()
cacheDF = dict()

def CacheURL(key: str) -> str:
    if key in cacheURL:
        return cacheURL[key]
    cacheURL[key] = NPDgetFieldURL(key)
    return cacheURL[key]

def CachePage(key: str) -> Page:
    
    if key in cachePage:
        return cachePage[key]
    cachePage[key] = Page(CacheURL(key))
    return cachePage[key]

def CacheWellURLs(key: str) ->list:
    if key in cacheWellURLs:
        return cacheWellURLs[key]
    cacheWellURLs[key] = getProductionWellURLs(CachePage(key))
    return cacheWellURLs[key]

def CacheStatus(key: str) ->list:
    if key in cacheStatus:
        return cacheStatus[key]
    wellURLs = CacheWellURLs(key)
    from Data.syncData import syncData
    cacheStatus[key] = syncData(wellURLs)
    return cacheStatus[key]

    
def CacheDiscovery(key: str) ->list:
 
    if key in cacheDiscovery:
        return cacheDiscovery[key]
    cacheDiscovery[key] = Page(getWellURL(CachePage(key)))
    return cacheDiscovery[key]

def CacheZip(key: str, zipFileUrl: str):
    if key in cacheZip:
        return cacheZip[key]
    zf = zipfile.ZipFile(wget.download(zipFileUrl)) 
    cacheZip[key] = zf
    return cacheZip[key] 

def csvURLtoDF(key: str, csvURL: str) ->pd.DataFrame:
    df = pd.read_csv((csvURL), sep = ";", low_memory=False)
    return df

def CacheDF(df: pd.DataFrame, key: str) ->pd.DataFrame:
    if checkKeyinDict(key) == 0:
        df = gd.ZiptoDF(zipFileUrl = "https://factpages.npd.no/downloads/csv/fldArea.zip")
        dumpDict(df, key)
    loaded = loadDict(key)
    return loaded

def dumpDict(dict: dict, name: str) ->None:
    d = shelve.open("savedDictionary")
    d[name] = dict
    d.close()
    return None

def checkKeyinDict(key: str)->bool:
    d = shelve.open("savedDictionary")
    if key in d:
        d.close()   
        return True
    d.close()
    return False

    
def loadDict(name: str) ->dict:
    d = shelve.open("savedDictionary")
    if name not in d:
        return 0
    dict = d[name]
    d.close()
    return dict
    