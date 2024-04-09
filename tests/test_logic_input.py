import json
import pytest
from unittest.mock import mock_open, patch, MagicMock, call
from src.logic.input import save_sim_input_json, save_opt_input_json, save_sim_input_from_opt_input_json, save_ms_opt_input_json, save_sim_input_from_ms_opt_input_json

@patch('src.logic.file.get_experimental_setup_json_from_file', return_value={'some': 'data'})
@patch('src.logic.file.get_detector_setup_json_from_file', return_value={'detector': 'setup'})
@patch('src.logic.file.get_calculation_setup_json_from_file', return_value={'calculation': 'setup'})
@patch('builtins.open', new_callable=mock_open)
def test_save_sim_input_json(mock_open, mock_calc_setup, mock_det_setup, mock_exp_setup):
    target = {'target': 'details'}
    save_sim_input_json('exp_setup_path', 'det_setup_path', 'calc_setup_path', target)

    mock_open.assert_called_once_with('files/input/sim_input.json', 'w')

    expected_dict = {
        "target": target,
        "experimentalSetup": {'some': 'data'},
        "detectorSetup": {'detector': 'setup'},
        "calculationSetup": {'calculation': 'setup'}
    }

    # Capture all calls to write and concatenate them
    written_content = "".join(call_args.args[0] for call_args in mock_open().write.call_args_list)

    # Compare the concatenated content to the expected JSON string
    assert json.loads(written_content) == expected_dict


from unittest.mock import call, patch, mock_open
import json

@patch('src.logic.spectra_reader.get_spectra_data', return_value=[{'spectrum': 'data'}])
@patch('src.logic.file.get_experimental_setup_json_from_file', return_value={'some': 'data'})
@patch('src.logic.file.get_detector_setup_json_from_file', return_value={'detector': 'setup'})
@patch('src.logic.file.get_calculation_setup_json_from_file', return_value={'calculation': 'setup'})
@patch('builtins.open', new_callable=mock_open)
def test_save_opt_input_json(mock_open, mock_calc_setup, mock_det_setup, mock_exp_setup, mock_spectra_data):
    selected_spectra = 'selected_spectra_path'
    experimental_setup = 'exp_setup_path'
    detector_setup = 'det_setup_path'
    calculation_setup = 'calc_setup_path'
    de_parameter = 'de_parameter_value'
    target = {'target': 'details'}

    save_opt_input_json(selected_spectra, experimental_setup, detector_setup, calculation_setup, de_parameter, target)

    # Verify the correct functions were called
    mock_spectra_data.assert_called_once_with(selected_spectra)
    mock_exp_setup.assert_called_once_with(experimental_setup)
    mock_det_setup.assert_called_once_with(detector_setup)
    mock_calc_setup.assert_called_once_with(calculation_setup)

    expected_dict = {
        "target": target,
        "experimentalSpectrum": {'spectrum': 'data'},
        "experimentalSetup": {'some': 'data'},
        "detectorSetup": {'detector': 'setup'},
        "calculationSetup": {'calculation': 'setup'},
        "deParameter": de_parameter
    }

    # Capture all calls to write and concatenate them
    written_content = "".join(call_args.args[0] for call_args in mock_open().write.call_args_list)

    # Compare the concatenated content to the expected JSON string
    assert json.loads(written_content) == expected_dict


@patch('builtins.open', new_callable=mock_open)
def test_save_sim_input_from_opt_input_json(mock_open):
    opt_input = {
        "experimentalSetup": {"exp_key": "exp_value"},
        "detectorSetup": {"det_key": "det_value"},
        "calculationSetup": {"calc_key": "calc_value"}
    }
    target = {"target_key": "target_value"}

    save_sim_input_from_opt_input_json(opt_input, target)

    expected_dict = {
        "target": target,
        "experimentalSetup": opt_input["experimentalSetup"],
        "detectorSetup": opt_input["detectorSetup"],
        "calculationSetup": opt_input["calculationSetup"]
    }

    # Verify that the file was opened for writing
    mock_open.assert_called_once_with("files/input/sim_input.json", "w")

    # Capture all calls to write and concatenate them
    written_content = "".join(call_args.args[0] for call_args in mock_open().write.call_args_list)

    # Since json.dump is being used, the output will be formatted with indent=4
    # We need to compare the expected dictionary with the actual written content by loading it back as JSON
    assert json.loads(written_content) == expected_dict


