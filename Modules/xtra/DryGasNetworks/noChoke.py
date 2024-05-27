import pandas as pd
import numpy as np
import Equations.DryGasFlowEquations as DGFE
from scipy.optimize import minimize
import warnings
#Network of two gas fields



def noChoke(PR1, PR2, C_R1, C_R2, n1, n2, S1, S2, C_t1, C_t2, C_W1, C_W2, C_PIPELINE, Psep):  
    #for storing the network data in the dataframe 
    def Network(PR1, PR2, C_R1, C_R2, n1, n2, S1, S2, C_t1, C_t2, C_W1, C_W2, C_PIPELINE, Psep): 
        df = pd.DataFrame(np.zeros((3, 12))) 
        #df[0][0:2] = PR
        df[0][0] = PR1
        df[0][1] = PR2
        df[1][0] = C_R1
        df[1][1] = C_R2
        df[2][0] = n1
        df[2][1] = n2
        df[3][0] = S1
        df[3][1] = S2
        df[4][0] = C_t1
        df[4][1] = C_t2
        df[5][0] = C_W1
        df[5][1] = C_W2
        df[5][2] = C_PIPELINE
        df[6][2] = Psep    
        return df

    def error(params, df): #for finding the optimal production volumes from each well we minimize the error by changing the bottomhole pressure for each well
        Pwf1, Pwf2 = params
        df[7][0] = Pwf1 #guess for bottomhole pressure well one
        df[7][1] = Pwf2 #guess for bottomhole pressure well two
        df[8][0] = DGFE.IPRqg(C_R1, n1, PR1, df.iloc[0, 7]) #q_well one
        df[8][1] = DGFE.IPRqg(C_R2, n2, PR2, df.iloc[1, 7]) #q_well two
        df[8][2] = df.iloc[0, 8] + df.iloc[1, 8] #q_total 
        df[9][0] = DGFE.Tubingp2(C_t1, S1, df.iloc[0, 7], df.iloc[0, 8]) #pressure at wellhead 1
        df[9][1] = DGFE.Tubingp2(C_t2, S2, df.iloc[1, 7], df.iloc[1, 8]) #pressure at wellhead 2
        df[10][0] = DGFE.Linep2(C_W1, df.iloc[0, 9], df.iloc[0, 8]) #pressure at junction
        df[10][1] = DGFE.Linep2(C_W2, df.iloc[1, 9], df.iloc[1, 8]) #pressure at junction
        df[10][2] = DGFE.Linep1(C_PIPELINE, Psep, df.iloc[2, 8]) #pressure at other side of junction
        Average = (df.iloc[0, 10]+df.iloc[1, 10]+df.iloc[2, 10])/3
        df[11][0] = (Average-df.iloc[0, 10])**2 #square error
        df[11][1] = (Average-df.iloc[1, 10])**2 #square error
        df[11][2] = (Average-df.iloc[2, 10])**2 #square errror
        return (df.iloc[0, 11] + df.iloc[1, 11] + df.iloc[2, 11]) #sum of square errors, which we want to minimize to find our solution
    initial_guess = [1, 1] #our initial guess 
    df = Network(PR1, PR2, C_R1, C_R2, n1, n2, S1, S2, C_t1, C_t2, C_W1, C_W2, C_PIPELINE, Psep)    
     #ignoring warning that occurs due to initial guess leading to no solution
    warnings.filterwarnings("ignore")
    result = minimize(error, initial_guess, df)

    i = 1
    while (result.success == False and i<PR1*3): #updating our initial guess 
                                                #no need to check for solutions for unlikely bottomhole pressures
        i+=2
        initial_guess =  [i, i]
        result = minimize(error, initial_guess, df)
    if result.success:
        fitted_params = result.x
        #print(fitted_params)
        print(df.iloc[0, 8], "sm3/d from well 1 and", df.iloc[1, 8], "sm3/d from well 2.")
        return df
    else:
        raise ValueError('No solution found. Try guessing Pwf manually.') #no solution found
