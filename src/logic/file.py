import datetime, os, json
import src.logic.spectra_reader as spectra_reader
import streamlit as st


# Optimization with single spectra
def optimize_single_spectra(spectra_filename):
    # Create the optimization directory
    now_str = create_optimization_directory()
    # Add the spectra file to the optimization directory
    add_spectra_file_to_optimization_directory(spectra_filename, now_str)
    # Add the opt_input file to the optimization directory
    add_opt_input_file_to_optimization_directory(now_str)
    return now_str


def create_optimization_directory():
    """
    Create the optimization directory.
    :return:
    """
    # In files/optimization create a directory with the current time as name
    # Get the current time
    now = datetime.datetime.now()
    # Get the current time as a string
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Create the directory
    os.mkdir(os.path.join("files", "optimization", now_str))
    print("Created optimization directory")
    return now_str


def add_spectra_file_to_optimization_directory(filename, now_str):
    """
    Add a spectra file to the optimization directory.
    :param filename:
    :return:
    """
    file = None
    # Copy the file from files/spectra/json or txt to files/optimization/<current time> and rename it to spectra.json
    if filename.endswith(".txt"):
        file = open(os.path.join("files", "spectra", "txt", filename), "r")
    elif filename.endswith(".json"):
        file = open(os.path.join("files", "spectra", "json", filename), "r")
    spectra_json = file.read()
    file.close()
    if filename.endswith(".txt"):
        file = open(os.path.join("files", "optimization", now_str, "spectra.txt"), "w")
    elif filename.endswith(".json"):
        file = open(os.path.join("files", "optimization", now_str, "spectra.json"), "w")
    file.write(spectra_json)
    file.close()
    print("Added spectra file to optimization directory")


def add_opt_input_file_to_optimization_directory(now_str):
    """
    Add a input file to the optimization directory.
    :param filename:
    :return:
    """
    # Copy the opt_input file from files/input to files/optimization/<current time> and rename it to opt_input.json
    file = open(os.path.join("files", "input", "opt_input.json"), "r")
    opt_input_json = file.read()
    file.close()
    file = open(os.path.join("files", "optimization", now_str, "opt_input.json"), "w")
    file.write(opt_input_json)
    file.close()
    print("Added opt_input file to optimization directory")


def get_opt_input_json_from_optimization_directory(now_str):
    """
    Get the opt_input json from the optimization directory.
    :param now_str:
    :return:
    """
    file = open(os.path.join("files", "optimization", now_str, "opt_input.json"), "r")
    opt_input_json = file.read()
    file.close()
    return json.loads(opt_input_json)


def get_json_from_generated_sample(now_str):
    """
    Get the json from the generated sample.
    :param now_str:
    :return:
    """
    file = open(os.path.join("files", "optimization", now_str, "generated-opt-" + now_str + ".json"), "r")
    generated_sample_json = file.read()
    file.close()
    return json.loads(generated_sample_json)


def get_target_from_generated_sample(now_str):
    """
    Get the target from the generated sample.
    :param now_str:
    :return:
    """
    return get_json_from_generated_sample(now_str)["target"]


def get_data_from_generated_sample(now_str):
    """
    Get the data from the generated sample.
    :param now_str:
    :return:
    """
    data = get_json_from_generated_sample(now_str)
    del data["target"]
    return data


def get_all_optimization_dates():
    """
    Get all optimization dates.
    :return:
    """
    return os.listdir(os.path.join("files", "optimization"))


def get_spectra_json_file(now_str, original=True):
    filename = None
    # Get original or simulated spectra file in files/optimization/<current time>
    if original and os.path.exists(os.path.join("files", "optimization", now_str, "spectra.json")):
        filename = "spectra.json"
    elif original:
        filename = "spectra.txt"
    else:
        filename = "generated-sim-" + now_str + ".json"

    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the "optimization" directory
    optimization_directory = os.path.abspath(
        os.path.join(script_directory, '..', '..', 'files', 'optimization', now_str))
    # Check if the "optimization" directory exists
    if not os.path.exists(optimization_directory):
        print("The 'optimization' directory does not exist.")
        return
    # Define the path to the file
    file_path = os.path.join(optimization_directory, filename)
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file '{filename}' does not exist.")
        return
    # Open the file
    with open(file_path, 'r') as file:
        file = file.read()
        if filename.endswith(".txt"):
            return spectra_reader.convert_spectra_txt_to_list(file)
        else:
            file_dict = json.loads(file)
            return file_dict["spectra"]


