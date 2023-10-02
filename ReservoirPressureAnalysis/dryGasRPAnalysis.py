class ReservoirPressureAnalysis:
    import pandas as pd
    def __init__(self):
        import streamlit as st
        self.__field = 'NO FIELD CHOSEN'
    def updateFromDropdown(self):
        import Data.getData as get
        import Plotting.plotFunc as Plot
        fieldnames = get.fieldNames()
        fieldnames.insert(0, 'NO FIELD CHOSEN')
        self.__field = Plot.dropdown(options = fieldnames)
    def run(self):
        if self.__field != 'NO FIELD CHOSEN':
            import Data.dataProcessing.dataProcessing as dP 
            import pandas as pd
            import streamlit as st
            df = pd.DataFrame()
            #df = dP.addActualProdYtoPlot(self.__field, df)
            #df = dP.addProducedYears(self.__field, df)
            st.write(df.head())


    


