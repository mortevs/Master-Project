from Data.DefaultData import default_FD_data
def NodalAnalysis(precision: str, Parameters: list = default_FD_data()):
    """precision = 'implicit' or 'explicit' and field. The implicit method is more accurate, but may fail due to root-finding problems."""
    if precision == 'EXPLICIT':
        from Modules.FIELD_DEVELOPMENT.Nodal.dfNodalExplicit import Nodal
    elif precision == 'IMPLICIT':
        from Modules.FIELD_DEVELOPMENT.Nodal.dfNodalImplicit import Nodal
    else:
        import streamlit as st
        st.write("Precision is not explicit or implicit")
        st.write(precision)

    df = Nodal(*Parameters)
    df.columns=('Field Rates [Sm3/d]', 'Yearly Gas Offtake [Sm3]', 'Cumulative Gas Offtake [Sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir Pressure [bara]', 'Rates per Well [Sm3/d]', 'Bottomhole Pressure [bara]', 'Wellhead Pressure [bara]', 'Template Pressure [bara]', 'Pressure Pipeline Entry Module [bara]', 'Seperator Pressure [bara]', 'Rates per Template [Sm3/d]', 'Choke Pressure [bara]', 'Ratio PTemp to PWellHead', 'Production Potential Rates [Sm3/d]' )
    return df
    

