import streamlit as st
from streamlit_option_menu import option_menu

import src.logic.helper as helper
import src.logic.file as file


def change_target_in_state():
    st.session_state["target"] = file.get_target_setup_json_from_file(st.session_state["target_setup_menu"])


def show():
    st.title("Target setup")

    # H5 title that says 'Select experimental setup'
    st.markdown("### Select target setup")

    # Dropdown menu to select the target setup
    selected_target = st.selectbox("", file.get_all_target_setup_names(), on_change=change_target_in_state, key='target_setup_menu')

    # Load the target setup json from the file
    # target_setup_json = file.get_target_setup_json_from_file(selected_target)
    target_setup_json = st.session_state["target"]

    st.markdown("### Change name")

    # Change name of the target setup
    new_name = st.text_input("", value=selected_target.split('.')[0])

    # Header
    st.header("Target")

    # Create 3 columns
    col1, col2, col3 = st.columns(3)

    # Column 1
    with col1:

        # 2 columns for buttons
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            # Add new layer button
            if st.button("Add new layer"):
                st.session_state["target"]["layerList"].append({
                    "arealDensity": 0,
                    "min_AD": 0,
                    "max_AD": 0,
                    "massDensity": 0,
                    "thickness": 0,
                    "elementList": [
                        {
                            "isotopeList": [
                                {
                                    "mass": 0,
                                    "abundance": 0
                                }
                            ],
                            "atomicNumber": 0,
                            "arealDensity": 0,
                            "ratio": 0,
                            "min_ratio": 0,
                            "max_ratio": 0
                        }
                    ]
                })

        with col1_2:
            if st.button("Remove layer"):
                remove_selected = st.session_state["target_layer_menu"]
                selected_remove = helper.get_target_layer_index_from_menu_list(remove_selected)
                st.session_state["target"]["layerList"].pop(selected_remove)

        selected = option_menu("Layers", helper.get_target_layer_menu_list(target_setup_json) or [], default_index=0, key='target_layer_menu')
        selected_index = helper.get_target_layer_index_from_menu_list(selected)


        # Add layer properties
        areal_density = st.text_input("Areal Density",
                                      value=st.session_state["target"]["layerList"][selected_index]["arealDensity"])
        # Create 2 columns for min and max areal density
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            min_AD = st.text_input("Min areal density",
                                   value=st.session_state["target"]["layerList"][selected_index]["min_AD"])
        with col1_2:
            max_AD = st.text_input("Max areal density",
                                   value=st.session_state["target"]["layerList"][selected_index]["max_AD"])
        mass_density = st.text_input("Mass Density",
                                     value=st.session_state["target"]["layerList"][selected_index]["massDensity"])
        thickness = st.text_input("Thickness",
                                  value=st.session_state["target"]["layerList"][selected_index]["thickness"])

        # Add save button
        if st.button("Save layer"):
            st.session_state["target"]["layerList"][selected_index]["arealDensity"] = areal_density
            st.session_state["target"]["layerList"][selected_index]["min_AD"] = min_AD
            st.session_state["target"]["layerList"][selected_index]["max_AD"] = max_AD
            st.session_state["target"]["layerList"][selected_index]["massDensity"] = mass_density
            st.session_state["target"]["layerList"][selected_index]["thickness"] = thickness

    # Column 2
    with col2:
        selected_element = None
        selected_element_index = 0
        # 2 columns for buttons
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            # Add new element button
            if st.button("Add new element"):
                st.session_state["target"]["layerList"][selected_index]["elementList"].append({
                    "isotopeList": [
                        {
                            "mass": 0,
                            "abundance": 0
                        }
                    ],
                    "atomicNumber": 0,
                    "arealDensity": 0,
                    "ratio": 0,
                    "min_ratio": 0,
                    "max_ratio": 0
                })

        with col2_2:
            if st.button("Remove element"):
                remove_selected = st.session_state["target_element_menu"]
                selected_remove = helper.get_element_index_from_menu_list(target_setup_json, remove_selected, selected_index)
                st.session_state["target"]["layerList"][selected_index]["elementList"].pop(selected_remove)
                if len(st.session_state["target"]["layerList"][selected_index]["elementList"]) == 0:
                    selected_element = None
        if len(st.session_state["target"]["layerList"][selected_index]["elementList"]) == 0:
            st.warning("No elements in layer")
        else:

            selected_element = option_menu("Elements", helper.get_elememt_menu_list(target_setup_json, selected_index), default_index=0, key='target_element_menu')
            selected_element_index = helper.get_element_index_from_menu_list(target_setup_json, selected_element, selected_index)

            # Add element properties
            atomic_number = st.text_input("Atomic number",
                                          value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["atomicNumber"])
            areal_density_element = st.text_input("Areal density",
                                                  value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["arealDensity"])
            ratio = st.text_input("Ratio",
                                    value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["ratio"])
            # Create 2 columns for min and max ratio
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                min_ratio = st.text_input("Min ratio",
                                           value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["min_ratio"])

            with col2_2:
                max_ratio = st.text_input("Max ratio",
                                           value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["max_ratio"])

            # Add save button
            if st.button("Save element"):
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["atomicNumber"] = atomic_number
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["arealDensity"] = areal_density_element
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["ratio"] = ratio
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["min_ratio"] = min_ratio
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["max_ratio"] = max_ratio

    # Column 3
    with col3:
        selected_isotope = None
        if selected_element is None:
            selected_isotope = None
        # 2 columns for buttons
        col3_1, col3_2 = st.columns(2)

        with col3_1:
            # Add new isotope button
            if st.button("Add new isotope"):
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"].append({
                    "mass": 0,
                    "abundance": 0
                })

        with col3_2:
            if st.button("Remove isotope"):
                remove_selected = st.session_state["target_isotope_menu"]
                selected_remove = helper.get_isotope_index_from_menu_list(target_setup_json, remove_selected, selected_index, selected_element_index)
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"].pop(selected_remove)
                if len(st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"]) == 0:
                    selected_isotope = None
        if selected_element_index and len(st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"]) == 0:
            st.warning("No isotopes in element")
        else:
            selected_isotope = option_menu("Isotopes", helper.get_isotope_menu_list(target_setup_json, selected_index, selected_element_index), default_index=0, key='target_isotope_menu')
            selected_isotope_index = helper.get_isotope_index_from_menu_list(target_setup_json, selected_isotope, selected_index, selected_element_index)

            # Add isotope properties
            mass = st.text_input("Mass",
                                    value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"][selected_isotope_index]["mass"])
            abundance = st.text_input("Abundance",
                                        value=st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"][selected_isotope_index]["abundance"])

            # Add save button
            if st.button("Save isotope"):
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"][selected_isotope_index]["mass"] = mass
                st.session_state["target"]["layerList"][selected_index]["elementList"][selected_element_index]["isotopeList"][selected_isotope_index]["abundance"] = abundance

    # Create 3 columns (10%, 10%, 80%)
    col4_1, col4_2, col4_3 = st.columns([0.10, 0.11, 0.8])
    with col4_1:
        # Save button
        if st.button("Save target"):
            # If new_name or selected is default, pass
            if new_name == "default" or selected_target == "default.json":
                pass
            else:
                # Check if name changed
                if new_name != selected_target.split('.')[0]:
                    # Delete old file
                    file.delete_target_setup_json_from_file(selected_target)
                    # Save new file
                    file.save_target_setup_json_to_file(new_name + ".json", st.session_state["target"])
                else:
                    file.save_target_setup_json_to_file(selected_target, st.session_state["target"])

    with col4_2:
        # Delete button
        if st.button("Delete target"):
            # If selected is default, pass
            if selected_target == "default.json":
                pass
            else:
                file.delete_target_setup_json_from_file(selected_target)

    with col4_3:
        # New button
        if st.button("Create new target"):
            if new_name == "default":
                pass
            else:
                file.save_target_setup_json_to_file(new_name + ".json", st.session_state["target"])
