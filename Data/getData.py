import pandas as pd
import zipfile
import wget
import os
import requests
import streamlit as st
import time
from Data.Storage.Cache import delete_files
import Data.Storage.Cache as c
data_storage_folder = os.path.join(os.getcwd(), 'Data', 'Storage')

def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

def ZiptoDF(zipname='fldArea.zip', zipFileUrl='https://factpages.sodir.no/downloads/csv/fldArea.zip'):
    zip_file_path = os.path.join(data_storage_folder, zipname)
    if os.path.exists(zip_file_path):
        zf = zipfile.ZipFile(zip_file_path)
    else:
        response = requests.get(zipFileUrl)
        if response.status_code == 200:
            wget.download(zipFileUrl, out=zip_file_path)            
            zf = zipfile.ZipFile(zip_file_path)
        else:
            st.write(f'Failed to get data from sodir, status code: {response.status_code}')
    df = pd.read_csv(zf.open(zf.namelist()[0]), low_memory=False)
    zf.close()
    return df

def CompanyNames():
    if c.checkKeyinDict('ownerships'):
        p = c.CacheDF(df = None, key ='ownerships')  
    else:
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_licensee_hst&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.commaCSVURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key ='ownerships')  
        else:
            st.write(f'Failed to get Ownership data, status code: {response.status_code}')
    return set(p[ 'cmpLongName'])

def licenseData():
    if c.checkKeyinDict('ownerships'):
        p = c.CacheDF(df = None, key ='ownerships')  
    else:
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_licensee_hst&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.commaCSVURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key ='ownerships')  
        else:
            st.write(f'Failed to get Ownership data, status code: {response.status_code}')
    return p


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
    p = c.CacheDF(df = ZiptoDF(zipname = 'wlbPoint.zip', zipFileUrl = 'https://factpages.sodir.no/downloads/csv/wlbPoint.zip'), key = 'wlbPoint')
    p.drop(p[p['wlbField'] != fieldName].index, inplace=True)
    return p

def producing_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'PRODUCING'].index, inplace=True)
    p = swap_columns(p, "wlbNpdidWellbore", "wlbWellboreName")
    p = p.astype(str)
   
    return p

def injecting_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'INJECTING'].index, inplace=True)
    p = swap_columns(p, "wlbNpdidWellbore", "wlbWellboreName")
    p = p.astype(str)

    return p

def PA_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'P&A'].index, inplace=True)
    p = swap_columns(p, "wlbNpdidWellbore", "wlbWellboreName")
    p = p.astype(str)
    return p

def closed_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'CLOSED'].index, inplace=True)
    p = swap_columns(p, "wlbNpdidWellbore", "wlbWellboreName")
    p = p.astype(str)
    return p

def plugged_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'PLUGGED'].index, inplace=True)
    p = swap_columns(p, "wlbNpdidWellbore", "wlbWellboreName")
    p = p.astype(str)
    return p

def junked_wlb(fieldName):
    p = wlbPoint_field_sorted(fieldName)
    p.drop(p[p['wlbStatus'] != 'JUNKED'].index, inplace=True)
    p.set_index("WlbWellboreName", drop = True, inplace = True)

    return p

def Ownerships(company):
    if c.checkKeyinDict('ownerships'):
        p = c.CacheDF(df = None, key ='ownerships')  
    else:
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_licensee_hst&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key ='ownerships')  
        else:
            st.write(f'Failed to get Ownership data, status code: {response.status_code}')
    return None


def CSVProductionMonthly(fieldName: str):
    if c.checkKeyinDict('monthlyProduction'):
        p = c.CacheDF(df = None, key ='monthlyProduction')  
    else:
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key ='monthlyProduction')  
        else:
            st.write(f'Failed to get production data, status code: {response.status_code}')
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
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_production_yearly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'yearlyProduction')
        else:
            st.write(f'Failed to get SODIR data from Data.Norge, status code: {response.status_code}')
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
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_production_yearly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'yearlyProduction')
        else:
            st.write(f'Failed to get production data, status code: {response.status_code}')
    p.drop(p[p['prfInformationCarrier'] != fieldName.upper()].index, inplace=True)
    years = p['prfYear'].tolist()
    return years

def CSVProducedMonths(fieldName: str) -> list:
    if c.checkKeyinDict('monthlyProduction'):
        p = c.CacheDF(df = None, key = 'monthlyProduction')
    else:
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'monthlyProduction')
        else:
            st.write(f'Failed to get Sodir data, status code: {response.status_code}')
    p.drop(p[p['prfInformationCarrier'] != fieldName.upper()].index, inplace=True)
    years = p['prfYear'].tolist()
    months = p['prfMonth'].tolist()
    return years, months

def deleteAndLoadNewDataFromNPD():
    zipfile_URLs = [
        'https://factpages.sodir.no/downloads/csv/fldArea.zip',
        'https://factpages.sodir.no/downloads/csv/wlbPoint.zip',
        'https://factpages.sodir.no/public?/Factpages/external/tableview/field_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false',
        'https://factpages.sodir.no/public?/Factpages/external/tableview/field_production_yearly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false',
        'https://factpages.sodir.no/public?/Factpages/external/tableview/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false',  
        'https://factpages.sodir.no/public?/Factpages/external/tableview/field_licensee_hst&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false',
    ]  
    try:
        response_list = [requests.get(url).status_code for url in zipfile_URLs]
        if all(status == 200 for status in response_list):
            delete_files()
            ZiptoDF()
            ZiptoDF(zipname = 'wlbPoint.zip', zipFileUrl = 'https://factpages.sodir.no/downloads/csv/wlbPoint.zip')
            return True
        else:
            raise Exception("Not all Sodir resources are available. Visit Sodir/Data.Norge for further information.")
    except requests.exceptions.RequestException as e:
        my = st.warning(f"Request error: {e}")
        time.sleep(5)
        my.empty()
    except Exception as e:
        my2 = st.warning(f"Error: {e}")
        time.sleep(5)
        my2.empty()
    return False

def CSV_reserves():
    if c.checkKeyinDict('reserves'):
        p = c.CacheDF(df = None, key = 'reserves')
    else:
        csvURL = 'https://factpages.sodir.no/public?/Factpages/external/tableview/field_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&IpAddress=not_used&CultureCode=nb-no&rs:Format=CSV&Top100=false'
        response = requests.get(csvURL)
        if response.status_code == 200:
            data_to_store = c.csvURLtoDF(csvURL)
            p = c.CacheDF(df = data_to_store, key = 'reserves')
        else:
            st.write(f'Failed to get SODIR data, status code: {response.status_code}')
    return p

def Temp(fieldName):
    if c.checkKeyinDict('wlbPoint'):
        p = c.CacheDF(df = None, key = 'wlbPoint')
    else:
        data_to_store = ZiptoDF(zipname = 'wlbPoint.zip', zipFileUrl = 'https://factpages.sodir.no/downloads/csv/wlbPoint.zip')
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
    return 276 #reservoir pressure bara

