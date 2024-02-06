import streamlit as st


def get_experimental_setup_from_state():
    return {
        "E0": st.session_state['es_E0'],
        "deltaE0": st.session_state['es_deltaE0'],
        "alpha": st.session_state['es_alpha'],
        "theta": st.session_state['es_theta'],
        "beta": st.session_state['es_beta'],
        "charge": st.session_state['es_charge'],
        "minCharge": st.session_state['es_minCharge'],
        "maxCharge": st.session_state['es_maxCharge'],
        "projectile": {
            "Z": st.session_state['es_projectile_Z'],
            "M": st.session_state['es_projectile_M'],
            "E": st.session_state['es_projectile_E']
        }
    }


def get_detector_setup_from_state():
    return {
        "calibration": {
            "factor": st.session_state['ds_calibration_factor'],
            "factor_min": st.session_state['ds_calibration_factor_min'],
            "factor_max": st.session_state['ds_calibration_factor_max'],
            "offset": st.session_state['ds_calibration_offset'],
            "offset_min": st.session_state['ds_calibration_offset_min'],
            "offset_max": st.session_state['ds_calibration_offset_max']
        },
        "resolution": st.session_state['ds_resolution'],
        "minRes": st.session_state['ds_resolution_min'],
        "maxRes": st.session_state['ds_resolution_max'],
        "solidAngle": st.session_state['ds_solidAngle']
    }


def get_calculation_setup_from_state():
    return {
        "stoppingData": st.session_state['cs_stoppingData'],
        "crossSectionData": st.session_state['cs_crossSectionData'],
        "numberOfChannels": st.session_state['cs_numberOfChannels'],
        "stoppingPowerCalculationMode": st.session_state['cs_stoppingPowerCalculationMode'],
        "compoundCalculationMode": st.session_state['cs_compoundCalculationMode'],
        "screeningMode": st.session_state['cs_screeningMode'],
        "stragglingMode": st.session_state['cs_stragglingMode'],
        "chargeFractionMode": st.session_state['cs_chargeFractionMode'],
        "useLookUpTable": st.session_state['cs_useLookUpTable'],
        "simulateIsotopes": st.session_state['cs_simulateIsotopes'],
        "showIsotopes": st.session_state['cs_showIsotopes'],
        "showLayers": st.session_state['cs_showLayers'],
        "showElements": st.session_state['cs_showElements']
    }


def get_de_parameter_from_state():
    return {
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
