import json


def get_experiment_data_from_file(filename):
    data = read_experiment_data(filename)
    data = convert_dict_to_desired_format(data)
    return data


def get_experiment_ms_data_from_file(filename):
    data = read_experiment_data(filename)
    return data


# Read json from files/experiment_data
def read_experiment_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def convert_dict_to_desired_format(data):
    new_data = {}
    new_data["target"] = data["target"]
    new_data["experimentalSetup"] = data["experimentalSetup"]
    new_data["detectorSetup"] = data["detectorSetup"]
    new_data["calculationSetup"] = data["calculationSetup"]
    new_data["deParameter"] = data["deParameter"]
    new_data["experimentalSpectrum"] = {
        "name": data["spectrumName"],
        "data": convert_double_list_to_int(data["experimentalSpectrum"])
    }
    return new_data


def convert_double_list_to_int(data):
    for i in range(len(data)):
        data[i] = int(data[i])
    return data


