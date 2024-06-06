import pandas as pd
import numpy as np
class Curve_fitting():
    def __init__(self, dfs, FC_length, time, data_points):
        self._data_points = data_points
        self._curve_fitted_dfs = [] 
        for df in dfs:
            df_length = len(df.index)
            if df_length < self._data_points:
                self._data_points = df_length
            empty_df = pd.DataFrame(data = 0, index=range(FC_length), columns=df.columns)
            if time[0] == 'Yearly':
                self.__custom_index = [(df.index[-2]+i) for i in range(0, FC_length)]
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
            for column in empty_df:
                if time[0] == 'Yearly':
                    empty_df[column] = self.curve_fit(df[column][-(self._data_points)-1:-1], FC_length, time)
                else:
                    empty_df[column] = self.curve_fit(df[column][-self._data_points:], FC_length, time)                
            curve_fitted_df = empty_df
            self._curve_fitted_dfs.append(curve_fitted_df)
    
    def curve_fit(self, list, FC_length, time ):
        if time[0] == 'Yearly':
            self.__clean_data = self.remove_outliers_year(list)
        else:
            self.__clean_data = self.remove_outliers_month(list)
        self._data = self.__clean_data
        curve_fitted_data = []
        for i in range(FC_length):
            x_values = np.arange(len(self._data))
            try:
                coefficients = np.polyfit(x_values, self._data, deg=1)
                next_x = len(self._data)
                next_value = np.polyval(coefficients, next_x)
                self._data.append(next_value)
                curve_fitted_data.append(next_value)
            except:
                curve_fitted_data.append(0)
        return curve_fitted_data      
    
    def get_curve_fitted_dfs(self):
        return self._curve_fitted_dfs 
    
    def remove_outliers_year(self, lst):
        lst = [el for el in lst[:-1] if el > 0]
        average = np.average(np.array(lst))
        lst = [el for el in lst if el >= average * 0.5]
        return lst
    
    def remove_outliers_month(self, lst):
        lst = [el for el in lst if el > 0]
        average = np.average(np.array(lst))
        lst = [el for el in lst if el >= average * 0.5]
        return lst




    
        