import pytest
from unittest.mock import patch, mock_open, MagicMock
import datetime
import json, os
import src.logic.file as ou


@pytest.fixture
def setup_environment(tmp_path):
    # Setup a temporary directory structure
    d = tmp_path / "files" / "optimization"
    d.mkdir(parents=True)
    (tmp_path / "files" / "spectra" / "txt").mkdir(parents=True)
    (tmp_path / "files" / "spectra" / "json").mkdir(parents=True)
    (tmp_path / "files" / "input").mkdir(parents=True)
    # Create dummy opt_input.json file
    p = tmp_path / "files" / "input" / "opt_input.json"
    p.write_text('{"dummy_key": "dummy_value"}')
    return tmp_path


@patch('src.logic.file.create_optimization_directory')
@patch('src.logic.file.add_spectra_file_to_optimization_directory')
@patch('src.logic.file.add_opt_input_file_to_optimization_directory')
def test_optimize_single_spectra(mock_add_opt_input, mock_add_spectra_file, mock_create_dir, setup_environment):
    mock_create_dir.return_value = "2021-01-01_00-00-00"

    # Set the base directory for the test
    base_dir = setup_environment
    spectra_filename = "dummy_spectra.txt"

    # Create dummy spectra file
    p = base_dir / "files" / "spectra" / "txt" / spectra_filename
    p.write_text('dummy spectra content')

    # Adjust the module's os.path.join to work with the temporary directory
    with patch('os.path.join', side_effect=lambda *args: base_dir.joinpath(*args)):
        now_str = ou.optimize_single_spectra(spectra_filename)

    assert now_str == "2021-01-01_00-00-00"
    mock_create_dir.assert_called_once()
    mock_add_spectra_file.assert_called_once_with(spectra_filename, now_str)
    mock_add_opt_input.assert_called_once_with(now_str)


@patch("os.mkdir")
def test_create_optimization_directory(mock_mkdir):
    expected_dir_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result = ou.create_optimization_directory()

    assert result == expected_dir_name
    mock_mkdir.assert_called_once_with(f"files/optimization/{expected_dir_name}")


@patch("builtins.open", new_callable=mock_open)
def test_add_spectra_file_to_optimization_directory(mock_file):
    now_str = "2022-01-01_12-00-00"
    filename = "test_spectra.txt"

    ou.add_spectra_file_to_optimization_directory(filename, now_str)

    # Check if files are opened correctly for reading and writing
    mock_file.assert_any_call(f"files/spectra/txt/{filename}", "r")
    mock_file.assert_any_call(f"files/optimization/{now_str}/spectra.txt", "w")


@patch("builtins.open", new_callable=mock_open)
def test_add_spectra_json_file_to_optimization_directory(mock_file):
    now_str = "2022-01-01_12-00-00"
    filename = "test_spectra.json"

    ou.add_spectra_file_to_optimization_directory(filename, now_str)

    # Check if files are opened correctly for reading and writing
    mock_file.assert_any_call(f"files/spectra/json/{filename}", "r")
    mock_file.assert_any_call(f"files/optimization/{now_str}/spectra.json", "w")


# Test add_opt_input_file_to_optimization_directory
@patch("builtins.open", new_callable=mock_open)
def test_add_opt_input_file_to_optimization_directory(mock_file):
    now_str = "2022-01-01_12-00-00"

    ou.add_opt_input_file_to_optimization_directory(now_str)

    # Check if files are opened correctly for reading and writing
    mock_file.assert_any_call("files/input/opt_input.json", "r")
    mock_file.assert_any_call(f"files/optimization/{now_str}/opt_input.json", "w")


@patch("builtins.open", mock_open(read_data='{"key": "value"}'))
def test_get_opt_input_json_from_optimization_directory():
    now_str = "2022-01-01_12-00-00"
    result = ou.get_opt_input_json_from_optimization_directory(now_str)

    assert result == {"key": "value"}


