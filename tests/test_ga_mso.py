import json, os
from unittest.mock import patch

import src.GA.multi_spectra_optimization as mso


# Test optimize_multi_spectra
@patch('src.GA.ga_input_output.simulate_spectra')
def test_optimize_multi_spectra(mock_simulate_spectra):
    ms_opt_input = None
    # Get ms_opt_input from file
    if not os.path.exists("files/input/ms_opt_input.json"):
        with open("../files/input/ms_opt_input.json", "r") as file:
            ms_opt_input = file.read()
    else:
        with open("files/input/ms_opt_input.json", "r") as file:
            ms_opt_input = file.read()

    # Simulate the return value of the simulate_spectra function
    simulated_spectra = json.loads(ms_opt_input)["measurements"][0]["spectrum"]["data"]
    mock_simulate_spectra.return_value = simulated_spectra

    # Call the function under test
    result = mso.optimize_multi_spectra(ms_opt_input)

    # Make assertions about the result
    assert result["optimizationTime"] > 0
    assert result["fitness"] > 0
    assert result["spectraParameters"][0]["charge"] > json.loads(ms_opt_input)["measurements"][0]["experimentalSetup"]["minCharge"]
    assert result["spectraParameters"][0]["charge"] < json.loads(ms_opt_input)["measurements"][0]["experimentalSetup"]["maxCharge"]
    assert result["spectraParameters"][0]["resolution"] > json.loads(ms_opt_input)["measurements"][0]["detectorSetup"]["minRes"]
    assert result["spectraParameters"][0]["resolution"] < json.loads(ms_opt_input)["measurements"][0]["detectorSetup"]["maxRes"]
    assert result["spectraParameters"][0]["factor"] > json.loads(ms_opt_input)["measurements"][0]["detectorSetup"]["calibration"]["factor_min"]
    assert result["spectraParameters"][0]["factor"] < json.loads(ms_opt_input)["measurements"][0]["detectorSetup"]["calibration"]["factor_max"]
    assert result["spectraParameters"][0]["offset"] > json.loads(ms_opt_input)["measurements"][0]["detectorSetup"]["calibration"]["offset_min"]
    assert result["spectraParameters"][0]["offset"] < json.loads(ms_opt_input)["measurements"][0]["detectorSetup"]["calibration"]["offset_max"]
