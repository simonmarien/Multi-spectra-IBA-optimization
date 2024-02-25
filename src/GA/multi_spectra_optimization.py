from scipy.optimize import differential_evolution
from scipy.signal import savgol_filter
from src.GA import ga_input_output, experiment_input
import math, datetime, numpy as np

optimization_object = None
global_logger = None
stop = False
iteration = 0
OLD = False


class OptimizationObjectMS:
    def __init__(self, params, optimization_dict):
        self.params = params
        self.optimization_dict = optimization_dict
        self.reference_spectra = self.get_reference_spectra()
        self.ratio_indices = []  # [][]
        self.measurement_indices = []
        self.bounds = self.get_bounds()

    def evaluate(self):
        """
        Evaluates the objective function
        :return:
        """
        # For each measurement, calculate the simulated spectra
        simulated_spectra = self.simulate_spectra()
        if simulated_spectra is None:
            return 1e-6
        # Calculate the objective function value
        fitness = self.calculate_fitness(simulated_spectra)
        return fitness

    def simulate_spectra(self):
        """
        Simulates the spectra with the given parameters
        :return:
        """
        simulated_spectra = []
        # For each measurement, fill in the variable parameters
        for i in range(len(self.measurement_indices)):
            measurement, target = self.fill_in_variable_parameters(i)
            sim_input = self.get_sim_input(measurement, target)
            # Simulate the spectra
            simulated_spectrum = ga_input_output.simulate_spectra(sim_input)
            if simulated_spectrum is None:
                return None
            simulated_spectra.append(simulated_spectrum)
        return simulated_spectra

    def get_reference_spectra(self):
        """
        Gets the reference spectra from the optimization dictionary
        :param optimization_dict:
        :return:
        """
        reference_spectra = []
        # For each measurement
        for measurement in self.optimization_dict['measurements']:
            # Get the reference spectrum
            reference_spectrum = measurement['spectrum']['data']
            reference_spectra.append(reference_spectrum)
        return reference_spectra

    def get_bounds(self):
        """
        Returns the bounds for the optimization
        :return:
        """
        bounds = []
        # Get the bounds for the target
        bounds += self.get_target_bounds()
        index = len(bounds)
        # Get the bounds for each measurement
        for i in range(len(self.optimization_dict['measurements'])):
            bounds += self.get_measurement_bounds(i)
            self.measurement_indices.append([index, index + 1, index + 2, index + 3])
            index += 4
        return bounds

    def get_target_bounds(self):
        """
        Returns the bounds for the target
        :return:
        """
        bounds = []
        index = 0
        # For each layer in the target model
        for layer in self.optimization_dict['target']['layerList']:
            if OLD or len(layer['elementList']) > 1:
                # Add arealDensity
                bounds.append((layer['min_AD'], layer['max_AD']))
                index += 1
                ratio_indices = []
                # For each element in the layer
                for element in layer['elementList']:
                    # Add ratio
                    bounds.append((element['min_ratio'], element['max_ratio']))
                    ratio_indices.append(index)
                    index += 1
                self.ratio_indices.append(ratio_indices)
        return bounds

    def get_measurement_bounds(self, i):
        """
        Returns the bounds for the i-th measurement
        :param i:
        :return:
        """
        bounds = []
        # Set the experimental setup charge
        bounds.append((self.optimization_dict['measurements'][i]['experimentalSetup']['minCharge'],
                       self.optimization_dict['measurements'][i]['experimentalSetup']['maxCharge']))
        # Set the detector setup calibration factor
        bounds.append((self.optimization_dict['measurements'][i]['detectorSetup']['calibration']['factor_min'],
                       self.optimization_dict['measurements'][i]['detectorSetup']['calibration']['factor_max']))
        # Set the detector setup calibration offset
        bounds.append((self.optimization_dict['measurements'][i]['detectorSetup']['calibration']['offset_min'],
                          self.optimization_dict['measurements'][i]['detectorSetup']['calibration']['offset_max']))
        # Set the detector setup resolution
        bounds.append((self.optimization_dict['measurements'][i]['detectorSetup']['minRes'],
                       self.optimization_dict['measurements'][i]['detectorSetup']['maxRes']))
        return bounds

    def fill_in_variable_parameters(self, i):
        """
        Fills in the variable parameters for the i-th measurement
        :param i:
        :return:
        """
        # Get the measurement
        measurement = self.optimization_dict['measurements'][i]
        # Get the ratio indices
        ratio_indices = self.ratio_indices
        # Get the variable parameter indices
        variable_param_indices = self.measurement_indices[i]
        # Fill in the variable parameters
        # Set the experimental setup charge
        measurement['experimentalSetup']['charge'] = self.params[variable_param_indices[0]]
        # Set the detector setup calibration factor
        measurement['detectorSetup']['calibration']['factor'] = self.params[variable_param_indices[1]]
        # Set the detector setup calibration offset
        measurement['detectorSetup']['calibration']['offset'] = self.params[variable_param_indices[2]]
        # Set the detector setup resolution
        measurement['detectorSetup']['resolution'] = self.params[variable_param_indices[3]]
        # Get the target
        target = self.optimization_dict['target']
        index = 0
        layer = 0
        # Set the target variables
        for ratio in ratio_indices:
            # Add arealDensity
            target['layerList'][layer]['arealDensity'] = self.params[index]
            index += 1
            # For each element in the layer
            for i in range(len(ratio)):
                # Add ratio
                target['layerList'][layer]['elementList'][i]['ratio'] = self.params[index]
                # Add areal density
                target['layerList'][layer]['elementList'][i]['arealDensity'] = self.params[index] * target['layerList'][layer]['arealDensity']
                index += 1
            layer += 1

        # self.optimization_dict['measurements'][i] = measurement
        # self.optimization_dict['target'] = target
        return measurement, target

    def calculate_fitness(self, simulated_spectra):
        """
        Calculates the fitness of the simulated spectra
        :param simulated_spectra: list of simulated spectra
        :return: sum of fitness values
        """
        fitness = 0
        # For each measurement
        for i in range(len(self.measurement_indices)):
            # Calculate the fitness
            fitness += self.calculate_measurement_fitness(i, simulated_spectra[i])
        print("Sum of fitness: ", fitness)
        fitness = fitness / len(self.measurement_indices)
        # fitness = self.calculate_measurement_fitness(0, simulated_spectra[0])
        # print("Fitness: ", 1/fitness)
        return fitness

    def calculate_measurement_fitness(self, i, simulated_spectrum):
        """
        Calculates the fitness of the simulated spectrum
        :param i: index of the measurement
        :param simulated_spectrum: simulated spectrum
        :return: fitness value
        """
        # Get the reference spectrum
        reference_spectrum = self.reference_spectra[i]
        # Get the start and end channel
        start_ch, end_ch = self.get_start_and_end_channel(i)
        # Calculate the fitness
        fitness = self.calculate_fitness_value(i, reference_spectrum, simulated_spectrum, start_ch, end_ch)
        return fitness

    def calculate_fitness_value(self, i, reference_spectrum, simulated_spectrum, start_ch, end_ch):
        """
        Calculates the fitness value
        :param i: index of the measurement
        :param reference_spectrum: reference spectrum
        :param simulated_spectrum: simulated spectrum
        :param start_ch: start channel
        :param end_ch: end channel
        :return: fitness value
        """
        sigma_2 = 0
        for j in range(start_ch, end_ch):
            ref_spectr = reference_spectrum[j]
            sim_spectr = int(simulated_spectrum[j])
            sigma_2 += (ref_spectr - sim_spectr) ** 2

        lff = self.calculate_lff(i)

        if sigma_2 == 0:
            sigma_2 = 1e-10
            global iteration
            iteration = 0
            global stop
            stop = True
        sigma_2 = math.log(lff) / math.log(sigma_2)
        return sigma_2

    def calculate_lff(self, i):
        """
        Calculates the lff value
        :param i: index of the measurement
        :return: lff value
        """
        # Get the reference spectrum
        reference_spectrum = self.reference_spectra[i]
        # Get the start and end channel
        start_ch, end_ch = self.get_start_and_end_channel(i)
        # Get detector setup resolution
        detector_setup_resolution = self.optimization_dict['measurements'][i]['detectorSetup']['resolution']
        # Get detector_setup_calibration_factor
        detector_setup_calibration_factor = self.optimization_dict['measurements'][i]['detectorSetup']['calibration']['factor']

        temp = detector_setup_resolution / detector_setup_calibration_factor
        filter_length = int(math.floor(math.floor(temp/2.0)) * 2.0 + 1.0)
        if filter_length < 4:
            filter_length = 4

        smoothed_reference_spectrum = savgol_filter(reference_spectrum, filter_length, 3)
        lff = 0
        for j in range(start_ch, end_ch):
            lff += (reference_spectrum[j] - smoothed_reference_spectrum[j]) ** 2

        return lff

    def get_start_and_end_channel(self, i):
        start_channel = self.optimization_dict['measurements'][i]['deStartCh']
        end_channel = self.optimization_dict['measurements'][i]['deEndCh']
        return start_channel, end_channel

    def normalize_ratios(self):
        """
        Normalizes the ratios
        :return:
        """
        for ratio in self.ratio_indices:
            temp = 0
            for i in ratio:
                temp += self.params[i]
            for i in ratio:
                self.params[i] = self.params[i] / temp

    def get_sim_input(self, measurement, target):
        """
        Gets the simulation input for the i-th measurement
        :param i:
        :return:
        """
        sim_input = {}
        sim_input["experimentalSetup"] = measurement["experimentalSetup"]
        sim_input["detectorSetup"] = measurement["detectorSetup"]
        sim_input["target"] = target
        sim_input["calculationSetup"] = self.optimization_dict["calculationSetup"]
        return sim_input


