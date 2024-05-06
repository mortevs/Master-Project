import pandas as pd, plotly.graph_objects as go, streamlit as st
from datetime import datetime
def multi_plot_PR(dfs, addAll = True, addProduced = False, time_frame = "Yearly"):
    if time_frame == "Monthly":
        date_format = '%m:%Y'
        period = "M"
    else:
        date_format = '%Y'
        period = "Y"

    fig = go.Figure()
    axis_titles = {
        'Estimated Reservoir Pressure [bara]': ('Date', 'Bara'),
        'Cumulative Produced Gas [Sm3]': ('Date', 'Sm3'),
        'GasSm3Yearly': ('Date', 'Sm3'),
        'NGLSm3Yearly': ('Date', 'Sm3'),
        'OilSm3Yearly': ('Date', 'Sm3'),
        'CondensateSm3Yearly': ('Date', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Date', 'Sm3'),
        'WaterSm3Yearly': ('Date', 'Sm3'),
        'GasSm3Monthly': ('Date', 'Sm3'),
        'NGLSm3Monthly': ('Date', 'Sm3'),
        'OilSm3Monthly': ('Date', 'Sm3'),
        'CondensateSm3Monthly': ('Date', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Date', 'Sm3'),
        'WaterSm3Monthly': ('Date', 'Sm3'),
        'Produced Gas [Sm3]': ('Date', 'Sm3'),
        'Watercut': ('Date', '%'),
    }

    columns_to_plot = []
    columns_set = set() 

    for df in dfs:
        if addProduced:
            columns_to_add = ['Field Rates [Sm3/d]', 'GasSm3perDay']
            for column in columns_to_add:
                if column not in columns_set:
                    columns_to_plot.append(column)
                    columns_set.add(column)
            all_label = 'Estimated vs Actual Produced Rates'
        else:
            for column in df.columns:
                if column not in columns_set:
                    columns_to_plot.append(column)
                    columns_set.add(column)
            all_label = 'All'
        try:
            for column in columns_to_plot:
                fig.add_trace(
                    go.Scatter(
                        x = pd.to_datetime(df.index, format=date_format).to_period(period).to_timestamp(period),
                        y = df[column],
                        name = column,
                        mode = 'lines',
                        visible = 'legendonly' if not addAll and column != df.columns[0] else True  # Change visibility here
                    )
                )
        except Exception as e:
            try:
                for column in columns_to_plot:
                    fig.add_trace(
                        go.Scatter(
                            x = df.index,
                            y = df[column],
                            name = column,
                            mode = 'lines',
                            visible = 'legendonly' if not addAll and column != df.columns[0] else True  # Change visibility here
                        )
                    )
            except Exception:
                st.error("The data format on the uploaded data should be ")
                

    button_all = dict(label = all_label,
                    method = 'update',
                    args = [{'visible': [True]*len(columns_to_plot),
                            'title': all_label,
                            'showlegend':True}])

    def create_layout_button(column):
        return dict(label=column,
                    method='update',
                    args=[{'visible': [column == col for col in columns_to_plot],
                           'title': column,
                           'showlegend': True},
                          {'xaxis': {'title': axis_titles[column][0]}, 'yaxis': {'title': axis_titles[column][1]}}])

    all_buttons = ([button_all] * addAll) + [create_layout_button(column) for column in columns_to_plot]

    # Add buttons for all columns in the dataframe
    all_buttons += [create_layout_button(column) for column in df.columns if column not in columns_to_plot]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0 if addAll else columns_to_plot.index(columns_to_plot[0]),  # Change active button here
            buttons = all_buttons
            )
        ],
        showlegend=addAll,  # Change showlegend here
        xaxis_title="Date",  # X-axis title
        yaxis_title="Pressure [bara]"  # Y-axis title
    )

    # Update remaining layout properties
    fig.update_layout(
        height=450,
    
    )
    st.plotly_chart(fig, use_container_width=True)
