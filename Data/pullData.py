import Data.getData as get
from Data.NPDgetURL import NPDgetFieldURL, getWellURL, getProductionWellURLs
from Data.classPage import Page



def pullData(field: str) -> list:
    
    IGIP = get.IGIP(field)
 
    TR = get.temperature(field) #TR from discovery well data
    
    PRi = get.reservoirPressure(field)
 
    gasMolecularWeight = get.gasDensity(field) #[g/mol]
   
    upTime = 355 #Already accouning for uptime when looking at yearly produced volumes
    
    qFieldTarget = get.target(field, upTime) #Qfield data from production data
    
    
    NWells = get.gasProducingWells(field)
    if NWells == 0:
        print ("Zero gas producing wells were found. Using default value = 9 wells")
        NWells = 9
    
    
    N_temp = 3 #number of templates, we dont really need this, it is used to determine how many wells we have in total, and we have that already.
    
    NWellsPerTemplate = NWells / N_temp #number of wells per template
    
    abandonmentRate = qFieldTarget/4 #rate for abandonment, 
    
    
    C_t = 40288.1959178652#Ct, Tubing flow coefficient (2100 MDx0.15 ID  m)
    S = 0.155#tubing elevation coefficient
    C_FL = 283126.866184114#flowline coefficient from template-PLEM (5000x0.355  ID m)
    C_PL = 275064.392725841#CPL Pipeline coefficient from PLEM-Shore (158600x0.68  ID m)
    #fieldRate = qFieldTarget
    P_sep =30 #seperator pressure in bara
    C_R = 1000 #inflow backpressure coefficient
    n = 1 #Inflow backpressure exponent 
    list = [qFieldTarget, PRi, abandonmentRate, TR, gasMolecularWeight, C_R, n, N_temp, NWellsPerTemplate, upTime, C_t, S, C_FL, C_PL, P_sep, IGIP]
    return list