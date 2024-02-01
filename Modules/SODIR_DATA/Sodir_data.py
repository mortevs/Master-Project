import pandas as pd
from Data.Storage.Cache import SessionState
import GUI.GUI_functions as display
from GUI.GUI_class import SODIR_feature
import streamlit as st
from shapely.wkt import loads
import plotly.graph_objects as go

class Sodir_prod(SODIR_feature):
    def __init__(self, parent, session_id:str, field:str = 'No field chosen'):
        self.__field = field
        self.__session_id = session_id
        self.__result = []
        self.__time_frame = []
        self.__state = SessionState.get(id=session_id, result=[], field=[], time_frame = [])
        self.parent  = parent

    def updateFromDropDown(self, fieldName, time):
         self.__field, self.__time_frame = fieldName, time
    
    def get_current_time_frame(self):
        return self.__time_frame
    def get_current_field(self):
        return self.__field
    def get_current_result(self):
        return self.__result

    def runY(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)  
        import Data.dataProcessing as dP
        df = dP.yearly_produced_DF(self.__field, df = pd.DataFrame())
        df = dP.addProducedYears(self.__field, df)
        return df
    
    def runM(self):
        self.append_field(self.__field)
        self.append_time_frame(self.__time_frame)  
        import Data.dataProcessing as dP
        df = dP.monthly_produced_DF(self.__field, df = pd.DataFrame())
        df = dP.addProducedMonths(self.__field, df)
        return df

    
    def plot(self, comp=False):
        import streamlit as st
        from pandas import DataFrame
        res = self.getResult()
        if comp == False:
            for i in range(len(res)):
                if isinstance(res[i], DataFrame):
                    field = self.getField()
                    st.title('Produced volumes: ' + field[i])
                    display.multi_plot([res[i]], addAll= False)
        else:
            dfs = []
            for df in self.__state.result:
                reset_ind_df = df.reset_index(drop = True)
                dfs.append(reset_ind_df)
            display.multi_plot(dfs, addAll=False)

    def clear_output(self):
        from Data.Storage.Cache import SessionState
        SessionState.delete(id = self.__session_id)
        self.__state = SessionState.get(id=self.__session_id, result=[], field=[], time_frame = [])
    

    def getResult(self) -> list:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'result', [])

    def get_time_frame(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'time_frame', pd.DataFrame())
    
    def getField(self) -> pd.DataFrame:
        session_state = self.__state.get(self.__session_id)
        return getattr(session_state, 'field', pd.DataFrame())

    def getState(self) -> SessionState:
        session_state = self.__state.get(self.__session_id)
        return session_state
    
    def append_time_frame(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'time_frame', value = item)

    def append_result(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'result', value = item)
    
    def append_field(self, item) -> str:
        SessionState.append(id = self.__session_id, key = 'field', value = item)
        
class PolygonPlotter:
    def __init__(self, wkt_str):
        self.wkt_str = wkt_str
        self.fig = self.plot()

    def plot(self):
        multipolygon = loads(self.wkt_str)
        traces = [
            go.Scatter(
                x=list(polygon.exterior.xy[0]),
                y=list(polygon.exterior.xy[1]),
                mode = 'lines',
                fill='toself',
                fillcolor='red',
                line=dict(color='white', width=1),
                name='Reservoir'
            ) for polygon in multipolygon.geoms
        ]

        fig = go.Figure(traces)
        fig.update_layout(
            height=800,
            width=800,
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            showlegend=True,
            paper_bgcolor='black',
            plot_bgcolor='black'
        )

        return fig

def wlb_plot_production(fig, df, field):
    # Extract latitude and longitude from the WKT coordinates
    df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.extract(r'POINT \((\d+\.\d+) (\d+\.\d+)\)').astype(float)

    # Create a scatter trace
    scatter_trace = go.Scatter(
        x=df['Longitude'],
        y=df['Latitude'],
        text=df['wlbWellboreName'],  # Use the 'wlbWellboreName' column for text labels
        mode='markers', #+text
        name = "Production wells",
        marker=dict(size=10, color='white', symbol='circle'))

    # Add the scatter trace to the provided figure
    fig.add_trace(scatter_trace)

    # Update layout properties (optional)
    fig.update_layout(
        title='Reservoir and well locations ' + str(field),
        xaxis_title='Longitude',
        yaxis_title='Latitude',
    )

    return fig

def wlb_plot_injection(fig, df, field):
    # Extract latitude and longitude from the WKT coordinates
    df[['Longitude', 'Latitude']] = df['wlbPointGeometryWKT'].str.extract(r'POINT \((\d+\.\d+) (\d+\.\d+)\)').astype(float)

    # Create a scatter trace
    scatter_trace = go.Scatter(
        x=df['Longitude'],
        y=df['Latitude'],
        text=df['wlbWellboreName'],  # Use the 'wlbWellboreName' column for text labels
        mode='markers', #+text
        name = "Injection wells",
        #hoverinfo=df['wlbContentPlanned'],
        marker=dict(size=10, color='blue', symbol='circle'),
    )

    # Add the scatter trace to the provided figure
    fig.add_trace(scatter_trace)

    # Update layout properties (optional)
    fig.update_layout(
        title='Reservoir and well locations ' + str(field),
        xaxis_title='Longitude',
        yaxis_title='Latitude',
    )

    return fig
    
def makePlot(field):
    fig = go.Figure()
    import Data.getData as get
    wkt_str = get.polygon_coordinates(field)
    polygon_plotter = PolygonPlotter(wkt_str)
    col1, col2, col3, col4 = st.columns(4)

    with col2:
        updated_fig = wlb_plot_production(polygon_plotter.fig, get.producing_wlb(field), field)
        updated_fig = wlb_plot_injection(polygon_plotter.fig, get.injecting_wlb(field), field)   
        st.plotly_chart(updated_fig)
   