def download_spectra_file(filename):
    """
    Download a spectra json file.
    :param filename:
    :return:
    """
    file = None
    # Download the file from files/spectra/json or txt
    if filename.endswith(".txt"):
        file = open(os.path.join("files", "spectra", "txt", filename), "r")
    elif filename.endswith(".json"):
        file = open(os.path.join("files", "spectra", "json", filename), "r")
    spectra_json = file.read()
    file.close()
    return spectra_json


def download_spectra_filename(filename):
    """
    Return the filename of the spectra file.
    :param filename:
    :return:
    """
    if filename.endswith(".txt"):
        return "spectra.txt"
    elif filename.endswith(".json"):
        return "spectra.json"


# Optimization with multiple spectra
def optimize_multiple_spectra(selected_spectra_dictionary):
    """
    Optimize multiple spectra.
    :return:
    """
    # Create the optimization directory
    now_str = create_optimization_ms_directory()
    # Add the spectra file to the optimization directory
    add_multiple_spectra_files_to_optimization_directory(selected_spectra_dictionary, now_str)
    # Add the opt_input file to the optimization directory
    add_ms_opt_input_file_to_optimization_directory(now_str)
    return now_str


def create_optimization_ms_directory():
    """
    Create the optimization directory.
    :return:
    """
    # In files/optimization_ms create a directory with the current time as name
    # Get the current time
    now = datetime.datetime.now()
    # Get the current time as a string
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Create the directory
    os.mkdir(os.path.join("files", "optimization_ms", now_str))
    print("Created optimization directory")
    return now_str


def add_multiple_spectra_files_to_optimization_directory(selected_spectra_dictionary, now_str):
    """
    Add multiple spectra files to the optimization_ms directory.
    :param selected_spectra_dictionary:
    :return:
    """
    index = 1
    # Copy the file from files/spectra/json or txt to files/optimization/<current time> and rename it to spectra.json
    for spectra in selected_spectra_dictionary:
        print(selected_spectra_dictionary)
        file = None
        if spectra.endswith(".txt"):
            file = open(os.path.join("files", "spectra", "txt", spectra), "r")
        elif spectra.endswith(".json"):
            file = open(os.path.join("files", "spectra", "json", spectra), "r")
        spectra_json = file.read()
        file.close()
        filename = "o" + str(index) + "_" + spectra
        if spectra.endswith(".txt"):
            file = open(os.path.join("files", "optimization_ms", now_str, filename), "w")
        elif spectra.endswith(".json"):
            file = open(os.path.join("files", "optimization_ms", now_str, filename), "w")
        file.write(spectra_json)
        file.close()
        index += 1
    print("Added spectra files to optimization directory")


def add_ms_opt_input_file_to_optimization_directory(now_str):
    """
    Add a input file to the optimization directory.
    :param filename:
    :return:
    """
    # Copy the opt_input file from files/input to files/optimization/<current time> and rename it to opt_input.json
    file = open(os.path.join("files", "input", "ms_opt_input.json"), "r")
    ms_opt_input_json = file.read()
    file.close()
    file = open(os.path.join("files", "optimization_ms", now_str, "ms_opt_input.json"), "w")
    file.write(ms_opt_input_json)
    file.close()
    print("Added ms_opt_input file to optimization directory")


def get_ms_opt_input_json_from_optimization_directory(now_str):
    """
    Get the ms_opt_input json from the optimization directory.
    :param now_str:
    :return:
    """
    file = open(os.path.join("files", "optimization_ms", now_str, "ms_opt_input.json"), "r")
    ms_opt_input_json = file.read()
    file.close()
    return json.loads(ms_opt_input_json)



# Optimize multiple spectra
def get_all_optimization_ms_dates():
    """
    Get all optimization dates.
    :return:
    """
    return os.listdir(os.path.join("files", "optimization_ms"))


def get_json_from_generated_sample_ms(now_str):
    """
    Get the json from the generated sample.
    :param now_str:
    :return:
    """
    file = open(os.path.join("files", "optimization_ms", now_str, "generated-opt-" + now_str + ".json"), "r")
    generated_sample_json = file.read()
    file.close()
    return json.loads(generated_sample_json)


