import streamlit as st
import src.logic.file as file  # Assuming you have a similar file handling module for differential evolution


def show():
    st.title("Differential Evolution Setup")

    st.markdown("### Select Differential Evolution Setup")
    selected = st.selectbox("", file.get_all_de_setup_names())  # Adjust function name as per your module

    de_setup_json = file.get_de_setup_json_from_file(selected)  # Adjust function name as per your module

    st.markdown("### Change Name")
    new_name = st.text_input("", value=selected.split('.')[0])

    # Header
    st.header("Setup")

    # Create two columns for Differential Evolution settings
    col1, col2 = st.columns(2)

    # Column 1
    with col1:
        de_setup_json['populationSize'] = st.number_input("Population Size", value=de_setup_json['populationSize'], min_value=1, max_value=100, step=1)
        de_setup_json['F'] = st.number_input("F", value=de_setup_json['F'], min_value=0.0, max_value=1.0, step=0.1)
        de_setup_json['CR'] = st.number_input("CR", value=de_setup_json['CR'], min_value=0.0, max_value=1.0, step=0.1)
        de_setup_json['THR'] = st.number_input("THR", value=de_setup_json['THR'], min_value=0.0, max_value=1.0, step=0.1)
        de_setup_json['numBins'] = st.number_input("Number of Bins", value=de_setup_json['numBins'], min_value=1, max_value=10, step=1)

    # Column 2
    with col2:
        de_setup_json['startCH'] = st.number_input("Start Channel", value=de_setup_json['startCH'], min_value=0, max_value=10000, step=10)
        de_setup_json['endCH'] = st.number_input("End Channel", value=de_setup_json['endCH'], min_value=0, max_value=10000, step=10)
        de_setup_json['endTime'] = st.number_input("End Time", value=de_setup_json['endTime'], min_value=0.0, max_value=100.0, step=0.1)
        de_setup_json['endFitness'] = st.number_input("End Fitness", value=de_setup_json['endFitness'], min_value=0.0, max_value=100.0, step=0.1)
        de_setup_json['endGeneration'] = st.number_input("End Generation", value=de_setup_json['endGeneration'], min_value=0.0, max_value=100.0, step=1.0)
        de_setup_json['isotopeTime'] = st.number_input("Isotope Time", value=de_setup_json['isotopeTime'], min_value=0.0, max_value=100.0, step=0.1)

    # Button Layout
    col3_1, col3_2, col3_3 = st.columns([0.06, 0.07, 0.9])

    with col3_1:
        if st.button("Save"):
            if new_name == "default" or selected == "default.json":
                pass
            else:
                if new_name != selected.split('.')[0]:
                    file.delete_de_setup_json_from_file(selected)  # Adjust function name as per your module
                    file.save_de_setup_json_to_file(new_name + ".json", de_setup_json)  # Adjust function name as per your module
                else:
                    file.save_de_setup_json_to_file(selected, de_setup_json)  # Adjust function name as per your module

    with col3_2:
        if st.button("Delete"):
            if selected != "default.json":
                file.delete_de_setup_json_from_file(selected)  # Adjust function name as per your module

    with col3_3:
        if st.button("Create New"):
            if new_name != "default":
                file.save_de_setup_json_to_file(new_name + ".json", de_setup_json)  # Adjust function name as per your module
