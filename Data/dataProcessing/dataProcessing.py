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
    pyear = get.CSVProductionYearly(field)
    while pyear[0] == 0:
        pyear.pop(0)
    del pyear[len(df):]
    while len(df) != len(pyear):
        pyear.append(0)
    pyear = [i*10**9/365 for i in pyear] #should i consider adjusting for uptime?
    df = df.assign(ActualProducedRatesSM3perday=pyear)
    return df





    


    