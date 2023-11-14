from Data.datasetToDict import datasetToDict
def dictToFunc(inputDataSet):
    dataDict = datasetToDict(inputDataSet)   
    qFieldTarget = dataDict.get('qFieldTarget')[0]
    PRi = dataDict.get('PRi')[0]
    abandonmentRate = dataDict.get('abandonmentRate')[0]
    TR = dataDict.get('TR')[0]
    gasMolecularWeight = dataDict.get('gasMolecularWeight')[0]
    C_R = dataDict.get('C_R')[0]
    n = dataDict.get('n')[0]
    N_temp = dataDict.get('N_temp')[0]
    NWellsPerTemplate = dataDict.get('NWellsPerTemplate')[0]
    upTime = dataDict.get('upTime')[0]
    C_t = dataDict.get('C_t')[0]
    S = dataDict.get('S')[0]
    C_FL = dataDict.get('C_FL')[0]
    C_PL = dataDict.get('C_PL')[0]
    P_sep = dataDict.get('P_sep')[0]
    IGIP = dataDict.get('IGIP')[0]
    
    
    return [qFieldTarget, PRi, abandonmentRate, TR, gasMolecularWeight, C_R, n, N_temp, NWellsPerTemplate, upTime, C_t, S, C_FL, C_PL, P_sep, IGIP]
    
