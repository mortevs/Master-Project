import pandas as pd
import numpy as np
from Equations.ZfacStanding import ZfacStanding
from Equations.pWfMinEstimation import pWfMinEstimation
from IPR.qPotWell import qPotWell
import Equations.DryGasFlowEquations as DGFE
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF
from scipy.optimize import fsolve

def IPROnly(qFieldTarget: float, PRi: float, abandonmentRate: float, TR:float, gasMolecularWeight: float, C_R: float, n:float, N_temp: float, NWellsPerTemplate: float, upTime: int, C_t: float, S:float, C_FL:float, C_PL:float, P_sep: float, IGIP: float) -> pd.DataFrame:
    """
    qFieldTarget =  plateau rate, [sm3/day]
    PRi = initial reservoir pressure, [bara]
    abandonmentRate = rate for abandonment, [sm3/day]
    gasMolecularWeight = molecular weight of gas at standard conditions #[g/mol],
    C_R = inflow backpressure coefficient,
    n = Inflow backpressure exponent,
    N_temp = number of templates
    NWellsPerTemplate = number of wells per template. Assumes the same amount of wells per template.
    upTime = number of operational days in a year, 
    C_t = tubing flow coefficient, 
    S = tubing elevation coefficient,
    C_FL = flowline coefficient from template-PLEM ,
    C_PL = Pipeline coefficient from PLEM-Shore,
    p_sep = seperator pressure [bara],
    IGIP = initial gas in place [sm3].
    """
    ticker = 0
    years = 200 #maximum simulation time 200 years
    NWells = N_temp*NWellsPerTemplate
    df = pd.DataFrame(np.zeros((years, 13)))
    df[0][0:years] = qFieldTarget #QFieldTarget, what we want our field to produce   
    df[1][0:years] = df[0]/NWells #qWell Target, what we want each well to produce
    fieldRate = qFieldTarget #assuming we can produce the target rate initially 
    #estimating the minimim bottomhole pressure
    pWfMin = pWfMinEstimation(C_t, S, C_FL, C_PL, fieldRate, P_sep, N_temp, NWellsPerTemplate) 
    df[4][0:years] = pWfMin #assuming PwfMin is constant during the fields lifetime
    #calculating initial Zfactor.
    Zi = ZfacStanding(PRi, TR, gasMolecularWeight)
    i = 0
    while (i<years): #Doing the calculations for each year
        if i == 0: 
            df[2][0] = PRi #Initial reservoir pressure year 0
            df[9][0] = 0 #initial yearly gas of take = 0
            df[10][0] = 0 #initial cumulative gas of take = 0    
        else:
            #calculating the reservoir pressure with time numerically using scipy fsolve
            def f(x, df):
                df[5][i] = qPotWell(C_R, n, x, pWfMin) #potential flow for one well
                df[6][i] = df.iloc[i, 5] * NWells #potential for field  
                if df.iloc[i, 6] >= qFieldTarget: #checking if we have high enough potential to produce desired plateau rate
                    df[7][i] = qFieldTarget
                else: #if we cant produce our target rate, the plateau period is ended.
                    df[7][i]= df.iloc[i, 6]          
                df[9][i] = df.iloc[i-1, 7]*upTime #yearly gas offtake = rates [sm3/day] * upTime[days]

                df[10][i] = df.iloc[i-1, 10] + df.iloc[i, 9]          
                return x - MBgastank_PR(PRi, Zi, ZfacStanding(df.iloc[i-1, 2], TR, gasMolecularWeight), RF(df[10][i], IGIP ))         
            a = fsolve(f, pWfMin, df)
            df[2][i] = a    
        #calculating the z-factor which is dependent on the reservoir pressure which in its turn is dependent on the z-factor
        df[3][i] = ZfacStanding(df.iloc[i, 2], TR, gasMolecularWeight)
        df[5][i] = qPotWell(C_R, n, df.iloc[i, 2], pWfMin) #potential flow for one well
        df[6][i] = df.iloc[i, 5] * NWells #potential for field  
        if df.iloc[i, 6] >= qFieldTarget: #checking if we have high enough potential to produce desired plateau rate
            df[7][i] = qFieldTarget
        else: #if we cant produce our target rate, the plateau period is ended.
            df[7][i] = df.iloc[i, 6] #lower potential than wanted then then we produce what we can     
            #if we produce less than abandonmentRate we have reached abandoment
            if (df.iloc[i, 7]) < abandonmentRate and ticker == 0: 
                abandonmentLength = i
                years = i 
                df = df.iloc[0:years+1, :] #we are not interested in doing more calculations.
                ticker = 1
                break
        df[8][i] = df.iloc[i, 7] / NWells #what we produce per well 
        df[11][i] = RF(df[10][i], IGIP) # recovery factor. 
        PWf = DGFE.IPRpwf(C_R, n, df.iloc[i, 2], df.iloc[i, 8])
        df[12][i] = PWf # potential wellflow
        i+=1
    return df


