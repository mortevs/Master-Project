def MBgastank_PR(PRi, Zi, ZR, RF):
    """
    Simple reservoir model. Returns reservoir pressure at year i based on: 
    ZR = Z factor at year i,
    Pi = initial reservoir pressure year 0,
    Zi = intial Z factor year 0,
    RF = recovery factor at year i.
    """
    MBgastank_PR = (ZR * (PRi/Zi)*(1-RF))
    return MBgastank_PR
