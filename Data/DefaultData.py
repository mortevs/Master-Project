def default_FD_data() -> list:
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
    buildup_period = 3 #years
    list = [qFieldTarget, PRi, abandonmentRate, TR, gasMolecularWeight, C_R, n, N_temp, NWellsPerTemplate, upTime, C_t, S, C_FL, C_PL, P_sep, IGIP, buildup_period]
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
    buildUp_length = 2
    uptime = 365
    list = [GAS_Price, Discount_Rate, buildUp_length, uptime]
    return list

def manualData_NPV_CAPEX() -> list:
    well_cost = 100 #MUSD
    p_u = 500 #MUSD, Pipeline and umbilicals
    Mani = 20 #MUSD , Cost Per Subsea Manifold  
    LNG_plant = 2000
    LNG_vessels = 500
    list = [well_cost, p_u, Mani, LNG_plant, LNG_vessels]
    return list

def manualData_NPV_OPEX() -> list:
    well_cost = 200 #1E06 USD
    list = [well_cost]
    return list

def default_well_template_distribution(NWellsPerTemplate, N_temp, prod_stop) ->list:
    import streamlit as st
    def_well_list = [0 for _ in range(prod_stop)]
    def_temp_list = def_well_list.copy()    
    nr_wells = NWellsPerTemplate*N_temp
    
    if nr_wells == 0 and N_temp == 0:
        return def_well_list, def_temp_list
    
    elif nr_wells == 1:
        def_well_list[0] = 1
        def_temp_list[0] = 1
        return def_well_list, def_temp_list
    
    well_count = 0
    if nr_wells % 2 == 0:
        for i in range(prod_stop):
            def_well_list[i] = 2
            well_count +=2
            if well_count == nr_wells:
                break
    else:
        for i in range(prod_stop):
            def_well_list[i] = 2
            well_count +=2
            if well_count+1 == nr_wells:
                def_well_list[i+1] = 1
                break


    m= int(min(prod_stop, NWellsPerTemplate))
    for i in range (m):
        def_temp_list[i] = 1
    
    return def_well_list, def_temp_list