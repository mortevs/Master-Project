import pandas as pd, pages.GUI.GUI_functions as display, streamlit as st, plotly.graph_objects as go, streamlit as st
from Data.Storage.Cache import SessionState
from shapely.wkt import loads
from shapely.geometry import Polygon, MultiPolygon
from pandas import DataFrame
import Data.dataProcessing as dP

class Sodir_prod(): 
    def __init__(self, parent, session_id:str, field:str = 'No field chosen'):
        self.__field = field
        self.__session_id = session_id
        self.__result = []
        self.__time_frame = []
        self.__state = SessionState.get(id=session_id, result=[], field=[], time_frame = [])
        self.parent  = parent

    def updateFromDropDown(self, fieldName, time, align, company):
         self.__field, self.__time_frame, self._aligned, self.__company = fieldName, time, align, company


    def get_current_time_frame(self):
        return self.__time_frame
    def get_current_field(self):
        return self.__field
    def get_current_result(self):
        return self.__result
    def get_current_alignment(self):
        return self._aligned

    
    def runY(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)  
        df = dP.yearly_produced_DF(self.__field, df = pd.DataFrame())
        df = dP.add_cumulative_columns(df, columns_to_ignore = ["Watercut"])
        df = dP.addProducedYears(self.__field, df)
        return df
    
    def runM(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)  
        df = dP.monthly_produced_DF(self.__field, df = pd.DataFrame())
        df = dP.add_cumulative_columns(df, columns_to_ignore = ["Watercut"])
        df = dP.addProducedMonths(self.__field, df) 
        return df

    def runCompanyY(self):
        #self.append_company(self.__company)
        self.append_field(self.__company)

        self.append_time_frame(self.__time_frame)
        company_licences = dP.company_licences(self.__company)
        company_production = {}
        for key in company_licences:
            if dP.check_addProducedYears(key):
                df = dP.yearly_produced_DF(key, df = pd.DataFrame())
                df = dP.addProducedYears(key, df)    
                company_production[key] = df.mul(company_licences[key]/100) #need to multiply license in, and i need to have license with time
        combined_df = list(company_production.values())[0]
        for key in list(company_production.keys())[1:]:
            combined_df = combined_df.add(company_production[key], fill_value=0)
    
        combined_df['Watercut'] = (100*combined_df["WaterSm3Yearly"]/(combined_df["WaterSm3Yearly"] + combined_df['OilSm3Yearly'] + combined_df['CondensateSm3Yearly'] + combined_df['NGLSm3Yearly']))
        
        st.write("Field ownerships:")
        for key, value in company_licences.items():
            st.write(f"{key}: {value}")        
                
        #df = dP.add_cumulative_columns(df, columns_to_ignore = ["Watercut"])
        return combined_df
    
    
    def runCompanyM(self):
        self.append_field(self.__company)
        self.append_time_frame(self.__time_frame)
        company_licences = dP.company_licences(self.__company) #
        company_production = {}
        for key in company_licences:
            if dP.check_addProducedYears(key):
                df = dP.monthly_produced_DF(key, df = pd.DataFrame())
                df = dP.addProducedMonths(key, df)
                company_production[key] = df.mul(company_licences[key]/100) #need to multiply license in, and i need to have license with time
        combined_df = list(company_production.values())[0]
        for key in list(company_production.keys())[1:]:
            combined_df = combined_df.add(company_production[key], fill_value=0)
        combined_df['Watercut'] = (100*combined_df["WaterSm3Monthly"]/(combined_df["WaterSm3Monthly"] + combined_df['OilSm3Monthly'] + combined_df['CondensateSm3Monthly'] + combined_df['NGLSm3Monthly']))
        st.write("Field ownerships:")
        for key, value in company_licences.items():
            st.write(f"{key}: {value}")        
        #hola
        st.write(combined_df)
        #df = dP.add_cumulative_columns(df, columns_to_ignore = ["Watercut"])
        return combined_df
     
    
    def plot_forecast(self, res_forcast):
        lst = self.get_time_frame()
        fields = []
        for field in self.__state.field:
            fields.append(field)
        res = res = self.getResult()
        display.multi_plot_SODIR_forecast(self.__state.field, res, res_forcast, lst[0])

    def plot(self, comp=False):

        res = self.getResult()
        lst = self.get_time_frame()
        if comp == False:
            for i in reversed(range(len(res))):
                if isinstance(res[i], DataFrame):
                    field = self.getField()
                    st.title('Produced volumes: ' + field[i])
                    display.multi_plot_SODIR([res[i]], lst[i])
        elif len(set(lst)) != 1:
            st.error("To compare different fields the timeframes must be the same. Can not compare yearly rates with monthly rates. If you would like to compare, clear output and plot production profiles with the same time frame.")
            
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            fields = []
            for field in self.__state.field:
                fields.append(field)
            display.multi_plot_SODIR_compare(dfs, fields, res, self._aligned, lst[0])

    def clear_output(self):
        from Data.Storage.Cache import SessionState
        SessionState.delete(id = self.__session_id)
        self.__state = SessionState.get(id=self.__session_id, result=[], field=[], time_frame = [], company = [])
    
    def getResult(self) -> list:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'result', [])

    def get_time_frame(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'time_frame', pd.DataFrame())
    
    def getField(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'field', pd.DataFrame())
    
    def getCompany(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'company', pd.DataFrame())

    def getPolyPlot(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'polyPlot', pd.DataFrame())

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state
    
    def append_time_frame(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'time_frame', value = item)

    def append_result(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'result', value = item)
    
    def append_field(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'field', value = item)
    
    def append_company(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'company', value = item)

    def store_polyPlot(self, item) -> str:
        SessionState.store_one(id = self.__session_id, key = 'polyPlot', value = item)
        
