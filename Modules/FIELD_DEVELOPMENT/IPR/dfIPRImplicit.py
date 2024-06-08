import pandas as pd, numpy as np, Equations.DryGasFlowEquations as DGFE, streamlit as st
from Equations.ZfacStanding import ZfacStanding
from Equations.pWfMinEstimation import pWfMinEstimation
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF
from scipy.optimize import fsolve

def IPROnly(qFieldTarget: float, PRi: float, abandonmentRate: float, TR:float, gasMolecularWeight: float, C_R: float, n:float, N_temp: float, NWellsPerTemplate: float, upTime: int, C_t: float, S:float, C_FL:float, C_PL:float, P_sep: float, IGIP: float, build_up: int) -> pd.DataFrame:
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
    pWfMin = pWfMinEstimation(C_t, S, C_FL, C_PL, qFieldTarget, P_sep, N_temp, NWellsPerTemplate) 
    Zi = ZfacStanding(PRi, TR, gasMolecularWeight)
    
    def simple_production_build_up(qFieldTarget = qFieldTarget, PRi = PRi, TR = TR, gasMolecularWeight = gasMolecularWeight, C_R = C_R, n = n, upTime = upTime, IGIP = IGIP, build_up = build_up, max_sim_time = max_sim_time) -> pd.DataFrame: 
        buildUp_df = pd.DataFrame(np.zeros((max_sim_time, 13)))
        buildup_rate = qFieldTarget/build_up
        build_up_list = [buildup_rate*i for i in range(build_up)]
        gas_offtake = [0]
        cumulative_gas_offtake = [0] 
        for i in range(1, build_up):
            gas_offtake.append((build_up_list[i-1]+build_up_list[i])/2 * upTime) #Trapezoidal rule
            cumulative_gas_offtake.append(cumulative_gas_offtake[i-1]+gas_offtake[i])
        buildUp_df[0][0:build_up] = build_up_list #what we want to produce
        buildUp_df[1][0:build_up] = buildUp_df[0][0:build_up]/NWells 
        buildUp_df[2][0:build_up] = PRi #simplification with the IPR approach, Reservoir pressure remains constant during build-up
        buildUp_df[3][0:build_up] = ZfacStanding(PRi, TR, gasMolecularWeight) #As a consequence, the Z-factor also remains constant during build-up
        buildUp_df[4][0:max_sim_time] = pWfMin #assumption IPR-method. pWfMin remains constant throughout fields lifetime
        buildUp_df[5][0:build_up] = DGFE.IPRqg(C_R, n, PRi, pWfMin) #As a consequence, the well potential also remains constant during build-up
        buildUp_df[6][0:build_up] = buildUp_df.iloc[i, 5] * NWells #field potential
        for i in range(build_up):
            buildUp_df[7][i] = build_up_list[i]
            buildUp_df[8][i] = build_up_list[i]/(NWells)
            buildUp_df[9][i] = gas_offtake[i]
            buildUp_df[10][i] = cumulative_gas_offtake[i]
            buildUp_df[11][build_up] = RF(buildUp_df[10][build_up], IGIP)
            buildUp_df[12][i] = DGFE.IPRpwf(C_R, n, PRi, buildUp_df.iloc[i, 8])
        return buildUp_df         
    df = simple_production_build_up()
    df[0][build_up:max_sim_time] = qFieldTarget
    df[1][0:max_sim_time] = df[0]/NWells 
    i = build_up
    while (i<max_sim_time):
        def f(x, df):
            df[5][i] = DGFE.IPRqg(C_R, n,  x, pWfMin) #potential flow for one well
            df[6][i] = df.iloc[i, 5] * NWells #potential for field  
            if df.iloc[i, 6] >= qFieldTarget: 
                df[7][i] = qFieldTarget
            else: 
                df[7][i]= df.iloc[i, 6]              
            df[9][i] = (df.iloc[i-1, 7] + df.iloc[i, 7])/2 * upTime #yearly gas offtake calculated with trapezoidal rule
            df[10][i] = df.iloc[i-1, 10] + df.iloc[i, 9] #cumulative gas offtake    
            return x - MBgastank_PR(PRi, Zi, ZfacStanding(x, TR, gasMolecularWeight), RF(df[10][i], IGIP )) 
        sol = fsolve(f, pWfMin, df)
        df[2][i] = sol  #PR 
        #Updating calculations to the solution found
        df[3][i] = ZfacStanding(df.iloc[i, 2], TR, gasMolecularWeight)
        df[5][i] = DGFE.IPRqg(C_R, n, df.iloc[i, 2], pWfMin) #potential flow for one well
        df[6][i] = df.iloc[i, 5] * NWells #potential for field  
        if df.iloc[i, 6] >= qFieldTarget: 
            df[7][i] = qFieldTarget 
        else: 
            df[7][i] = df.iloc[i, 6]      
            if (df.iloc[i, 7]) <= abandonmentRate: 
                df = df.iloc[0:i, :] 
                break    
        df[8][i] = df.iloc[i, 7] / NWells #what we produce per well
        df[9][i] = (df.iloc[i-1, 7] + df.iloc[i, 7])/2 * upTime #yearly gas offtake calculated with trapezoidal rule
        df[10][i] = df.iloc[i-1, 10] + df.iloc[i, 9] #cumulative gas offtake   
        df[11][i] = RF(df[10][i], IGIP) # recovery factor. 
        df[12][i] = DGFE.IPRpwf(C_R, n, df.iloc[i, 2], df.iloc[i, 8]) 
        if i == 300:
            st.error("Max simulation time = 300 years encountered")
            return df
        i+=1
    return df