# Test get_json_from_generated_sample
@patch("builtins.open", mock_open(read_data='{"key": "value"}'))
def test_get_json_from_generated_sample():
    now_str = "2022-01-01_12-00-00"
    result = ou.get_json_from_generated_sample(now_str)

    assert result == {"key": "value"}


# Test get_target_from_generated_sample
@patch("src.logic.file.get_json_from_generated_sample")
def test_get_target_from_generated_sample(mock_get_json):
    now_str = "2022-01-01_12-00-00"
    mock_get_json.return_value = {"target": "dummy_target"}

    result = ou.get_target_from_generated_sample(now_str)

    assert result == "dummy_target"


# Test get_data_from_generated_sample
@patch("src.logic.file.get_json_from_generated_sample")
def test_get_data_from_generated_sample(mock_get_json):
    now_str = "2022-01-01_12-00-00"
    mock_get_json.return_value = {"data": "dummy_data", "target": "dummy_target"}

    result = ou.get_data_from_generated_sample(now_str)

    assert result == {"data": "dummy_data"}


# Test get_all_optimization_dates
@patch("os.listdir")
def test_get_all_optimization_dates(mock_listdir):
    mock_listdir.return_value = ["2022-01-01_12-00-00", "2022-01-01_12-00-01"]

    result = ou.get_all_optimization_dates()

    assert result == ["2022-01-01_12-00-00", "2022-01-01_12-00-01"]


# Test download_spectra_file
# Test download_spectra_file function for a JSON file
@patch('builtins.open', new_callable=mock_open, read_data='{"data": "test data"}')
@patch('os.path.join', return_value='fakepath/filename.json')
def test_download_spectra_file_json(mock_join, mock_file):
    filename = 'testfile.json'
    result = ou.download_spectra_file(filename)
    assert result == '{"data": "test data"}'
    mock_file.assert_called_once_with('fakepath/filename.json', 'r')
    mock_join.assert_called_once_with('files', 'spectra', 'json', filename)


@patch('builtins.open', new_callable=mock_open, read_data='test data in txt')
@patch('os.path.join', return_value='fakepath/filename.txt')
def test_download_spectra_file_txt(mock_join, mock_file):
    filename = 'testfile.txt'
    result = ou.download_spectra_file(filename)
    assert result == 'test data in txt'
    mock_file.assert_called_once_with('fakepath/filename.txt', 'r')
    mock_join.assert_called_once_with('files', 'spectra', 'txt', filename)


# Test download_spectra_filename
def test_download_spectra_filename():
    filename = "testfile.json"
    result = ou.download_spectra_filename(filename)
    assert result == "spectra.json"

    filename = "testfile.txt"
    result = ou.download_spectra_filename(filename)
    assert result == "spectra.txt"


# Test optimize_multiple_spectra
@patch('src.logic.file.create_optimization_ms_directory')
@patch('src.logic.file.add_multiple_spectra_files_to_optimization_directory')
@patch('src.logic.file.add_ms_opt_input_file_to_optimization_directory')
def test_optimize_multiple_spectra(mock_add_ms_opt_input, mock_add_ms_spectra_file, mock_create_ms_dir, setup_environment):
    mock_create_ms_dir.return_value = "2021-01-01_00-00-00"

    # Set the base directory for the test
    base_dir = setup_environment
    spectra_filenames = ["dummy_spectra1.txt", "dummy_spectra2.txt"]

    # Create dummy spectra files
    for filename in spectra_filenames:
        p = base_dir / "files" / "spectra" / "txt" / filename
        p.write_text('dummy spectra content')

    # Adjust the module's os.path.join to work with the temporary directory
    with patch('os.path.join', side_effect=lambda *args: base_dir.joinpath(*args)):
        now_str = ou.optimize_multiple_spectra(spectra_filenames)

    assert now_str == "2021-01-01_00-00-00"
    mock_create_ms_dir.assert_called_once()
    mock_add_ms_spectra_file.assert_called_once_with(spectra_filenames, now_str)
    mock_add_ms_opt_input.assert_called_once_with(now_str)


