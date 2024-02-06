import streamlit as st
from src.logic import file

print("Initializing session state...")


def initialize_session_state():
    if 'initialized' not in st.session_state:
        # Initialize the session state
        st.session_state.initialized = True

        # Initialize experimentalSetup data
        st.session_state["es_E0"] = 1520.0
        st.session_state["es_deltaE0"] = 0.0
        st.session_state["es_alpha"] = -11.0
        st.session_state["es_theta"] = 170.0
        st.session_state["es_beta"] = 21.0
        st.session_state["es_charge"] = 25.0
        st.session_state["es_minCharge"] = 15.0
        st.session_state["es_maxCharge"] = 30.0
        st.session_state["es_projectile_Z"] = 2
        st.session_state["es_projectile_M"] = 4.002603
        st.session_state["es_projectile_E"] = 1520.0

        # Initialize detectorSetup data
        st.session_state["ds_calibration_factor"] = 1.5
        st.session_state["ds_calibration_factor_min"] = 1.4
        st.session_state["ds_calibration_factor_max"] = 1.6
        st.session_state["ds_calibration_offset"] = 25.0
        st.session_state["ds_calibration_offset_min"] = 20.0
        st.session_state["ds_calibration_offset_max"] = 30.0
        st.session_state["ds_resolution"] = 15.0
        st.session_state["ds_resolution_min"] = 14.0
        st.session_state["ds_resolution_max"] = 17.0
        st.session_state["ds_solidAngle"] = 1.0

        # Initialize calculationSetup data
        st.session_state["cs_stoppingData"] = "StoppingData.json"
        # st.session_state["cs_stoppingData"] = ""
        st.session_state["cs_crossSectionData"] = []
        st.session_state["cs_numberOfChannels"] = 1024
        st.session_state["cs_stoppingPowerCalculationMode"] = "ZB"
        st.session_state["cs_compoundCalculationMode"] = "BRAGG"
        st.session_state["cs_screeningMode"] = "ANDERSON"
        st.session_state["cs_stragglingMode"] = "CHU"
        st.session_state["cs_chargeFractionMode"] = "LINEAR"
        st.session_state["cs_useLookUpTable"] = True
        st.session_state["cs_simulateIsotopes"] = False
        st.session_state["cs_showIsotopes"] = False
        st.session_state["cs_showLayers"] = False
        st.session_state["cs_showElements"] = True

        # Target test data
        st.session_state["target"] = file.get_target_json_from_file("default.json")
