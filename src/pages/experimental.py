import streamlit as st
import src.logic.file as file


def show():

    st.title("Experimental setup")

    # H5 title that says 'Select experimental setup'
    st.markdown("### Select experimental setup")

    # Dropdown menu to select the experimental setup
    selected = st.selectbox("", file.get_all_experimental_setup_names())

    # Load the experimental setup json from the file
    experimental_setup_json = file.get_experimental_setup_json_from_file(selected)

    st.markdown("### Change name")

    # Change name of the experimental setup
    new_name = st.text_input("", value=selected.split('.')[0])

    # Define the number of input groups in each column
    num_columns = 2

    # Create two columns
    col1, col2 = st.columns(num_columns)

    # Create input fields for each group in the first column
    with col1:
        st.header("Incident Beam")
        experimental_setup_json['E0'] = st.number_input("Energy E0 (keV)", value=experimental_setup_json['E0'], step=1.0)
        experimental_setup_json['deltaE0'] = st.number_input("Energy spread dE0 (keV)", value=experimental_setup_json['deltaE0'], step=1.0)
        experimental_setup_json['charge'] = st.number_input("Charge (µC)", value=experimental_setup_json['charge'], step=1.0)
        # Create new columns for min and max charge
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            experimental_setup_json['minCharge'] = st.number_input("Min charge (µC)", value=experimental_setup_json['minCharge'], step=1.0)
        with col1_2:
            experimental_setup_json['maxCharge'] = st.number_input("Max charge (µC)", value=experimental_setup_json['maxCharge'], step=1.0)
        st.subheader("Projectile")
        # Create new columns for Z, M and E
        col1_3, col1_4, col1_5 = st.columns(3)
        with col1_3:
            experimental_setup_json['projectile']['Z'] = st.number_input("Z", value=experimental_setup_json['projectile']['Z'], step=1)
        with col1_4:
            experimental_setup_json['projectile']['M'] = st.number_input("M", value=experimental_setup_json['projectile']['M'], step=1.0)
        with col1_5:
            experimental_setup_json['projectile']['E'] = st.number_input("E (keV)", value=experimental_setup_json['projectile']['E'], step=1.0)


    # Create input fields for each group in the second column
    with col2:
        st.header("Geometry")
        experimental_setup_json['alpha'] = st.number_input("Incident angle alpha (deg)", value=experimental_setup_json['alpha'], step=1.0)
        experimental_setup_json['theta'] = st.number_input("Scattering angle theta (deg)", value=experimental_setup_json['theta'], step=1.0)
        experimental_setup_json['beta'] = st.number_input("Detector angle beta (deg)", value=experimental_setup_json['beta'], step=1.0)

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
                    file.delete_experimental_setup_json_from_file(selected)
                    # Save new file
                    file.save_experimental_setup_json_to_file(new_name + ".json", experimental_setup_json)
                else:
                    # Save file
                    file.save_experimental_setup_json_to_file(selected, experimental_setup_json)

    with col3_2:
        # Delete button
        if st.button("Delete"):
            # If selected is default, pass
            if selected == "default.json":
                pass
            else:
                file.delete_experimental_setup_json_from_file(selected)

    with col3_3:
        # New button
        if st.button("Create new"):
            # If new_name is default, pass
            if new_name == "default":
                pass
            else:
                file.save_experimental_setup_json_to_file(new_name + ".json", experimental_setup_json)
