import streamlit as st
import pandas as pd
class Curve_fitting():
    def __init__(self, dfs, FC_length, time):
        self._curve_fitted_dfs = [] 
        for df in dfs:
            df_length = len(df.index)
            empty_df = pd.DataFrame(data = 0, index=range(FC_length), columns=df.columns)
            
            if time[0] == 'Yearly':
                self.__custom_index = [(df.index[-1]+i) for i in range(0, FC_length)]
            else:
                prev_ind = df.index[-1]
                def next_month_year(prev_ind):
                    month, year = prev_ind.split(':')
                    if int(month)<12:
                        string = str(int(month)+1)+':'+year
                        return string
                    else:
                        string = str(1)+':'+str((int(year)+1))
                        return string
                self.__custom_index = [(prev_ind)]
                for i in range(FC_length-1):
                     last_el = self.__custom_index[-1]
                     self.__custom_index.append(next_month_year(last_el))
            empty_df.index = self.__custom_index
            #df = pd.concat([df, empty_df])
            df = empty_df
            self._curve_fitted_dfs.append(df)

    def get_curve_fitted_dfs(self):
        return self._curve_fitted_dfs


    
        