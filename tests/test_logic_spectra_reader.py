import pytest
from unittest.mock import mock_open, patch, MagicMock
import os
import json
# Assuming your functions are in a module named spectra_reader.py
from src.logic.spectra_reader import (
    list_spectra_file_names,
    get_spectra_data,
    get_spectra_txt_file,
    convert_spectra_txt_to_list,
    save_spectra_txt,
    get_spectra_json_file,
    convert_spectra_json_to_list,
    save_spectra_json,
    delete_spectra_file,
)


# Mocking the file system paths and existence checks
@pytest.fixture
def mock_file_system(monkeypatch):
    # Mocked file system structure
    mock_file_structure = {
        'txt': ['file1.txt', 'file2.txt'],
        'json': ['file1.json', 'file2.json'],
    }

    def mock_os_path_exists(path):
        # Assuming the path always exists for simplicity
        return True

    def mock_os_listdir(path):
        if 'txt' in path:
            return mock_file_structure['txt']
        elif 'json' in path:
            return mock_file_structure['json']
        return []

    monkeypatch.setattr(os.path, "exists", mock_os_path_exists)
    monkeypatch.setattr(os, "listdir", mock_os_listdir)
    monkeypatch.setattr(os.path, "abspath", lambda path: path)  # Simplify path to be the same


@pytest.mark.usefixtures("mock_file_system")
class TestSpectraReader:
    def test_list_spectra_file_names(self):
        expected_files = ['file1.txt', 'file2.txt', 'file1.json', 'file2.json']
        assert sorted(list_spectra_file_names()) == sorted(expected_files)

    @patch('builtins.open', new_callable=mock_open, read_data='Test content')
    def test_get_spectra_txt_file(self, mock_file):
        assert get_spectra_txt_file('file1.txt') == 'Test content'

    def test_convert_spectra_txt_to_list(self):
        spectra_txt = "1,100\n2,200"
        expected_result = [{"name": "spectra", "data": [100, 200]}]
        assert convert_spectra_txt_to_list(spectra_txt) == expected_result

    @patch('builtins.open', new_callable=mock_open, read_data='{"spectra": [100, 200]}')
    def test_get_spectra_json_file(self, mock_file):
        assert json.loads(get_spectra_json_file('file1.json')) == {"spectra": [100, 200]}

    def test_convert_spectra_json_to_list(self):
        spectra_json = '{"spectra": [100, 200]}'
        expected_result = [100, 200]
        assert convert_spectra_json_to_list(spectra_json) == expected_result

    @patch('builtins.open', new_callable=mock_open)
    def test_save_spectra_txt(self, mock_file):
        save_spectra_txt('test.txt', 'Some content')
        mock_file().write.assert_called_once_with('Some content')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_spectra_json(self, mock_file):
        save_spectra_json('test.json', '{"test": "content"}')
        mock_file().write.assert_called_once_with('{"test": "content"}')

    @patch('os.remove')
    def test_delete_spectra_file_txt(self, mock_remove):
        delete_spectra_file('file1.txt')

    @patch('os.remove')
    def test_delete_spectra_file_json(self, mock_remove):
        delete_spectra_file('file1.json')

    @patch('src.logic.spectra_reader.convert_spectra_json_to_list')
    @patch('src.logic.spectra_reader.get_spectra_json_file', return_value='{"spectra": [100, 200]}')
    def test_get_spectra_data_json(self, mock_get_json_file, mock_convert_json_to_list):
        # Setup expected data
        expected_data = [100, 200]
        mock_convert_json_to_list.return_value = expected_data

        # Execute the function
        result = get_spectra_data('file1.json')

        # Assertions
        mock_get_json_file.assert_called_once_with('file1.json')
        mock_convert_json_to_list.assert_called_once_with('{"spectra": [100, 200]}')
        assert result == expected_data

    @patch('src.logic.spectra_reader.convert_spectra_txt_to_list')
    @patch('src.logic.spectra_reader.get_spectra_txt_file', return_value='1,100\n2,200')
    def test_get_spectra_data_txt(self, mock_get_txt_file, mock_convert_txt_to_list):
        # Setup expected data
        expected_result = [{"name": "spectra", "data": [100, 200]}]
        mock_convert_txt_to_list.return_value = expected_result

        # Execute the function
        result = get_spectra_data('file1.txt')

        # Assertions
        mock_get_txt_file.assert_called_once_with('file1.txt')
        mock_convert_txt_to_list.assert_called_once_with('1,100\n2,200')
        assert result == expected_result