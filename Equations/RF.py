def RF(Gp, IGIP):
    """
    Returns recovery factor based on:
    Gp = total gass offtake,
    IGIP = initial gas in place
    """
    RF = Gp/IGIP
    return RF

