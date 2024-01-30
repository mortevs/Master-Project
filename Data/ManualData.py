def manualData() -> list:
    qFieldTarget = 20e6 #target rate sm3/d
    PRi = 276 #reservoir pressure bara
    IGIP = 270e9 #Initial gas in place
    abandonmentRate = 5e6 
    TR = 92 #reservoir temperature [C]
    gasMolecularWeight = 16 #[g/mol]
    C_t = 40288.1959178652#Ct, Tubing flow coefficient (2100 MDx0.15 ID  m)
    S = 0.155#tubing elevation coefficient
    C_FL = 283126.866184114#flowline coefficient from template-PLEM (5000x0.355  ID m)
    C_PL = 275064.392725841#CPL Pipeline coefficient from PLEM-Shore (158600x0.68  ID m)
    P_sep =30 #seperator pressure in bara
    N_temp = 3 #number of templates
    NWellsPerTemplate = 3 #number of wells per template
    C_R = 1000 #inflow backpressure coefficient
    n = 1 #Inflow backpressure exponent
    upTime = 365
    list = [qFieldTarget, PRi, abandonmentRate, TR, gasMolecularWeight, C_R, n, N_temp, NWellsPerTemplate, upTime, C_t, S, C_FL, C_PL, P_sep, IGIP]
    return list

def manualData_RP() -> list:
    PRi = 276 #reservoir pressure bara
    IGIP = 270e9 #Initial gas in place   
    TR = 92 #reservoir temperature [C]
    gasMolecularWeight = 16 #[g/mol]
    list = [PRi, TR, gasMolecularWeight, IGIP]
    return list


def manualData_NPV() -> list:
    GAS_Price = 0.1 #uds/Sm^3
    Discount_Rate = 5 #%
    list = [GAS_Price, Discount_Rate]
    return list

def manualData_NPV_CAPEX() -> list:
    well_cost = 100 #1E06 USD
    list = [well_cost]
    return list

def manualData_NPV_OPEX() -> list:
    well_cost = 100 #1E06 USD
    list = [well_cost]
    return list