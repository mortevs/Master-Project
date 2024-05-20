from Equations.DryGasFlowEquations import IPRqg
def qPotWell(C_R, n, P_R, PWfMin):
    """
    Returns potential wellflow given:
    P_R = Reservoir pressure
    C_R = inflow backpressure coefficient
    n = inflow backpressure coefficient
    PWfMin = minimum bottomhole pressure|
    """
    q_potWell = IPRqg(C_R, n, P_R, PWfMin)
    return q_potWell


