import os
import json


def list_spectra_file_names():
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the "spectra/txt" directory
    spectra__txt_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'txt'))

    # Check if the "spectra/txt" directory exists
    if not os.path.exists(spectra__txt_directory):
        print("The 'spectra' directory does not exist.")
        return

    # List all files in the "spectra/txt" directory
    file_names = os.listdir(spectra__txt_directory)

    # Define the path to the "spectra/json" directory
    spectra__json_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'json'))

    # Check if the "spectra/json" directory exists
    if not os.path.exists(spectra__json_directory):
        print("The 'spectra' directory does not exist.")
        return

    # List all files in the "spectra/json" directory
    json_file_names = os.listdir(spectra__json_directory)

    # Append the json file names to the file names
    file_names.extend(json_file_names)

    return file_names


def get_spectra_data(filename):
    # If the filename ends with ".txt"
    if filename.endswith(".txt"):
        file = get_spectra_txt_file(filename)
        return convert_spectra_txt_to_list(file)
    # If the filename ends with ".json"
    elif filename.endswith(".json"):
        file = get_spectra_json_file(filename)
        return convert_spectra_json_to_list(file)
    else:
        print(f"The file '{filename}' is not a supported file type.")
        return


def get_spectra_txt_file(filename):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the "spectra" directory
    spectra_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'txt'))

    # Check if the "spectra" directory exists
    if not os.path.exists(spectra_directory):
        print("The 'spectra' directory does not exist.")
        return

    # Define the path to the file
    file_path = os.path.join(spectra_directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file '{filename}' does not exist.")
        return

    # Open the file
    with open(file_path, 'r') as file:
        return file.read()


def convert_spectra_txt_to_list(spectra_txt):
    # Start with an empty list
    spectra_list = []

    # Split the text into lines
    lines = spectra_txt.splitlines()

    # Loop through the lines
    for line in lines:
        # If first character is a number, then it is a line with data
        if line[0].isdigit():
            # split the line on the comma
            split_line = line.split(',')
            # get the second part of the split line
            second_part = split_line[1].strip()
            # convert the second part to an integer
            integer = int(second_part)
            # add the integer to the list
            spectra_list.append(integer)

    return [{"name": "spectra", "data": spectra_list}]


def save_spectra_txt(filename, spectra_string):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the "spectra" directory
    spectra_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'txt'))

    # Check if the "spectra" directory exists
    if not os.path.exists(spectra_directory):
        print("The 'spectra' directory does not exist.")
        return

    # Define the path to the file
    file_path = os.path.join(spectra_directory, filename)

    # Open the file
    with open(file_path, 'w') as file:
        file.write(spectra_string)


def get_spectra_json_file(filename):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the "spectra" directory
    spectra_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'json'))

    # Check if the "spectra" directory exists
    if not os.path.exists(spectra_directory):
        print("The 'spectra' directory does not exist.")
        return

    # Define the path to the file
    file_path = os.path.join(spectra_directory, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file '{filename}' does not exist.")
        return

    # Open the file
    with open(file_path, 'r') as file:
        return file.read()


def convert_spectra_json_to_list(spectra_json):
    # Convert the json string to a dictionary
    spectra_dict = json.loads(spectra_json)
    return spectra_dict['spectra']


def save_spectra_json(filename, spectra_dict):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the "spectra" directory
    spectra_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'json'))

    # Check if the "spectra" directory exists
    if not os.path.exists(spectra_directory):
        print("The 'spectra' directory does not exist.")
        return

    # Define the path to the file
    file_path = os.path.join(spectra_directory, filename)

    # Open the file
    with open(file_path, 'w') as file:
        file.write(spectra_dict)


def delete_spectra_file(filename):
    # Get the current directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    spectra_directory = None

    if filename.endswith(".txt"):
        # Define the path to the "spectra/txt" directory
        spectra_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'txt'))
    elif filename.endswith(".json"):
        # Define the path to the "spectra/json" directory
        spectra_directory = os.path.abspath(os.path.join(script_directory, '..', '..', 'files', 'spectra', 'json'))

    # Define the path to the file
    file_path = os.path.join(spectra_directory, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)


# test
# filenames = list_spectra_file_names()
# print(filenames)
# spectra_txt = get_spectra_txt_file(filenames[0])
# l = convert_spectra_txt_to_list(spectra_txt)
# print(l)
# print(len(l))