def multi_plot(dfs, addAll=True, addProduced=False, num=None, comp = False):
    fig = go.Figure()
    axis_titles = {
        'Field Rates [Sm3/d]': ('Year', 'Sm3/d'),
        'Yearly Gas Offtake [Sm3]': ('Year', 'Sm3'),
        'Cumulative Gas Offtake [Sm3]': ('Year', 'Sm3'),
        'Recovery Factor': ('Year', 'Recovery Factor'),
        'Z-factor': ('Year', 'Z-factor'),
        'Reservoir Pressure [bara]': ('Year', 'Bara'),
        'Rates per Well [Sm3/d]': ('Year', '[Sm3/d]'),
        'Bottomhole Pressure [bara]': ('Year', 'Bara'),
        'Wellhead Pressure [bara]': ('Year', 'Bara'),
        'Template Pressure [bara]': ('Year', 'Bara'),
        'Pressure Pipeline Entry Module [bara]': ('Year', 'Bara'),
        'Seperator Pressure [bara]': ('Year', 'Bara'),
        'Rates per Template [Sm3/d]': ('Year', 'Sm3/d'),
        'Choke Pressure [bara]': ('Year', 'Bara'),
        'Ratio PTemp to PWellHead': ('Year', 'Ratio'),
        'Production Potential Rates [Sm3/d]': ('Year', 'Sm3/d'),
        'QFieldTarget [Sm3/d]': ('Year', 'Sm3/d'),
        'QWellTarget [Sm3/d]': ('Year', 'Sm3/d'),
        'Minimum Bottomhole Pressure [bara]': ('Year', 'Bara'),
        'Potential Rates per Well [Sm3/d]': ('Year', 'Sm3/d'),
        'Potential Field Rates [Sm3/d]': ('Year', 'Sm3/d'),
        'Well Production Rates [Sm3/d]': ('Year', 'Sm3/d'),
        'GasSm3perDay': ('Year', 'Sm3/d'),
        'NGLSm3perDay': ('Year', 'Sm3/d'),
        'OilSm3perDay': ('Year', 'Sm3/d'),
        'CondensateSm3perDay': ('Year', 'Sm3/d'), 
        'OilEquivalentsSm3perDay': ('Year', 'Sm3/d'),  
        'WaterSm3perDay': ('Year', 'Sm3/d'),
        #'GasSm3Yearly': ('Year', 'Sm3'),
        #'NGLSm3Yearly': ('Year', 'Sm3'),
        #'OilSm3Yearly': ('Year', 'Sm3'),
        #'CondensateSm3Yearly': ('Year', 'Sm3'),
        #'OilEquivalentsSm3Yearly': ('Year', 'Sm3'),
        #'WaterSm3Yearly': ('Year', 'Sm3'),
        #'GasSm3Monthly': ('Month:Year', 'Sm3'),
        #'NGLSm3Monthly': ('Month:Year', 'Sm3'),
        #'OilSm3Monthly': ('Month:Year', 'Sm3'),
        #'CondensateSm3Monthly': ('Month:Year', 'Sm3'),
        #'OilEquivalentsSm3Monthly': ('Month:Year', 'Sm3'),
        #'WaterSm3Monthly': ('Month:Year', 'Sm3'),
    }

    columns_to_plot = []
    columns_set = set() 

    for i in range(len(dfs)):
        df = dfs[i]
        if comp == True:
            num = i+1
        if addProduced:
            columns_to_add = ['Field Rates [Sm3/d]', 'GasSm3perDay']
            for column in columns_to_add:
                if column not in columns_set:
                    columns_to_plot.append(column)
                    columns_set.add(column)
            all_label = 'Estimated vs Actual Produced Rates'
        else:
            for column in df.columns:
                if column not in columns_set:
                    columns_to_plot.append(column)
                    columns_set.add(column)
            all_label = 'All'
        try:
            for column in columns_to_plot:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[column],
                        #name=column,
                        mode = 'lines',
                        name = f"Production Profile {num} - {column}",
                        showlegend=True,
                        visible='legendonly' if not addAll and column != df.columns[0] else True  # Change visibility here
                    )
                )
        except KeyError as e:
            st.warning("Due to name differences, not all columns can be compared in the same plot")

    button_all = dict(label=all_label,
                      method='update',
                      args=[{'visible': [True] * len(columns_to_plot),
                             'title': all_label,
                             'showlegend': True}])

    def create_layout_button(column):
        return dict(label=column,
                    method='update',
                    args=[{'visible': [column == col for col in columns_to_plot],
                           'title': column,
                           'showlegend': True},
                          {'xaxis': {'title': axis_titles[column][0]}, 'yaxis': {'title': axis_titles[column][1]}}])

    all_buttons = ([button_all] * addAll) + [create_layout_button(column) for column in columns_to_plot]

    # Add buttons for all columns in the dataframe
    all_buttons += [create_layout_button(column) for column in df.columns if column not in columns_to_plot]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0 if addAll else columns_to_plot.index(columns_to_plot[0]),  # Change active button here
            buttons=all_buttons
        )
        ],
        showlegend=True,  # Change showlegend here
        xaxis_title="Year",  # X-axis title
        yaxis_title="Sm3/d",  # Y-axis title
        height=450,
        
    )
    # Modify legend entries for the initially active option
    active_column = list(columns_to_plot)[0]
    for trace in fig.data:
        if active_column not in trace.name:
            trace.showlegend = False
    st.plotly_chart(fig, use_container_width=True)
