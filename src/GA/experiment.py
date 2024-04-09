from log import Logger
from multi_spectra_optimization import run_experiment as run_experiment_ms
from single_spectrum_optimization import run_experiment as run_experiment_ss
import os

amount_of_runs = 20
name_experiment = "SrtiOx ms restart"
log_directory = "../../files/logs/"
input_file_ms = "../../files/experiment_data/SrTiO3_ms.json"
input_file_ss = "../../files/experiment_data/SrTiOx copy.json"
strategies = ['best1bin', 'rand1bin', 'randtobest1bin']

# # Loop over strategies
# for strategy in strategies:
# Create the logger
logger = Logger()
experiment_name = name_experiment
# Create the log directory
logger.create_log_directory(log_directory, experiment_name)

for i in range(amount_of_runs):
    # Create the log file
    logger.create_log_file()
    # Log the amount of runs
    logger.log_message(f"Amount of runs: {amount_of_runs}")
    # Log the experiment name
    logger.log_message(f"Experiment name: {experiment_name}")
    # Log the input file
    logger.log_message(f"Input file: {input_file_ms}")
    #
    # # Run the experiment
    # run_experiment_ms(input_file_ms, logger)

    # logger.log_message(f"Input file: {input_file_ss}")
    try:
        # Run the experiment
        # run_experiment_ss(input_file_ss, logger, 'best1bin')
        run_experiment_ms(input_file_ms, logger)
    except Exception as e:
        logger.log_message(f"Error: {e}")
