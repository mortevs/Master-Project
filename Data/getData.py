import pandas as pd
import zipfile
import wget
import os
import requests
import streamlit as st
import time
from Data.Storage.Cache import delete_files
import Data.Storage.Cache as c

#cacheZip = {}
#cacheDF = {}
data_storage_folder = os.path.join(os.getcwd(), 'Data\Storage')

# def CacheZip(key, zipFileUrl):
#     if key in cacheZip:
#         return cacheZip[key]    
#     os.makedirs(data_storage_folder, exist_ok=True)
#     zip_file_path = os.path.join(data_storage_folder, key + '.zip')
#     wget.download(zipFileUrl, out=zip_file_path)
#     zf = zipfile.ZipFile(zip_file_path)
#     cacheZip[key] = zf
#     return cacheZip[key]

def ZiptoDF(zipname='fldArea.zip', zipFileUrl='https://factpages.npd.no/downloads/csv/fldArea.zip'):
    zip_file_path = os.path.join(os.getcwd(), 'Data\Storage', zipname)
    if os.path.exists(zip_file_path):
        zf = zipfile.ZipFile(zip_file_path)
    else:
        response = requests.get(zipFileUrl)
        if response.status_code == 200:
            wget.download(zipFileUrl, out=zip_file_path)            
            zf = zipfile.ZipFile(zip_file_path)
        else:
            st.write(f'Failed to get data from NPD, status code: {response.status_code}')
    df = pd.read_csv(zf.open(zf.namelist()[0]))
    zf.close()
    return df

def fieldNames():
    fldData = c.CacheDF(df=ZiptoDF(), key='fldArea')
    field_names = list(fldData['fldName'])
    return field_names

def polygon_coordinates(fieldName):
    p = c.CacheDF(df=ZiptoDF(), key='fldArea')
    p.drop(p[p['fldName'] != fieldName].index, inplace=True)
    fldAreaGeometryWKT = p['fldAreaGeometryWKT'].iloc[0]
    return fldAreaGeometryWKT

def wlbPoint_field_sorted(fieldName):
    p = c.CacheDF(df = ZiptoDF(zipname = 'wlbPoint.zip', zipFileUrl = 'https://factpages.npd.no/downloads/csv/wlbPoint.zip'), key = 'wlbPoint')
    p.drop(p[p['wlbField'] != fieldName].index, inplace=True)
    return p

def producing_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'PRODUCING'].index, inplace=True)
    return p

def injecting_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'INJECTING'].index, inplace=True)
    return p

def PA_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'P&A'].index, inplace=True)
    return p

def closed_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'CLOSED'].index, inplace=True)
    return p

def junked_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'junked'].index, inplace=True)
    return p

def CSVProductionMonthly(fieldName: str):
    if c.checkKeyCached('monthlyProduction'):
        p = c.CacheDF(df = None, key ='monthlyProduction')  
    else:
        csvURL = 'https://hotell.difi.no/download/npd/field/production-monthly-by-field'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key ='monthlyProduction')  
        else:
            st.write(f'Failed to get NPD data using digitaliseringsdirektoratets API, status code: {response.status_code}')
    p.drop(p[p['prfInformationCarrier'] != fieldName.upper()].index, inplace=True)
    gas = p['prfPrdGasNetBillSm3'].tolist()
    NGL = p['prfPrdNGLNetMillSm3'].tolist()
    oil = p['prfPrdOilNetMillSm3'].tolist()
    cond = p['prfPrdCondensateNetMillSm3'].tolist()
    Oe = p['prfPrdOeNetMillSm3'].tolist()
    w = p['prfPrdProducedWaterInFieldMillSm3'].tolist()
    return gas, NGL, oil, cond, Oe, w

def CSVProductionYearly(field: str):
    if c.checkKeyinDict('yearlyProduction'):
        p = c.CacheDF(df = None, key = 'yearlyProduction')
    else:
        csvURL = 'https://hotell.difi.no/download/npd/field/production-yearly-by-field'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'yearlyProduction')
        else:
            st.write(f'Failed to get NPD data using digitaliseringsdirektoratets API, status code: {response.status_code}')
    p.drop(p[p['prfInformationCarrier'] != field.upper()].index, inplace=True)
    gas = p['prfPrdGasNetBillSm3'].tolist()
    NGL = p['prfPrdNGLNetMillSm3'].tolist()
    oil = p['prfPrdOilNetMillSm3'].tolist()
    cond = p['prfPrdCondensateNetMillSm3'].tolist()
    Oe = p['prfPrdOeNetMillSm3'].tolist()
    w = p['prfPrdProducedWaterInFieldMillSm3'].tolist()
    return gas, NGL, oil, cond, Oe, w

