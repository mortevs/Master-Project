from Equations.DryGasFlowEquations import Linep1, Tubingp1
def pWfMinEstimation(C_t: float, S: float, C_FL: float, C_PL:float , fieldRate: float, p_sep: float, N_temp: int, NWellsPerTemplate: int)->float:
    """
    Returns a minimum estimation of bottomhole pressure based on the following data. Assumes pressure at wellhead equal to pressure at template.  
    C_t = tubing coefficient [sm3/bar],
    S = tubing elevation coefficient,
    C_FL = flowline coefficient,
    C_PL = Pipeline coefficient,
    P_sep = Pressure at separator,
    N_temp = Number of templates,
    NWellsPerTemplate = Number of wells per template,
    Field rate.
    """     
    p_plem = Linep1(C_PL, p_sep , fieldRate) #pressure pipeline entry module  
    q_temp = fieldRate / N_temp #gasrate per template
    p_temp = Linep1(C_FL, p_plem, q_temp) #pressure at template
    p_wh = p_temp #assuming that pressure at wellhead is equal to pressure at the template 
    q_well = q_temp / NWellsPerTemplate
    p_wf = Tubingp1(C_t, S, p_wh, q_well)
    return p_wf 