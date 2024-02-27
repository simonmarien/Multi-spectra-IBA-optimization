import streamlit as st
import src.logic.command_line as cmd
import src.logic.input as input
import src.logic.spectra_reader as spectra_reader
import src.logic.convert as convert
import src.logic.helper as helper
import src.logic.file as file
import src.logic.client as client
import src.widgets.target as target_widget
import matplotlib.pyplot as plt


def show():
    # st.title("Home")
    tab1, tab2, tab3 = st.tabs(["Simulation", "Optimization", "Optimization with multiple spectra"])

    with tab1:

        # Simulate size 4 markdown header
        st.markdown("#### Simulation")

        st.markdown("##### Experimental setup")
        # Have dropdown menu to select the experimental setup
        selected_experimental_setup_sim = st.selectbox("Select experimental setup", file.get_all_experimental_setup_names_without_default() or [])
        # Have a show experimental setup button
        if st.button("Show experimental setup"):
            st.table(helper.flatten(file.get_experimental_setup_json_from_file(selected_experimental_setup_sim)))

        st.markdown("##### Detector setup")
        # Have dropdown menu to select the detector setup
        selected_detector_setup_sim = st.selectbox("Select detector setup", file.get_all_detector_setup_names_without_default() or [])
        # Have a show detector setup button
        if st.button("Show detector setup"):
            # Show detectorSetup data in a pretty way
            st.table(helper.flatten(file.get_detector_setup_json_from_file(selected_detector_setup_sim)))

        st.markdown("##### Calculation setup")
        # Have dropdown menu to select the calculation setup
        selected_calculation_setup_sim = st.selectbox("Select calculation setup", file.get_all_calculation_setup_names_without_default() or [])
        # Have a show calculation setup button
        if st.button("Show calculation setup"):
            # Show calculationSetup data in a pretty way
            cal_setup = file.get_calculation_setup_json_from_file(selected_calculation_setup_sim)
            del cal_setup["crossSectionData"]
            st.table(cal_setup)

        st.markdown('##### Target')
        # Have a dropdown menu to select the target
        selected_target_sim = st.selectbox("Select target", file.get_all_target_setup_names_without_default() or [])

        # Have a show target button
        if st.button("Show target"):
            target_widget.display_target(file.get_target_json_from_file(selected_target_sim))

        # Generate spectra button
        if st.button("Generate spectra"):
            print("Generate spectra button pressed")
            input.save_sim_input_json(selected_experimental_setup_sim, selected_detector_setup_sim, selected_calculation_setup_sim, file.get_target_json_from_file(selected_target_sim))
            client.simulate_spectra()
            # cmd.simulate_spectrum()

    with tab2:

        # Optimize size 4 markdown header
        st.markdown("#### Optimization")

        # Radio button to choose Ruthelde or SciPy DE
        de_radio = st.radio("Choose DE implementation", ("Ruthelde", "SciPy"))

        st.markdown("##### Spectra selection")
        # Select spectra dropdown
        selected_spectra_opt = st.selectbox("Select spectra", spectra_reader.list_spectra_file_names() or [])

        # Have a show spectrum button
        if st.button("Show spectrum"):
            # Get the selected spectra data list [{name: name, data: data}]
            data = spectra_reader.get_spectra_data(selected_spectra_opt)

            fig, ax = plt.subplots()

            # Loop through the data
            for spectra in data:
                ax.plot(spectra["data"], label=spectra["name"])

            # Add legend
            plt.legend()

            # Add title
            plt.title("Spectra")

            # Add to streamlit
            st.pyplot(fig)

        st.markdown("##### Experimental setup")
        # Have dropdown menu to select the experimental setup
        selected_experimental_setup_opt = st.selectbox("Select experimental setup ", file.get_all_experimental_setup_names_without_default() or [])
        # Have a show experimental setup button
        if st.button("Show experimental setup "):
            st.table(helper.flatten(file.get_experimental_setup_json_from_file(selected_experimental_setup_opt)))

        st.markdown("##### Detector setup")
        # Have dropdown menu to select the detector setup
        selected_detector_setup_opt = st.selectbox("Select detector setup ", file.get_all_detector_setup_names_without_default() or [])
        # Have a show detector setup button
        if st.button("Show detector setup "):
            # Show detectorSetup data in a pretty way
            st.table(helper.flatten(file.get_detector_setup_json_from_file(selected_detector_setup_opt)))

        st.markdown("##### Calculation setup")
        # Have dropdown menu to select the calculation setup
        selected_calculation_setup_opt = st.selectbox("Select calculation setup ", file.get_all_calculation_setup_names_without_default() or [])
        # Have a show calculation setup button
        if st.button("Show calculation setup "):
            # Show calculationSetup data in a pretty way
            cal_setup = file.get_calculation_setup_json_from_file(selected_calculation_setup_opt)
            del cal_setup["crossSectionData"]
            st.table(cal_setup)

        st.markdown("##### DE parameter")

        # Have dropdown menu to select the de parameter
        selected_de_parameter_opt = st.selectbox("Select de parameter ", file.get_de_setup_names_without_default() or [])

        # Have a show de parameter button
        if st.button("Show de parameter"):
            st.table(helper.flatten(file.get_de_setup_json_from_file(selected_de_parameter_opt)))

        st.markdown('##### Target')

        # Have a dropdown menu to select the target
        selected_target = st.selectbox("Select target", file.get_all_target_setup_names_without_default() or [], key="target_opt")

        # Have a show target button
        if st.button("Show target", key="target_btn_opt"):
            target_widget.display_target(file.get_target_json_from_file(selected_target))

        # Generate sample button
        opt_button = st.button("Start Optimization")

        if opt_button:
            # input.save_opt_input_json(selected_spectra_opt, selected_experimental_setup_opt, selected_detector_setup_opt, selected_calculation_setup_opt, convert.get_de_parameter_from_state(), file.get_target_json_from_file(selected_target))
            now_str = file.optimize_single_spectra(selected_spectra_opt)
            # cmd.optimize_spectrum(now_str)

            # Create a placeholder for the progress bar
            progress_bar_placeholder = st.empty()
            status_text_placeholder = st.empty()

            progress_bar = progress_bar_placeholder.progress(0)

            end_generation = int(file.get_de_setup_json_from_file(selected_de_parameter_opt)['endGeneration'])
            # If Ruthelde is selected
            if de_radio == "Ruthelde":
                for progress in client.optimize_spectra(now_str):
                    if progress > int(end_generation - 2):
                        # Remove progress bar and status text
                        progress_bar_placeholder.empty()
                        status_text_placeholder.empty()
                        break
                    status_percentage = progress/end_generation
                    progress_bar.progress(status_percentage)
                    status_text_placeholder.text(f"Current progress: {status_percentage*100}%")
            # If SciPy is selected
            else:
                client.optimize_spectra_de(now_str)

            opt_input = file.get_opt_input_json_from_optimization_directory(now_str)
            target = file.get_target_from_generated_sample(now_str)
            input.save_sim_input_from_opt_input_json(opt_input, target)
            # cmd.simulate_optimized_spectrum(now_str)
            client.simulate_optimized_spectra(now_str)

    with tab3:

        # Optimize multiple size 4 markdown header
        st.markdown("## Optimize with multiple spectra")
        # Radio button to choose Ruthelde or SciPy DE
        de_radio_ms = st.radio("Choose DE implementation", ("Ruthelde", "SciPy"), key="de_radio_ms")

        # Select spectra dropdown
        selected_spectra_ms = st.multiselect("Select spectra", spectra_reader.list_spectra_file_names() or [])

        # Spectra setup list
        spectra_setup_list = []

        # For each selected spectra
        for index, spectra_name in enumerate(selected_spectra_ms):
            spectra_setup_list.append(multiple_optimization_widget(spectra_name, index))

        st.markdown("### Shared setup")

        st.markdown("##### Calculation setup")

        # Select calculation setup
        selected_calculation_setup_ms = st.selectbox("Select calculation setup ", file.get_all_calculation_setup_names_without_default() or [], key="calculation_setup")
        # Have a show calculation setup button
        if st.button("Show calculation setup ", key="calculation_setup_btn"):
            # Show calculationSetup data in a pretty way
            cal_setup = file.get_calculation_setup_json_from_file(selected_calculation_setup_ms)
            del cal_setup["crossSectionData"]
            st.table(cal_setup)

        st.markdown("##### DE parameter")

        # Have dropdown menu to select the de parameter
        selected_de_parameter_ms_opt = st.selectbox("Select de parameter ", file.get_de_setup_names_without_default() or [], key="de_parameter")

        # Have a show de parameter button
        if st.button("Show de parameter", key="de_parameter_btn"):
            st.table(helper.flatten(file.get_de_setup_json_from_file(selected_de_parameter_ms_opt)))

        st.markdown('##### Target')

        # Have a dropdown menu to select the target
        selected_target_ms_opt = st.selectbox("Select target", file.get_all_target_setup_names_without_default() or [], key="target_ms")

        # Have a show target button
        if st.button("Show target", key="target_btn"):
            target_widget.display_target(file.get_target_json_from_file(selected_target_ms_opt))

        # Generate sample button
        ms_opt_button =  st.button("Start optimization with multiple spectra", disabled=len(spectra_setup_list) <= 1)

        if ms_opt_button:
            # input.save_ms_opt_input_json(spectra_setup_list, selected_calculation_setup_ms, file.get_de_setup_json_from_file(selected_de_parameter_ms_opt), file.get_target_json_from_file(selected_target_ms_opt))
            now_str = file.optimize_multiple_spectra(selected_spectra_ms)

            # Create a placeholder for the progress bar
            progress_bar_placeholder_ms = st.empty()
            status_text_placeholder_ms = st.empty()

            progress_bar_ms = progress_bar_placeholder_ms.progress(0)

            end_generation = int(file.get_de_setup_json_from_file(selected_de_parameter_ms_opt)['endGeneration'])
            # If Ruthelde is selected
            if de_radio_ms == "Ruthelde":
                for progress in client.optimize_multiple_spectra(now_str):
                    if progress > int(end_generation - 2):
                        # Remove progress bar and status text
                        progress_bar_placeholder_ms.empty()
                        status_text_placeholder_ms.empty()
                        break
                    status_percentage = progress/end_generation
                    progress_bar_ms.progress(status_percentage)
                    status_text_placeholder_ms.text(f"Current progress: {status_percentage*100}%")
            # If SciPy is selected
            else:
                client.optimize_multiple_spectra_de(now_str)

            ms_opt_input = file.get_ms_opt_input_json_from_optimization_directory(now_str)
            target = file.get_target_from_generated_sample_ms(now_str)
            for index, _ in enumerate(selected_spectra_ms):
                input.save_sim_input_from_ms_opt_input_json(ms_opt_input, target, index)
                # cmd.simulate_optimized_spectrum(now_str)
                client.simulate_optimized_ms_spectra(now_str, file_prefix="s" + str(index+1) + "_")

            print("Generate multiple samples")


