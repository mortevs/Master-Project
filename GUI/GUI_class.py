import streamlit as st
import GUI.GUI_functions as display
import time
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
        if opt == 'RESERVOIR PRESSURE FROM PRODUCTION DATA':
             self.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA()

    def FIELD_DEVELOPMENT(self):
        from Modules.FIELD_DEVELOPMENT.run_Analysis import DryGasAnalysis
        Analysis = DryGasAnalysis(session_id='DryGasAnalysis')
        #st.title('Field development')
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
            if st.button('Restart', 'Restart FD'):
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
        

    def RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(self):
        #st.title('Reservoir Pressure calculations')
        from Data.StreamlitUpload import upload 
        df_prod = upload(text = "Upload a CSV file / Excel file with the following format or choose field from dropdown menu below")
        import Data.getData as get
        fieldnames = get.fieldNames()
        import locale
        def locale_aware_sort(arr, locale_str='nb_NO.UTF-8'):
            locale.setlocale(locale.LC_ALL, locale_str)            
            arr.sort(key=locale.strxfrm) 
        locale_aware_sort(fieldnames)
        fieldnames.insert(0, 'No field chosen')
        import GUI.GUI_functions as GUI
        col10, col11 = st.columns(2)
        with col10:     
            selected_field = GUI.dropdown(label = 'Get gas production data from the following field:', options = fieldnames, labelVisibility="visible")
        with col11:
            selected_time = GUI.dropdown(label = 'Choose yearly, monthly or daily time perspective', options = ['Yearly', 'Monthly', 'Daily'], labelVisibility="visible")
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.run_R_analysis import ReservoirPressureAnalysis
        RES_Analysis = ReservoirPressureAnalysis(session_id='ReservoirPressureAnalysis')
        RES_Analysis.updateFromDropdown(selected_field, selected_time)
        col12, col13= st.columns(2)
        with col12:     
            if st.button('Run Analysis', 'Run RP'):
                if selected_field == 'No field chosen' and df_prod == None:
                    alert2 = st.warning('Upload data or chose a field from list above')
                    time.sleep(3)
                    alert2.empty()
                else:
                    RES_Analysis.getResult().append((RES_Analysis.run(selected_field, selected_time, df_prod)))
                    #st.dataframe(RES_Analysis.run(selected_field, selected_time, df_prod))
        RES_Analysis.plot()
        with col13:     
            if st.button('Restart', 'Restart RESPRES'):
                from Data.Storage.Cache import clear_state2
                #ReservoirPressureAnalysis.reset_lists()
                clear_state2(RES_Analysis.getState())
        
            
            

        #RES_Analysis.updateParameterListfromTable() 

    # #file_name = 'productionProfile.xlsx'
    # #df.to_excel(file_name) 
    # #import Data.getData as get 
    # #print(get.CSVProductionYearly("Snøhvit"))
    # return None