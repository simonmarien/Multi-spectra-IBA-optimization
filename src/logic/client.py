import socket, datetime, pickle, time, sys
from src.logic import config, helper


class ProcessData:
    def __init__(self, data):
        self.data = data

    def __str__(self): return self.data


def simulate_spectra():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    run_client_sim(config.SIM_INPUT_FILE, config.SIM_OUTPUT_FOLDER + "generated-" + now_str + ".json")


def optimize_spectra_de(now_str):
    # now = datetime.datetime.now()
    # now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    # run_client_sim('../../files/input/sim_input.json', "../../files/spectra/json/generated-" + now_str + ".json", port=config.DE_DOCKER_PORT)
    # run_client_no_progress("OPTIMIZE", "../../files/input/opt_input.json",
    #                        "../../files/spectra/json/generated-opt-" + ".json", port=config.DE_DOCKER_PORT)
    run_client_no_progress("OPTIMIZE", config.OPT_INPUT_FILE,
                           config.OPT_OUTPUT_FOLDER + now_str + "/generated-opt-" + now_str + ".json",
                           port=config.DE_DOCKER_PORT)


def simulate_optimized_spectra(now_str, file_prefix=""):
    run_client_sim(config.SIM_INPUT_FILE,
                   config.OPT_OUTPUT_FOLDER + now_str + "/" + file_prefix + "generated-sim-" + now_str + ".json")


def optimize_spectra(now_str):
    for progress in run_client("OPTIMIZE", config.OPT_INPUT_FILE,
                               config.OPT_OUTPUT_FOLDER + now_str + "/generated-opt-" + now_str + ".json"):
        yield progress


def simulate_optimized_ms_spectra(now_str, file_prefix=""):
    run_client_sim(config.SIM_INPUT_FILE,
                   config.OPT_MS_OUTPUT_FOLDER + now_str + "/" + file_prefix + "generated-sim-" + now_str + ".json")


def optimize_multiple_spectra(now_str):
    for progress in run_client("OPTIMIZE_MS", config.OPT_MS_INPUT_FILE,
                               config.OPT_MS_OUTPUT_FOLDER + now_str + "/generated-opt-" + now_str + ".json"):
        yield progress


def run_client_sim(input_file, output_file, port=config.JAVA_DOCKER_PORT):
    server = config.JAVA_DOCKER_NAME
    if not config.DOCKERIZED:
        server = "localhost"

    try:
        with open(input_file, 'r') as file:
            input_str = file.read()
            print("Loading Input File ..... Done")
    except Exception as ex:
        print("Error loading input file:", ex)
        return
    print(input_str)
    try:
        print("Connecting to server ... ", end="")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, int(port)))
            print("Done")

            request_str = "si_" + input_str

            print("Sending input .......... ", end="")

            request_str += " \nEnd_Of_Transmission\n"

            s.sendall(request_str.encode())
            print("Done")

            reply = None

            # Receive reply from server
            print("Waiting for reply ..... ", end="")
            reply = ""
            while True:
                chunk = s.recv(4096).decode()
                if "End_Of_Transmission" in chunk:
                    reply += chunk[:chunk.find("End_Of_Transmission")]
                    break
                reply += chunk
            print("Done")

            print("Writing output file .... ", end="")
            with open(output_file, 'w') as file:
                file.write(reply)
                print("Done")

    except Exception as ex:
        print("Error:", ex)

    print("\n\rEnding process\n\r")


