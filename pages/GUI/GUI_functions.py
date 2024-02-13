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

def display_table(list1, list2, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, width=750, height=596, hide_index=True)
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

def display_table_NPV(list1, list2, edible=False, key = 'df_table_editor'):
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })
    if edible:
        edited_df = st.data_editor(df_table, key=key, width=750, height=196, hide_index=True)
        return edited_df['Value'].to_list()
    else:
        st.table(df_table)

from Modules.FIELD_DEVELOPMENT.run_Analysis import NPVAnalysis

class NPV_sheet(NPVAnalysis):
    def __init__(self, parent, Analysis, opt, user_input, key):
        self.parent = parent
        self.__Analysis = Analysis
        self.__opt = opt
        self.__production_profile = Analysis.get_production_profile(opt = opt)
        self.__NPV_variables = user_input[0]
        self.__CAPEX = user_input[1]
        self.__OPEX = user_input[2]
        self.__sheet = self.display_table_NPV_Sheet(key)
 

    def display_table_NPV_Sheet(self, key):
        param = (self.__Analysis.getParameters())[self.__opt-1]
        N_temp = param[7]
        N_Wells_per_Temp = param[8]
        from Data.ManualData import default_well_template_distribution
        self.__end_prod = len(self.__production_profile)
        well, templ = default_well_template_distribution(N_temp, N_Wells_per_Temp, self.__end_prod)
        self.__Gas_Price = self.__NPV_variables[0]
        self.__Discount_Rate = self.__NPV_variables[1]
        self.__Well_Cost = self.__CAPEX[0]
        self.__p_u = self.__CAPEX[1]
        p_u_list = [self.__p_u]
        for i in range(1, self.__end_prod):
            p_u_list.append(0)

        self.__Mani = self.__CAPEX[2]

        self.__OPEX = self.__OPEX[0]
        self.__DRILLEX =[element * self.__Well_Cost for element in well]

        
        stop_prod = len(self.__production_profile)
        years = []
        for i in range(stop_prod):
            years.append(i)            
        df_table = pd.DataFrame({
            'End of year': years,
            'Nr Wells': well,
            'DRILLEX': self.__DRILLEX,
            'Pipeline & Umbilicals': p_u_list,
            'Manifold & Compressors': [element * self.__Mani for element in templ],
            'Other': [0 for element in well],
            'TOTAL CAPEX': years,
            'Yearly gas offtake': self.__production_profile,
            'Revenues': years,
            'OPEX': [self.__OPEX for element in well],
            'Cash Flow': years,
            'Discounted Cash Flow': years,
            'NPV': years,
        })
        edited_df = st.data_editor(df_table, key=key, width=4000, height=500, hide_index=True)
        return edited_df['Nr Wells'].to_list(), edited_df['DRILLEX'].to_list()

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