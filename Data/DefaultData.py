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

def defaultData_RP() -> list:
    PRi = 276 #reservoir pressure bara
    IGIP = 270e9 #Initial gas in place   
    TR = 92 #reservoir temperature [C]
    gasMolecularWeight = 16 #[g/mol]
    list = [PRi, TR, gasMolecularWeight, IGIP]
    return list

def default_data_NPV() -> list:
    GAS_Price = 0.1 #uds/Sm^3
    Discount_Rate = 5 #%
    nr_wells_per_year = 4
    CAPEX_period = 5
    list = [GAS_Price, Discount_Rate, nr_wells_per_year, CAPEX_period]
    return list

def default_data_NPV_CAPEX() -> list:
    well_cost = 100 #MUSD
    p_u = 500 #MUSD, Pipeline and umbilicals
    Mani = 20 #MUSD , Cost Per Subsea Manifold  
    LNG_unit_cost = 160 #usd/ Sm^3/d
    LNG_carrier_cost= 200 #1E6 USD
    list = [well_cost, p_u, Mani, LNG_unit_cost, LNG_carrier_cost]
    return list

def default_data_NPV_OPEX() -> list:
    well_cost = 200 #1E06 USD
    list = [well_cost]
    return list

def default_well_distribution(NWellsPerTemplate, N_temp, prod_stop, Max_Number_Wells) -> list:
    def_well_list = [0 for _ in range(prod_stop)]
    
    nr_wells = NWellsPerTemplate * N_temp

    if nr_wells % Max_Number_Wells == 0:
        well_count = 0
        for i in range(prod_stop):
            def_well_list[i] = Max_Number_Wells
            well_count += Max_Number_Wells
            if well_count == nr_wells:
                break
    else:
        well_count = 0
        for i in range(prod_stop):
            if well_count + Max_Number_Wells <= nr_wells:
                def_well_list[i] = Max_Number_Wells
                well_count += Max_Number_Wells
            else:
                def_well_list[i] = nr_wells - well_count
                well_count = nr_wells
            if well_count == nr_wells:
                break
    return def_well_list

def default_template_distribution(def_well_list, N_temp, NWellsPerTemp, prod_stop):
    def_temp_list = [0] * prod_stop
    temp_count = sum(def_temp_list)

    free_slots = 0
    for i in range(prod_stop):
        while def_temp_list[i]*NWellsPerTemp < (def_well_list[i]-free_slots) and temp_count < N_temp:
            def_temp_list[i] += 1
            temp_count +=1
        free_slots += def_temp_list[i]*NWellsPerTemp-def_well_list[i]
        if temp_count == N_temp:
            break
    return def_temp_list

def default_Optimization_table(f_variables):
    nr_temps =f_variables[7]
    wpertemp = f_variables[8]
    list1 = ['Plateau rate [Sm3/d]', 'Nr Wells', 'Rate of Abandonment [Sm3/d]']
    list2 = [10000000,wpertemp, 1e6] 
    list3 = [40000000,wpertemp*nr_temps*2, None] 
    list4 = [4,None,None] 
    return list1,list2,list3,list4

def default_MC():
    list1 = ['Gas Price [USD/Sm3]', 'IGIP [1E9 Sm3]', 'LNG Plant [USD/Sm3/d]', 'OPEX [1E6 USD]', 'Well Cost [1E6 USD]', 'Pipe & Umbilical [1E6 USD]', 'Template cost [1E6 USD]', 'Cost per LNG Carrier [1E6 USD]']
    list2 = [0.05,250.0, 100.0, 150.0, 80.0, 400.0, 10.0, 150.0] 
    list3 = [0.15,300.0, 220.0, 250.0, 120.0, 600.0, 30.0, 250.0]
    return list1, list2, list3 

def default_MC_params():
    list1 = ['Nr of Random Samples', 'Nr Bins', 'Nr production profiles']
    list2 = [100000,25, 20] 
    return list1, list2

def default_MC_params2():
    list1 = ['Nr of Random samples', 'Nr Bins']
    list2 = [5000000,50] 
    return list1, list2

def default_MC_SA():
    list1 = ['Time 1 [Hours]', 'Time 2 [Hours]', 'Time 3 [Hours]']    
    list2 = [13.0,39.0, 11.0] 
    list3 = [17.0, 44.0, 13.0]
    list4 = [25.0,64.0, 22.0]
    return list1, list2, list3, list4

def probability_distributions():
    return ['pert (default)', 'triangular', 'uniform', 'normal', 'exponential'] 

def default_network_of_wells():
    PR1 = 90
    PR2 = 160
    C_R1 = 52
    C_R2 = 40
    n1 = 0.8
    n2 = 0.75
    S1 = 0.13
    S2 = 0.11
    C_t1 = 7680
    C_t2 = 8600
    C_W1 = 8673
    C_W2 = 7563
    C_PIPELINE = 14080
    Psep = 28.6
    names = ["PR1", "PR2", "C_R1", "C_R2", "n1", "n2", "S1", "S2", "C_t1", "C_t2", "C_W1", "C_W2", "C_PIPELINE", "Psep"]
    return [names, [PR1, PR2, C_R1, C_R2, n1, n2, S1, S2, C_t1, C_t2, C_W1, C_W2, C_PIPELINE, Psep]]