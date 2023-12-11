import pandas as pd
import Data.dataProcessing as dP
import pandas as pd
import numpy as np
from Equations.ZfacStanding import ZfacStanding
import Equations.DryGasFlowEquations as DGFE
from Equations.MBgastank_PR import MBgastank_PR
from Equations.RF import RF

def ResAnalysis(produced:list, parameters:list):
    df = build_analysis(produced, *parameters) 
    df.columns=('PR', 'cumulative produced gas [sm3]', 'produced gas [sm3]')
    return df

def build_analysis(produced:list, PRi: float, TR:float, gasMolecularWeight: float, IGIP) -> float: 
    sim_len = len(produced)
    df = pd.DataFrame(np.zeros((sim_len, 3)))
    Zi = ZfacStanding(PRi, TR, gasMolecularWeight)
    df[0][0:sim_len] = produced #assign column one to what has been produced.
    df[1][0] = produced[0] 
    for i in range(sim_len):
        df[1][i] = df.iloc[i, 0] + df.iloc[i-1, 1]
    from scipy.optimize import fsolve
    def swapColumns(df, col1, col2):
        col_list = list(df.columns)
        x, y = col_list.index(col1), col_list.index(col2)
        col_list[y], col_list[x] = col_list[x], col_list[y]
        df = df[col_list]
        return df
    def f(X):                             
        return X - MBgastank_PR(PRi, Zi, ZfacStanding(X, TR, gasMolecularWeight), RF(df.iloc[i, 1],IGIP)) 
    for i in range(sim_len):
        if i == 0:
            df[2][0] = fsolve(f, PRi)
        else:
            df[2][i] = fsolve(f, df.iloc[i-1,2])    
    df = swapColumns(df, 0, 2)
    return df

