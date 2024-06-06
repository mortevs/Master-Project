import pandas as pd, numpy as np, Equations.DryGasFlowEquations as DGFE, streamlit as st
from Equations.ZfacStanding import ZfacStanding
from Equations.pWfMinEstimation import pWfMinEstimation
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF
from scipy.optimize import root
from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.dry_gas_R_analysis import ResAnalysis
def Nodal(qFieldTarget: float, PRi: float, abandonmentRate: float, TR:float, gasMolecularWeight: float, C_R: float, n:float, N_temp: float, NWellsPerTemplate: float, upTime: int, C_t: float, S:float, C_FL:float, C_PL:float, P_sep: float, IGIP: float, build_up: int) -> pd.DataFrame: 
    """
    qFieldTarget =  plateau rate, [sm3/day],
    PRi = initial reservoir pressure [bara],
    abandonmentRate = rate for abandonment [sm3/day],
    gasMolecularWeight = molecular weight of gas at standard conditions #[g/mol],
    C_R = inflow backpressure coefficient,
    n = Inflow backpressure exponent,
    N_temp = number of templates,
    NWellsPerTemplate = number of wells per template. Assumes the same amount of wells per template,
    upTime = number of operational days in a year, 
    C_t = tubing flow coefficient, 
    S = tubing elevation coefficient,
    C_FL = flowline coefficient from template-PLEM,
    C_PL = Pipeline coefficient from PLEM-Shore,
    p_sep = seperator pressure [bara],
    IGIP = initial gas in place [sm3],
    build_up = build_up period [years].
    """
    NWells = N_temp*NWellsPerTemplate
    max_sim_time = 300 
    build_up = int(build_up)
    
    #build-up to plateau:
    def production_build_up(qFieldTarget = qFieldTarget, PRi = PRi, TR = TR, gasMolecularWeight = gasMolecularWeight, C_R = C_R, n = n, N_temp = N_temp, NWellsPerTemplate = NWellsPerTemplate, upTime = upTime, C_t = C_t, S = S, C_FL = C_FL, C_PL = C_PL, P_sep = P_sep, IGIP = IGIP, build_up = build_up, max_sim_time = max_sim_time) -> pd.DataFrame: 
        buildUp_df = pd.DataFrame(np.zeros((max_sim_time, 16)))
        buildup_rate = qFieldTarget/build_up
        build_up_list = [buildup_rate*i for i in range(build_up)]
        gas_offtake = [0]   
        for i in range(1, len(build_up_list)):
            gas_offtake.append((build_up_list[i-1]+build_up_list[i])/2 * upTime) #Trapezoidal rule
        
        build_up_Analysis = ResAnalysis(gas_offtake, [PRi, TR, gasMolecularWeight, IGIP]) #dataframe
        buildUp_df[0][0:build_up] = build_up_list
        buildUp_df[1][0:build_up] = build_up_Analysis['Produced Gas [Sm3]'].copy()
        buildUp_df[2][0:build_up] = build_up_Analysis['Cumulative Produced Gas [Sm3]'].copy()
        buildUp_df[5][0:build_up] = build_up_Analysis['Estimated Reservoir Pressure [bara]'].copy()
        buildUp_df[11][0:max_sim_time] = P_sep
        i = 0
        while (i<build_up):
            buildUp_df[3][i] = RF(buildUp_df.iloc[i, 2], IGIP)   
            buildUp_df[4][i] = ZfacStanding(buildUp_df.iloc[i, 5], TR, gasMolecularWeight)
            buildUp_df[6][i] = buildUp_df.iloc[i, 0] / NWells #Qwell
            buildUp_df[7][i] = DGFE.IPRpwf(C_R, n, buildUp_df.iloc[i, 5], buildUp_df.iloc[i, 6]) #Pwf
            buildUp_df[8][i] = DGFE.Tubingp2(C_t, S, buildUp_df.iloc[i, 7], buildUp_df.iloc[i, 6]) #Pwh
            buildUp_df[10][i] = DGFE.Linep1(C_PL, buildUp_df.iloc[i, 11], buildUp_df.iloc[i, 0]) #Pplem (pipeline entry module)
            buildUp_df[12][i] = buildUp_df.iloc[i, 0] / N_temp #Qtemp
            buildUp_df[9][i] = DGFE.Linep1(C_FL, buildUp_df.iloc[i, 10], buildUp_df.iloc[i, 12]) #Ptemplate
            buildUp_df[13][i] = (buildUp_df.iloc[i, 8] - buildUp_df.iloc[i, 9])#deltaPChoke , simple model, difference between p_wh and p_template
            buildUp_df[14][i] = (buildUp_df.iloc[i, 9] / buildUp_df.iloc[i, 8])#ratio p_temp to p_wh
            
            def f(x): #potential production rate (if fully open choke)
                return DGFE.Tubingp2(C_t, S, DGFE.IPRpwf(C_R, n, buildUp_df.iloc[i, 5], x / NWells), x / NWells) - DGFE.Linep1(C_FL, DGFE.Linep1(C_PL, P_sep, x), x / N_temp)
            try:
                sol = root(f, buildUp_df.iloc[i, 0])
            except ValueError:
                sol = 0
            buildUp_df[15][i] = sol.x #production potential
            i+=1
        return buildUp_df
    
    df = production_build_up()
    df[0][build_up:max_sim_time] = qFieldTarget
    Zi = ZfacStanding(PRi, TR, gasMolecularWeight)
    i = build_up
    while (i<max_sim_time):
        def g(x, df):
            df[1][i] = (df.iloc[i-1, 0] + df.iloc[i, 0])/2 * upTime #yearly gas offtake calculated with trapezoidal rule
            df[2][i] = df.iloc[i-1, 2] + df.iloc[i, 1] #cumulative gas offtake
            df[3][i] = RF(df.iloc[i, 2], IGIP)
            return MBgastank_PR(PRi, Zi, ZfacStanding(x, TR, gasMolecularWeight), df.iloc[i, 3])-x
        
        pWfMin = pWfMinEstimation(C_t, S, C_FL, C_PL, df.iloc[i, 0], P_sep, N_temp, NWellsPerTemplate)
        solv = root(g, pWfMin, df)
        df[5][i] = solv.x
        df[4][i] = ZfacStanding(solv.x, TR, gasMolecularWeight) # z-factor  
        def f(x): #calculate potential production rate for choke 0, we can then determine how much we have to choke to reach desired rates
            return DGFE.Tubingp2(C_t, S, DGFE.IPRpwf(C_R, n, solv.x, x / NWells), x / NWells) - DGFE.Linep1(C_FL, DGFE.Linep1(C_PL, P_sep, x), x / N_temp)
        if i == 1:
            guess = qFieldTarget
        else:
            guess = df.iloc[i-1, 15] #initial guess based on the previous initial guess
        solv2 = root(f, guess)
        if solv2.success == True:
            df[15][i] = solv2.x
        else:
            guess_scale = [1/32, 1/16, 1/8, 1/4, 1/3, 1/2, 2, 3, 4, 5, 8, 12, 20, 32]
            for scale in guess_scale:
                guess = qFieldTarget*scale
                solv2 = root(f, guess)
                if solv2.success == True:
                    df[15][i] = solv2.x
                    break    
                elif scale == 32 and solv2.success == False:
                    st.error("The problem could not be solved using Nodal Implicit. Try solving it with the Explicit method, or using the IPR method")
    
        #update rest of the calculations with the solved rate and pressure:
        if df.iloc[i, 15] < qFieldTarget: #check if our potential is less than our desired rates
            df[0][i] = df.iloc[i, 15] #Can no longer produce the target rate. Instead we must produce what we can, with choke fully open 
            df[13][i] = 0 #set choke to 0

        #then update all the other calculations to the rate determined
        df[1][i] = (df.iloc[i-1, 0] + df.iloc[i, 0])/2 * upTime #yearly gas offtake calculated with trapezoidal rule
        df[2][i] = df.iloc[i-1, 2] + df.iloc[i, 1]
        df[3][i] = RF(df.iloc[i, 2], IGIP)
        df[6][i] = df.iloc[i, 0] / NWells #Qwell
        df[7][i] = DGFE.IPRpwf(C_R, n, df.iloc[i, 5], df.iloc[i, 6]) #Pwf
        df[8][i] = DGFE.Tubingp2(C_t, S, df.iloc[i, 7], df.iloc[i, 6]) #Pwh
        df[10][i] = DGFE.Linep1(C_PL, df.iloc[i, 11], df.iloc[i, 0]) #Pplem (pipeline entry module)
        df[12][i] = df.iloc[i, 0] / N_temp #Qtemp
        df[9][i] = DGFE.Linep1(C_FL, df.iloc[i, 10], df.iloc[i, 12]) #Ptemplate
        if df.iloc[i, 15] >= qFieldTarget:
            df[13][i] = (df.iloc[i, 8] - df.iloc[i, 9])#deltaPChoke , simple model, difference between p_wh and p_template
        df[14][i] = df.iloc[i, 9] / df.iloc[i, 8]#ratio p_temp to p_wh
        if (df.iloc[i, 15]) <= abandonmentRate:
            df = df.iloc[0:i, :] #we are not interested in doing more calculations than necessary
            return df
        i+=1
    st.error("Max simulation time (300 years) encountered")
    return df #returns the dataframe with production lasting until Max simulation