# Test create_optimization_ms_directory
@patch("os.mkdir")
def test_create_optimization_ms_directory(mock_mkdir):
    expected_dir_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result = ou.create_optimization_ms_directory()

    assert result == expected_dir_name
    mock_mkdir.assert_called_once_with(f"files/optimization_ms/{expected_dir_name}")


# Test add_multiple_spectra_files_to_optimization_directory
@patch("builtins.open", new_callable=mock_open)
def test_add_multiple_spectra_files_to_optimization_directory(mock_file):
    now_str = "2022-01-01_12-00-00"
    filenames = ["test_spectra1.txt", "test_spectra2.txt"]

    ou.add_multiple_spectra_files_to_optimization_directory(filenames, now_str)

    # Check if files are opened correctly for reading and writing
    mock_file.assert_any_call(f"files/spectra/txt/{filenames[0]}", "r")
    mock_file.assert_any_call(f"files/spectra/txt/{filenames[1]}", "r")
    mock_file.assert_any_call(f"files/optimization_ms/{now_str}/o2_test_spectra2.txt", "w")


# Test add_multiple_spectra_files_to_optimization_directory_json
@patch("builtins.open", new_callable=mock_open)
def test_add_multiple_spectra_files_to_optimization_directory_json(mock_file):
    now_str = "2022-01-01_12-00-00"
    filenames = ["test_spectra1.json", "test_spectra2.json"]

    ou.add_multiple_spectra_files_to_optimization_directory(filenames, now_str)

    # Check if files are opened correctly for reading and writing
    mock_file.assert_any_call(f"files/spectra/json/{filenames[0]}", "r")
    mock_file.assert_any_call(f"files/spectra/json/{filenames[1]}", "r")
    mock_file.assert_any_call(f"files/optimization_ms/{now_str}/o2_test_spectra2.json", "w")


# Test add_ms_opt_input_file_to_optimization_directory
@patch("builtins.open", new_callable=mock_open)
def test_add_ms_opt_input_file_to_optimization_directory(mock_file):
    now_str = "2022-01-01_12-00-00"

    ou.add_ms_opt_input_file_to_optimization_directory(now_str)

    # Check if files are opened correctly for reading and writing
    mock_file.assert_any_call("files/optimization_ms/" + now_str + "/ms_opt_input.json", "w")
    mock_file.assert_any_call(f"files/optimization_ms/{now_str}/ms_opt_input.json", "w")


# get_ms_opt_input_json_from_optimization_directory
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_get_ms_opt_input_json_from_optimization_directory(mock_file):
    now_str = "2022-01-01_12-00-00"
    result = ou.get_ms_opt_input_json_from_optimization_directory(now_str)

    assert result == {"key": "value"}
    mock_file.assert_called_once_with(f"files/optimization_ms/{now_str}/ms_opt_input.json", "r")


# Test get_all_optimization_ms_dates
@patch("os.listdir")
def test_get_all_optimization_ms_dates(mock_listdir):
    mock_listdir.return_value = ["2022-01-01_12-00-00", "2022-01-01_12-00-01"]

    result = ou.get_all_optimization_ms_dates()

    assert result == ["2022-01-01_12-00-00", "2022-01-01_12-00-01"]


# Test get_json_from_generated_sample_ms
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_get_json_from_generated_sample_ms(mock_file):
    now_str = "2022-01-01_12-00-00"
    result = ou.get_json_from_generated_sample_ms(now_str)

    assert result == {"key": "value"}
    mock_file.assert_called_once_with(f"files/optimization_ms/{now_str}/generated-opt-{now_str}.json", "r")


