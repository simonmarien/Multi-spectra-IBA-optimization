import subprocess
import datetime
import src.logic.config as config


def run_command(command):
    """Run a command and return its output as a string."""
    return subprocess.check_output(command, shell=True)


def simulate_spectrum():
    """Simulate a spectrum."""
    # Get the current time
    now = datetime.datetime.now()
    # Get the current time as a string
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    cd = "cd " + config.RUTHELDE_JAR_PATH
    if config.DOCKERIZED:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " SIMULATE ../../files/input/sim_input.json ../../files/spectra/json/generated-" + now_str + ".json " + config.JAVA_DOCKER_NAME + " " + str(config.JAVA_DOCKER_PORT)
    else:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " SIMULATE ../../files/input/sim_input.json ../../files/spectra/json/generated-" + now_str + ".json localhost 9090"
    print(run_command(f"{cd} && {command}"))
    print("Simulated spectrum command successfully executed")


def optimize_spectrum(now_str):
    """
    Optimize a spectrum.
    :param now_str:
    :return:
    """

    cd = "cd " + config.RUTHELDE_JAR_PATH
    if config.DOCKERIZED:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " OPTIMIZE ../../files/input/opt_input.json ../../files/optimization/" + now_str + "/generated-opt-" + now_str + ".json " + config.JAVA_DOCKER_NAME + " " + str(config.JAVA_DOCKER_PORT)
    else:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " OPTIMIZE ../../files/input/opt_input.json ../../files/optimization/" + now_str + "/generated-opt-" + now_str + ".json localhost 9090"

    print(run_command(f"{cd} && {command}"))
    print("Optimized spectrum command successfully executed")


def simulate_optimized_spectrum(now_str):
    """
    Simulate a optimized spectrum.
    :param now_str:
    :return:
    """

    cd = "cd " + config.RUTHELDE_JAR_PATH
    if config.DOCKERIZED:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " SIMULATE ../../files/input/sim_input.json ../../files/optimization/" + now_str + "/generated-sim-" + now_str + ".json " + config.JAVA_DOCKER_NAME + " " + str(config.JAVA_DOCKER_PORT)
    else:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " SIMULATE ../../files/input/sim_input.json ../../files/optimization/" + now_str + "/generated-sim-" + now_str + ".json localhost 9090"

    print(run_command(f"{cd} && {command}"))
    print("Simulated optimized spectrum command successfully executed")


def optimize_multiple_spectra():
    """
    Optimize multiple spectra.
    :return:
    """
    cd = "cd " + config.RUTHELDE_JAR_PATH
    if config.DOCKERIZED:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " OPTIMIZE_MS ../../files/input/ms_opt_input.json ../../files/optimization/generated-opt.json " + config.JAVA_DOCKER_NAME + " " + str(config.JAVA_DOCKER_PORT)
    else:
        command = "java -jar -Djava.awt.headless=true " + config.RUTHELDE_JAR_NAME + " OPTIMIZE_MS ../../files/input/ms_opt_input.json ../../files/optimization/generated-opt.json localhost 9090"

    print(run_command(f"{cd} && {command}"))
    print("Optimized multiple spectra command successfully executed")
