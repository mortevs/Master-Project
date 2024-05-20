from pages.GUI.main_page import main_page_GUI
import streamlit as st
if __name__ == "__main__":
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
        menu_items={'Get Help': email_link_Help,
        'Report a bug': email_link_BUG,
        'About': "# Master project by Morten Vier Simensen"
    }
        )
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(204, 49, 49);
    }
    </style>""", unsafe_allow_html=True)
    
    main_page_GUI()

