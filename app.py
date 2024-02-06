import streamlit as st
from streamlit_option_menu import option_menu
from src.pages import home, viewer, experimental, detector, calculation, target, file_upload, differential_evolution
from src.logic import initialize as init

st.set_page_config(layout="wide")

# Initialize the session state
init.initialize_session_state()

with st.sidebar:
    selected = option_menu("Ruthelde extension", ["Home", 'Viewer', 'Experimentation', 'Detector', 'Calculation', 'Target', 'Differential Evolution', 'File Upload'],
                           icons=['house', 'lightbulb', 'eyedropper', 'camera-video', 'calculator', 'layers', 'virus', 'upload'], default_index=0)

if selected == "Home":
    home.show()
elif selected == "Viewer":
    viewer.show()
elif selected == "Experimentation":
    experimental.show()
elif selected == "Detector":
    detector.show()
elif selected == "Calculation":
    calculation.show()
elif selected == "Target":
    target.show()
elif selected == "Differential Evolution":
    differential_evolution.show()
elif selected == "File Upload":
    file_upload.show()

