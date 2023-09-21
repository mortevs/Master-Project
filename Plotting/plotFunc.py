import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def multi_plot(df, title, addAll = True):
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
        title_text=title,
        height=800,
        width=1300
    
    )

    st.plotly_chart(fig)
def display_table(list1, list2):
    # Create a DataFrame from the two lists
    df_table = pd.DataFrame({
        'Column1': list1,
        'Column2': list2
    })

    # Display the DataFrame as a table in the sidebar
    st.sidebar.table(df_table)