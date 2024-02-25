import pytest
from src.logic.helper import (
    get_target_layer_menu_list,
    get_target_layer_index_from_menu_list,
    get_elememt_menu_list,  # Notice there's a typo in the function name; should be `get_element_menu_list`
    get_element_index_from_menu_list,
    get_isotope_menu_list,
    get_isotope_index_from_menu_list,
    flatten,
    get_x_axis_data,
    down_sample_data,
    get_everything_until_last_close_bracket
)
import numpy as np


@pytest.fixture
def sample_target():
    return {
        "layerList": [
            {
                "elementList": [
                    {"atomicNumber": 1, "isotopeList": [{"mass": 1}, {"mass": 2}]},
                    {"atomicNumber": 2, "isotopeList": [{"mass": 4}]}
                ]
            },
            {
                "elementList": [
                    {"atomicNumber": 3, "isotopeList": [{"mass": 6}, {"mass": 7}]}
                ]
            }
        ]
    }

@pytest.mark.parametrize("target,expected", [
    ({"layerList": []}, []),
    ({"layerList": [{}]}, ["Layer 1"]),
    ({"layerList": [{}, {}]}, ["Layer 1", "Layer 2"])
])
def test_get_target_layer_menu_list(target, expected):
    assert get_target_layer_menu_list(target) == expected

def test_get_target_layer_index_from_menu_list():
    assert get_target_layer_index_from_menu_list("Layer 1") == 0
    assert get_target_layer_index_from_menu_list("Layer 2") == 1

def test_get_element_menu_list(sample_target):
    assert get_elememt_menu_list(sample_target, 0) == ['1', '2']

def test_get_element_index_from_menu_list(sample_target):
    assert get_element_index_from_menu_list(sample_target, '1', 0) == 0
    assert get_element_index_from_menu_list(sample_target, '2', 0) == 1

def test_get_isotope_menu_list(sample_target):
    assert get_isotope_menu_list(sample_target, 0, 0) == ['1', '2']

def test_get_isotope_index_from_menu_list(sample_target):
    assert get_isotope_index_from_menu_list(sample_target, '1', 0, 0) == 0
    assert get_isotope_index_from_menu_list(sample_target, '2', 0, 0) == 1

def test_flatten():
    nested_dict = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
    assert flatten(nested_dict) == {"a": 1, "c": 2, "e": 3}

def test_get_x_axis_data():
    original_data = [{"data": [10, 20, 30, 40]}]
    assert get_x_axis_data("Line number", original_data, 0, 1) == [0, 1, 2, 3]
    assert get_x_axis_data("Other", original_data, 5, 2) == [5, 7, 9, 11]

def test_down_sample_data():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert down_sample_data(data, 2) == [1.5, 3.5, 5.5, 7.5, 9.5]

def test_get_everything_until_last_close_bracket():
    test_string = "Here is {some} text {with} brackets}"
    assert get_everything_until_last_close_bracket(test_string) == "Here is {some} text {with} brackets}"
