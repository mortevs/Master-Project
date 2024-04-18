import pandas as pd, plotly.graph_objects as go, streamlit as st
def multi_plot_PR(dfs, addAll = True, addProduced = False):
    fig = go.Figure()
    axis_titles = {
        'Estimated Reservoir Pressure [bara]': ('Year', 'Bara'),
        'Cumulative Produced Gas [Sm3]': ('Year', 'Sm3'),
        'GasSm3Yearly': ('Year', 'Sm3'),
        'NGLSm3Yearly': ('Year', 'Sm3'),
        'OilSm3Yearly': ('Year', 'Sm3'),
        'CondensateSm3Yearly': ('Year', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Year', 'Sm3'),
        'WaterSm3Yearly': ('Year', 'Sm3'),
        'GasSm3Monthly': ('Month:Year', 'Sm3'),
        'NGLSm3Monthly': ('Month:Year', 'Sm3'),
        'OilSm3Monthly': ('Month:Year', 'Sm3'),
        'CondensateSm3Monthly': ('Month:Year', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Month:Year', 'Sm3'),
        'WaterSm3Monthly': ('Month:Year', 'Sm3'),
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
        xaxis_title="Time",  # X-axis title
        yaxis_title="Pressure [bara]"  # Y-axis title
    )

    # Update remaining layout properties
    fig.update_layout(
        height=600,
    
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
        'GasSm3Yearly': ('Year', 'Sm3'),
        'NGLSm3Yearly': ('Year', 'Sm3'),
        'OilSm3Yearly': ('Year', 'Sm3'),
        'CondensateSm3Yearly': ('Year', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Year', 'Sm3'),
        'WaterSm3Yearly': ('Year', 'Sm3'),
        'GasSm3Monthly': ('Month:Year', 'Sm3'),
        'NGLSm3Monthly': ('Month:Year', 'Sm3'),
        'OilSm3Monthly': ('Month:Year', 'Sm3'),
        'CondensateSm3Monthly': ('Month:Year', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Month:Year', 'Sm3'),
        'WaterSm3Monthly': ('Month:Year', 'Sm3'),
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
        height=600,
        
    )
    # Modify legend entries for the initially active option
    active_column = list(columns_to_plot)[0]
    for trace in fig.data:
        if active_column not in trace.name:
            trace.showlegend = False
    st.plotly_chart(fig, use_container_width=True)


def multi_plot_SODIR(dfs):        
    fig = go.Figure()
    axis_titles = {
        'GasSm3Yearly': ('Year', 'Sm3'),
        'NGLSm3Yearly': ('Year', 'Sm3'),
        'OilSm3Yearly': ('Year', 'Sm3'),
        'CondensateSm3Yearly': ('Year', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Year', 'Sm3'),
        'WaterSm3Yearly': ('Year', 'Sm3'),
        'GasSm3Monthly': ('Month:Year', 'Sm3'),
        'NGLSm3Monthly': ('Month:Year', 'Sm3'),
        'OilSm3Monthly': ('Month:Year', 'Sm3'),
        'CondensateSm3Monthly': ('Month:Year', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Month:Year', 'Sm3'),
        'WaterSm3Monthly': ('Month:Year', 'Sm3'),
        'Watercut': ('Time', '%'),

    }
    columns_to_plot = []
    columns_set = set()

    for df in dfs:
        for column in df.columns:
            if column not in columns_set:
                columns_to_plot.append(column)
                columns_set.add(column)
        try:
            for column in columns_to_plot:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
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

    unique_columns = columns_to_plot[:7]
    all_buttons = [create_layout_button(column) for column in unique_columns]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,  # Change active button here
            buttons=all_buttons
        )
        ],
        xaxis_title="Time",  # X-axis title
        yaxis_title="Sm3",  # Y-axis title
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)



def multi_plot_SODIR_compare(dfs, fields, res, comp_align):        
    fig = go.Figure()
    columns_to_plot = []
    axis_titles = {
        'GasSm3Yearly': ('Year', 'Sm3'),
        'NGLSm3Yearly': ('Year', 'Sm3'),
        'OilSm3Yearly': ('Year', 'Sm3'),
        'CondensateSm3Yearly': ('Year', 'Sm3'),
        'OilEquivalentsSm3Yearly': ('Year', 'Sm3'),
        'WaterSm3Yearly': ('Year', 'Sm3'),
        'GasSm3Monthly': ('Month:Year', 'Sm3'),
        'NGLSm3Monthly': ('Month:Year', 'Sm3'),
        'OilSm3Monthly': ('Month:Year', 'Sm3'),
        'CondensateSm3Monthly': ('Month:Year', 'Sm3'),
        'OilEquivalentsSm3Monthly': ('Month:Year', 'Sm3'),
        'WaterSm3Monthly': ('Month:Year', 'Sm3'),
        'Watercut': ('Time', '%'),

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
                            x=pd.to_datetime(df.index, format='%m:%Y'), #format='mixed'
                            y=df[column],
                            mode = 'lines',
                            name = f"{fields[i]} - {column}",
                            visible='legendonly' if column != df.columns[0] else True,
                            showlegend=True,
                        )
                    )
            except Exception as e:
                try:
                    for column in df.columns:
                        fig.add_trace(
                            go.Scatter(
                                x=pd.to_datetime(df.index, format='%Y'), #format='mixed'
                                y=df[column],
                                mode = 'lines',
                                name = f"{fields[i]} - {column}",
                                visible='legendonly' if column != df.columns[0] else True,
                                showlegend=True,
                            )
                        )
                except KeyError:
                    st.error("Cannot compare yearly and monthly time frames.")
    else:
        for i in range(len(dfs)):
            df = dfs[i]
            columns_to_plot += df.columns.to_list()
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
        return dict(label=column,
                    method='update',
                    args=[{'visible': [column in trace.name for trace in fig.data],
                           'title': column,
                           'showlegend': True},
                          {'xaxis': {'title': axis_titles[column][0]}, 'yaxis': {'title': axis_titles[column][1]}}])

    all_buttons = [create_layout_button(column) for column in columns_to_plot]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,  # Change active button here
            buttons=all_buttons
        )
        ],
        xaxis_title="Time",  # X-axis title
        yaxis_title="Sm3",  # Y-axis title
        height=600,
        showlegend=True  # Ensure legend visibility
    )
    
    # Modify legend entries for the initially active option
    active_column = list(columns_to_plot)[0]
    for trace in fig.data:
        if active_column not in trace.name:
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
    #plataeu = f_variables[0]
    #nr_temps =f_variables[8]
    #pertemp = f_variables[0]
    list1 = ['Plateau rate [Sm3/d]', 'Nr Templates', 'Nr Wells per Template', 'Rate of Abandonment [Sm3/d]']
    list2 = [10000000,2,2, 1e6] 
    list3 = [40000000,5,5, None] 
    list4 = [4,4,4,None] 
    df_table = pd.DataFrame({
        'Input': list1,
        'Min': list2,
        'Max': list3,
        'Steps': list4

    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df

def display_table_Monte_Carlo(Variables = None):    
    list1 = ['Gas Price [USD/Sm3]', 'IGIP [Sm3]', 'OPEX [1E6 USD]']
    list2 = [0.05,250000000000, 100] 
    list3 = [1,300000000000, 300] 
    df_table = pd.DataFrame({
        'Input': list1,
        'Min': list2,
        'Max': list3,
    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df

def display_table_Monte_Carlo_param():    
    list1 = ['Nr of Random Numbers', 'Nr Bins']
    list2 = [1000000,50] 
    df_table = pd.DataFrame({
        'Parameter': list1,
        'Value': list2,
    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df['Value']

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