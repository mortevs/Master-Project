import streamlit as st
import pages.GUI.GUI_functions as GUI
import Data.getData as get
from Data.dataProcessing import get_field_list_inc_No_field_chosen


class SODIR_feature:
    def __init__(self):
        def make_pretty(styler):
            styler.set_properties(subset = None, **{'color': 'red'})
            return styler
    
        try:
            self.__fieldnames = get_field_list_inc_No_field_chosen()
        except Exception as e:
            st.write(e)
            st.warning("could not get list of fieldnames from SODIR")
            self.__fieldnames = ["None"]
        on_information = st.toggle("Show me information on how to use the SODIR data feature", value=False, label_visibility="visible")
        if on_information:
            st.write(""" Choose a field from the NCS from the dropdown menu below. Choose a timeframe (yearly or montly) from the second
                     dropdown menu. Now press Plot production profile to display the produced volumes. By default, the gas volumes are
                     visualized, but from the plots dropdown menu the user can choose to display NGL, oil, condendsate, Oil equivilants,
                     water volumes, cumulative volumes and the gas rate.""")
            st.write(""" To compare fields follow these steps: Step 1 - Choose a field, Step 2 - Press Plot production profile, Step 3 -
                     choose a new field, Step 4 - press Plot production profile again, Step 5 - press Compare fields. Keep the same timeframe,
                     dont change between years and months when comparing multiple fields. Compare year with year or month by month, not year with month, it will
                     result in poor comparisons.
                     """)
            st.write(""" Click clear output to remove all the plots and start over again""")

            st.write(""" Click Plot reservoir area to plot a polygon of the reservor area with the wells for the chosen field.
                     The wells can be toggled on and off. By default the closed, and pluggend and abandonend are not shown.
                     To use the forecast functionality, you must first choose a field and click show produced volumes. These data will then be used in 
                     the forecast analysis. Multiple fields can be forecasted at the same time. """)

        from Modules.SODIR_DATA.Sodir_data import Sodir_prod
        sodir_obj = Sodir_prod(parent = SODIR_feature, session_id='sodir_prod', field = 'No field chosen')
        col4, col5  = st.columns(2)
        with col4:
            self.__field = GUI.dropdown(label = 'Choose a field', options = self.__fieldnames, labelVisibility="visible")
        with col5:
            self.__time = GUI.dropdown(label = 'Time frame of interest', options = ['Yearly', 'Monthly'], labelVisibility="visible")
        colA, colB, colC = st.columns(3)
        with colC:
            align = GUI.dropdown(label = 'Compare fields alignment', options = ['Compare from production startup', 'Compare by dates'], labelVisibility="visible")
        sodir_obj.updateFromDropDown(fieldName = self.__field, time = self.__time, align = align)
        col6, col7 = st.columns(2)
        with col6:
            run = st.button('Show Produced Volumes', 'Show produced volumes', use_container_width=True)
        with col7:
            comp = st.button('Compare Fields', 'Compare', use_container_width=True)
        col8, col9 = st.columns(2)
        with col8:
            poly_button = st.button('Show Reservoir Area', 'polygon plotter', use_container_width=True)
        with col9:
            clear =  st.button('Clear Output', 'clear sodir', use_container_width=True)
        if run and self.__field == 'No field chosen':
            import time as t
            alert3 = st.warning('Choose a field first')
            t.sleep(1.5)
            alert3.empty()

        elif run and self.__time == 'Yearly':
            result = sodir_obj.runY()
            sodir_obj.append_result(result)

        elif run and self.__time == 'Monthly':
            result = sodir_obj.runM()
            sodir_obj.append_result(result)

        if clear:
            sodir_obj.clear_output()

        if comp and len(sodir_obj.getResult()) == 0:
            st.error("""No fields to compare. Choose a field and press Plot production profile. Choose another field and then press
                     Plot production profile again. Then press compare fields.""")
        elif comp:
            st.title('Comparison of Produced Volumes')
            sodir_obj.plot(comp = True)
        sodir_obj.plot()

        st.write(' ')
        st.write(' ')
        st.write(' ')

        if poly_button and self.__field == 'No field chosen':
            import time
            alert4 = st.warning('Choose a field first')
            time.sleep(3)
            alert4.empty()
        elif poly_button and self.__field != 'No field chosen':
            from Modules.SODIR_DATA.Sodir_data import makePolyPlot
            sodir_obj.store_polyPlot(makePolyPlot(self.__field))

        from Modules.SODIR_DATA.Sodir_data import plotPolyPlot
        polyFig = sodir_obj.getPolyPlot()
        if len(polyFig) == 0:
            pass
        else:
            plotPolyPlot(polyFig[-1])

        show_more_prod = st.toggle(label = ("Show me more information about the producing wells on "+ self.__field))
        if show_more_prod:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.producing_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)

        show_more_inj = st.toggle(label = ("Show me more information about the injection wells on  "+ self.__field))
        if show_more_inj:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.injecting_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)

        show_more_closed = st.toggle(label = ("Show me more information about the closed wells on  "+ self.__field))
        if show_more_closed:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.closed_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)
        show_more_PA = st.toggle(label = ("Show me more information about the P&A wells on  "+ self.__field))
        if show_more_PA:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.PA_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)
        show_more_PLUGGED = st.toggle(label = ("Show me more information about the plugged wells on  "+ self.__field))
        if show_more_PLUGGED:
            if self.__field == "No field chosen":
                st.error("No field chosen")
            else:
                st.dataframe(get.plugged_wlb(self.__field).style.pipe(make_pretty), hide_index=True, use_container_width=True)


        CF = self.Curve_fitting(sodir_obj, self.__field)
    class Curve_fitting():
        def __init__(self, parent, field):
            self.parent = parent
            my_title = "Forecasting "+ str(parent.getField())
            st.title(my_title)
            col0, col1 = st.columns(2)
            forecast_l = []
            for i in range(1, 501):
                forecast_l.append(i)
            with col0:
                FC_length = GUI.dropdown(label="Forecast length (time frame of interst - Years/Months)", options = forecast_l, index = 2, labelVisibility='visible')
                CF_button = st.button('Forecast with Curve Fit Analysis', 'Curve fit', use_container_width=True)
            with col1:
                data_points = GUI.dropdown(label="Number of last datapoints to consider (excluding year to date volumes)", options = forecast_l, index = 9, labelVisibility='visible')

            import Modules.SODIR_DATA.Curve_Fitting as CF
            import Data.dataProcessing as dP
            if CF_button:
                self.__time = parent.get_time_frame()
                self.__dfs = parent.getResult()

                if len(self.__dfs) == 0:
                    st.warning("""You must choose a field first and then click 'Show Produced Volumes'.
                               Repeat for as many fields as desired. Then click
                               'Forecast with Curve Fit Analysis'.""")
                else:
                    if len(set(self.__time)) != 1:
                        st.error("""Forecasts will be made for all fields above.
                                    Several fields require that the fields have the same
                                    time frame. Clear Output. Then click Show Produced volumes
                                    for each field desired, and do not change Time frame of interest between the fields""")
                    else:
                        self.__Curve_fitted__obj = CF.Curve_fitting(self.__dfs, FC_length+1, self.__time , data_points)
                        self.__res_forecast = self.__Curve_fitted__obj.get_curve_fitted_dfs()
                        
                        parent.plot_forecast(self.__res_forecast)
email_address = "morten.viersi@gmail.com"
email_subject_Help = "Get help with the SMIPPS application"
email_body_Help = "Hi Morten, \n\n I need help with using the SMIPPS Application. I need help with the following: .........."
email_subject_BUG = "Report a SMIPPS Bug"
email_body_BUG = "Hi Morten, \n\n I'm sending you an email experiencing a bug while using the SMIPPS Application. I experienced the bug after performing the following steps .........."
email_link_Help = f"mailto:{email_address}?subject={email_subject_Help}&body={email_body_Help}"
email_link_BUG = f"mailto:{email_address}?subject={email_subject_BUG}&body={email_body_BUG}"

st.set_page_config(
    page_title="Smipps",
    layout="wide",
    page_icon=":wrench:",
    menu_items={'Get Help': email_link_Help,
    'Report a bug': email_link_BUG,
    'About': "# Master project by Morten Vier Simensen"}
    )
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(264, 49, 49);
}
</style>""", unsafe_allow_html=True)
st.title('Sodir Data Investigation')
NPD_DATA = SODIR_feature()
