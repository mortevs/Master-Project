import Data.getData as get
import streamlit as st
from pandas import DataFrame

def get_field_list_inc_No_field_chosen():
    fieldnames = get.fieldNames()

    def custom_sort_key(s, char_map):
        return ''.join(char_map.get(c, c) for c in s)

    def locale_aware_sort(arr):
        # Map special characters to a representation for sorting
        char_map = {'Ø': 'Oz', 'Æ': 'Ae', 'Å': 'Aa'}

        # Sort using the custom sort key
        arr.sort(key=lambda s: custom_sort_key(s, char_map))

    locale_aware_sort(fieldnames)
    fieldnames.insert(0, 'No field chosen')
    return fieldnames

               
def estimatedReservoirPressure(TVD: float) -> float:
    """
    takes in discoveryWell and returns the estimated reservoir pressure in bara. estimate: pressure increases with 1.1 bar for every 10 m of depth

    """
    pressure = TVD/10 * 1.1
    return pressure

def addActualProdYtoDF(field: str, df: DataFrame,  adjustLength = True) ->DataFrame:
    gas, NGL, oil, cond, Oe, w = get.CSVProductionYearly(field)
    if adjustLength == True: #should i remove 0 production
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
    gas = [i*10**9/365 for i in gas] #prfPrdGasNetBillSm3
    df = df.assign(gasSM3perday=gas)
    NGL = [i*10**6/365 for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6/365 for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6/365 for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6/365 for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6/365 for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(NGLSM3perday=NGL)
    df = df.assign(oilSM3perday=oil)
    df = df.assign(condensateSM3perday=cond)
    df = df.assign(OilEquivalentsSM3perday=Oe)
    df = df.assign(WaterSM3perday=w)
    return df

def yearly_produced_DF(field: str, df: DataFrame) ->DataFrame:
    import streamlit as st
    gas, NGL, oil, cond, Oe, w = get.CSVProductionYearly(field)
    gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
    NGL = [i*10**6 for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6 for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6 for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6 for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6 for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(gasSM3Yearly=gas)
    df = df.assign(NGLSM3Yearly=NGL)
    df = df.assign(oilSM3Yearly=oil)
    df = df.assign(condensateSM3Yearly=cond)
    df = df.assign(OilEquivalentsSM3Yearly=Oe)
    df = df.assign(WaterSM3Yearly=w)
    return df

def monthly_produced_DF(field: str, df: DataFrame) ->DataFrame:
    import streamlit as st
    gas, NGL, oil, cond, Oe, w = get.CSVProductionMonthly(field)
    gas = [i*10**9 for i in gas] #prfPrdGasNetBillSm3
    NGL = [i*10**6 for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6 for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6 for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6 for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6 for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(gasSM3Monthly=gas)
    df = df.assign(gasSM3Monthly=gas)
    df = df.assign(NGLSM3Monthly=NGL)
    df = df.assign(oilSM3Monthly=oil)
    df = df.assign(condensateSM3Monthly=cond)
    df = df.assign(OilEquivalentsSM3Monthly=Oe)
    df = df.assign(WaterSM3Monthly=w)
    return df

def addProducedYears(field: str, df: DataFrame, adjustLength=True) -> DataFrame:
    try:
        sY = min(get.CSVProducedYears(field))
        years = [sY]

        if adjustLength:
            i = 1
            while len(years) < len(df.iloc[:, 0]):
                years.append(sY + i)
                i += 1

        df.index = years
        return df
    except Exception as e:
        st.warning(f"Field has likely not produced anything yet. Could not get the produced years due to the following error: {e}.")
        return df

def addProducedMonths(field: str, df: DataFrame) -> DataFrame:
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




    


    