def run_client(request_type, input_file, output_file, port=config.JAVA_DOCKER_PORT):
    server = config.JAVA_DOCKER_NAME
    if not config.DOCKERIZED:
        server = "localhost"

    try:
        with open(input_file, 'r') as file:
            input_str = file.read()
            print("Loading Input File ..... Done")
    except Exception as ex:
        print("Error loading input file:", ex)
        return

    try:
        print("Connecting to server ... ", end="")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, int(port)))
            print("Done")

            request_str = ""
            if request_type == "OPTIMIZE":
                request_str = "op_"
            elif request_type == "OPTIMIZE_MS":
                request_str = "ms_"
            request_str += input_str

            print("Sending input .......... ", end="")

            request_str += " \nEnd_Of_Transmission\n"

            s.sendall(request_str.encode())
            print("Done")

            reply = None
            print("\n\rServer output:\n\r")
            print("Waiting for result ..... ", end="")
            with s.makefile('rb') as ois:
                while True:
                    try:
                        msg = ois.readline().decode()
                        identifier = msg[:7]
                        if identifier == "DE-INFO":
                            core_msg = msg[8:]
                            # print(core_msg, end="")
                            # Check if core_msg is an integer and larger than 0
                            try:
                                if int(core_msg) > 0:
                                    print(core_msg, end="")
                                    yield int(core_msg)
                            except:
                                pass
                        elif msg == "DE_FINISHED\n":
                            print("\n\rDone")
                            break
                    except Exception as ex:
                        print("Error getting server message:", ex)
                        break

            print("\n\rClosing connection ..... ", end="")
            print("Done")

            # Receive reply from server
            print("Waiting for reply ..... ", end="")
            reply = ""
            while True:
                chunk = s.recv(4096).decode()
                if "End_Of_Transmission" in chunk:
                    reply += chunk[:chunk.find("End_Of_Transmission")]
                    break
                reply += chunk
            print("Done")

            print("Writing output file .... ", end="")
            with open(output_file, 'w') as file:
                file.write(reply)
                print("Done")

    except Exception as ex:
        print("Error:", ex)

    print("\n\rEnding process\n\r")


def simulate_spectra_from_dict(input_dict, port=config.JAVA_DOCKER_PORT, debug=False, logger=None):
    server = config.JAVA_DOCKER_NAME
    if not config.DOCKERIZED:
        server = "localhost"

    try:
        if debug:
            print("Connecting to server ... ", end="")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, int(port)))
            if debug:
                print("Done")

            request_str = "si_" + str(input_dict)

            if debug:
                print("Sending input .......... ", end="")

            request_str += " \nEnd_Of_Transmission\n"
            # print(request_str)

            s.sendall(request_str.encode())
            if debug:
                print("Done")

            # Receive reply from server
            if debug:
                print("Waiting for reply ..... ", end="")
            reply = ""
            amount_of_chunks = 0
            while True:
                chunk = s.recv(4096).decode()
                amount_of_chunks += 1
                if amount_of_chunks > 1000:
                    print("Error: Too many chunks received")
                    reply = helper.get_everything_until_last_close_bracket(reply)
                    print(reply)
                    # if logger:
                    #     logger.log_message(request_str)
                    # Wait for 5 seconds to restart
                    time.sleep(3)
                    return None
                if "End" in chunk:
                    reply += chunk[:chunk.find("End")]
                    break
                if "Transmission" in chunk:
                    # Get reply untill last "}"" in reply
                    reply = helper.get_everything_until_last_close_bracket(reply)
                    break
                if "_O" in chunk:
                    reply = helper.get_everything_until_last_close_bracket(reply)
                    break
                if "Of" in chunk:
                    reply = helper.get_everything_until_last_close_bracket(reply)
                    break
                reply += chunk
            if debug:
                print("Done")

            if debug:
                print("Returning output ....... ", end="")
            return reply

    except Exception as ex:
        print("Error:", ex)
        print("Request string:", request_str)


def run_client_no_progress(request_type, input_file, output_file, port=config.DE_DOCKER_PORT):
    server = config.DE_DOCKER_NAME
    if not config.DOCKERIZED:
        server = "localhost"

    try:
        with open(input_file, 'r') as file:
            input_str = file.read()
            print("Loading Input File ..... Done")
    except Exception as ex:
        print("Error loading input file:", ex)
        return

    try:
        print("Connecting to server ... ", end="")
        print(server, int(port))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Socket created: ", s)
            s.connect((server, int(port)))
            print("Done")

            request_str = ""
            if request_type == "OPTIMIZE":
                request_str = "op_"
            elif request_type == "OPTIMIZE_MS":
                request_str = "ms_"
            request_str += input_str

            print("Sending input .......... ", end="")

            request_str += " \nEnd_Of_Transmission\n"

            s.sendall(request_str.encode())
            print("Done")

            reply = None

            # Receive reply from server
            print("Waiting for reply ..... ", end="")
            reply = ""
            while True:
                chunk = s.recv(4096).decode()
                if "End_Of_Transmission" in chunk:
                    reply += chunk[:chunk.find("End_Of_Transmission")]
                    break
                reply += chunk
            print("Done")

            print("Writing output file .... ", end="")
            with open(output_file, 'w') as file:
                file.write(reply)
                print("Done")

    except Exception as ex:
        print("Error:", ex)


# optimize_spectra_de("2020-10-30_15-00-00")