# get_data_from_generated_sample_ms
@patch("src.logic.file.get_json_from_generated_sample_ms")
def test_get_data_from_generated_sample_ms(mock_get_json):
    now_str = "2022-01-01_12-00-00"
    mock_get_json.return_value = {"data": "dummy_data", "targetModel": "dummy_target"}

    result = ou.get_data_from_generated_sample_ms(now_str)

    assert result == {"data": "dummy_data"}


# Test get_target_from_generated_sample_ms
@patch("src.logic.file.get_json_from_generated_sample_ms")
def test_get_target_from_generated_sample_ms(mock_get_json):
    now_str = "2022-01-01_12-00-00"
    mock_get_json.return_value = {"data": "dummy_data", "targetModel": "dummy_target"}

    result = ou.get_target_from_generated_sample_ms(now_str)

    assert result == "dummy_target"


# Test get_all_original_spectra_json_data
@patch('os.listdir', return_value=['o1_spectra.json', 'o2_spectra.txt', 'ignore_file.json'])
@patch('os.path.join', side_effect=lambda *args: '/'.join(args))
@patch('builtins.open', new_callable=mock_open, read_data='{"spectra": [1, 2, 3]}')
@patch('src.logic.spectra_reader.convert_spectra_txt_to_list', return_value=[1, 2, 3])
def test_get_all_original_spectra_json_data(mock_convert, mock_open, mock_join, mock_listdir):
    now_str = '2023-01-01_12-00-00'
    result = ou.get_all_original_spectra_json_data(now_str)

    # Expected result considering the mock_files list and mocked file content
    expected = [
        [1, 2, 3],  # From o1_spectra.json
        [1, 2, 3]   # From o2_spectra.txt (converted)
    ]

    assert result == expected
    assert mock_open.call_count == 2  # Ensure open was called for both files


# Test get_all_optimized_spectra_json_data
@patch('os.listdir', return_value=['o1_spectra.json', 'o2_spectra.txt', 'ignore_file.json'])
@patch('os.path.join', side_effect=lambda *args: '/'.join(args))
@patch('builtins.open', new_callable=mock_open, read_data='{"spectra": [1, 2, 3]}')
@patch('src.logic.spectra_reader.convert_spectra_txt_to_list', return_value=[1, 2, 3])
def test_get_all_optimized_spectra_json_data(mock_convert, mock_open, mock_join, mock_listdir):
    now_str = '2023-01-01_12-00-00'
    result = ou.get_all_optimized_spectra_json_data(now_str)

    # Expected result considering the mock_files list and mocked file content
    expected = [
        [1, 2, 3],  # From o1_spectra.json
        [1, 2, 3]   # From o2_spectra.txt (converted)
    ]

    assert result == expected
    assert mock_open.call_count == 2

# ------------- Setup ------------- #
# Experimental setup

