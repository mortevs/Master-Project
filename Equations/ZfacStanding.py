import math 
    
#valid = {1, 2}


def ZfacStanding(p1: float, T1: float, gasMolecularWeight: float) ->float:
    """
    Returns Z-factor based on Hall&Yarborough equation fitted to Standing-Katz Chart. Use psia and °F or bara and °C.
    p1 = pressure [psia] or [bara],
    T1 = Temperature [°F] or [°C],
    GasMolecularWeight = molecular weight of the gas at standard conditions (air=1)
    """
    #Unit = If field units used (psia and °F): [1]. If Metric Units used (bara and °C): [2] 
    #Unit check
    #if unit not in valid:
    #    raise ValueError('Zfacstanding unit must be one of %r' % valid)
        
    #Calculating Specific Gravity (air = 1) Yg
    massAir = 28.967 #g/mol (could use 28.967 instead)
    Yg = gasMolecularWeight/massAir
    
    
    #Calculating pseudocriticaltemperature and pressure
    
    #Suttons suggestion for correlations for hydrocarbon gas mixtures
    Tpc = 169.2 + 349.5 * Yg - 74 * Yg**2
    Ppc = 756.8 - 131 * Yg - 3.6*Yg**2
    #if unit == 2:
    T = 9/5 *T1 + 32
    p = 14.5038*p1
    #else:
        #T = T1
        #p = p1
    
    #Calculating pseudo reduced properties
    Tpr = (T + 460) / Tpc
    Ppr = p / Ppc
    T = 1 / Tpr
    A = 0.06125 * T * (math.e)**(-1.2 * (1 - T) ** 2)
    Y = 0.001
    i = 0
    F=1
    
    #Finding the Z factor by looping. Adding constraint that the loop should only run 1000 iterations in case it doesnt converge
    
    while abs(F) > 0.00000001 and i < 1000: 
        fy = -A * Ppr + (Y + Y**2 + Y**3 - Y ** 4) / ((1 - Y) ** 3) - (14.76 * T - 9.76 * T**2 + 4.58 * T**3) * Y**2 + (90.7 * T - 242.2 * T**2 + 42.4 * T**3) * Y**(2.18 + 2.82 * T)
        
        dfY = (1 + 4 * Y + 4 * Y**2 - 4 * Y**3 + Y**4) / ((1 - Y) ** 4) - (29.52 * T - 19.52 * T**2 + 9.16 * T** 3) * Y + (2.18 + 2.82 * T) * (90.7 * T - 242.2 * T ** 2 + 42.4 * T**3) * Y**(1.18 + 2.82 * T)
        Y = Y - fy / dfY
        F = fy / dfY
        i+=1
        
    Z = A * Ppr / Y
    ZfacStanding = Z
    return ZfacStanding

