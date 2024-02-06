import json
import streamlit as st
import src.logic.convert as convert
import src.logic.spectra_reader as spectra_reader
import src.logic.file as file


def save_sim_input_json(experimental_setup, detector_setup, calculation_setup, target):
    # Create the input dictionary
    input_dict = {"target": target,
                  "experimentalSetup": file.get_experimental_setup_json_from_file(experimental_setup),
                  "detectorSetup": file.get_detector_setup_json_from_file(detector_setup),
                  "calculationSetup": file.get_calculation_setup_json_from_file(calculation_setup)}

    # Save the input dictionary as a json file at ../../files/input/sim_input.json
    with open("files/input/sim_input.json", "w") as outfile:
        json.dump(input_dict, outfile, indent=4)
    print("Saved sim_input.json file")


def save_opt_input_json(selected_spectra, experimental_setup, detector_setup, calculation_setup, de_parameter, target):
    # Create the input dictionary
    input_dict = {"target": target,
                  "experimentalSpectrum": spectra_reader.get_spectra_data(selected_spectra)[0],
                  "experimentalSetup": file.get_experimental_setup_json_from_file(experimental_setup),
                  "detectorSetup": file.get_detector_setup_json_from_file(detector_setup),
                  "calculationSetup": file.get_calculation_setup_json_from_file(calculation_setup),
                  "deParameter": de_parameter}

    # Save the input dictionary as a json file at ../../files/input/opt_input.json
    with open("files/input/opt_input.json", "w") as outfile:
        json.dump(input_dict, outfile, indent=4)


def save_sim_input_from_opt_input_json(opt_input, target):
    # Create the input dictionary
    input_dict = {"target": target,
                  "experimentalSetup": opt_input["experimentalSetup"],
                  "detectorSetup": opt_input["detectorSetup"],
                  "calculationSetup": opt_input["calculationSetup"]}

    # Save the input dictionary as a json file at ../../files/input/sim_input.json
    with open("files/input/sim_input.json", "w") as outfile:
        json.dump(input_dict, outfile, indent=4)
    print("Saved sim_input.json file")


def save_ms_opt_input_json(selected_spectra_dictionary, calculation_setup, de_parameter, target):
    """
    Saves the input json file for the MS optimization
    :param selected_spectra_dictionary: [{'spectra_name': 'RBS23_152_01B_d01.txt', 'experimental_setup': 'test_setupee.json', 'detector_setup': 'test.json', 'deWeight': 0.5, 'deStartCh': 100, 'deEndCh': 1005, 'deNumBins': 5}]
    :param calculation_setup:
    :param de_parameter:
    :return:
    """
    measurement_list = []
    for spectra in selected_spectra_dictionary:
        measurement_list.append({
            "spectrum": spectra_reader.get_spectra_data(spectra["spectra_name"])[0],
            "experimentalSetup": file.get_experimental_setup_json_from_file(spectra["experimental_setup"]),
            "detectorSetup": file.get_detector_setup_json_from_file(spectra["detector_setup"]),
            "deWeight": spectra["deWeight"],
            "deStartCh": spectra["deStartCh"],
            "deEndCh": spectra["deEndCh"],
            "deNumBins": spectra["deNumBins"]
        })

    # Create the input dictionary
    input_dict = {"target": target,
                    "measurements": measurement_list,
                    "calculationSetup": file.get_calculation_setup_json_from_file(calculation_setup),
                    "deParameter": de_parameter}

    # Save the input dictionary as a json file at ../../files/input/ms_opt_input.json
    with open("files/input/ms_opt_input.json", "w") as outfile:
        json.dump(input_dict, outfile, indent=4)
    print("Saved ms_opt_input.json file")


def save_sim_input_from_ms_opt_input_json(ms_opt_input, target, index):
    # Create the input dictionary
    input_dict = {"target": target,
                  "experimentalSetup": ms_opt_input["measurements"][index]["experimentalSetup"],
                  "detectorSetup": ms_opt_input["measurements"][index]["detectorSetup"],
                  "calculationSetup": ms_opt_input["calculationSetup"]}

    # Save the input dictionary as a json file at ../../files/input/sim_input.json
    with open("files/input/sim_input.json", "w") as outfile:
        json.dump(input_dict, outfile, indent=4)
    print("Saved sim_input.json file")