def multiple_optimization_widget(spectra_name, index):
    print(spectra_name, index)
    # Markdown header with the spectra name
    st.markdown("### Spectra " + str(index+1) + ": " + spectra_name)

    # Have a show spectrum button
    if st.button("Show spectrum", key=spectra_name):
        # Get the selected spectra data list [{name: name, data: data}]
        data = spectra_reader.get_spectra_data(spectra_name)

        fig, ax = plt.subplots()

        # Loop through the data
        for spectra in data:
            ax.plot(spectra["data"], label=spectra["name"])

        # Add legend
        plt.legend()

        # Add title
        plt.title("Spectra")

        # Add to streamlit
        st.pyplot(fig)

    st.markdown("##### Experimental setup")
    # Have dropdown menu to select the experimental setup
    selected_experimental_setup_ms = st.selectbox("Select experimental setup ", file.get_all_experimental_setup_names_without_default() or [], key=spectra_name + "experimental_setup")
    # Have a show experimental setup button
    if st.button("Show experimental setup ", key=spectra_name + "experimental_setup_btn"):
        st.table(helper.flatten(file.get_experimental_setup_json_from_file(selected_experimental_setup_ms)))

    st.markdown("##### Detector setup")
    # Have dropdown menu to select the detector setup
    selected_detector_setup_ms = st.selectbox("Select detector setup ", file.get_all_detector_setup_names_without_default() or [], key=spectra_name + "detector_setup")
    # Have a show detector setup button
    if st.button("Show detector setup ", key=spectra_name + "detector_setup_btn"):
        # Show detectorSetup data in a pretty way
        st.table(helper.flatten(file.get_detector_setup_json_from_file(selected_detector_setup_ms)))

    st.markdown("##### DE parameters spectra")

    # Fill in the de parameters
    deWeight = st.number_input("Weight", value=0.5, step=0.1, key=spectra_name + "deWeight")
    deStartCh = st.number_input("Start channel", value=100, step=1, key=spectra_name + "deStartCh")
    deEndCh = st.number_input("End channel", value=1000, step=1, key=spectra_name + "deEndCh")
    deNumBins = st.number_input("Number of bins", value=2, step=1, key=spectra_name + "deNumBins")

    # Return dictionary
    return {"spectra_name": spectra_name,
            "experimental_setup": selected_experimental_setup_ms,
            "detector_setup": selected_detector_setup_ms,
            "deWeight": deWeight,
            "deStartCh": deStartCh,
            "deEndCh": deEndCh,
            "deNumBins": deNumBins}

