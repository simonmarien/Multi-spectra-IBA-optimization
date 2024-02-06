import streamlit as st
import numpy as np


def get_target_layer_menu_list(target):
    amount_of_layers = len(target["layerList"])
    return [f"Layer {i + 1}" for i in range(amount_of_layers)]


def get_target_layer_index_from_menu_list(selected):
    return int(selected.split(" ")[1]) - 1


def get_elememt_menu_list(target, layer_index):
    elements = target["layerList"][layer_index]["elementList"]
    # List atomic numbers
    return [f"{element['atomicNumber']}" for element in elements]


def get_element_index_from_menu_list(target, selected, layer_index):
    elements = target["layerList"][layer_index]["elementList"]
    # Loop through elements
    for i in range(len(elements)):
        if elements[i]["atomicNumber"] == int(selected):
            return i


def get_isotope_menu_list(target, layer_index, element_index):
    isotopes = target["layerList"][layer_index]["elementList"][element_index]["isotopeList"]
    # List atomic numbers
    return [f"{isotope['mass']}" for isotope in isotopes]


def get_isotope_index_from_menu_list(target, selected, layer_index, element_index):
    isotopes = target["layerList"][layer_index]["elementList"][element_index]["isotopeList"]
    # Loop through elements
    for i in range(len(isotopes)):
        if isotopes[i]["mass"] == float(selected):
            return i


def flatten(my_dict):
    result = {}
    for key, value in my_dict.items():
        if isinstance(value, dict):
            result.update(flatten(value))
        else:
            result[key] = value
    return result


def get_x_axis_data(x_axis_radio, original_data, offset, factor):
    if x_axis_radio == "Line number":
        return [i for i in range(len(original_data[0]["data"]))]
    else:
        return [offset + factor * i for i in range(len(original_data[0]["data"]))]


def down_sample_data(original_data, down_sample_factor):
    return [np.mean(original_data[i:i + down_sample_factor]) for i in range(0, len(original_data), down_sample_factor)]


def get_everything_until_last_close_bracket(string):
    return string[:string.rfind("}") + 1]
