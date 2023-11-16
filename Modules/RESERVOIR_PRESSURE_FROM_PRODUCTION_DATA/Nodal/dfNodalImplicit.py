import pandas as pd
import numpy as np
from Equations.ZfacStanding import ZfacStanding
import Equations.DryGasFlowEquations as DGFE
from Equations.pWfMinEstimation import pWfMinEstimation
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF
from scipy.optimize import fsolve
from scipy.optimize import root
import matplotlib.pyplot as plt



def Nodal(qFieldTarget: float, PRi: float, abandonmentRate: float, TR:float, gasMolecularWeight: float, C_R: float, n:float, N_temp: float, NWellsPerTemplate: float, upTime: int, C_t: float, S:float, C_FL:float, C_PL:float, P_sep: float, IGIP: float) -> float: 
    """
    qFieldTarget =  plateau rate, [sm3/day]
    PRi = initial reservoir pressure, [bara]
    abandonmentRate = rate for abandonment, [sm3/day]
    gasMolecularWeight = 16 #[g/mol],
    C_R = 1000 #inflow backpressure coefficient,
    n = 1 #Inflow backpressure exponent,
    N_temp = 3 #number of templates
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
    df = pd.DataFrame(np.zeros((years, 16)))
    Zi = ZfacStanding(PRi, TR, gasMolecularWeight)
    
    qField = qFieldTarget
    fieldRate = qFieldTarget

    df[0][0:years] = qField #Assuming we can produce at the desired rate
    
    df[11][0:years] = P_sep #assuming constant seperator pressure

    pWfMin = pWfMinEstimation(C_t, S, C_FL, C_PL, fieldRate, P_sep, N_temp, NWellsPerTemplate)

    i = 0
    while (i<years): #Doing the calculations for each year
        if i == 0: 
            df[1][0] = 0 #initial yearly gas of take = 0
            df[2][0] = 0 #initial cumulative gas of take = 0
            df[3][0] = 0 #recovery factor = 0
            df[4][i] = Zi
            df[5][0] = PRi #Initial reservoir pressure year 0
            
            
            
        else:
            
            def g(x, df):
                df[1][i] = df.iloc[i-1, 0]*upTime #yearly gas offtake = rates [sm3/day] * upTime[days]
                df[2][i] = df.iloc[i-1, 2] + df.iloc[i, 1]
                df[3][i] = RF(df.iloc[i, 2], IGIP)
                
                return MBgastank_PR(PRi, Zi, ZfacStanding(x, TR, gasMolecularWeight), df.iloc[i, 3])-x
                
            b = root(g, pWfMin, df)
            df[5][i] = b.x
            df[4][i] = ZfacStanding(df.iloc[i, 5], TR, gasMolecularWeight) # z-factor
        
        x = df.iloc[i, 0]
        
        def f(x): #calculate potential produciton rate for choke 0, we then can determine how much we have to choke to reach desired rates
            return DGFE.Tubingp2(C_t, S, DGFE.IPRpwf(C_R, n, df.iloc[i, 5], x / NWells), x / NWells) - DGFE.Linep1(C_FL, DGFE.Linep1(C_PL, P_sep, x), x / N_temp)
        a = root(f, df.iloc[i-1, 0])
        df[15][i] = a.x
        
        if df.iloc[i, 15] < qFieldTarget: #check if our potential is less than our desired rates
            df[0][i] = df.iloc[i, 15] #if so, then we must produce what we can
            df[13][i] = 0 #set choke to 0 
                  
        df[6][i] = df.iloc[i, 0] / NWells #Qwell
        df[7][i] = DGFE.IPRpwf(C_R, n, df.iloc[i, 5], df.iloc[i, 6]) #Pwf
        df[8][i] = DGFE.Tubingp2(C_t, S, df.iloc[i, 7], df.iloc[i, 6]) #Pwh
        df[10][i] = DGFE.Linep1(C_PL, df.iloc[i, 11], df.iloc[i, 0]) #Pplem (pipeline entry module)
        df[12][i] = df.iloc[i, 0] / N_temp #Qtemp
        df[9][i] = DGFE.Linep1(C_FL, df.iloc[i, 10], df.iloc[i, 12]) #Ptemplate
        df[13][i] = round(df.iloc[i, 8] - df.iloc[i, 9])#deltaPChoke , simple model, difference between p_wh and p_template
        df[14][i] = df.iloc[i, 9] / df.iloc[i, 8]#ratio p_temp to p_wh
        

        if (df.iloc[i, 0]) <= abandonmentRate and ticker == 0: 
            years = i 
            df = df.iloc[0:i+1, :] #we are not interested in doing more calculations than necessary
            return df
            
        i+=1
    return df