def objective_function(params):
    """
    Objective function for the optimization
    :param params:
    :return:
    """
    global iteration
    iteration += 1
    print("Iteration: ", iteration)
    if iteration > 20000:
        global stop
        stop = True
    global optimization_object
    optimization_object.params = params
    optimization_object.normalize_ratios()
    fitness = optimization_object.evaluate()
    return 1/fitness


def callback_function(xk, convergence):
    # Normalize the ratios
    global optimization_object
    ratio_indices = optimization_object.ratio_indices
    for ratio in ratio_indices:
            temp = 0
            for i in ratio:
                temp += xk[i]
            for i in ratio:
                xk[i] = xk[i] / temp
    print(f"Current best solution: {xk}, Convergence: {convergence}")
    print(datetime.datetime.now())
    global global_logger
    global iteration
    global_logger.log_message(f"Iteration: {iteration}")
    global_logger.log_message(f"Current best solution: {xk}, Convergence: {convergence}")
    global stop
    if stop:
        stop = False
        print("Stop minimizing")
        iteration = 0
        return True


def run(filename):
    """
    Runs the optimization
    :param filename:
    :return:
    """
    input_data = experiment_input.get_experiment_ms_data_from_file(filename)
    global optimization_object
    optimization_object = OptimizationObjectMS([], input_data)
    # Get the de parameters
    de_parameters = ga_input_output.get_de_parameter_dict_from_opt(input_data)
    pop_size, max_iter, mutation_factor, crossover_rate, threshold = ga_input_output.get_de_parameters_from_opt(de_parameters)
    # Get the bounds
    bounds = optimization_object.bounds
    # Run the optimization
    result = differential_evolution(objective_function, bounds, popsize=pop_size, maxiter=max_iter, mutation=mutation_factor, recombination=crossover_rate, disp=True, polish=True, callback=callback_function, tol=0)
    print(result.x)


