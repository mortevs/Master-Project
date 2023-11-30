import streamlit as st
import GUI.GUI_functions as display
import time
import Data.getData as get
from Data.dataProcessing import get_field_list_inc_No_field_chosen
fieldnames = get_field_list_inc_No_field_chosen()

class GUI():
    def __init__(self):
        st.markdown(''':green[Specialization Project by Morten Vier Simensen, supervised by Prof. Milan Stanko]''')
        col1, col2, col3 = st.columns(3)
        with col3:
            load = st.button('Load New Data from NPD',  'NPD')
            if load:
                from Data.getData import deleteAndloadNewDatafromNPD
                deleteAndloadNewDatafromNPD() 

        opt = display.dropdown(label = 'What do you want to use the application for?',options = ['NO OPTION CHOSEN', 'FIELD DEVELOPMENT', 'PRODUCTION FORECASTING', 'RESERVOIR PRESSURE FROM PRODUCTION DATA', 'NPD DATA', 'IPR TUNING', 'TPR TUNING'], labelVisibility='visible')   
        if opt == 'FIELD DEVELOPMENT':
            self.field_development = FIELD_DEVELOPMENT(parent=GUI)
        elif opt == 'RESERVOIR PRESSURE FROM PRODUCTION DATA':
             self.reservoir_pressure_from_production_data = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(self)
        elif opt == 'NPD DATA':
             self.NPD_DATA = NPD_DATA(GUI)           

class FIELD_DEVELOPMENT(GUI):
    def __init__(self, parent):
        from Modules.FIELD_DEVELOPMENT.run_Analysis import DryGasAnalysis
        Analysis = DryGasAnalysis(parent = FIELD_DEVELOPMENT, session_id='DryGasAnalysis')
        method, precision = display.columnDisplay2(list1=[['NODAL', 'IPR'], ['IMPLICIT', 'EXPLICIT']])
        Analysis.updateFromDropdown(method = method, precision=precision)
        Analysis.updateParameterListfromTable() 
        plot_comp = False  
        col4, col5, col6 = st.columns(3)
        with col4:
            run = st.button('Run Analysis', 'Run DG')
        with col6: 
            if st.button('Compare different models', 'Compare'):
                    plot_comp = True
        col7, col8, col9 = st.columns(3)
        with col7:
            clear =  st.button('Clear output', 'clear FD')
        with col9: 
            field = display.dropdown(label = 'Choose a field to compare with', options = fieldnames, labelVisibility="visible")
            Analysis.updateField(field)
        
        if clear:
            Analysis.clear_output()

        field_name = Analysis.get_current_field()
        if run and field_name == 'No field chosen':
            result = Analysis.run()
            Analysis.append_result(result)

        elif run and field_name != 'No field chosen':
            result = Analysis.run_field(field)
            Analysis.append_result(result)
        if plot_comp == True:
            Analysis.plot(comp = True)
        Analysis.plot()
        self.parent = parent

class RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA(GUI):
    def __init__(self, parent):
        eq = display.dropdown(label = 'What equation do you want to use?', options = ['Material balance with Z-factor calculation'], labelVisibility="visible")
        if eq == 'Backpressure equation':
            pass
        from Data.StreamlitUpload import upload 
        uploaded = upload(text = "Upload a CSV file / Excel file with the following format or choose field from dropdown menu below")
        col10, col11 = st.columns(2)
        with col10:     
            field = display.dropdown(label = 'Get gas production data from the following field:', options = fieldnames, labelVisibility="visible")
        with col11:
            selected_time = display.dropdown(label = 'Choose yearly or monthly producted volumes', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        from Modules.RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA.run_R_analysis import ReservoirPressureAnalysis
        
        RES_Analysis = ReservoirPressureAnalysis(parent = RESERVOIR_PRESSURE_FROM_PRODUCTION_DATA, session_id='ReservoirPressureAnalysis')
        RES_Analysis.updateFromDropDown(fieldName= field, time = selected_time)
        RES_Analysis.update_from_upload(uploaded)
        
        st.write("The following data for " + field[0]+field[1:].lower() + " was found at NPD" )
        RES_Analysis.updateParameterListfromTable()
        col12, col13= st.columns(2)
        with col12:   
            run = st.button('Run Analysis', 'Run RP')
        with col13: 
            clear = st.button('Clear output', 'clear RESPRES')
            
        if run and field == 'No field chosen':
            alert3 = st.warning('Choose a field first')
            time.sleep(1.5)
            alert3.empty()
        
        elif run and selected_time == 'Yearly':
            result = RES_Analysis.runY()
            RES_Analysis.append_result(result)

        elif run and selected_time == 'Monthly':
            result = RES_Analysis.runM()
            RES_Analysis.append_result(result)

        if clear:
            RES_Analysis.clear_output()
        RES_Analysis.plot()
        self.parent = parent
        

class NPD_DATA(GUI):
    def __init__(self, parent):
        st.write('To compare fields follow these steps:')
        st.write('Step 1 - Choose a field, Step 2- Click Show plot, Step 3 - Repeat step 1 and 2, Step 4 - Click Compare fields')
        from Modules.NPD_DATA.npd_data import npd_prod
        npd_obj = npd_prod(parent = NPD_DATA, session_id='npd_prod', field = 'No field chosen')
        col4, col5  = st.columns(2)
        with col4:
            field = display.dropdown(label = 'Choose a field', options = fieldnames, labelVisibility="visible")
        with col5:
            time = display.dropdown(label = 'Time frame of interest', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        
        npd_obj.updateFromDropDown(fieldName = field, time = time)
        col6, col7, col8 = st.columns(3)
        with col6:
            run = st.button('Plot production profile', 'Show produced volumes')
        with col7:
            comp = st.button('Compare fields', 'Compare')
        with col8: 
            clear =  st.button('Clear output', 'clear FD')
        
        if run and field == 'No field chosen':
            alert3 = st.warning('Choose a field first')
            time.sleep(1.5)
            alert3.empty()
        
        elif run and time == 'Yearly':
            result = npd_obj.runY()
            npd_obj.append_result(result)

        elif run and time == 'Monthly':
            result = npd_obj.runM()
            npd_obj.append_result(result)

        if clear:
            npd_obj.clear_output()

        if comp:
            npd_obj.plot(comp = True)
        npd_obj.plot()
        self.parent = parent

        st.write(' ')
        st.write(' ')
        st.write(' ')

        poly_button = st.button('Plot reservoir area', 'polygon plotter')
        if poly_button and field == 'No field chosen':
            import time
            alert4 = st.warning('Choose a field first')
            time.sleep(1.5)
            alert4.empty()
        elif poly_button and field != 'No field chosen':
            from Modules.NPD_DATA.npd_data import PolygonPlotter
            wkt_str = get.polygon_coordinates(field)
            polygon = PolygonPlotter(wkt_str)
            polygon.plot()
        
