import Data.getData as gd
from Data.dataProcessing.dataProcessing import *
from Data.NPDgetURL import *
from Data.classPage import Page
import zipfile, wget
import pandas as pd

cacheURL = dict()
cachePage = dict()
cacheWellURLs = dict()
cacheDiscovery = dict()
cacheStatus = dict()
cacheZip = dict()


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