def get_data_from_generated_sample_ms(now_str):
    """
    Get the data from the generated sample.
    :param now_str:
    :return:
    """
    data = get_json_from_generated_sample_ms(now_str)
    del data["targetModel"]
    return data


def get_target_from_generated_sample_ms(now_str):
    """
    Get the target from the generated sample.
    :param now_str:
    :return:
    """
    return get_json_from_generated_sample_ms(now_str)["targetModel"]


def get_all_original_spectra_json_data(now_str):
    """
    Get all original spectra json files.
    :param now_str:
    :return:
    """
    data = []
    for file in os.listdir(os.path.join("files", "optimization_ms", now_str)):
        if file.startswith("o"):
            file = open(os.path.join("files", "optimization_ms", now_str, file), "r")
            if file.name.endswith(".txt"):
                data.append(spectra_reader.convert_spectra_txt_to_list(file.read()))
            else:
                data.append(json.loads(file.read())["spectra"])
            file.close()

    return data


def get_all_optimized_spectra_json_data(now_str):
    """
    Get all optimized spectra json files.
    :param now_str:
    :return:
    """
    data = []
    for file in os.listdir(os.path.join("files", "optimization_ms", now_str)):
        if file.startswith("o"):
            file = open(os.path.join("files", "optimization_ms", now_str, file), "r")
            if file.name.endswith(".txt"):
                data.append(spectra_reader.convert_spectra_txt_to_list(file.read()))
            else:
                data.append(json.loads(file.read())["spectra"])
            file.close()

    return data


# ------------- Setup ------------- #
# Experimental setup


def get_all_experimental_setup_names():
    """
    Get all experimental setup names.
    :return:
    """
    names = os.listdir(os.path.join("files", "setup", "experimental"))
    # Put default.json at the beginning of the list
    names.insert(0, names.pop(names.index("default.json")))
    return names


def get_all_experimental_setup_names_without_default():
    """
    Get all experimental setup names without default.
    :return:
    """
    names = os.listdir(os.path.join("files", "setup", "experimental"))
    # Remove default.json from the list
    names.remove("default.json")
    return names


def get_experimental_setup_json_from_file(filename):
    """
    Get the experimental setup json from a file.
    :param filename:
    :return:
    """
    file = open(os.path.join("files", "setup", "experimental", filename), "r")
    experimental_setup_json = file.read()
    file.close()
    return json.loads(experimental_setup_json)


def save_experimental_setup_json_to_file(filename, experimental_setup_json):
    """
    Save the experimental setup json to a file.
    :param filename:
    :param experimental_setup_json:
    :return:
    """
    file = open(os.path.join("files", "setup", "experimental", filename), "w")
    file.write(json.dumps(experimental_setup_json, indent=4))
    file.close()


def delete_experimental_setup_json_from_file(filename):
    """
    Delete the experimental setup json from a file.
    :param filename:
    :return:
    """
    os.remove(os.path.join("files", "setup", "experimental", filename))


# Detector setup


def get_all_detector_setup_names():
    """
    Get all detector setup names.
    :return:
    """
    names = os.listdir(os.path.join("files", "setup", "detector"))
    # Put default.json at the beginning of the list
    names.insert(0, names.pop(names.index("default.json")))
    return names


def get_all_detector_setup_names_without_default():
    """
    Get all detector setup names without default.
    :return:
    """
    names = os.listdir(os.path.join("files", "setup", "detector"))
    # Remove default.json from the list
    names.remove("default.json")
    return names


def get_detector_setup_json_from_file(filename):
    """
    Get the detector setup json from a file.
    :param filename:
    :return:
    """
    file = open(os.path.join("files", "setup", "detector", filename), "r")
    detector_setup_json = file.read()
    file.close()
    return json.loads(detector_setup_json)


def save_detector_setup_json_to_file(filename, detector_setup_json):
    """
    Save the detector setup json to a file.
    :param filename:
    :param detector_setup_json:
    :return:
    """
    file = open(os.path.join("files", "setup", "detector", filename), "w")
    file.write(json.dumps(detector_setup_json, indent=4))
    file.close()


