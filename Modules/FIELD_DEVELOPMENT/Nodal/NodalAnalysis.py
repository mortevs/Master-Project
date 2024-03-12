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
    df.columns=('Field rates [sm3/d]', 'yearly gas of take [sm3]', 'cumulative gas of take [sm3]', 'Recovery Factor', 'Z-factor', 'Reservoir pressure [bara]', 'Rates per well [sm3/d]', 'Bottomhole pressure [bara]', 'Wellhead pressure [bara]', 'Template pressure [bara]', 'Pressure pipeline entry module [bara]', 'Seperator pressure [Bara]', 'Rates per template [sm3/d]', 'choke pressure [bara]', 'ratio PTemp to PWellHead', 'Production Potential rates [Sm3/d]' )
    return df
    

