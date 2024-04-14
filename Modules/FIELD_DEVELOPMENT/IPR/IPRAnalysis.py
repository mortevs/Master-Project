from Data.DefaultData import default_FD_data

def IPRAnalysis(precision: str, parameters: list = default_FD_data()):
    if precision == 'EXPLICIT':
        from Modules.FIELD_DEVELOPMENT.IPR.dfIPRExplicit import IPROnly
    elif precision == 'IMPLICIT': 
        from Modules.FIELD_DEVELOPMENT.IPR.dfIPRImplicit import IPROnly
    else:
        import streamlit as st
        st.write("Precision is not explicit or implicit")
        st.write(precision)
        
    df = IPROnly(*parameters)
    df.columns=('QFieldTarget [Sm3/d]', 'QWellTarget [Sm3/d]', 'Reservoir Pressure [bara]', 'Z-factor', 'Minimum Bottomhole Pressure [bara]', 'Potential Rates per Well [Sm3/d]', 'Potential Field Rates [Sm3/d]', 'Field Rates [Sm3/d]', 'Well Production Rates [Sm3/d]', 'Yearly Gas Offtake [Sm3]', 'Cumulative Gas Offtake [Sm3]', 'Recovery Factor', 'Bottomhole Pressure [bara]')
    df = swapColumns(df, 'QFieldTarget [Sm3/d]', 'Field Rates [Sm3/d]')
    return df

def swapColumns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df





      




      


