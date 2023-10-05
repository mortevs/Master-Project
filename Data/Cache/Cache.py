import Data.getData as gd
from Data.dataProcessing.dataProcessing import *
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

def CacheZip(key: str, zipFileUrl: str)->zipfile:
    if key in cacheZip:
        return cacheZip[key]
    zf = zipfile.ZipFile(wget.download(zipFileUrl)) 
    cacheZip[key] = zf
    return cacheZip[key] 

def csvURLtoDF(csvURL: str) ->pd.DataFrame:
    df = pd.read_csv((csvURL), sep = ";", low_memory=False)
    return df

def CacheDF(df:None, key: str)->pd.DataFrame:
    if checkKeyinDict(key) == 0:
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
    