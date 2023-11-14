import streamlit as st
import GUI.GUI_functions as display
class GUI():
    def __init__(self):
        st.markdown(''':green[Specialization Project by Morten Vier Simensen, supervised by Prof. Milan Stanko]''')
        col1, col2, col3 = st.columns(3)
        with col3:
            if st.button('Load New Data from NPD',  'NPD'):
                from Data.getData import deleteAndloadNewDatafromNPD
                deleteAndloadNewDatafromNPD() 
        opt = display.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')   
        if opt == 'FIELD DEVELOPMENT':
            self.FIELD_DEVELOPMENT()

    def FIELD_DEVELOPMENT(self):
        from Modules.FIELD_DEVELOPMENT.Dry_gas_analysis import DryGasAnalysis
        Analysis = DryGasAnalysis()
        st.title('Field development')
        Analysis.updateFromDropdown()
        Analysis.updateParameterListfromTable() 
        plot_comp = False  
        col4, col5, col6 = st.columns(3)
        with col4:     
            if st.button('Run Analysis', 'Run'):
                Analysis.getResult().append(Analysis.run())
        with col6: 
            if st.button('Compare different models', 'Compare'):
                    plot_comp = True
        col7, col8, col9 = st.columns(3)
        with col7:
            if st.button('Restart', 'Restart'):
                from Data.Storage.Cache import clear_state
                clear_state(Analysis.getState())
        with col9: 
                import Data.getData as get
                fieldnames = get.fieldNames()
                import locale
                def locale_aware_sort(arr, locale_str='nb_NO.UTF-8'):
                    locale.setlocale(locale.LC_ALL, locale_str)            
                    arr.sort(key=locale.strxfrm) 
                locale_aware_sort(fieldnames)
                fieldnames.insert(0, 'No field chosen')
                import GUI.GUI_functions as GUI
                selected_option1 = GUI.dropdown(label = 'Choose a field to compare with', options = fieldnames, labelVisibility="visible")
                #if selected_option1 != 'NO FIELD CHOSEN':
#                   df = dP.addActualProdYtoDF(field, df)
#                   df = dP.addProducedYears(field, df)

#         if self.__state.field[i] != 'NO FIELD CHOSEN':
#     st.write(self.__state.method[i], self.__state.precision[i], self.__state.field[i])
#     display.multi_plot([self.__state.result[i]], addProduced=True)
# else:
                #selected_option1 = st.dropdown(options = fieldnames)
        if plot_comp == True:
            Analysis.plot(comp = True)
        Analysis.plot()
        




    # #file_name = 'productionProfile.xlsx'
    # #df.to_excel(file_name) 
    # #import Data.getData as get 
    # #print(get.CSVProductionYearly("Snøhvit"))
    # return None