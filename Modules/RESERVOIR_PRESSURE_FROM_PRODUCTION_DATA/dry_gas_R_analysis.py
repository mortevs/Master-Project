import pandas as pd
import pandas as pd
import numpy as np
from Equations.ZfacStanding import ZfacStanding
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF

def ResAnalysis(produced:list, parameters:list, Trapezoidal = False):
    df = build_analysis(produced, *parameters, Trapezoidal)
    df.columns=('Estimated Reservoir Pressure [bara]', 'Produced Gas [Sm3]', 'Cumulative Produced Gas [Sm3]')
    return df

def build_analysis(produced:list, PRi: float, TR:float, gasMolecularWeight: float, IGIP, Trapezoidal) -> float:
    if Trapezoidal == True:
        produced = [produced[0]/2] + produced #Trapezoidal Rule
    sim_len = int(len(produced))
    df = pd.DataFrame(np.zeros((sim_len, 3)))
    Zi = ZfacStanding(PRi, TR, gasMolecularWeight)
    df[0][0] = PRi
    df[1][0] = produced[0] #gas offtake
    df[2][0] = produced[0] #cumulative gas offtake
    for i in range(1, sim_len):
        df[1][i] = produced[i] #gas offtake 
        df[2][i] = df.iloc[i, 1] + df.iloc[i-1, 2] #cumulative gas offtake
    from scipy.optimize import fsolve
    def f(X):                             
        return X - MBgastank_PR(PRi, Zi, ZfacStanding(X, TR, gasMolecularWeight), RF(df.iloc[i, 2],IGIP)) 
    for i in range(1, sim_len):
        sol = fsolve(f, df.iloc[i-1,0])
        df[0][i] = sol
    return df