def multi_plot_SODIR(dfs, time_frame):
    if time_frame == "Monthly":
        date_format = '%m:%Y'
        period = "M"
    else:
        date_format = '%Y'
        period = "Y"
    fig = go.Figure()
    axis_titles = {
        'GasSm3Yearly': ('Date', 'Sm3'),
        'NGLSm3Yearly': ('Date', 'Sm3'),
        'OilSm3Yearly': ('Date', 'Sm3'),
        'CondensateSm3Yearly': ('Date', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Date', 'Sm3'),
        'WaterSm3Yearly': ('Date', 'Sm3'),
        'GasSm3Monthly': ('Date', 'Sm3'),
        'NGLSm3Monthly': ('Date', 'Sm3'),
        'OilSm3Monthly': ('Date', 'Sm3'),
        'CondensateSm3Monthly': ('Date', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Date', 'Sm3'),
        'WaterSm3Monthly': ('Date', 'Sm3'),
        'Watercut': ('Date', '%'),        
        'GasSm3YearlyCumulative': ('Date', 'Sm3'),
        'NGLSm3YearlyCumulative': ('Date', 'Sm3'),
        'OilSm3YearlyCumulative': ('Date', 'Sm3'),
        'CondensateSm3YearlyCumulative': ('Date', 'Sm3'),
        'OilEquivalentsSm3YearlyCumulative': ('Date', 'Sm3'),
        'WaterSm3YearlyCumulative': ('Date', 'Sm3'),
        'GasSm3MonthlyCumulative': ('Date', 'Sm3'),
        'NGLSm3MonthlyCumulative': ('Date', 'Sm3'),
        'OilSm3MonthlyCumulative': ('Date', 'Sm3'),
        'CondensateSm3MonthlyCumulative': ('Date', 'Sm3'),
        'OilEquivalentsSm3MonthlyCumulative': ('Date', 'Sm3'),
        'WaterSm3MonthlyCumulative': ('Date', 'Sm3'),

    }
    columns_to_plot = []
    columns_set = set()

    for i in range(len(dfs)):
        df = dfs[i]
        if time_frame == "Monthly":
            date_format = '%m:%Y'
        else:
            date_format = '%Y'

        for column in df.columns:
            if column not in columns_set:
                columns_set.add(column)
                columns_to_plot.append(column)
        try:
            for column in columns_to_plot:
                fig.add_trace(
                    go.Scatter(
                        x = pd.to_datetime(df.index, format=date_format).to_period(period).to_timestamp(period),
                        y=df[column],
                        visible='legendonly' if column != df.columns[0] else True,
                        showlegend=False,
                        mode = 'lines'
                    )
                )
        except KeyError:
            st.error("Can not compare yearly and monthly time frame. ")
    
    def create_layout_button(column):
        return dict(label=column,
                    method='update',
                    args=[{'visible': [column == col for col in columns_to_plot],
                           'title': column,
                           'showlegend': False},
                          {'xaxis': {'title': axis_titles[column][0]}, 'yaxis': {'title': axis_titles[column][1]}}])

    all_buttons = [create_layout_button(column) for column in columns_to_plot]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,  # Change active button here
            buttons=all_buttons
        )
        ],
        xaxis_title="Date",  # X-axis title
        yaxis_title="Sm3",  # Y-axis title
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)
def multi_plot_SODIR_compare(dfs, fields, res, comp_align, time_frame):
    if time_frame == "Monthly":
        date_format = '%m:%Y'
        period = "M"
    else:
        date_format = '%Y'
        period = "Y"

    fig = go.Figure()
    columns_to_plot = []
    axis_titles = {
        'GasSm3Yearly': ('Date', 'Sm3'),
        'NGLSm3Yearly': ('Date', 'Sm3'),
        'OilSm3Yearly': ('Date', 'Sm3'),
        'CondensateSm3Yearly': ('Date', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Date', 'Sm3'),
        'WaterSm3Yearly': ('Date', 'Sm3'),
        'GasSm3Monthly': ('Date', 'Sm3'),
        'NGLSm3Monthly': ('Date', 'Sm3'),
        'OilSm3Monthly': ('Date', 'Sm3'),
        'CondensateSm3Monthly': ('Date', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Date', 'Sm3'),
        'WaterSm3Monthly': ('Date', 'Sm3'),
        'Watercut': ('Date', '%'),
        'GasSm3YearlyCumulative': ('Date', 'Sm3'),
        'NGLSm3YearlyCumulative': ('Date', 'Sm3'),
        'OilSm3YearlyCumulative': ('Date', 'Sm3'),
        'CondensateSm3YearlyCumulative': ('Date', 'Sm3'),
        'OilEquivalentsSm3YearlyCumulative': ('Date', 'Sm3'),
        'WaterSm3YearlyCumulative': ('Date', 'Sm3'),
        'GasSm3MonthlyCumulative': ('Date', 'Sm3'),
        'NGLSm3MonthlyCumulative': ('Date', 'Sm3'),
        'OilSm3MonthlyCumulative': ('Date', 'Sm3'),
        'CondensateSm3MonthlyCumulative': ('Date', 'Sm3'),
        'OilEquivalentsSm3MonthlyCumulative': ('Date', 'Sm3'),
        'WaterSm3MonthlyCumulative': ('Date', 'Sm3'),
    }
    columns_to_plot = []
    columns_set = set()
    if comp_align == "Compare by dates":
        for i in range(len(res)):
            df = res[i]
            for column in df.columns:
                if column not in columns_set:
                    columns_to_plot.append(column)
                    columns_set.add(column)
            try:
                for column in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x = pd.to_datetime(df.index, format=date_format).to_period(period).to_timestamp(period),
                            y=df[column],
                            mode = 'lines',
                            name = f"{fields[i]} - {column}",
                            visible='legendonly' if column != df.columns[0] else True,
                            showlegend=True,
                        )
                    )
            except KeyError:
                st.error("Cannot compare fields")
    else:
        for i in range(len(dfs)):
            df = dfs[i]
            for column in df.columns:
                if column not in columns_set:
                    columns_to_plot.append(column)
                    columns_set.add(column)
            try:
                for column in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df[column],
                            name = f"{fields[i]} - {column}",
                            visible='legendonly' if column != df.columns[0] else True,
                            showlegend=True,
                            mode = 'lines'
                        )
                    )
            except KeyError:
                st.error("Cannot compare yearly and monthly time frames.")

    
    def create_layout_button(column):
        # Define the function to create a button
        return dict(
            label=column,
            method='update',
            args=[
                {
                    # Check each trace name and determine visibility based on the column name
                    'visible': [trace.name.split(' - ')[1] == column for trace in fig.data],
                    'title': column,
                    'showlegend': True
                },
                {
                    'xaxis': {'title': axis_titles[column][0]},
                    'yaxis': {'title': axis_titles[column][1]}
                }
            ]
        )

    all_buttons = [create_layout_button(column) for column in columns_to_plot]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,  # Change active button here
            buttons=all_buttons)],
        xaxis_title="Date",  
        yaxis_title="Sm3", 
        height=450,
        showlegend=True  
    )
    active_column = list(columns_to_plot)[0]
    for trace in fig.data:
        if trace.name.split(' - ')[1] != active_column:
            trace.showlegend = False

    st.plotly_chart(fig, use_container_width=True)

