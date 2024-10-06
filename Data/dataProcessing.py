import Data.getData as get
import streamlit as st
from pandas import DataFrame
import pandas as pd
from datetime import datetime

def get_field_list_inc_No_field_chosen():
    fieldnames = get.fieldNames()

    def custom_sort_key(s, char_map):
        return ''.join(char_map.get(c, c) for c in s)

    def locale_aware_sort(arr):
        char_map = {'Ø': 'Oz', 'Æ': 'Ae', 'Å': 'Aa'}
        arr.sort(key=lambda s: custom_sort_key(s, char_map))

    locale_aware_sort(fieldnames)
    fieldnames.insert(0, 'No field chosen')
    return fieldnames

def get_all_company_list():
    comps = get.CompanyNames()
    comps_list = sorted(list(comps))
    comps_list.insert(0, 'No company chosen')
    return comps_list

def company_licences(company):
    df = get.licenseData()
    comp_df = df[df['cmpLongName'].isin([company])]
    comp_df['fldLicenseeFrom'] = pd.to_datetime(comp_df['fldLicenseeFrom'], format='%d.%m.%Y')
    result = comp_df.groupby('fldName').apply(
        lambda x: x.loc[x['fldLicenseeFrom'].idxmax(), 'fldCompanyShare']
    ).to_dict()
    return result





               
# def estimatedReservoirPressure(TVD: float) -> float:
#     """
#     takes in discoveryWell and returns the estimated reservoir pressure in bara. estimate: pressure increases with 1.1 bar for every 10 m of depth
#     """
#     pressure = TVD/10 * 1.1
#     return pressure

def addActualProdYtoDF(field: str, df: DataFrame,  adjustLength = True, upTime = 365) ->DataFrame:
    gas, NGL, oil, cond, Oe, w = get.CSVProductionYearly(field)
    if adjustLength == True:
        while len(df) != len(gas):
            gas.append(0)
        while len(df) != len(NGL):
            NGL.append(0)
        while len(df) != len(oil):
            oil.append(0)
        while len(df) != len(cond):
            cond.append(0)
        while len(df) != len(Oe):
            Oe.append(0)
        while len(df) != len(w):
            w.append(0)
    gas = [i*10**9/upTime for i in gas] #prfPrdGasNetBillSm3
    NGL = [i*10**6/upTime for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6/upTime for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6/upTime for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6/upTime for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6/upTime for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(GasSm3perDay=gas)
    df = df.assign(NGLSm3perDay=NGL)
    df = df.assign(OilSm3perDay=oil)
    df = df.assign(CondensateSm3perDay=cond)
    df = df.assign(OilEquivalentsSm3perDay=Oe)
    df = df.assign(WaterSm3perDay=w)
    return df
def add_cumulative_columns(df, columns_to_ignore=[]):
    columns = list(df.columns)
    for name in columns_to_ignore:
        columns.remove(name)

    for column_name in columns:
        cumulative_column = df[column_name].cumsum()        
        new_column_name = f"{column_name}Cumulative"        
        df[new_column_name] = cumulative_column
    return df
def yearly_produced_DF(field: str, df: DataFrame) ->DataFrame:
    gas, NGL, oil, cond, Oe, w = get.CSVProductionYearly(field)
    gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
    NGL = [i*10**6 for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6 for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6 for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6 for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6 for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(GasSm3Yearly=gas)
    df = df.assign(NGLSm3Yearly=NGL)
    df = df.assign(OilSm3Yearly=oil)
    df = df.assign(CondensateSm3Yearly=cond)
    df = df.assign(OilEquivalentsSm3Yearly=Oe)
    df = df.assign(WaterSm3Yearly=w)
    df = df.assign(Watercut=(100*df["WaterSm3Yearly"]/(df["WaterSm3Yearly"] + df['OilSm3Yearly'] + df['CondensateSm3Yearly'] + df['NGLSm3Yearly'])))

    return df

def monthly_produced_DF(field: str, df: DataFrame) ->DataFrame:
    gas, NGL, oil, cond, Oe, w = get.CSVProductionMonthly(field)
    gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
    NGL = [i*10**6 for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6 for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6 for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6 for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6 for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(GasSm3Monthly=gas)
    df = df.assign(NGLSm3Monthly=NGL)
    df = df.assign(OilSm3Monthly=oil)
    df = df.assign(CondensateSm3Monthly=cond)
    df = df.assign(OilEquivalentsSm3Monthly=Oe)
    df = df.assign(WaterSm3Monthly=w)
    df = df.assign(Watercut=(100*df["WaterSm3Monthly"]/(df["WaterSm3Monthly"] + df['OilSm3Monthly'] + df['CondensateSm3Monthly'] + df['NGLSm3Monthly'])))
    return df

import pandas as pd

def addProducedYears(field: str, df: pd.DataFrame, adjustLength=True) -> pd.DataFrame:
    try:
        sY = min(get.CSVProducedYears(field))
        years = [sY]

        if adjustLength:
            i = 1
            while len(years) < len(df.iloc[:, 0]):
                years.append(sY + i)
                i += 1
        
        date_format = '%Y'
        period = "Y"
        df.index = pd.to_datetime(years, format=date_format).to_period(period).to_timestamp(period)
        return df

    except Exception as e:
        st.warning(f"Field has not produced anything yet. Could not get the produced years due to the following error: {e}.")
        return df

def check_addProducedYears(field: str) -> DataFrame:
    try:
        sY = min(get.CSVProducedYears(field))
        return True
    except Exception as e:
        return False

def addProducedMonthsOLD(field: str, df: DataFrame) -> DataFrame:
    try:
        dates = []
        years, months = get.CSVProducedMonths(field)
        for year, month in zip(years, months):
            date = f"{month}:{year}"  
            dates.append(date)
        
        df.index = dates
        return df
    except Exception as e:
        st.warning(f"Field has likely not produced anything yet. Could not get the produced year-months due to the following error: {e}.")
        return df

def addProducedMonths(field: str, df: pd.DataFrame) -> pd.DataFrame:
    try:
        years, months = get.CSVProducedMonths(field)
        dates = [datetime.strptime(f"{month}:{year}", "%m:%Y") for year, month in zip(years, months)]
        df.index = pd.to_datetime(dates).to_period('M').to_timestamp('M')
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return df





    


    