def delete_detector_setup_json_from_file(filename):
    """
    Delete the detector setup json from a file.
    :param filename:
    :return:
    """
    os.remove(os.path.join("files", "setup", "detector", filename))


# Calculation setup


def get_all_calculation_setup_names():
    """
    Get all calculation setup names.
    :return:
    """
    names = os.listdir(os.path.join("files", "setup", "calculation"))
    # Put default.json at the beginning of the list
    names.insert(0, names.pop(names.index("default.json")))
    return names


def get_all_calculation_setup_names_without_default():
    """
    Get all calculation setup names without default.
    :return:
    """
    names = os.listdir(os.path.join("files", "setup", "calculation"))
    # Remove default.json from the list
    names.remove("default.json")
    return names


def get_calculation_setup_json_from_file(filename):
    """
    Get the calculation setup json from a file.
    :param filename:
    :return:
    """
    file = open(os.path.join("files", "setup", "calculation", filename), "r")
    calculation_setup_json = file.read()
    file.close()
    return json.loads(calculation_setup_json)


def save_calculation_setup_json_to_file(filename, calculation_setup_json):
    """
    Save the calculation setup json to a file.
    :param filename:
    :param calculation_setup_json:
    :return:
    """
    file = open(os.path.join("files", "setup", "calculation", filename), "w")
    file.write(json.dumps(calculation_setup_json, indent=4))
    file.close()


def delete_calculation_setup_json_from_file(filename):
    """
    Delete the calculation setup json from a file.
    :param filename:
    :return:
    """
    os.remove(os.path.join("files", "setup", "calculation", filename))


# Differential setup

def get_all_de_setup_names():
    """
    Get all differential setup names.
    """
    names = os.listdir(os.path.join("files", "setup", "differential"))
    names.insert(0, names.pop(names.index("default.json")))
    return names


def get_de_setup_names_without_default():
    """
    Get all differential setup names without default.
    """
    names = os.listdir(os.path.join("files", "setup", "differential"))
    names.remove("default.json")
    return names

def get_de_setup_json_from_file(filename):
    """
    Get the differential setup json from a file.
    :param filename:
    """
    file = open(os.path.join("files", "setup", "differential", filename), "r")
    differential_setup_json = file.read()
    file.close()
    return json.loads(differential_setup_json)

def save_de_setup_json_to_file(filename, differential_setup_json):
    """
    Save the differential setup json to a file.
    :param filename:
    :param differential_setup_json:
    """
    file = open(os.path.join("files", "setup", "differential", filename), "w")
    file.write(json.dumps(differential_setup_json, indent=4))
    file.close()

def delete_de_setup_json_from_file(filename):
    """
    Delete the differential setup json from a file.
    :param filename:
    """
    os.remove(os.path.join("files", "setup", "differential", filename))


# ------------- Target ------------- #
def get_target_json_from_file(filename):
    """
    Get the target json from a file.
    :param filename:
    :return:
    """
    file = open(os.path.join("files", "target", filename), "r")
    target_json = file.read()
    file.close()
    return json.loads(target_json)


def get_all_target_setup_names():
    """
    Get all target setup names.
    :return:
    """
    names = os.listdir(os.path.join("files", "target"))
    # Put default.json at the beginning of the list
    names.insert(0, names.pop(names.index("default.json")))
    return names


def get_all_target_setup_names_without_default():
    """
    Get all target setup names without default.
    :return:
    """
    names = os.listdir(os.path.join("files", "target"))
    # Remove default.json from the list
    names.remove("default.json")
    return names


def get_target_setup_json_from_file(filename):
    """
    Get the target setup json from a file.
    :param filename:
    :return:
    """
    file = open(os.path.join("files", "target", filename), "r")
    target_setup_json = file.read()
    file.close()
    return json.loads(target_setup_json)


def save_target_setup_json_to_file(filename, target_setup_json):
    """
    Save the target setup json to a file.
    :param filename:
    :param target_setup_json:
    :return:
    """
    file = open(os.path.join("files", "target", filename), "w")
    file.write(json.dumps(target_setup_json, indent=4))
    file.close()


def delete_target_setup_json_from_file(filename):
    """
    Delete the target setup json from a file.
    :param filename:
    :return:
    """
    os.remove(os.path.join("files", "target", filename))

