import pandas as pd, plotly.graph_objects as go, streamlit as st
import plotly.graph_objects as go
import numpy as np
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
                        visible = 'legendonly' if not addAll and column != df.columns[4] else True  # Change visibility here
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
                            visible = 'legendonly' if not addAll and column != df.columns[4] else True  # Change visibility here
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
            active = 4 if addAll else columns_to_plot.index(columns_to_plot[0]),  # Change active button here
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
def multi_plot(dfs, addAll=True, addProduced=False, num=None, comp=False):
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
        'WaterSm3perDay': ('Year', 'Sm3/d')
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
                        mode='lines',
                        name=f"Production Profile {num} - {column}",
                        showlegend=True,
                        visible='legendonly' if not addAll and column != columns_to_plot[0] else True  # Change visibility here
                    )
                )
        except KeyError as e:
            st.warning("Due to methodology differences, not all sub-calculations can be compared")

    button_all = dict(label=all_label,
                      method='update',
                      args=[{'visible': [True] * len(fig.data),
                             'title': all_label,
                             'showlegend': True}])

    def create_layout_button(column):
        visibility = [column in trace.name for trace in fig.data]
        return dict(label=column,
                    method='update',
                    args=[{'visible': visibility,
                           'title': column,
                           'showlegend': True},
                          {'xaxis': {'title': axis_titles[column][0]}, 'yaxis': {'title': axis_titles[column][1]}}])

    all_buttons = ([button_all] * addAll) + [create_layout_button(column) for column in columns_to_plot]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=4 if addAll else columns_to_plot.index(columns_to_plot[0]), 
            buttons=all_buttons
        )],
        showlegend=True, 
        xaxis_title="Year", 
        yaxis_title="Sm3/d",
        height=450
    )

    active_column = list(columns_to_plot)[0]
    for trace in fig.data:
        if active_column not in trace.name:
            trace.showlegend = False

    st.plotly_chart(fig, use_container_width=True)
def multi_plot_SODIR(dfs, time_frame):
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
        for column in df.columns:
            if column not in columns_set:
                columns_set.add(column)
                columns_to_plot.append(column)
        try:
            for column in columns_to_plot:
                fig.add_trace(
                    go.Scatter(
                        #x = pd.to_datetime(df.index, format=date_format).to_period(period).to_timestamp(period),
                        x = df.index,
                        y=df[column],
                        visible='legendonly' if column != df.columns[4] else True,
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
            active=4,  # Change active button here
            buttons=all_buttons
        )
        ],
        xaxis_title="Date",  # X-axis title
        yaxis_title="Sm3",  # Y-axis title
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)
def multi_plot_SODIR_compare(dfs, fields, res, comp_align, time_frame):
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
                            x = df.index,
                            y=df[column],
                            mode = 'lines',
                            name = f"{fields[i]} - {column}",
                            visible='legendonly' if column != df.columns[4] else True,
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
                            visible='legendonly' if column != df.columns[4] else True,
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
            active=4,  # Change active button here
            buttons=all_buttons)],
        xaxis_title="Date",  
        yaxis_title="Sm3", 
        height=450,
        showlegend=True  
    )
    active_column = list(columns_to_plot)[4]
    for trace in fig.data:
        if trace.name.split(' - ')[1] != active_column:
            trace.showlegend = False

    st.plotly_chart(fig, use_container_width=True)

def multi_plot_SODIR_forecast(fields, res, res_forecast, time_frame):
    if time_frame == "Monthly":
        pass
    else:
        res = [el[0:-1] for el in res] 


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

    # Plot res
    for i in range(len(res)):
        df = res[i]
        for column in df.columns:
            if column not in columns_to_plot:
                columns_to_plot.append(column)
        try:
            for column in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x = df.index,
                        y=df[column],
                        mode='lines',
                        name=f"{fields[i]} - {column}",
                        visible='legendonly' if column != df.columns[4] else True,
                        showlegend=True,
                    )
                )
        except KeyError:
            st.error("Can not compare fields")

    for i in range(len(res_forecast)):
        df = res_forecast[i]
        for column in df.columns:
            if column not in columns_to_plot:
                columns_to_plot.append(column)
        try:
            for column in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x = df.index,
                        y=df[column],
                        mode='lines',
                        name=f"{fields[i]} - {column} (Forecast)",
                        line=dict(color='red', dash = 'dash'),
                        visible='legendonly' if column != df.columns[4] else True,
                        showlegend=True,
                    )
                )
        except KeyError:
            st.error("Can not plot forecast fields")

    def create_layout_button(column):
        # Define the function to create a button
        return dict(
            label=column,
            method='update',
            args=[
                {
                    # Check each trace name and determine visibility based on the column name
                    'visible': [trace.name.split(' - ')[1] == column or trace.name.split(' - ')[1] == f"{column} (Forecast)" for trace in fig.data],
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
            active=4,  # Change active button here
            buttons=all_buttons)],
        xaxis_title="Date",  
        yaxis_title="Sm3", 
        height=450,
        showlegend=True  
    )
    active_column = list(columns_to_plot)[0]
    for trace in fig.data:
        if trace.name.split(' - ')[1] != active_column and trace.name.split(' - ')[1] != f"{active_column} (Forecast)":
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