def CSVProducedYears(fieldName: str) -> list:
    if c.checkKeyinDict('yearlyProduction'):
        p = c.CacheDF(df = None, key = 'yearlyProduction')
    else:
        csvURL = 'https://hotell.difi.no/download/npd/field/production-yearly-by-field'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'yearlyProduction')
        else:
            st.write(f'Failed to get NPD data using digitaliseringsdirektoratets API, status code: {response.status_code}')
    p.drop(p[p['prfInformationCarrier'] != fieldName.upper()].index, inplace=True)
    years = p['prfYear'].tolist()
    return years


def CSVProducedMonths(fieldName: str) -> list:
    if c.checkKeyinDict('monthlyProduction'):
        p = c.CacheDF(df = None, key = 'monthlyProduction')
    else:
        csvURL = 'https://hotell.difi.no/download/npd/field/production-monthly-by-field'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'monthlyProduction')
        else:
            st.write(f'Failed to get NPD data using digitaliseringsdirektoratets API, status code: {response.status_code}')
    p.drop(p[p['prfInformationCarrier'] != fieldName.upper()].index, inplace=True)
    years = p['prfYear'].tolist()
    months = p['prfMonth'].tolist()
    return years, months

def deleteAndloadNewDatafromNPD():
    delete_files()
    ZiptoDF()
    ZiptoDF(zipname = 'wlbPoint.zip', zipFileUrl = 'https://factpages.npd.no/downloads/csv/wlbPoint.zip')


def CSV_reserves():
    if c.checkKeyinDict('reserves'):
        p = c.CacheDF(df = None, key = 'reserves')
    else:
        csvURL = 'https://hotell.difi.no/download/npd/field/reserves?download'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'reserves')
        else:
            st.write(f'Failed to get NPD data using digitaliseringsdirektoratets API, status code: {response.status_code}')
    return p

# def PRi(fieldName):
#     return Pr_initial
# def T_R(field):
#     temp = 
#     return temp
# def gasMolecularWeight(fieldName):
#     gMW = 
#     return gMW 

def Temp(fieldName):
    if c.checkKeyinDict('wlbPoint'):
        p = c.CacheDF(df = None, key = 'wlbPoint')
    else:
        data_to_store = ZiptoDF(zipname = 'wlbPoint.zip', zipFileUrl = 'https://factpages.npd.no/downloads/csv/wlbPoint.zip')
        p = c.CacheDF(df = data_to_store, key = 'wlbPoint')
    p.drop(p[p['wlbField'] != fieldName.upper()].index, inplace=True)
    mean_temp = p["wlbBottomHoleTemperature"].mean()
    return round(mean_temp,1)


def IGIP(fieldName):
    reserves = CSV_reserves()
    reserves.drop(reserves[reserves['fldName'] != fieldName.upper()].index, inplace=True)
    reserves = reserves.reset_index(drop = True)
    fldRecoverableGas = reserves.loc[0,'fldRecoverableGas']
    fldRemainingGas = reserves.loc[0, 'fldRemainingGas']
    initial_GIP = fldRecoverableGas + fldRemainingGas
    return initial_GIP*1e9

def gas_molecular_weight(fieldName):
    #default value used. could not find data at NPD
    return 16 #g/mol 

def initial_reservoir_pressure(fieldName):
    #default value used, could not find data at NPD
    return  276 #reservoir pressure bara




def fieldStatus(fieldName: str) -> str:
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        zipFileUrl = 'https://factpages.npd.no/downloads/csv/fldArea.zip'
        index = fieldList.index(fieldName.upper())
        df = c.CacheDF('fldArea')
        status = df['fldCurrentActivitySatus'].values[index]
        return status
    raise ValueError('No field with name ', fieldName, ' at NPD')
    
def mainArea(fieldName: str) -> str:        
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        df = c.CacheDF('fldArea')
        index = fieldList.index(fieldName.upper())
        area = df['fldMainArea'].values[index]
        return area
    raise ValueError('No field with name ', fieldName, ' at NPD')
    
def fldMainSupplyBase(fieldName: str) -> str:        
    fieldList = fieldNames()
    if fieldName.upper() in fieldList:
        df = c.CacheDF('fldArea')
        index = fieldList.index(fieldName.upper())
        base = df['fldMainSupplyBase'].values[index]
        return base
    raise ValueError('No field with name ', fieldName, ' at NPD')


