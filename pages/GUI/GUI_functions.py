import pandas as pd, plotly.graph_objects as go, streamlit as st
def multi_plot_PR(dfs, addAll = True, addProduced = False):
    fig = go.Figure()
    columns_to_plot = []

    for df in dfs:
        if addProduced:
            columns_to_plot += ['Field rates [sm3/d]', 'gasSM3perday']
            all_label = 'Estimated vs Actual produced rates'
        else:
            columns_to_plot += df.columns.to_list()
            all_label = 'All'

        for column in columns_to_plot:
            fig.add_trace(
                go.Scatter(
                    x = df.index,
                    y = df[column],
                    name = column,
                    visible = 'legendonly' if not addAll and column != df.columns[0] else True  # Change visibility here
                )
            )

    button_all = dict(label = all_label,
                    method = 'update',
                    args = [{'visible': [True]*len(columns_to_plot),
                            'title': all_label,
                            'showlegend':True}])

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'visible': [column == col for col in columns_to_plot],
                            'title': column,
                            'showlegend': True}])

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
        height=600,
        width=1000
    
    )
    st.plotly_chart(fig)

def multi_plot(dfs, addAll = True, addProduced = False):
    fig = go.Figure()
    columns_to_plot = []

    for df in dfs:
        if addProduced:
            columns_to_plot += ['Field rates [sm3/d]', 'gasSM3perday']
            all_label = 'Estimated vs Actual produced rates'
        else:
            columns_to_plot += df.columns.to_list()
            all_label = 'All'

        for column in columns_to_plot:
            fig.add_trace(
                go.Scatter(
                    x = df.index,
                    y = df[column],
                    name = column,
                    visible = 'legendonly' if not addAll and column != df.columns[0] else True  # Change visibility here
                )
            )

    button_all = dict(label = all_label,
                    method = 'update',
                    args = [{'visible': [True]*len(columns_to_plot),
                            'title': all_label,
                            'showlegend':True}])

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'visible': [column == col for col in columns_to_plot],
                            'title': column,
                            'showlegend': True}])

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
        xaxis_title="Year",  # X-axis title
        yaxis_title="Cubic meter"  # Y-axis title
    )

    # Update remaining layout properties
    fig.update_layout(
        height=600,    
    )
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