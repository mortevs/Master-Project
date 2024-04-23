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

def addActualProdYtoDF(field: str, df: DataFrame,  adjustLength = True, upTime = 365) ->DataFrame:
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

def yearly_produced_DF(field: str, df: DataFrame) ->DataFrame:
    import streamlit as st
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
    df = df.assign(Watercut=lambda x: 100 * x["WaterSm3Yearly"] / (x["WaterSm3Yearly"] + x['OilSm3Yearly'] + x['CondensateSm3Yearly'] + x['NGLSm3Yearly']).replace({0: np.nan}))

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




    


    