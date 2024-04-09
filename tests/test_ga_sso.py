import json, os
from unittest.mock import patch, mock_open

import src.GA.single_spectrum_optimization as sso


# Test optimize_single_spectrum
@patch('src.GA.ga_input_output.simulate_spectra')
def test_optimize_single_spectrum(mock_simulate_spectra):
    opt_input = None
    # Get opt_input from file
    if not os.path.exists("files/input/opt_input.json"):
        with open("../files/input/opt_input.json", "r") as file:
            opt_input = file.read()
    else:
        with open("files/input/opt_input.json", "r") as file:
            opt_input = file.read()

    # Simulate the return value of the simulate_spectra function
    simulated_spectra = json.loads(opt_input)["experimentalSpectrum"]["data"]
    # Add 5 to every value in the simulated spectrum
    for i in range(len(simulated_spectra)):
        simulated_spectra[i] += 5
    mock_simulate_spectra.return_value = simulated_spectra

    # Call the function under test
    result = sso.optimize_single_spectrum(opt_input)

    # Make assertions about the result
    assert result["optimizationTime"] > 0
    assert result[
               "fitness"] > 0
    assert result["charge"] > json.loads(opt_input)["experimentalSetup"]["minCharge"]
    assert result["charge"] < json.loads(opt_input)["experimentalSetup"]["maxCharge"]
    assert result["resolution"] > json.loads(opt_input)["detectorSetup"]["minRes"]
    assert result["resolution"] < json.loads(opt_input)["detectorSetup"]["maxRes"]
    assert result["factor"] > json.loads(opt_input)["detectorSetup"]["calibration"]["factor_min"]
    assert result["factor"] < json.loads(opt_input)["detectorSetup"]["calibration"]["factor_max"]
    assert result["offset"] > json.loads(opt_input)["detectorSetup"]["calibration"]["offset_min"]
    assert result["offset"] < json.loads(opt_input)["detectorSetup"]["calibration"]["offset_max"]
