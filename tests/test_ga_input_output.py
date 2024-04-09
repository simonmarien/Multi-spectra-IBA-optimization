import json

import pytest
from unittest.mock import patch, mock_open

import src.GA.ga_input_output as gio

target_example = {
    "layerList": [
        {
            "elementList": [
                {
                    "isotopeList": [
                        {
                            "mass": 15.99492,
                            "abundance": 0.99762
                        },
                        {
                            "mass": 16.99913,
                            "abundance": 3.8E-4
                        },
                        {
                            "mass": 17.99916,
                            "abundance": 0.002
                        }
                    ],
                    "atomicNumber": 8,
                    "arealDensity": 371.42857142857144,
                    "ratio": 0.619047619047619,
                    "min_ratio": 0.0,
                    "max_ratio": 1.0
                },
                {
                    "isotopeList": [
                        {
                            "mass": 45.95263,
                            "abundance": 0.08
                        },
                        {
                            "mass": 46.95176,
                            "abundance": 0.073
                        },
                        {
                            "mass": 47.94795,
                            "abundance": 0.738
                        },
                        {
                            "mass": 48.94787,
                            "abundance": 0.055
                        },
                        {
                            "mass": 49.94479,
                            "abundance": 0.054
                        }
                    ],
                    "atomicNumber": 22,
                    "arealDensity": 114.28571428571429,
                    "ratio": 0.19047619047619047,
                    "min_ratio": 0.0,
                    "max_ratio": 1.0
                },
                {
                    "isotopeList": [
                        {
                            "mass": 83.91343,
                            "abundance": 0.0056
                        },
                        {
                            "mass": 85.90926,
                            "abundance": 0.0986
                        },
                        {
                            "mass": 86.90888,
                            "abundance": 0.07
                        },
                        {
                            "mass": 87.90561,
                            "abundance": 0.8258
                        }
                    ],
                    "atomicNumber": 38,
                    "arealDensity": 114.28571428571429,
                    "ratio": 0.19047619047619047,
                    "min_ratio": 0.0,
                    "max_ratio": 1.0
                }
            ],
            "arealDensity": 600.0,
            "massDensity": 2.2387428571428574,
            "thickness": 158.88411567718666,
            "min_AD": 600.0,
            "max_AD": 1300.0
        },
        {
            "elementList": [
                {
                    "isotopeList": [
                        {
                            "mass": 27.97693,
                            "abundance": 0.9223
                        },
                        {
                            "mass": 28.9765,
                            "abundance": 0.0467
                        },
                        {
                            "mass": 29.97377,
                            "abundance": 0.031
                        },
                        {
                            "mass": 31.97415,
                            "abundance": 0.0
                        }
                    ],
                    "atomicNumber": 14,
                    "arealDensity": 5300.0,
                    "ratio": 1.0,
                    "min_ratio": 0.0,
                    "max_ratio": 1.0
                }
            ],
            "arealDensity": 5300.0,
            "massDensity": 2.3212,
            "thickness": 1064.5197924146216,
            "min_AD": 5300.0,
            "max_AD": 5300.0
        }
    ]
}


# Test convert_opt_input_to_ga_input
@patch("src.logic.spectra_reader.get_spectra_data")
@patch("src.logic.file.get_experimental_setup_json_from_file")
@patch("src.logic.file.get_detector_setup_json_from_file")
@patch("src.logic.file.get_calculation_setup_json_from_file")
@patch("src.GA.ga_input_output.get_variable_parameters")
def test_convert_opt_input_to_ga_input(mock_get_variable_parameters, mock_get_calculation_setup_json_from_file,
                                       mock_get_detector_setup_json_from_file,
                                       mock_get_experimental_setup_json_from_file, mock_get_spectra_data):
    # Mock the return values
    mock_get_spectra_data.return_value = [{"name": "name", "data": [1, 2, 3]}]
    mock_get_experimental_setup_json_from_file.return_value = {"charge": 1}
    mock_get_detector_setup_json_from_file.return_value = {"calibration": {"factor": 1, "offset": 2}, "resolution": 3}
    mock_get_calculation_setup_json_from_file.return_value = "calculationSetup"
    mock_get_variable_parameters.return_value = [1, 2, 3, 4]
    # Create the input dictionary
    input_dict = {"target": "target",
                  "experimentalSpectrum": {"name": "name", "data": [1, 2, 3]},
                  "experimentalSetup": {"charge": 1},
                  "detectorSetup": {"calibration": {"factor": 1, "offset": 2}, "resolution": 3},
                  "calculationSetup": "calculationSetup",
                  "deParameter": "de_parameter"}

    # Get variable parameters
    var_params = gio.get_variable_parameters(input_dict)
    # Get fixed parameters
    fixed_params = input_dict
    # Get reference spectra
    reference_spectra = input_dict["experimentalSpectrum"]

    assert gio.convert_opt_input_to_ga_input("selected_spectra", "experimental_setup", "detector_setup",
                                             "calculation_setup", "de_parameter", "target") == (
               var_params, fixed_params, reference_spectra)


# Test get_variable_parameters
def test_get_variable_parameters():
    # Create the input dictionary
    input_dict = {"experimentalSetup": {"charge": 1},
                  "detectorSetup": {"calibration": {"factor": 1, "offset": 2}, "resolution": 3},
                  "target": target_example}

    assert gio.get_variable_parameters(input_dict) == (
        [1, 1, 2, 3, 600.0, 0.619047619047619, 0.19047619047619047], [[5, 6]])