def display_FD_variables_table(list1, list2, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, use_container_width=True, height=213, hide_index=True)
        return edited_df['Value'].to_list()
    else:
        st.table(df_table)
def display_FD_variables_table2(list2):
    def make_pretty(styler):
        styler.set_properties(**{'color': 'red'})
        return styler
    list1 = ['Target Rate [Sm3/d]', 'Initial Reservoir Pressure [bara]', 'Rate of Abandonment [Sm3/d]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Inflow backpressure coefficient', 'Inflow backpressure exponent', 'Number of Templates', 'Number of Wells per Template', 'Uptime [days]', 'Tubing Flow Coefficient', 'Tubing Elevation Coefficient', 'Flowline Coefficient from Template-PLEM', 'Pipeline coefficient from PLEM-Shore', 'Seperator Pressure [bara]', 'Initial Gas in Place [sm3]', 'Build-up period [years]']
    pd.set_option('display.float_format', '{:.0f}'.format)
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })
    df_table['Value'] = df_table['Value'].astype(str)
    pd.set_option("display.max_rows", 2)
    st.dataframe(df_table.style.pipe(make_pretty), hide_index=True, use_container_width=True, height=633)
def display_table_RESPRES(list1, list2, edible = False, clear_table = False) ->list:
    # Create a DataFrame from the two lists
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })

    if edible:
        edited_df = st.data_editor(df_table, key='df_table_editor', use_container_width=True, height=175, hide_index=True)
        return edited_df['Value'].to_list()

