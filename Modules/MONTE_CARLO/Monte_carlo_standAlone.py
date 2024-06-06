import numpy as np
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import scipy.stats as stats
def pert_distribution(a, b, c, size=1):
   r = c-a
   alpha = 1 + 4*(b-a) / r
   beta = 1 + 4 * (c-b) / r
   return a + np.random.beta(alpha, beta, size = size) * r

def calculate_mean_std_from_p1_p99(p1_value, p99_value):
    z1 = stats.norm.ppf(0.01)
    z99 = stats.norm.ppf(0.99)
    std_dev = (p99_value - p1_value) / (z99 - z1)
    mean = p1_value - z1 * std_dev
    return [mean, std_dev]

def calculate_scale_from_p1_p50_p99(p1_value, p50_value, p99_value):
    q1 = stats.expon.ppf(0.01)
    q50 = stats.expon.ppf(0.50)
    q99 = stats.expon.ppf(0.99)
    scale_from_p1 = p1_value / q1
    scale_from_p50 = p50_value / q50
    scale_from_p99 = p99_value / q99    
    scale = np.mean([scale_from_p1, scale_from_p50, scale_from_p99])
    return scale

def RandomNumbers_with_Distribution_consideration(df, size):
    rows = len(df.index)
    function_map = {'uniform': np.random.uniform, 'normal': np.random.normal, 'pert (default)': pert_distribution, 'normal': np.random.normal, 'lognormal' : np.random.lognormal, 'triangular' : np.random.triangular, 'exponential': np.random.exponential}
    dist_dict = {'uniform': ['P1', 'P99'], 'pert (default)' : ['P1', 'P50', 'P99'], 'triangular' : ['P1', 'P50', 'P99'], 'normal': ['P1', 'P99'], 'exponential': ['P1', 'P50', 'P99']}
    rand_variables = []
    for i in range(rows):
        func = (function_map[df.iloc[i]['P Dist']])
        func_var = df[dist_dict[df.iloc[i]['P Dist']]].loc[i].to_list()
        if df.iloc[i]['P Dist'] == 'normal':
            func_var = calculate_mean_std_from_p1_p99(*func_var)
        elif df.iloc[i]['P Dist'] == 'exponential':
            func_var = calculate_scale_from_p1_p50_p99(*func_var)
        var = func(*func_var, size = size)
        rand_variables.append(var)
    return rand_variables

def Monte_Carlo_Simulation(bins, results, Nr_random, title_xaxis = 'NPV [1E06 USD]'):
    nr_bins = bins
    bins = np.linspace(results.min(),results.max(),nr_bins)
    counts = np.histogram(results,bins)[0]
    pdf = counts/Nr_random
    bin_for_plotting = (bins[0:-1]+bins[1:])/2

    fig_pdf = go.Figure()
    fig_pdf.add_trace(go.Scatter(x=bin_for_plotting, y=pdf, mode='lines', name='pdf'))
    fig_pdf.update_layout(title='PDF', xaxis_title=title_xaxis, yaxis_title='frequency', showlegend=True)
    
    # Calculate CDF
    cdf = np.cumsum(pdf)
    invcdf = 1 - cdf
    bins_cdfplot = bins[1:]

    # Create CDF plot
    fig_cdf = go.Figure()
    fig_cdf.add_trace(go.Scatter(x=bins_cdfplot, y=invcdf, mode='lines', name='ccdf'))
    fig_cdf.update_layout(title='CCPF', xaxis_title=title_xaxis, yaxis_title='Complementary cumulative probability distribution', showlegend=True)

    
    std = round(np.std(results),2)
    mean = round(np.mean(results),2)
    table = pd.DataFrame({'Variable':['P90','P50','P10', 'Mean', 'Std'],
    'Value':[round(np.percentile(results,10),2),round(np.percentile(results,50),2),round(np.percentile(results,90),2), mean, std]})

    return fig_pdf, fig_cdf, table
        
class uncertainity_table():
    def __init__(self, df_table):
        edited_df = st.data_editor(df_table, hide_index=True, use_container_width=True)

  
        