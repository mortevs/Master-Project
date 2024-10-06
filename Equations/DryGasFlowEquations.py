import math, warnings

def IPRqg(C_R: float, n:float, p_R:float, p_wf:float) -> float:
    """
    Returns gas rate bottomhole. 
    C_R = backpressure coefficient [sm^3/bar^(2*n)], 
    n = Backpressure exponent (typically assumed 1),
    p_R = reservoir pressure [bar],
    p_wf = pressure bottomhole well, wellflow [bar].
    """
    IPRqg = C_R*(p_R**2-p_wf**2)**n
    return IPRqg

def IPRpwf(C_R:float, n:float, p_R:float, q_g:float) -> float:
    """
    Returns pressure bottomhole. 
    C_R = backpressure coefficient [sm^3/bar^(2*n)], 
    n = Backpressure exponent (typically assumed 1),
    p_R = reservoir pressure [bar],
    p_wf = pressure bottomhole well, wellflow [bar].
    """
    IPRpwf=(p_R**2-(q_g/C_R)**(1/n))**0.5
    return IPRpwf

def IPR_PR(C_R:float, n:float, p_wf:float, q_g:float) -> float:
    """
    Returns reservoir pressure. Equation based on IPR equation solved for P_R with Pwf as input
    pressure upstream wf (reservoir pressure) (moving counter stream from 2 to 1).
.
    C_R = backpressure coefficient [sm^3/bar^(2*n)], 
    n = Backpressure exponent (typically assumed 1),
    p_wf = pressure bottomhole well, wellflow [bar].
    p_R = reservoir pressure [bar],
    """
    P_R=(p_wf**2+(q_g/C_R)**(1/n))**0.5
    return P_R

def Tubingqg(C_T:float, s:float, p1:float, p2:float) -> float:
    """
    Returns gas rate tubingline.
    C_T = tubing coefficient [sm3/bar],
    p1 = pressure upstream the tube [bar],
    p2 = pressure downstream the tube [bar],
    s = tubing elevation coefficient.
    """
    Tubingqg = C_T*(p1**2/(math.e)**s-p2**2)**0.5
    return Tubingqg

def Tubingp1(C_T:float, s:float, p2:float, q_g:float) -> float:
    import math
    """
    Returns pressure upstream tubingline (moving counter stream from 2 to 1).
    C_T = tubing coefficient [sm3/bar],
    p2 = pressure downstream the tube [bar],
    s = tubing elevation coefficient,
    """
    Tubingp1 = (math.e)**(s/2)*(p2**2+(q_g/C_T)**2)**0.5
    return Tubingp1

def Tubingp2(C_T:float, s:float, p1:float, q_g:float) -> float:    
    """
    Returns pressure downstream tubingline (moving with stream from 1 to 2). 
    C_T = tubing coefficient [sm3/bar],
    p1 = pressure upstream the tube [bar],
    s = tubing elevation coefficient.
    """
    #warnings.filterwarnings("ignore", message="invalid value encountered in sqrt") #tryging to root negative root number warning
    Tubingp2 = (p1**2/math.e**s-(q_g/C_T)**2)**0.5 
    return Tubingp2

def Lineqg(C_FL:float, p1:float, p2:float) -> float:
    """
    Returns gasrate.
    Assumes horizontal line,
    p1 = pressure upstream,
    p2 = pressure downstream.
    C_FL = flowline coefficient
    """
    Lineqg = C_FL*(p1**2-p2**2)**0.5
    return Lineqg

def Linep1(C_FL:float, p2:float, q_g:float) -> float:
    """
    Returns pressure upstream line (moving counter stream from 2 to 1).
    Assumes horizontal line,
    C_FL = flowline coefficient,
    p2 = pressure downstream.
    """
    Linep1 = (p2**2 + (q_g/C_FL)**2)**0.5
    return Linep1

def Linep2(C_FL:float, p1:float, q_g:float) -> float:
    """
    Returns pressure downstream line (moving with stream from 1 to 2).
    Assumes horizontal line,
    C_FL = flowline coefficient,
    p1 = pressure upstream.
    """
    Linep2= (p1**2-(q_g/C_FL)**2)**0.5
    return Linep2

