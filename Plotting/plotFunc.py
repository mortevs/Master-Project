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
                name = column
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
            active = 0,
            buttons = ([button_all] * addAll) + list(df.columns.map(lambda column: create_layout_button(column)))
            )
        ],
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

    # Display the DataFrame as a table in the sidebar
    st.sidebar.table(df_table)
def dropdown(options, index = 0)->str:
    selected_option = st.selectbox(' ', options, index, label_visibility='collapsed')
    return selected_option

def columnDisplay(list1:list, list2:list):
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_option1 = dropdown(list2[0])

    with col2:
        selected_option2 = dropdown(list2[1])

    with col3:
        selected_option3 = dropdown(list2[2])
    return selected_option1, selected_option2, selected_option3