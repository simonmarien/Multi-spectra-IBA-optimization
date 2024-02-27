import os
import datetime


class Logger:
    def __init__(self):
        self.log_directory = None
        self.experiment_name = None
        self.index = -1

    def create_log_directory(self, log_directory, experiment_name):
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = log_directory + experiment_name + "_" + timestamp
        os.mkdir(path)
        self.log_directory = path
        self.experiment_name = experiment_name

    def create_log_file(self):
        self.index += 1
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{self.experiment_name}_{self.index}.log"
        path = self.log_directory + "/" + filename
        with open(path, 'w') as f:
            f.write(f"Log file {self.index} for {self.experiment_name}, created at {timestamp}\n")

    def log_message(self, message):
        filename = f"{self.experiment_name}_{self.index}.log"
        if self.log_directory is not None:
            path = self.log_directory + "/" + filename
            with open(path, 'a') as f:
                f.write(f"{message}\n")
        else:
            print("Error: Log directory not created. Call create_log_file first.")
