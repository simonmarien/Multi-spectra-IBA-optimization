# Convert optimization object structure to GA object structure
from src.logic import file
from src.logic import spectra_reader
from src.logic import client
from src.GA import log
import json
import numpy as np

OLD = False


def convert_opt_input_to_ga_input(selected_spectra, experimental_setup, detector_setup, calculation_setup, de_parameter, target):
    """
    Converts the optimization input to the GA input (var params, fixed params, reference spectra)
    :param selected_spectra:
    :param experimental_setup:
    :param detector_setup:
    :param calculation_setup:
    :param de_parameter:
    :param target:
    :return:
    """
    # Create the input dictionary
    input_dict = {"target": target,
                  "experimentalSpectrum": spectra_reader.get_spectra_data(selected_spectra)[0],
                  "experimentalSetup": file.get_experimental_setup_json_from_file(experimental_setup),
                  "detectorSetup": file.get_detector_setup_json_from_file(detector_setup),
                  "calculationSetup": file.get_calculation_setup_json_from_file(calculation_setup),
                  "deParameter": de_parameter}

    # Get variable parameters
    var_params = get_variable_parameters(input_dict)
    # Get fixed parameters
    fixed_params = input_dict
    # Get reference spectra
    reference_spectra = input_dict["experimentalSpectrum"]

    return var_params, fixed_params, reference_spectra


def get_variable_parameters(input_dict):
    """
    Returns the variable parameters from the input dictionary
    :param input_dict:
    :return:
    """
    var_params = []
    ratio_indices = []
    current_index = 0
    # Experimental setup charge
    var_params.append(input_dict["experimentalSetup"]["charge"])

    # Detector setup calibration factor
    var_params.append(input_dict["detectorSetup"]["calibration"]["factor"])

    # Detector setup calibration offset
    var_params.append(input_dict["detectorSetup"]["calibration"]["offset"])

    # Detector setup resolution
    var_params.append(input_dict["detectorSetup"]["resolution"])

    current_index += 3

    # Target model
    # For each layer in the target model
    for layer in input_dict["target"]["layerList"]:
        # If there are more than 1 element in the layer
        if OLD or len(layer["elementList"]) > 1:
            # Add arealDensity
            var_params.append(layer["arealDensity"])
            current_index += 1
            ratio_list = []
            # For each element in the layer
            for element in layer["elementList"]:
                # Add ratio
                var_params.append(element["ratio"])
                current_index += 1
                ratio_list.append(current_index)
            ratio_indices.append(ratio_list)

    return var_params, ratio_indices


def set_variable_parameters(input_dict, var_params, ratio_indices):
    """
    Sets the variable parameters in the input dictionary
    :param input_dict:
    :param var_params:
    :return:
    """

    # Experimental setup charge
    input_dict["experimentalSetup"]["charge"] = var_params[0]

    # Detector setup calibration factor
    input_dict["detectorSetup"]["calibration"]["factor"] = var_params[1]

    # Detector setup calibration offset
    input_dict["detectorSetup"]["calibration"]["offset"] = var_params[2]

    # Detector setup resolution
    input_dict["detectorSetup"]["resolution"] = var_params[3]

    index = 4
    layer = 0

    # Target model
    for ratio_indice in ratio_indices:
        # Add arealDensity
        input_dict["target"]["layerList"][layer]["arealDensity"] = var_params[index]
        index += 1
        # For each element in the layer
        for i in range(len(ratio_indice)):
            # Add ratio
            input_dict["target"]["layerList"][layer]["elementList"][i]["ratio"] = var_params[index]
            # Add areal density
            input_dict["target"]["layerList"][layer]["elementList"][i]["arealDensity"] = var_params[index] * input_dict["target"]["layerList"][layer]["arealDensity"]
            index += 1
        layer += 1
    return input_dict


def get_reference_spectra(input_dict):
    """
    Returns the reference spectra from the input dictionary
    :param input_dict:
    :return:
    """
    reference_spectra = input_dict["experimentalSpectrum"]
    return reference_spectra


def get_start_and_end_channel(input_dict):
    """
    Returns the start and end channel of the de parameter
    :param input_dict:
    :return:
    """
    start_channel = input_dict["deParameter"]["startCH"]
    end_channel = input_dict["deParameter"]["endCH"]
    return start_channel, end_channel


def get_bounds(input_dict):
    """
    Get the bounds (max, min) for the variable parameters
    :param var_params:
    :return:
    """
    bounds = []
    # Experimental setup charge
    bounds.append((input_dict["experimentalSetup"]["minCharge"], input_dict["experimentalSetup"]["maxCharge"]))
    # Detector setup calibration factor
    bounds.append((input_dict["detectorSetup"]["calibration"]["factor_min"], input_dict["detectorSetup"]["calibration"]["factor_max"]))
    # Detector setup calibration offset
    bounds.append((input_dict["detectorSetup"]["calibration"]["offset_min"], input_dict["detectorSetup"]["calibration"]["offset_max"]))
    # Detector setup resolution
    bounds.append((input_dict["detectorSetup"]["minRes"], input_dict["detectorSetup"]["maxRes"]))
    # Target model
    # For each layer in the target model
    for layer in input_dict["target"]["layerList"]:
        # If there are more than 1 element in the layer
        if OLD or len(layer["elementList"]) > 1:
            # Add arealDensity
            bounds.append((layer["min_AD"], layer["max_AD"]))
            # For each element in the layer
            for element in layer["elementList"]:
                # Add ratio
                bounds.append((element["min_ratio"], element["max_ratio"]))

    return bounds


def simulate_spectra(input_dict, logger=None):
    """
    Simulates the spectra with the given parameters
    :param input_dict:
    :param logger:
    :return:
    """
    # Simulate the spectra
    simulated_spectra = client.simulate_spectra_from_dict(input_dict, logger=logger)
    # Check if the spectra is not None
    if simulated_spectra is None:
        return None
    # Convert to json
    simulated_spectra = json.loads(simulated_spectra)
    # Get the spectra data
    simulated_spectra = simulated_spectra["spectra"][0]["data"]
    return simulated_spectra


def simulate_spectra_return_all(input_dict, logger=None):
    """
    Simulates the spectra with the given parameters
    :param input_dict:
    :param logger:
    :return:
    """
    # Simulate the spectra
    simulated_spectra = client.simulate_spectra_from_dict(input_dict, logger=logger)
    # Check if the spectra is not None
    if simulated_spectra is None:
        return None
    # Convert to json
    simulated_spectra = json.loads(simulated_spectra)
    return simulated_spectra


def get_opt_from_file(opt_file):
    """
    Returns the optimization input from the given file
    :param opt_file:
    :return:
    """
    with open(opt_file) as json_file:
        opt_input = json.load(json_file)
    return opt_input


def get_de_parameter_dict_from_opt(opt_input):
    """

    :param opt_input:
    :return:
    """
    return opt_input["deParameter"]


def get_de_parameters_from_opt(de_parameters):
    """
    Returns the de parameters from the optimization input
    :param de_parameters:
    :return:
    """
    pop_size = de_parameters["populationSize"]
    max_iter = int(de_parameters["endGeneration"])
    mutation_factor = de_parameters["F"]
    crossover_rate = de_parameters["CR"]
    threshold = de_parameters["THR"]
    return pop_size, max_iter, mutation_factor, crossover_rate, threshold


# Test
# opt = get_opt_from_file("../../files/input/opt_input.json")
# # Simulate the spectra
# simulated_spectra = simulate_spectra(opt)
# print(simulated_spectra)
# # Get the variable parameters
# var_params = get_variable_parameters(opt)
# print(var_params)