class PolygonPlotter:
    def __init__(self, wkt_str):
        self.wkt_str = wkt_str
        self.fig = None
        try:
            self.fig = self.plot()
        except Exception as e:
            self.handle_error(e)

    def plot(self):
        try:
            multipolygon = loads(self.wkt_str)

            if isinstance(multipolygon, MultiPolygon):
                traces = [
                    go.Scatter(
                        x=list(polygon.exterior.xy[0]),
                        y=list(polygon.exterior.xy[1]),
                        mode='lines',
                        fill='toself',
                        fillcolor='red',
                        line=dict(color='white', width=1),
                        name='Reservoir'
                    ) for polygon in multipolygon.geoms
                ]
            elif isinstance(multipolygon, Polygon):
                traces = [
                    go.Scatter(
                        x=list(multipolygon.exterior.xy[0]),
                        y=list(multipolygon.exterior.xy[1]),
                        mode='lines',
                        fill='toself',
                        fillcolor='red',
                        line=dict(color='white', width=1),
                        name='Reservoir'
                    )
                ]
            else:
                raise ValueError("Input is neither Polygon nor MultiPolygon")

            fig = go.Figure(data=traces)
            fig.update_layout(
                height=800,
                width=800,
                xaxis_title="Longitude",
                yaxis_title="Latitude",
                showlegend=True,
                #paper_bgcolor='black',
                #plot_bgcolor='black'
            )

            return fig
        except Exception as e:
            self.handle_error(e)
    def handle_error(self, error):
        st.write('Some error occured while plotting the reservoir area for this particular field', error)

def wlb_plot_production(fig, df, field):
    try:
        df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.strip('POINT ()').str.split(expand=True)
        df['Longitude'] = df['Longitude'].astype(float)
        df['Latitude'] = df['Latitude'].astype(float)    
        scatter_trace = go.Scatter(
            x=df['Longitude'],
            y=df['Latitude'],
            text=df['wlbWellboreName'],  
            mode='markers', 
            name = "Producing wells",
            marker=dict(size=10, color='green', symbol='circle'))
        fig.add_trace(scatter_trace)
        fig.update_layout(
            title='Reservoir and well locations ' + str(field),
            xaxis_title='Longitude',
            yaxis_title='Latitude',
        )
        return fig
    except Exception as e:
        #st.warning("No wells are categorized under wlbStatus as PRODUCING for this field")
        return fig
