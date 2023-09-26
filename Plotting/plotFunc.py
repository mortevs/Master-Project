import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def multi_plot(df, addAll = True):
    fig = go.Figure()

    for column in df.columns.to_list():
        fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[column],
                name = column,
                visible = True if column == df.columns[0] else 'legendonly'  # Change visibility here
            )
        )

    button_all = dict(label = 'All',
                      method = 'update',
                      args = [{'visible': [True]*len(df.columns),
                               'title': 'All',
                               'showlegend':True}])

    def create_layout_button(column):
        return dict(label = column,
                    method = 'update',
                    args = [{'visible': df.columns==column,
                             'title': column,
                             'showlegend': True}])

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active = 0 if addAll else df.columns.to_list().index(df.columns[0]),  # Change active button here
            buttons = ([button_all] * addAll) + list(df.columns.map(lambda column: create_layout_button(column)))
            )
        ],
        showlegend=addAll  # Change showlegend here
    )

    # Update remaining layout properties
    fig.update_layout(
        height=700,
        width=1200
    
    )
    st.plotly_chart(fig)

def display_table(list1, list2):
    # Create a DataFrame from the two lists
    df_table = pd.DataFrame({
        'Input': list1,
        'Value': list2
    })
    #edited_df = st.data_editor(df_table)

    #Display the DataFrame as a table in the sidebar
    #st.sidebar.table(edited_df)
    st.sidebar.table(df_table)

    row_to_edit = st.number_input('Row number of the input you want to edit:', min_value=0, max_value=len(df_table)-1)
        # Allow the user to enter new values
    new_value = st.number_input('Enter new value:')

    # Update the DataFrame if the user clicks the 'Update' button
    if st.button('Update'):
        df_table.loc[row_to_edit, 'Value'] = new_value
        # Display the updated DataFrame
        st.sidebar.table(df_table)
        

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