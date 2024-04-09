import pytest
from unittest.mock import patch, MagicMock
from src.logic.convert import (  # Adjust this import according to your actual module path
    get_experimental_setup_from_state,
    get_detector_setup_from_state,
    get_calculation_setup_from_state,
    get_de_parameter_from_state,
)


# Mock Streamlit's session_state
@pytest.fixture
def mock_st_session_state():
    with patch('streamlit.session_state', {}) as mock_state:
        yield mock_state


def test_get_experimental_setup_from_state(mock_st_session_state):
    mock_st_session_state.update({
        'es_E0': 15,
        'es_deltaE0': 0.1,
        'es_alpha': 0.2,
        'es_theta': 30,
        'es_beta': 0.3,
        'es_charge': 1,
        'es_minCharge': 0,
        'es_maxCharge': 2,
        'es_projectile_Z': 1,
        'es_projectile_M': 1,
        'es_projectile_E': 15
    })
    expected_result = {
        "E0": 15,
        "deltaE0": 0.1,
        "alpha": 0.2,
        "theta": 30,
        "beta": 0.3,
        "charge": 1,
        "minCharge": 0,
        "maxCharge": 2,
        "projectile": {
            "Z": 1,
            "M": 1,
            "E": 15
        }
    }
    assert get_experimental_setup_from_state() == expected_result


def test_get_detector_setup_from_state(mock_st_session_state):
    mock_st_session_state.update({
        'ds_calibration_factor': 1.0,
        'ds_calibration_factor_min': 0.9,
        'ds_calibration_factor_max': 1.1,
        'ds_calibration_offset': 0.0,
        'ds_calibration_offset_min': -0.1,
        'ds_calibration_offset_max': 0.1,
        'ds_resolution': 0.5,
        'ds_resolution_min': 0.4,
        'ds_resolution_max': 0.6,
        'ds_solidAngle': 0.1
    })
    expected_result = {
        "calibration": {
            "factor": 1.0,
            "factor_min": 0.9,
            "factor_max": 1.1,
            "offset": 0.0,
            "offset_min": -0.1,
            "offset_max": 0.1
        },
        "resolution": 0.5,
        "minRes": 0.4,
        "maxRes": 0.6,
        "solidAngle": 0.1
    }
    assert get_detector_setup_from_state() == expected_result


def test_get_calculation_setup_from_state(mock_st_session_state):
    mock_st_session_state.update({
        'cs_stoppingData': 'SRIM',
        'cs_crossSectionData': 'default',
        'cs_numberOfChannels': 1024,
        'cs_stoppingPowerCalculationMode': 'full',
        'cs_compoundCalculationMode': 'Bragg',
        'cs_screeningMode': 'none',
        'cs_stragglingMode': 'Bohr',
        'cs_chargeFractionMode': 'average',
        'cs_useLookUpTable': True,
        'cs_simulateIsotopes': True,
        'cs_showIsotopes': False,
        'cs_showLayers': True,
        'cs_showElements': True
    })
    expected_result = {
        "stoppingData": 'SRIM',
        "crossSectionData": 'default',
        "numberOfChannels": 1024,
        "stoppingPowerCalculationMode": 'full',
        "compoundCalculationMode": 'Bragg',
        "screeningMode": 'none',
        "stragglingMode": 'Bohr',
        "chargeFractionMode": 'average',
        "useLookUpTable": True,
        "simulateIsotopes": True,
        "showIsotopes": False,
        "showLayers": True,
        "showElements": True
    }
    assert get_calculation_setup_from_state() == expected_result


def test_get_de_parameter_from_state():
    # Since this function does not use streamlit.session_state,
    # we directly test the output.
    expected_result = {
        "populationSize": 30,
        "F": 0.5,
        "CR": 0.7,
        "THR": 0.9,
        "numBins": 2,
        "startCH": 100,
        "endCH": 1000,
        "endTime": 0.0,
        "endFitness": 0.0,
        "endGeneration": 40.0,
        "isotopeTime": 0.0
    }
    assert get_de_parameter_from_state() == expected_result