def create_uncertainty_table(list1, list2,list3, list4, p_dists):
    df_table = pd.DataFrame({
        'Input': list1,
        'P1': list2,
        'P50': list3,
        'P99': list4,
        'P Dist' : [p_dists[0] for el in list1]
    })
    edited_df = st.data_editor(
        df_table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "P Dist": st.column_config.SelectboxColumn(
                label="Prob dist",
                help="Probability distribution of the input variable",
                width="small",
                options=p_dists,
                required=True
            ),
            "P1": st.column_config.NumberColumn(
                label="P1",
                help="1% probability for variable to be below input"
            ),
            "P50": st.column_config.NumberColumn(
                label="P50",
                help="Most Likely value / Median value (50% probability)"
            ),
            "P99": st.column_config.NumberColumn(
                label="P99",
                help="99% probability for variable to be below input"
            )
        }
    )
    return edited_df
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

def create_uncertainty_table(list1, list2,list3, list4, p_dists):
    df_table = pd.DataFrame({
        'Input': list1,
        'P1': list2,
        'P50': list3,
        'P99': list4,
        'P Dist' : [p_dists[0] for el in list1]
    })
    edited_df = st.data_editor(
        df_table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "P Dist": st.column_config.SelectboxColumn(
                label="Prob dist",
                help="Probability distribution of the input variable",
                width="small",
                options=p_dists,
                required=True
            ),
            "P1": st.column_config.NumberColumn(
                label="P1",
                help="1% probability for variable to be below input"
            ),
            "P50": st.column_config.NumberColumn(
                label="P50",
                help="Most Likely value / Median value (50% probability)"
            ),
            "P99": st.column_config.NumberColumn(
                label="P99",
                help="99% probability for variable to be below input"
            )
        }
    )
    return edited_df

def display_uncertainty_table(Gas_Price, IGIP_input, LNG_plant_per_Sm3, OPEX_variable, well_cost, PU_cost, temp_cost, LNG_carrier):    
    from Data.DefaultData import default_MC, probability_distributions
    list3 = [Gas_Price, IGIP_input/1e9, LNG_plant_per_Sm3, OPEX_variable, well_cost, PU_cost, temp_cost, LNG_carrier]
    list1, list2, list4 = default_MC()
    p_dists = probability_distributions() 
    edited_df = create_uncertainty_table(list1, list2, list3, list4, p_dists)
    validate_uncertainty_table(edited_df)
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
def display_table_Monte_Carlo_param2():    
    from Data.DefaultData import default_MC_params2
    list1, list2 = default_MC_params2()
    df_table = pd.DataFrame({
        'Parameter': list1,
        'Value': list2,

    })
    edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)
    return edited_df['Value']

def validate_uncertainty_table(df):
    for index, row in df.iterrows():
        P1 = row["P1"]
        P50 = row["P50"]
        P99 = row["P99"]
        input_name = row["Input"]
        
        if P1 >= P50:
            st.error(f"Uncertainty table is not correct for '{input_name}': P1 must be less than P50.")
            st.stop()
        if P50 >= P99:
            st.error(f"Uncertainty table is not correct for '{input_name}': P50 must be less than P99.")
            st.stop()
    
        
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

