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
        width=1000
    
    )
    st.plotly_chart(fig)

def display_FD_variables_table(list1, list2, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, width=750, height=632, hide_index=True)
        return edited_df['Value'].to_list()
    else:
        st.table(df_table)

def display_table_RESPRES(list1, list2, edible = False, clear_table = False) ->list:
    # Create a DataFrame from the two lists
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })

    if edible:
        edited_df = st.data_editor(df_table, key='df_table_editor', width=790, height=175, hide_index=True)
        return edited_df['Value'].to_list()

def display_table_NPV(list1, list2, list3, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2,
        'Unit': list3
    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, hide_index=True)
        return edited_df['Value'].to_list()
    else:
        st.table(df_table)

def display_table_grid_search(list1, list2, list3, list4, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Min': list2,
        'Max': list3,
        'Steps': list4

    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, hide_index=True)
        return edited_df['Steps'].to_list()
    else:
        st.table(df_table)
class edible_df():
    def __init__(self, list2):
        self.df = self.initialize_table(list2)
    def initialize_table(self, list2):
        list1 = ['Initial Reservoir Pressure [bara]', 'Reservoir Temperature [degree C]', 'Gas Molecular Weight [g/mol]', 'Initial Gas in Place [sm3]']
        self.df_table = pd.DataFrame({
            'Input': list1,
            'Value': list2
        })
        edited_df = st.data_editor(self.df_table, key='df_table_editor', width=790, height=175, hide_index=True)
        return edited_df
    def update_table(self, new_values):
        self.df_table['Value'] = new_values
        return st.data_editor(self.df_table, key='df_table_editor__', width=790, height=175, hide_index=True)
    
    def get_parameters(self):
        return self.df_table['Value'].to_list()
        
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