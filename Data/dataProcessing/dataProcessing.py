import Data.getData as get
from pandas import DataFrame
def ratesToTarget(startUp:str, producedRates: list, producedYears: list, upTime: int) -> float:
        startUpYear = int(startUp[-4:])
        index = producedYears.index(startUpYear)
        producedRates = producedRates[:index+1]
        print(producedRates)
        maxRate = max(producedRates)
        sumRates = 0
        count = 0
        for el in producedRates:
            if el>maxRate/1.5:
                sumRates+=el
                count+=1

        estimatedYearly = sumRates/count
        estimatedDaily=round(estimatedYearly/upTime, 0)
        return estimatedDaily
    
def producingGassWells(status, purpose, content) -> int:
    statusList = status
    purposeList = purpose
    contentList = content
    NWells = 0
    NClosedWells = 0
    if len(statusList) != len(purposeList) != len(contentList):
        raise ValueError("statusList, purposeList and contentList have different sizes")
 
    for i in range(len(statusList)):
        if statusList[i] == 'PRODUCING' and purposeList[i] == 'PRODUCTION' and  contentList[i] == 'GAS':
            NWells+=1
        elif statusList[i] == 'CLOSED' and purposeList[i] == 'PRODUCTION' and  contentList[i] == 'GAS':
            NClosedWells+=1
    if NClosedWells > 1:
        print("NB!", NClosedWells, "gas wells are currently closed.")
    elif NClosedWells == 1:
        print("NB! One gas well is currently closed.")                   
    return NWells+NClosedWells
            
    
    
def estimatedReservoirPressure(TVD: float) -> float:
    """
    takes in discoveryWell and returns the estimated reservoir pressure in bara. estimate: pressure increases with 1.1 bar for every 10 m of depth

    """
    pressure = TVD/10 * 1.1
    return pressure


def addActualProdYtoPlot(field: str, df: DataFrame) ->DataFrame:
    
    gas, NGL, oil, cond, Oe, w = get.CSVProductionYearly(field)
    # while gas[0] == 0:
    #     gas.pop(0)
    # del gas[len(df):]
    while len(df) != len(gas):
        gas.append(0)

    # while NGL[0] == 0:
    #     NGL.pop(0)
    # del NGL[len(df):]
    while len(df) != len(NGL):
        NGL.append(0)

    # while oil[0] == 0 or not oil:
    #     oil.pop(0)
    # del oil[len(df):]
    while len(df) != len(oil):
        oil.append(0)
    
    # while cond[0] == 0:
    #     cond.pop(0)
    # del cond[len(df):]
    while len(df) != len(cond):
        cond.append(0)

    # while Oe[0] == 0:
    #     Oe.pop(0)
    # del Oe[len(df):]
    while len(df) != len(Oe):
        Oe.append(0)
    
    # while w[0] == 0:
    #     w.pop(0)
    # del w[len(df):]
    while len(df) != len(w):
        w.append(0)
    
    #should i consider adjusting for uptime?
    gas = [i*10**9/365 for i in gas] #prfPrdGasNetBillSm3
    NGL = [i*10**6/365 for i in NGL] #prfPrdOilNetMillSm3
    oil = [i*10**6/365 for i in oil] #prfPrdCondensateNetMillSm3
    cond = [i*10**6/365 for i in cond] #prfPrdOeNetMillSm3
    Oe = [i*10**6/365 for i in Oe] #prfPrdOeNetMillSm3
    w = [i*10**6/365 for i in w] #prfPrdProducedWaterInFieldMillSm3
    df = df.assign(gasSM3perday=gas)
    df = df.assign(NGLSM3perday=NGL)
    df = df.assign(oilSM3perday=oil)
    df = df.assign(condensateSM3perday=cond)
    df = df.assign(OilEquivalentsSM3perday=Oe)
    df = df.assign(WaterSM3perday=w)
    return df

def addProducedYears(field: str, df: DataFrame) ->DataFrame:
    sY = min(get.CSVProducedYears(field))
    years = [sY]
    i=1
    while len(years) < len(df.iloc[:, 0]):
        years.append(sY+i)
        i+=1
    df.index = years
    return df





    


    