def display_table_NPV(list1, list2, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2,
    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, use_container_width=True, hide_index=True)
        return edited_df['Value'].to_list()
    else:
        st.table(df_table)

def display_table_grid_search(f_variables=None, key = 'df_table_editor'):
    from Data.DefaultData import default_Optimization_table
    list1,list2,list3,list4 = default_Optimization_table(f_variables)
    df_table = pd.DataFrame({
        'Input': list1,
        'Min': list2,
        'Max': list3,
        'Steps': list4

    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df

def display_table_Monte_Carlo(Variables = None):    
    from Data.DefaultData import default_MC
    list1, list2, list3 = default_MC()
    df_table = pd.DataFrame({
        'Input': list1,
        'Min': list2,
        'Max': list3,
    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df

def display_table_Monte_Carlo_param():    
    from Data.DefaultData import default_MC_params
    list1, list2 = default_MC_params()
    df_table = pd.DataFrame({
        'Parameter': list1,
        'Value': list2,

    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df['Value']

def display_table_Monte_Carlo_SA():    
    from Data.DefaultData import default_MC_SA, probability_distributions
    list1, list2, list3, list4 = default_MC_SA()
    p_dists = probability_distributions()

    
    df_table = pd.DataFrame({
        'Input': list1,
        'Min': list2,
        'ML': list3,
        'Max': list4,
        'Distribution' : [p_dists[0] for el in list1]
    })
    
    edited_df = st.data_editor(
        df_table, hide_index=True, use_container_width=True, 
        column_config={"Distribution": st.column_config.SelectboxColumn(
                label ="Probability distribution",
                help="The probability distribution of the variable",
                width="medium",
                options=p_dists,
                required=True)})

    return edited_df


def validate_MC_SA(edited_MC_table):
    #needs implementation
    pass
# class edible_df():
#     def __init__(self, list2):
#         self.df = self.initialize_table(list2)
#     def initialize_table(self, list2):
#         list1 = ['Initial Reservoir Pressure [bara]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Initial Gas in Place [sm3]']
#         self.df_table = pd.DataFrame({
#             'Input': list1,
#             'Value': list2
#         })
#         edited_df = st.data_editor(self.df_table, key='df_table_editor', width=790, height=175, hide_index=True)
#         return edited_df
#     def update_table(self, new_values):
#         self.df_table['Value'] = new_values
#         return st.data_editor(self.df_table, key='df_table_editor__', width=790, height=175, hide_index=True)
    
#     def get_parameters(self):
#         return self.df_table['Value'].to_list()
        
def dropdown(label:str = ' ', options: list = None, index:int = 0, labelVisibility: str ='collapsed') ->str:
    selected_option = st.selectbox(label, options, index, label_visibility=labelVisibility)
    return selected_option

def columnDisplay(list1:list):
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_option1 = dropdown(options = list1[0])

    with col2:
        selected_option2 = dropdown(options = list1[1])

    with col3:
        selected_option3 = dropdown(options = list1[2])
    return selected_option1, selected_option2, selected_option3

def columnDisplay2(list1:list):
    col1, col2 = st.columns(2)

    with col1:
        selected_option1 = dropdown(options = list1[0])

    with col2:
        selected_option2 = dropdown(options = list1[1])

    return selected_option1, selected_option2

def columnDisplay1(list1:list):
    col1 = st.columns(2)

    with col1:
        selected_option1 = dropdown(options = list1)

    return selected_option1

def tornadoPlotSensitivity(NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax):
    gas_price_sensitivity = NPVgaspricemax - NPVgaspricemin
    LNG_plant_sensitivity = LNGPlantMin-LNGPlantMax 
    IGIP_sensitivity = NPV_IGIPmax - NPV_IGIPmin

    sensitivities = [gas_price_sensitivity, LNG_plant_sensitivity, IGIP_sensitivity]
    labels = ['Gas Price [USD/Sm3]', 'LNG Plant [USD/Sm3/d]', 'IGIP [Sm3]']
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=labels,
            x=sensitivities,
            orientation='h',  # horizontal bars
            marker=dict(
                color=['blue', 'orange', 'red'],
                opacity=0.7
            )
        )
    )

    # Add plot title and labels
    fig.update_layout(
        title='Tornado Plot of NPV Sensitivity',
        xaxis_title='NPV [1E6 USD]',
        yaxis_title='Variable',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

import plotly.graph_objects as go
import streamlit as st

def tornadoPlot(initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax):
    # Variable labels
    labels = ['Gas Price [USD/Sm3]', 'LNG Plant [USD/Sm3/d]', 'IGIP [Sm3]']
    
    
    min_values = [NPVgaspricemin, LNGPlantMax, NPV_IGIPmin]
    max_values = [NPVgaspricemax, LNGPlantMin, NPV_IGIPmax]
    
    # Create the plot
    fig = go.Figure()
    
    # Add left bars (from initial NPV to min values)
    for i, label in enumerate(labels):
        fig.add_trace(
            go.Bar(
                y=[label],
                x=[-abs(initial_NPV - min_values[i])],
                orientation='h',
                base=initial_NPV,
                marker=dict(
                    color='red',
                    opacity=0.7
                ),
                name=f'Min {label}',
                showlegend=False
            )
        )
    
    # Add right bars (from initial NPV to max values)
    for i, label in enumerate(labels):
        fig.add_trace(
            go.Bar(
                y=[label],
                x=[abs(max_values[i] - initial_NPV)],
                orientation='h',
                base=initial_NPV,
                marker=dict(
                    color='green',
                    opacity=0.7
                ),
                name=f'Max {label}',
                showlegend=False
            )
        )
    
    # Add vertical line at x = initial NPV
    fig.add_shape(
        type="line",
        x0=initial_NPV,
        x1=initial_NPV,
        y0=-0.5,
        y1=len(labels) - 0.5,
        line=dict(
            color="black",
            width=2
        )
    )
    
    # Update layout
    fig.update_layout(
        title='Tornado Plot of NPV Min and Max Values',
        xaxis_title='NPV [1E6 USD]',
        yaxis_title='Variable',
        barmode='overlay',
        showlegend=True
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

# Example usage:
# initial_NPV = 500, NPVgaspricemin = 400, NPVgaspricemax = 600
# LNGPlantMin = 350, LNGPlantMax = 650, NPV_IGIPmin = 450, NPV_IGIPmax = 700
# tornadoPlot(initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax)