# Test get_all_experimental_setup_names
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_experimental_setup_names(mock_listdir):
    result = ou.get_all_experimental_setup_names()

    assert result == ['default.json', '2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_all_experimental_setup_names_without_default
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_experimental_setup_names_without_default(mock_listdir):
    result = ou.get_all_experimental_setup_names_without_default()

    assert result == ['2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_experimental_setup_json_from_file
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_get_experimental_setup_json_from_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    result = ou.get_experimental_setup_json_from_file(filename)

    assert result == {"key": "value"}
    mock_open.assert_called_once_with(f"files/setup/experimental/{filename}", "r")


# Test save_experimental_setup_json_to_file
@patch('builtins.open', new_callable=mock_open)
def test_save_experimental_setup_json_to_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    data = {"key": "value"}
    ou.save_experimental_setup_json_to_file(filename, data)

    mock_open.assert_called_once_with(f"files/setup/experimental/{filename}", "w")
    mock_open.return_value.write.assert_called_once_with('{\n    "key": "value"\n}')


# Test delete_experimental_setup_json_from_file
@patch('os.remove')
def test_delete_experimental_setup_json_from_file(mock_remove):
    filename = '2023-01-01_12-00-00.json'
    ou.delete_experimental_setup_json_from_file(filename)

    mock_remove.assert_called_once_with(f"files/setup/experimental/{filename}")

# Detector setup

# Test get_all_detector_setup_names
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_detector_setup_names(mock_listdir):
    result = ou.get_all_detector_setup_names()

    assert result == ['default.json', '2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_all_detector_setup_names_without_default
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_detector_setup_names_without_default(mock_listdir):
    result = ou.get_all_detector_setup_names_without_default()

    assert result == ['2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_detector_setup_json_from_file
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_get_detector_setup_json_from_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    result = ou.get_detector_setup_json_from_file(filename)

    assert result == {"key": "value"}
    mock_open.assert_called_once_with(f"files/setup/detector/{filename}", "r")


# Test save_detector_setup_json_to_file
@patch('builtins.open', new_callable=mock_open)
def test_save_detector_setup_json_to_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    data = {"key": "value"}
    ou.save_detector_setup_json_to_file(filename, data)

    mock_open.assert_called_once_with(f"files/setup/detector/{filename}", "w")
    mock_open.return_value.write.assert_called_once_with('{\n    "key": "value"\n}')


# Test delete_detector_setup_json_from_file
@patch('os.remove')
def test_delete_detector_setup_json_from_file(mock_remove):
    filename = '2023-01-01_12-00-00.json'
    ou.delete_detector_setup_json_from_file(filename)

    mock_remove.assert_called_once_with(f"files/setup/detector/{filename}")


# Calculation setup

# Test get_all_calculation_setup_names
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_calculation_setup_names(mock_listdir):
    result = ou.get_all_calculation_setup_names()

    assert result == ['default.json', '2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_all_calculation_setup_names_without_default
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_calculation_setup_names_without_default(mock_listdir):
    result = ou.get_all_calculation_setup_names_without_default()

    assert result == ['2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_calculation_setup_json_from_file
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_get_calculation_setup_json_from_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    result = ou.get_calculation_setup_json_from_file(filename)

    assert result == {"key": "value"}
    mock_open.assert_called_once_with(f"files/setup/calculation/{filename}", "r")


# Test save_calculation_setup_json_to_file
@patch('builtins.open', new_callable=mock_open)
def test_save_calculation_setup_json_to_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    data = {"key": "value"}
    ou.save_calculation_setup_json_to_file(filename, data)

    mock_open.assert_called_once_with(f"files/setup/calculation/{filename}", "w")
    mock_open.return_value.write.assert_called_once_with('{\n    "key": "value"\n}')


# Test delete_calculation_setup_json_from_file
@patch('os.remove')
def test_delete_calculation_setup_json_from_file(mock_remove):
    filename = '2023-01-01_12-00-00.json'
    ou.delete_calculation_setup_json_from_file(filename)

    mock_remove.assert_called_once_with(f"files/setup/calculation/{filename}")


# DE parameter

# Test get_all_de_parameter_names
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_de_setup_names(mock_listdir):
    result = ou.get_all_de_setup_names()

    assert result == ['default.json', '2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_all_de_setup_names_without_default
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_de_setup_names_without_default(mock_listdir):
    result = ou.get_de_setup_names_without_default()

    assert result == ['2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_de_setup_json_from_file
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_get_de_setup_json_from_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    result = ou.get_de_setup_json_from_file(filename)

    assert result == {"key": "value"}
    mock_open.assert_called_once_with(f"files/setup/differential/{filename}", "r")


# Test save_de_setup_json_to_file
@patch('builtins.open', new_callable=mock_open)
def test_save_de_setup_json_to_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    data = {"key": "value"}
    ou.save_de_setup_json_to_file(filename, data)

    mock_open.assert_called_once_with(f"files/setup/differential/{filename}", "w")
    mock_open.return_value.write.assert_called_once_with('{\n    "key": "value"\n}')


# Test delete_de_setup_json_from_file
@patch('os.remove')
def test_delete_de_setup_json_from_file(mock_remove):
    filename = '2023-01-01_12-00-00.json'
    ou.delete_de_setup_json_from_file(filename)

    mock_remove.assert_called_once_with(f"files/setup/differential/{filename}")


# ------------- Target ------------- #

# Test get_all_target_setup_names
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_target_setup_names(mock_listdir):
    result = ou.get_all_target_setup_names()

    assert result == ['default.json', '2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_all_target_setup_names_without_default
@patch('os.listdir', return_value=['2023-01-01_12-00-00', '2023-01-01_12-00-01', 'default.json'])
def test_get_all_target_setup_names_without_default(mock_listdir):
    result = ou.get_all_target_setup_names_without_default()

    assert result == ['2023-01-01_12-00-00', '2023-01-01_12-00-01']


# Test get_target_json_from_file
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_get_target_json_from_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    result = ou.get_target_json_from_file(filename)

    assert result == {"key": "value"}
    mock_open.assert_called_once_with(f"files/target/{filename}", "r")


# Test get_target_setup_json_from_file
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_get_target_setup_json_from_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    result = ou.get_target_setup_json_from_file(filename)

    assert result == {"key": "value"}
    mock_open.assert_called_once_with(f"files/target/{filename}", "r")


# Test save_target_json_to_file
@patch('builtins.open', new_callable=mock_open)
def test_save_target_json_to_file(mock_open):
    filename = '2023-01-01_12-00-00.json'
    data = {"key": "value"}
    ou.save_target_setup_json_to_file(filename, data)

    mock_open.assert_called_once_with(f"files/target/{filename}", "w")
    mock_open.return_value.write.assert_called_once_with('{\n    "key": "value"\n}')


# Test delete_target_json_from_file
@patch('os.remove')
def test_delete_target_json_from_file(mock_remove):
    filename = '2023-01-01_12-00-00.json'
    ou.delete_target_setup_json_from_file(filename)

    mock_remove.assert_called_once_with(f"files/target/{filename}")


# Test get_spectra_json_file
# Test for original .json file
@patch('os.path.exists', side_effect=lambda x: x.endswith('spectra.json'))
@patch('os.path.dirname')
@patch('os.path.abspath')
@patch('builtins.open', new_callable=mock_open, read_data='{"spectra": [1, 2, 3]}')
def test_get_spectra_json_file_original_json(mock_open, mock_abspath, mock_dirname, mock_exists):
    now_str = '2023-01-01'
    result = ou.get_spectra_json_file(now_str)
    assert result == [1, 2, 3]  # Assuming the file contains {"spectra": [1, 2, 3]}


# Test for original .txt file
@patch('os.path.exists', side_effect=lambda x: 'spectra.json' not in x)
@patch('src.logic.spectra_reader.convert_spectra_txt_to_list', return_value=[4, 5, 6])
@patch('os.path.dirname')
@patch('os.path.abspath')
@patch('builtins.open', new_callable=mock_open, read_data='some text data')
def test_get_spectra_json_file_original_txt(mock_open, mock_abspath, mock_dirname, mock_convert, mock_exists):
    now_str = '2023-01-02'
    result = ou.get_spectra_json_file(now_str)
    assert result == [4, 5, 6]  # Assuming the .txt file is converted to [4, 5, 6]


# Test for simulated .json file
@patch('os.path.exists', return_value=True)
@patch('os.path.dirname')
@patch('os.path.abspath')
@patch('builtins.open', new_callable=mock_open, read_data='{"spectra": [7, 8, 9]}')
def test_get_spectra_json_file_simulated_json(mock_open, mock_abspath, mock_dirname, mock_exists):
    now_str = '2023-01-03'
    result = ou.get_spectra_json_file(now_str, original=False)
    assert result == [7, 8, 9]  # Assuming the file contains {"spectra": [7, 8, 9]}
