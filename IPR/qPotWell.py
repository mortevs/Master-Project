from Utilities.DryGasFlowEquations import IPRqg
def qPotWell(C_R, n, P_R_PreviousYear, PWfMin):
    """
    Returns potential wellflow given:
    P_R_PreviousYear = Reservoir pressure previous year
    C_R = inflow backpressure coefficient
    n = inflow backpressure coefficient
    PWfMin = minimum bottomhole pressure
    
    """
    
    q_potWell = IPRqg(C_R, n, P_R_PreviousYear, PWfMin)
    return q_potWell


