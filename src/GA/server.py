import socket, time, json, os, sys
import threading
import single_spectrum_optimization as sso


# Add the project root directory to the PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import src.logic.config as config


def handle_client_connection(client_socket):
    try:
        request_data = ""
        while True:
            chunk = client_socket.recv(4096).decode()
            if "End_Of_Transmission" in chunk:
                print("End of transmission found")
                request_data += chunk[:chunk.find("End_Of_Transmission")]
                print("Request data: ", request_data)
                break
            request_data += chunk
        # Assuming the request is immediately followed by "End_Of_Transmission"
        # request_data, _ = request_data.split(" \nEnd_Of_Transmission\n", 1)

        if request_data.startswith("si_"):
            response = simulate_spectra(request_data[3:])
        elif request_data.startswith("op_"):
            response = optimize_spectra(request_data[3:])
        elif request_data.startswith("ms_"):
            response = optimize_multiple_spectra(request_data[3:])
        else:
            response = "Invalid request type."

        # Send the response back to the client
        client_socket.sendall((response + " \nEnd_Of_Transmission\n").encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def simulate_spectra(data):
    # Your simulation logic here
    return "Simulated spectra based on " + data


def optimize_spectra(data):
    # # Your optimization logic here
    # for i in range(1, 101, 20):
    #     print(f"DE-INFO {i}%", flush=True)
    #     yield f"DE-INFO {i}%"
    #     time.sleep(1)
    # yield progress updates TODO

    # Optimize spectra
    opt = sso.optimize_single_spectrum(data)
    # To string
    opt = json.dumps(opt)
    return opt


def optimize_multiple_spectra(data):
    # Your optimization for multiple spectra logic here
    return "Optimized multiple spectra based on " + data


def start_server(host='localhost', port=9080):
    if config.DOCKERIZED:
        host = config.DE_DOCKER_NAME
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # max backlog of connections

    print(f"Listening on {host}:{port}")

    try:
        while True:
            client_sock, address = server.accept()
            print(f"Accepted connection from {address[0]}:{address[1]}")
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_sock,)
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