# Test set_variable_parameters
def test_set_variable_parameters():
    # Create the input dictionary
    input_dict = {"experimentalSetup": {"charge": 1},
                  "detectorSetup": {"calibration": {"factor": 1, "offset": 2}, "resolution": 3},
                  "target": target_example}

    var_params = [4, 3, 2, 1, 400.0, 0.4, 0.6]
    ratio_indices = [[5, 6]]

    new_input_dict = gio.set_variable_parameters(input_dict, var_params, ratio_indices)
    assert new_input_dict["experimentalSetup"]["charge"] == 4
    assert new_input_dict["detectorSetup"]["calibration"]["factor"] == 3
    assert new_input_dict["detectorSetup"]["calibration"]["offset"] == 2
    assert new_input_dict["detectorSetup"]["resolution"] == 1
    assert new_input_dict["target"]["layerList"][0]["arealDensity"] == 400.0
    assert new_input_dict["target"]["layerList"][0]["elementList"][0]["ratio"] == 0.4
    assert new_input_dict["target"]["layerList"][0]["elementList"][1]["ratio"] == 0.6


# Test get_reference_spectra
def test_get_reference_spectra():
    # Create the input dictionary
    input_dict = {"experimentalSpectrum": {"name": "name", "data": [1, 2, 3]}}

    assert gio.get_reference_spectra(input_dict) == {"name": "name", "data": [1, 2, 3]}


# Test get_start_and_end_channel
def test_get_start_and_end_channel():
    # Create the input dictionary
    input_dict = {"deParameter": {"startCH": 1, "endCH": 2}}
    start_channel, end_channel = gio.get_start_and_end_channel(input_dict)
    assert start_channel == 1
    assert end_channel == 2


# Test get_bounds
def test_get_bounds():
    # Create the input dictionary
    input_dict = {
        "target": target_example,
        "experimentalSetup": {"charge": 1, "minCharge": 1, "maxCharge": 2},
        "detectorSetup": {"calibration": {"factor": 1, "factor_min": 0, "factor_max": 2, "offset": 2, "offset_min": 0,
                                          "offset_max": 2}, "resolution": 3, "minRes": 1, "maxRes": 2},
    }
    bounds = gio.get_bounds(input_dict)
    assert bounds == [(1, 2), (0, 2), (0, 2), (1, 2), (600.0, 1300.0), (0.0, 1.0), (0.0, 1.0)]


# Test simulate_spectra
@patch("src.logic.client.simulate_spectra_from_dict")
def test_simulate_spectra(mock_simulate_spectra_from_dict):
    # Mock the return value
    mock_simulate_spectra_from_dict.return_value = json.dumps({"spectra": [{"name": "name", "data": [1, 2, 3]}]})
    # Create the input dictionary
    input_dict = {"input_dict": "input_dict"}
    assert gio.simulate_spectra(input_dict, 9090) == [1, 2, 3]


# Test simulate_spectra_return_all
@patch("src.logic.client.simulate_spectra_from_dict")
def test_simulate_spectra_return_all(mock_simulate_spectra_from_dict):
    # Mock the return value
    mock_simulate_spectra_from_dict.return_value = json.dumps({"spectra": [{"name": "name", "data": [1, 2, 3]}]})
    # Create the input dictionary
    input_dict = {"input_dict": "input_dict"}
    assert gio.simulate_spectra_return_all(input_dict, 9090) == {"spectra": [{"name": "name", "data": [1, 2, 3]}]}


# Test get_opt_from_file
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_get_opt_from_file(mock_open):
    assert gio.get_opt_from_file("file") == {"key": "value"}


# Test get_de_parameter_dict_from_opt
def test_get_de_parameter_dict_from_opt():
    # Create the input dictionary
    opt = {"deParameter": "de_parameter"}
    assert gio.get_de_parameter_dict_from_opt(opt) == "de_parameter"


# Test get_de_parameters_from_opt
def test_get_de_parameters_from_opt():
    # Create the input dictionary
    opt = {
        "populationSize": 20,
        "endGeneration": 100,
        "F": 0.7,
        "CR": 0.9,
        "THR": 0.1,
    }
    assert gio.get_de_parameters_from_opt(opt) == (20, 100, 0.7, 0.9, 0.1)


# Test create_single_opt_response_object
def test_create_single_opt_response_object():
    params = [1, 2, 3, 4, 5, 6]
    fitness = 0.3
    optimization_time = 100
    response = gio.create_single_opt_response_object(target_example, params, optimization_time, fitness)
    assert response["target"] == target_example
    assert response["charge"] == 1
    assert response["factor"] == 2
    assert response["offset"] == 3
    assert response["resolution"] == 4
    assert response["optimizationTime"] == 100
    assert response["fitness"] == 0.7


# Test create_multiple_opt_response_object
def test_create_multiple_opt_response_object():
    params = [400, 0.4, 0.6, 1, 2, 3, 4, 5, 6, 7, 8]
    fitness = 0.3
    optimization_time = 100
    measurement_indices = [[3, 4, 5, 6],[7, 8, 9, 10]]
    response = gio.create_multi_opt_response_object(target_example, params, optimization_time, fitness, measurement_indices)
    assert response["targetModel"] == target_example
    assert response["optimizationTime"] == 100
    assert response["fitness"] == 0.7
    spectra_parameters = response["spectraParameters"]
    assert spectra_parameters[0] == {
        "charge": 1,
        "factor": 2,
        "offset": 3,
        "resolution": 4,
        "name": "Simulated"
    }
    assert spectra_parameters[1] == {
        "charge": 5,
        "factor": 6,
        "offset": 7,
        "resolution": 8,
        "name": "Simulated"
    }


