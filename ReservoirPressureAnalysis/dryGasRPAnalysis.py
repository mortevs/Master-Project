class ReservoirPressureAnalysis:
    def __init__(self):
        import pandas as pd
        self.__productionData = pd.DataFrame()
        self.__field = 'NO FIELD CHOSEN'
        from Data.StreamlitUpload import upload 
        upload(text = "Upload a CSV file / Excel file with the following format or choose field from dropdown menu below")
        self.__timeframe = 'Yearly' 

    def updateFromDropdown(self):
        import Data.getData as get
        import Plotting.plotFunc as Plot
        fieldnames = get.fieldNames()
        fieldnames.insert(0, 'NO FIELD CHOSEN')
        import streamlit as st
        self.__field = Plot.dropdown(options = fieldnames)
        self.__timeframe = Plot.dropdown(options = ['Yearly', 'Monthly'])
    
    def run(self):
        if self.__field != 'NO FIELD CHOSEN':
            import Data.dataProcessing.dataProcessing as dP 
            import pandas as pd
            import streamlit as st
            import Data.getData as get
            if self.__timeframe == 'Yearly':
                self.__productionData['Yearly Produced Gas'] = get.CSVProductionYearly(self.__field)[0]
                self.__productionData = dP.addProducedYears(self.__field, self.__productionData)
            elif self.__timeframe == 'Monthly':
                self.__productionData['Monthly Produced Gas'] = get.CSVProductionMonthly(self.__field)[0]
                self.__productionData = dP.addProducedYears(self.__field, self.__productionData)
            
            st.dataframe(self.__productionData)

            

    


