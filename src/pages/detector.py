import streamlit as st
import src.logic.file as file


def show():
    st.title("Detector Setup")

    # H5 title that says 'Select detector setup'
    st.markdown("### Select detector setup")

    # Dropdown menu to select the detector setup
    selected = st.selectbox("", file.get_all_detector_setup_names())

    # Load the detector setup json from the file
    detector_setup_json = file.get_detector_setup_json_from_file(selected)

    st.markdown("### Change name")

    # Change name of the detector setup
    new_name = st.text_input("", value=selected.split('.')[0])

    # 2 Columns for the detector setup
    col1, col2 = st.columns(2)

    # Column 1
    with col1:
        # Calibration
        st.header("Calibration")
        detector_setup_json['calibration']['factor'] = st.number_input("Calibration factor", value=detector_setup_json['calibration']['factor'], step=0.1)
        # Create new columns for min and max calibration factor
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            detector_setup_json['calibration']['factor_min'] = st.number_input("Min calibration factor", value=detector_setup_json['calibration']['factor_min'], step=0.1)
        with col1_2:
            detector_setup_json['calibration']['factor_max'] = st.number_input("Max calibration factor", value=detector_setup_json['calibration']['factor_max'], step=0.1)
        detector_setup_json['calibration']['offset'] = st.number_input("Calibration offset", value=detector_setup_json['calibration']['offset'], step=1.0)
        # Create new columns for min and max calibration offset
        col1_3, col1_4 = st.columns(2)
        with col1_3:
            detector_setup_json['calibration']['offset_min'] = st.number_input("Min calibration offset", value=detector_setup_json['calibration']['offset_min'], step=1.0)
        with col1_4:
            detector_setup_json['calibration']['offset_max'] = st.number_input("Max calibration offset", value=detector_setup_json['calibration']['offset_max'], step=1.0)

    # Column 2
    with col2:
        # Resolution
        st.header("Resolution")
        detector_setup_json['resolution'] = st.number_input("Resolution", value=detector_setup_json['resolution'], step=0.1)
        # Create new columns for min and max resolution
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            detector_setup_json['minRes'] = st.number_input("Min resolution", value=detector_setup_json['minRes'], step=0.1)
        with col2_2:
            detector_setup_json['maxRes'] = st.number_input("Max resolution", value=detector_setup_json['maxRes'], step=0.1)
        detector_setup_json['solidAngle'] = st.number_input("Solid angle", value=detector_setup_json['solidAngle'], step=0.1)

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
                    # Delete old file
                    file.delete_detector_setup_json_from_file(selected)
                    # Save new file
                    file.save_detector_setup_json_to_file(new_name + ".json", detector_setup_json)
                else:
                    file.save_detector_setup_json_to_file(selected, detector_setup_json)

    with col3_2:
        # Delete button
        if st.button("Delete"):
            # If selected is default, pass
            if selected == "default.json":
                pass
            else:
                file.delete_detector_setup_json_from_file(selected)

    with col3_3:
        # New button
        if st.button("Create new"):
            if new_name == "default":
                pass
            else:
                file.save_detector_setup_json_to_file(new_name + ".json", detector_setup_json)
