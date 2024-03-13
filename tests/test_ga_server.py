import json
from unittest import TestCase
from unittest.mock import MagicMock, patch
import src.GA.server as server  # Replace with the name of your module


class TestServer(TestCase):
    @patch('socket.socket')
    def test_handle_client_connection(self, mock_socket):
        # Create a mock client socket
        client_socket = MagicMock()

        # Simulate receiving data from the client. Adjust the return_value to fit your protocol.
        client_socket.recv.return_value = 'si_data End_Of_Transmission'.encode()

        # Call the function under test with the mocked client socket
        server.handle_client_connection(client_socket)

        # Make assertions about how the mock was used
        client_socket.sendall.assert_called_once()  # Adjust this assertion based on your logic

        # Example to check if the response sent to the client is as expected
        expected_response = 'Simulated spectra based on data  \nEnd_Of_Transmission\n'.encode()
        client_socket.sendall.assert_called_with(expected_response)

    # Test optimize_spectra and optimize_multiple_spectra in a similar way
    @patch('src.GA.single_spectrum_optimization.optimize_single_spectrum')
    @patch('socket.socket')
    def test_optimize_spectra(self, mock_socket, mock_optimize_single_spectrum):
        # Create a mock client socket
        client_socket = MagicMock()

        # Simulate receiving data from the client. Adjust the return_value to fit your protocol.
        client_socket.recv.return_value = 'op_data End_Of_Transmission'.encode()

        # Simulate the return value of the optimization function
        mock_optimize_single_spectrum.return_value = json.dumps({"result": "some result"})
        # Call the function under test with the mocked client socket
        server.handle_client_connection(client_socket)

        # Make assertions about how the mock was used
        client_socket.sendall.assert_called_once()
        # Example to check if the response sent to the client is as expected
        expected_response = '"{\\"result\\": \\"some result\\"}"' + ' \nEnd_Of_Transmission\n'
        client_socket.sendall.assert_called_with(expected_response.encode())

    # Test optimize_multiple_spectra in a similar way
    @patch('src.GA.multi_spectra_optimization.optimize_multi_spectra')
    @patch('socket.socket')
    def test_optimize_multiple_spectra(self, mock_socket, mock_optimize_multi_spectra):
        # Create a mock client socket
        client_socket = MagicMock()

        # Simulate receiving data from the client. Adjust the return_value to fit your protocol.
        client_socket.recv.return_value = 'ms_data End_Of_Transmission'.encode()

        # Simulate the return value of the optimization function
        mock_optimize_multi_spectra.return_value = json.dumps({"result": "some result"})
        # Call the function under test with the mocked client socket
        server.handle_client_connection(client_socket)

        # Make assertions about how the mock was used
        client_socket.sendall.assert_called_once()
        # Example to check if the response sent to the client is as expected
        expected_response = '"{\\"result\\": \\"some result\\"}"' + ' \nEnd_Of_Transmission\n'
        client_socket.sendall.assert_called_with(expected_response.encode())