def wlb_plot_injection(fig, df, field):
    try:
        df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.strip('POINT ()').str.split(expand=True)
        df['Longitude'] = df['Longitude'].astype(float)
        df['Latitude'] = df['Latitude'].astype(float)    
        scatter_trace = go.Scatter(
            x=df['Longitude'],
            y=df['Latitude'],
            text=df['wlbWellboreName'],  
            mode='markers', 
            name = "Injecting wells",
            marker=dict(size=10, color='blue', symbol='circle'),
            showlegend= True

        )
        fig.add_trace(scatter_trace)
        fig.update_layout(
            title='Reservoir and well locations ' + str(field),
            xaxis_title='Longitude',
            yaxis_title='Latitude',
        )
        return fig
    except Exception as e:
        #st.warning("No wells are categorized under wlbStatus as INJECTING for this field") 
        return fig
def wlb_plot_closed(fig, df, field):
    try:
        df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.strip('POINT ()').str.split(expand=True)
        df['Longitude'] = df['Longitude'].astype(float)
        df['Latitude'] = df['Latitude'].astype(float)
        scatter_trace = go.Scatter(
            x=df['Longitude'],
            y=df['Latitude'],
            text=df['wlbWellboreName'],
            mode='markers',
            name = "Closed wells",
            marker=dict(size=10, color='yellow', symbol='circle'),
            showlegend= True

        )
        scatter_trace.visible = 'legendonly'
        # Add the scatter trace to the provided figure
        fig.add_trace(scatter_trace)

        # Update layout properties (optional)
        fig.update_layout(
            title='Reservoir and well locations ' + str(field),
            xaxis_title='Longitude',
            yaxis_title='Latitude',
        )

        return fig
    except Exception as e:
        #st.warning("No wells are categorized under wlbStatus as CLOSED for this field") 
        return fig
def wlb_plot_PA(fig, df, field):
    try:
        df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.strip('POINT ()').str.split(expand=True)
        df['Longitude'] = df['Longitude'].astype(float)
        df['Latitude'] = df['Latitude'].astype(float)    
        scatter_trace = go.Scatter(
            x=df['Longitude'],
            y=df['Latitude'],
            text=df['wlbWellboreName'],  
            mode='markers',
            name = "P&A wells",
            marker=dict(size=10, color='grey', symbol='circle'),
            showlegend= True
        )
        scatter_trace.visible = 'legendonly'
        fig.add_trace(scatter_trace)
        fig.update_layout(
            title='Reservoir and well locations ' + str(field),
            xaxis_title='Longitude',
            yaxis_title='Latitude',
        )

        return fig
    except Exception as e:
        #st.warning("No wells are categorized under wlbStatus as P&A for this field") 
        return fig
def wlb_plot_Plugged(fig, df, field):
    try:
        df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.strip('POINT ()').str.split(expand=True)
        df['Longitude'] = df['Longitude'].astype(float)
        df['Latitude'] = df['Latitude'].astype(float)    
        scatter_trace = go.Scatter(
            x=df['Longitude'],
            y=df['Latitude'],
            text=df['wlbWellboreName'], 
            mode='markers',
            name = "Plugged wells",
            marker=dict(size=10, color='black', symbol='circle'),
            showlegend= True
        )
        scatter_trace.visible = 'legendonly'
        fig.add_trace(scatter_trace)
        fig.update_layout(
            title='Reservoir and well locations ' + str(field),
            xaxis_title='Longitude',
            yaxis_title='Latitude',
        )
        return fig
    except Exception as e:
        #st.warning("No wells are categorized under wlbStatus as PLUGGED for this field") 
        return fig
def makePolyPlot(field):
    fig = go.Figure()
    import Data.getData as get
    wkt_str = get.polygon_coordinates(field)
    polygon_plotter = PolygonPlotter(wkt_str)
    try:
        try:
            updated_fig = wlb_plot_production(polygon_plotter.fig, get.producing_wlb(field), field)
        except:
            pass
        try:
            updated_fig = wlb_plot_injection(polygon_plotter.fig, get.injecting_wlb(field), field)
        except:
            pass
        try:
            updated_fig = wlb_plot_closed(polygon_plotter.fig, get.closed_wlb(field), field)
        except:
            pass
        try:
            updated_fig = wlb_plot_PA(polygon_plotter.fig, get.PA_wlb(field), field)
        except:
            pass
        try:
            updated_fig = wlb_plot_Plugged(polygon_plotter.fig, get.plugged_wlb(field), field)
        except:
            pass
        return updated_fig
    except:
        return polygon_plotter.fig
   
def plotPolyPlot(fig):
    st.plotly_chart(fig, use_container_width=True)


    