@patch('src.logic.file.get_detector_setup_json_from_file', return_value={'detector': 'setup'})
@patch('src.logic.file.get_experimental_setup_json_from_file', return_value={'experimental': 'setup'})
@patch('src.logic.spectra_reader.get_spectra_data', return_value=[{'spectrum': 'data'}])
@patch('src.logic.file.get_calculation_setup_json_from_file', return_value={'calculation': 'setup'})
@patch('builtins.open', new_callable=mock_open)
def test_save_ms_opt_input_json(mock_open, mock_get_calc_setup, mock_get_spectra_data, mock_get_exp_setup, mock_get_det_setup):
    selected_spectra_dictionary = [{'spectra_name': 'RBS23_152_01B_d01.txt', 'experimental_setup': 'test_setupee.json', 'detector_setup': 'test.json', 'deWeight': 0.5, 'deStartCh': 100, 'deEndCh': 1005, 'deNumBins': 5}]
    calculation_setup = 'calc_setup.json'
    de_parameter = 'de_param_value'
    target = 'target_details'

    save_ms_opt_input_json(selected_spectra_dictionary, calculation_setup, de_parameter, target)

    expected_dict = {
        "target": target,
        "measurements": [{
            "spectrum": {'spectrum': 'data'},
            "experimentalSetup": {'experimental': 'setup'},
            "detectorSetup": {'detector': 'setup'},
            "deWeight": 0.5,
            "deStartCh": 100,
            "deEndCh": 1005,
            "deNumBins": 5
        }],
        "calculationSetup": {'calculation': 'setup'},
        "deParameter": de_parameter
    }

    # Capture all calls to write and concatenate them
    written_content = "".join(call_args.args[0] for call_args in mock_open().write.call_args_list)

    # Compare the concatenated content to the expected JSON string
    assert json.loads(written_content) == expected_dict


@patch('builtins.open', new_callable=mock_open)
def test_save_sim_input_from_ms_opt_input_json(mock_open):
    # Setup the input data
    ms_opt_input = {
        "measurements": [
            {
                "experimentalSetup": {"setup1": "value1"},
                "detectorSetup": {"setup2": "value2"},
                "deWeight": 0.5,
                "deStartCh": 100,
                "deEndCh": 1005,
                "deNumBins": 5
            },
            {
                "experimentalSetup": {"setup1": "value3"},
                "detectorSetup": {"setup2": "value4"},
                "deWeight": 0.6,
                "deStartCh": 200,
                "deEndCh": 2005,
                "deNumBins": 6
            }
        ],
        "calculationSetup": {"calcSetup": "calcValue"}
    }
    target = "targetDetails"
    index = 1  # Choosing the second measurement for the test

    # Expected output JSON content
    expected_dict = {
        "target": target,
        "experimentalSetup": ms_opt_input["measurements"][index]["experimentalSetup"],
        "detectorSetup": ms_opt_input["measurements"][index]["detectorSetup"],
        "calculationSetup": ms_opt_input["calculationSetup"]
    }

    # Call the function under test
    save_sim_input_from_ms_opt_input_json(ms_opt_input, target, index)

    # Assert that the file was opened correctly
    mock_open.assert_called_once_with("files/input/sim_input.json", "w")

    # Capture all calls to write and concatenate them
    written_content = "".join(call.args[0] for call in mock_open().write.call_args_list)

    # Compare the concatenated content to the expected JSON string
    assert json.loads(written_content) == expected_dict