def run_experiment(filename, logger):
    """
    Runs the experiment
    :param filename:
    :param logger:
    :param run_number:
    :return:
    """
    # Get the input data
    input_data = experiment_input.get_experiment_ms_data_from_file(filename)
    global optimization_object
    optimization_object = OptimizationObjectMS([], input_data)
    global global_logger
    global_logger = logger
    # Get the de parameters
    de_parameters = ga_input_output.get_de_parameter_dict_from_opt(input_data)
    pop_size, max_iter, mutation_factor, crossover_rate, threshold = ga_input_output.get_de_parameters_from_opt(de_parameters)
    # Get the bounds
    bounds = optimization_object.bounds
    # Run the optimization
    # result = differential_evolution(objective_function, bounds, popsize=pop_size, maxiter=max_iter, mutation=mutation_factor, recombination=crossover_rate, disp=True, polish=True, callback=callback_function, tol=0)
    result = differential_evolution(objective_function, bounds, popsize=pop_size, maxiter=max_iter, mutation=mutation_factor, recombination=crossover_rate, disp=True, polish=True, callback=callback_function, tol=0.01)

    xk = result.x
    # Normalize ratios
    ratio_indices = optimization_object.ratio_indices
    for ratio in ratio_indices:
        temp = 0
        for i in ratio:
            temp += xk[i]
        for i in ratio:
            xk[i] = xk[i] / temp

    global iteration
    logger.log_message(f"End iteration: {iteration}")
    iteration = 0

    logger.log_message(f"Final solution: {xk}")


def evaluate_parameter_values(values, filename):
    """
    Evaluates the parameter values
    :param values:
    :param filename:
    :return:
    """
    input_data = experiment_input.get_experiment_ms_data_from_file(filename)
    global optimization_object
    optimization_object = OptimizationObjectMS(values, input_data)
    fitness = optimization_object.evaluate()
    print(fitness)
    return fitness