def tornadoPlotSensitivity(NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, NPV_OPEXmax, NPV_OPEXmin, NPV_Wellmax, NPV_Wellmin, NPV_PUmax, NPV_PUmin, NPV_tempmax, NPV_tempmin, NPV_Carriermax, NPV_Carriermin):
    gas_price_sensitivity = np.abs(NPVgaspricemax - NPVgaspricemin)
    LNG_plant_sensitivity = np.abs(LNGPlantMin-LNGPlantMax)
    IGIP_sensitivity = np.abs(NPV_IGIPmax - NPV_IGIPmin)
    OPEX_sensitivity = np.abs(NPV_OPEXmin-NPV_OPEXmax)

    well_sensitivity = np.abs(NPV_Wellmin-NPV_Wellmax)
    PU_sensitivity = np.abs(NPV_PUmin-NPV_PUmax)
    temp_sensitivity = np.abs(NPV_tempmin-NPV_tempmax)
    carrier_sensitivity = np.abs(NPV_Carriermin-NPV_Carriermax)


    sensitivities = [round(gas_price_sensitivity, 2),round(LNG_plant_sensitivity,2), round(IGIP_sensitivity,2), round(OPEX_sensitivity,2), round(well_sensitivity,2), round(PU_sensitivity,2), round(temp_sensitivity,2), round(carrier_sensitivity,2)]
    labels = ['Gas Price', 'LNG Plant', 'IGIP', 'OPEX', 'Well Cost', 'P&U Cost', 'Template Cost', 'LNG Carrier cost']
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=labels,
            x=sensitivities,
            orientation='h',  # horizontal bars
            marker=dict(
                color=['blue', 'orange', 'red', 'green', 'yellow', 'pink', 'lime', 'skyblue'],
                opacity=0.7
            ),
            text=sensitivities,  
            textposition='outside',
            textfont=dict(size=14)
        )
    )


    fig.update_layout(
        title={
            'text': 'Tornado Plot - NPV Sensitivity based on P1, P99',
            'font': {
                'size': 20  
            }
        },
        xaxis_title={
            'text': 'NPV [1E6 USD]',
            'font': {
                'size': 20  
            }
        },
        yaxis_title={
            'text': 'Variable',
            'font': {
                'size': 20 
            }
        },
        barmode='group',
    )
    st.plotly_chart(fig, use_container_width=True)

def tornadoPlot(initial_NPV, NPVgaspricemin, NPVgaspricemax, LNGPlantMin, LNGPlantMax, NPV_IGIPmin, NPV_IGIPmax, Gas_Price, IGIP_input, LNG_plant_per_Sm3, NPV_OPEXmax, NPV_OPEXmin, opex_cost, NPV_Wellmax, NPV_Wellmin, NPV_PUmax, NPV_PUmin, NPV_tempmax, NPV_tempmin, NPV_Carriermax, NPV_Carriermin, well_cost, PU_cost, temp_cost, LNG_carrier):
    labels = ['Gas Price', 'LNG Plant', 'IGIP', 'OPEX', 'Well Cost', 'P&U Cost', 'Template Cost', 'LNG Carrier cost']
    
    
    min_values = [round(NPVgaspricemin,2), round(LNGPlantMax,2), round(NPV_IGIPmin,2), round(NPV_OPEXmax, 2), round(NPV_Wellmax, 2), round(NPV_PUmax, 2), round(NPV_tempmax, 2), round(NPV_Carriermax, 2)]
    max_values = [round(NPVgaspricemax, 2), round(LNGPlantMin, 2), round(NPV_IGIPmax, 2), round(NPV_OPEXmin, 2), round(NPV_Wellmin, 2), round(NPV_PUmin, 2), round(NPV_tempmin, 2), round(NPV_Carriermin, 2)]
    
    fig = go.Figure()
    
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
                showlegend=False,
                text=min_values[i],  
                textposition='outside',
                textfont=dict(size=14)
                
            )
        )
    
    for i, label in enumerate(labels):
        fig.add_trace(
            go.Bar(
                y=[label],
                x=[(max_values[i] - initial_NPV)],
                orientation='h',
                base=initial_NPV,
                marker=dict(
                    color='green',
                    opacity=0.7
                ),
                name=f'Max {label}',
                showlegend=False,
                text=max_values[i],  
                textposition='outside',
                textfont=dict(size=14)
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
        title={
            'text': 'Tornado Plot - NPV from P1 and P99 input',
            'font': {
                'size': 20  # Adjust the size of the plot title text here (e.g., 20)
            }
        },
        xaxis_title={
            'text': 'NPV [1E6 USD]',
            'font': {
                'size': 20  # Adjust the size of the x-axis title text here (e.g., 16)
            }
        },
        yaxis_title={
            'text': 'Variable',
            'font': {
                'size': 20  # Adjust the size of the y-axis title text here (e.g., 16)
            }
        },
        barmode='overlay',
        showlegend=True
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'Base case NPV (with optimized rate of abandonment) = {initial_NPV} 1E6 USD with gas price = {Gas_Price} USD/Sm3, IGIP = {IGIP_input/1e9} 1E9 Sm3, LNG plant = {LNG_plant_per_Sm3} USD/Sm3/d  OPEX = {opex_cost} 1E6 USD, well cost = {well_cost} 1E6 USD, Pipeline & Umbilical = {PU_cost} 1E6 USD, template cost = {temp_cost} 1E6 USD, LNG vessel cost = {LNG_carrier} 1E6 USD')
