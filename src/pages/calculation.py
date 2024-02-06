import streamlit as st
import src.logic.file as file


def show():
    st.title("Calculation Setup")

    # H5 title that says 'Select calculation setup'
    st.markdown("### Select calculation setup")

    # Dropdown menu to select the calculation setup
    selected = st.selectbox("", file.get_all_calculation_setup_names())

    # Load the calculation setup json from the file
    calculation_setup_json = file.get_calculation_setup_json_from_file(selected)

    st.markdown("### Change name")

    # Change name of the calculation setup
    new_name = st.text_input("", value=selected.split('.')[0])

    # Header
    st.header("Setup")

    # Create two columns
    col1, col2 = st.columns(2)

    # Column 1
    with col1:
        calculation_setup_json['stoppingData'] = st.text_input("Stopping data", value=calculation_setup_json['stoppingData'])
        calculation_setup_json['crossSectionData'] = st.text_input("Cross section data", value=calculation_setup_json['crossSectionData'])
        calculation_setup_json['numberOfChannels'] = st.number_input("Number of channels", value=calculation_setup_json['numberOfChannels'], step=1)
        calculation_setup_json['stoppingPowerCalculationMode'] = st.selectbox("Stopping power calculation mode", options=["ZB", "ZBL", "Bethe", "BetheBloch"], index=0)  # TODO: fix index
        calculation_setup_json['useLookUpTable'] = st.checkbox("Use look up table", value=calculation_setup_json['useLookUpTable'])
        calculation_setup_json['simulateIsotopes'] = st.checkbox("Simulate isotopes", value=calculation_setup_json['simulateIsotopes'])
        calculation_setup_json['showIsotopes'] = st.checkbox("Show isotopes", value=calculation_setup_json['showIsotopes'])

    # Column 2
    with col2:
        calculation_setup_json['compoundCalculationMode'] = st.selectbox("Compound calculation mode", options=["BRAGG", "BetheBloch"], index=0)
        calculation_setup_json['screeningMode'] = st.selectbox("Screening mode", options=["ANDERSON", "ZBL"], index=0)
        calculation_setup_json['stragglingMode'] = st.selectbox("Straggling mode", options=["CHU", "BetheBloch"], index=0)
        calculation_setup_json['chargeFractionMode'] = st.selectbox("Charge fraction mode", options=["LINEAR", "ZIEGLER", "BetheBloch"], index=0)
        calculation_setup_json['showLayers'] = st.checkbox("Show layers", value=calculation_setup_json['showLayers'])
        calculation_setup_json['showElements'] = st.checkbox("Show elements", value=calculation_setup_json['showElements'])

    # Create 3 columns (10%, 10%, 80%)
    col3_1, col3_2, col3_3 = st.columns([0.06, 0.07, 0.9])

    with col3_1:
        # Save button
        if st.button("Save"):
            # If new_name or selected is default, pass
            if new_name == "default" or selected == "default.json":
                pass
            else:
                # Check if name changed
                if new_name != selected.split('.')[0]:
                    # Delete the old file
                    file.delete_calculation_setup_json_from_file(selected)
                    # Save the new file
                    file.save_calculation_setup_json_to_file(new_name + ".json", calculation_setup_json)
                else:
                    # Save the file
                    file.save_calculation_setup_json_to_file(selected, calculation_setup_json)

    with col3_2:
        # Delete button
        if st.button("Delete"):
            # If selected is default, pass
            if selected == "default.json":
                pass
            else:
                file.delete_calculation_setup_json_from_file(selected)

    with col3_3:
        # New button
        if st.button("Create new"):
            if new_name == "default":
                pass
            else:
                file.save_calculation_setup_json_to_file(new_name + ".json", calculation_setup_json)
