from scipy.optimize import differential_evolution
from scipy.signal import savgol_filter
import math, datetime, json, os, sys, numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import src.GA.ga_input_output as ga_input_output
import src.GA.experiment_input as experiment_input



global_logger = None
fixed_params_global = None
reference_spectra_global = None
optimization_object = None
ratio_indices_global = None
stop = False
iteration = 0
fitness = []


class OptimizationObject:
    def __init__(self, params, fixed_params, reference_spectra, ratio_indices):
        self.params = params
        self.fixed_params = fixed_params
        self.reference_spectra = reference_spectra['data']
        self.ratio_indices = ratio_indices
        self.last_fitness = None

    def evaluate(self):
        """
        Evaluates the objective function
        :return: The value of the objective function
        """
        # Calculate the simulated spectra
        simulated_spectra = self.simulate_spectra()
        # If the simulated spectra is None, return a low fitness value
        if simulated_spectra is None:
            self.last_fitness = 0
            return 0
        # Calculate the objective function value
        self.last_fitness = self.calculate_fitness(simulated_spectra)  # Update the fitness value
        return self.last_fitness

    def simulate_spectra(self):
        """
        Simulates the spectra with the given parameters
        :return:
        """
        # Fill in the variable parameters
        optimization_dict = ga_input_output.set_variable_parameters(self.fixed_params, self.params, self.ratio_indices)
        # Simulate the spectra
        global global_logger
        simulated_spectra = ga_input_output.simulate_spectra(optimization_dict, logger=global_logger)
        return simulated_spectra

    def simulate_spectra_return_all(self):
        """
        Simulates the spectra with the given parameters
        :return:
        """
        # Fill in the variable parameters
        optimization_dict = ga_input_output.set_variable_parameters(self.fixed_params, self.params, self.ratio_indices)
        # Simulate the spectra
        global global_logger
        simulated_spectra = ga_input_output.simulate_spectra_return_all(optimization_dict, logger=global_logger)
        return simulated_spectra

    def calculate_fitness(self, simulated_spectra):
        """
        Calculates the fitness of the simulated spectra
        :param simulated_spectra:
        :return:
        """
        start_ch, end_ch = ga_input_output.get_start_and_end_channel(self.fixed_params)

        sigma_2 = 0
        for i in range(start_ch, end_ch):
            ref_spectr = self.reference_spectra[i]
            sim_spectr = int(simulated_spectra[i])
            sigma_2 += (ref_spectr - sim_spectr) ** 2

        # print("Sigma_2: ", sigma_2)

        lff = self.calculate_lff()

        global iteration
        iteration += 1
        print("Iteration: ", iteration)
        # if iteration > 12000:
        #     sigma_2 = 1e-10
        #     global stop
        #     stop = True

        if sigma_2 == 0:
            iteration = 0
            return 1

        sigma_2 = math.log(lff) / math.log(sigma_2)
        # print("Variable parameters: ", self.params)
        # print("Fitness: ", sigma_2)
        # print(datetime.datetime.now())
        # print("Fitness: ", sigma_2)

        global fitness
        fitness.append(sigma_2)

        return sigma_2

    def calculate_lff(self):
        detector_setup_resolution = self.params[3]
        detector_setup_calibration_factor = self.params[1]

        temp = detector_setup_resolution / detector_setup_calibration_factor
        filter_length = int(math.floor(math.floor(temp/2.0)) * 2.0 + 1.0)
        if filter_length < 4:
            filter_length = 4

        smoothed_reference_spectra = savgol_filter(self.reference_spectra, filter_length, 3)

        result = 0
        start_ch, end_ch = ga_input_output.get_start_and_end_channel(self.fixed_params)
        for i in range(start_ch, end_ch):
            result += (smoothed_reference_spectra[i] - self.reference_spectra[i]) ** 2

        return result

    def normalize_ratios(self):
        """
        Normalizes the ratios
        :return:
        """
        # For each ratio_indice, the sum of the ratios must be 1
        # Add the ratio indicies and add it to constraints tuple
        for ratio_indice in self.ratio_indices:
            temp = 0
            for i in ratio_indice:
                temp += self.params[i]
            for i in ratio_indice:
                self.params[i] /= temp

    def round_params(self):
        """
        Rounds the parameters
        :return:
        """
        for i in range(len(self.params)):
            self.params[i] = round(self.params[i], 6)


def objective_function(params):
    # Check for nan values
    if np.isnan(params).any():
        return 1
    optimization_object.params = params
    # optimization_object.normalize_ratios()
    # optimization_object.round_params()
    return 1 - optimization_object.evaluate()


def normalize_ratios_global(params):
    """
    Normalizes the ratios
    :return:
    """
    # For each ratio_indice, the sum of the ratios must be 1
    # Add the ratio indicies and add it to constraints tuple
    global ratio_indices_global
    for ratio_indice in ratio_indices_global:
        temp = 0
        for i in ratio_indice:
            temp += params[i]
        for i in ratio_indice:
            params[i] /= temp
    return params


def callback_function(xk, convergence):
    # print("TEST")
    # global optimization_object
    # print("Generation completed. Best fitness so far:", optimization_object.last_fitness)
    # return False
    xk = normalize_ratios_global(xk)
    print(f"Current best solution: {xk}, Convergence: {convergence}")
    print(datetime.datetime.now())
    global global_logger
    global iteration
    if global_logger:
        # Log the iteration
        global_logger.log_message(f"Iteration: {iteration}")
        global_logger.log_message(f"Current best solution: {xk}, Convergence: {convergence}")
    global stop
    if stop:
        stop = False
        print("Stop minimizing")
        iteration = 0
        return True


def optimize_spectra(reference_spectra, fixed_params, bounds, de_parameters, ratio_indices, polish=True, disp=True, tol=0, strategy='best1bin'):
    global fixed_params_global
    global reference_spectra_global
    global optimization_object
    global ratio_indices_global

    fixed_params_global = fixed_params
    reference_spectra_global = reference_spectra
    optimization_object = OptimizationObject(None, fixed_params_global, reference_spectra_global, ratio_indices)
    ratio_indices_global = ratio_indices

    # Differential evolution parameters
    pop_size, max_iter, mutation_factor, crossover_rate, threshold = ga_input_output.get_de_parameters_from_opt(de_parameters)

    result = differential_evolution(objective_function, bounds, callback=callback_function, maxiter=max_iter, popsize=pop_size, mutation=mutation_factor, recombination=crossover_rate, polish=polish, disp=disp, strategy=strategy, tol=0.01)

    objective_value = result.fun

    return result.x, objective_value


def run(file_path):
    """
    Runs the optimization
    :param file_path:
    :return:
    """
    # If the file path is None, use the default file path
    opt_input = None
    if file_path is None:
        opt_input = ga_input_output.get_opt_from_file("../../files/input/opt_input.json")
    else:
        opt_input = experiment_input.get_experiment_data_from_file(file_path)
        print("Optimization input: ", opt_input)
    # Get experiment test data
    # opt_input = experiment_input.get_experiment_data_from_file("../../files/experiment_data/SrTiOx copy.json")
    # Get the variable parameters
    var_params, ratio_indices = ga_input_output.get_variable_parameters(opt_input)
    # Get the fixed parameters
    fixed_params = opt_input
    # Get the reference spectra
    reference_spectra = ga_input_output.get_reference_spectra(opt_input)
    # Get the bounds (+100% and -100%) of the variable parameters
    bounds = ga_input_output.get_bounds(opt_input)
    print("Bounds: ", bounds)
    # Get de parameters
    de_parameters = ga_input_output.get_de_parameter_dict_from_opt(opt_input)
    # Optimize the spectra
    print(datetime.datetime.now())
    optimized_params = optimize_spectra(reference_spectra, fixed_params, bounds, de_parameters, ratio_indices)
    print(datetime.datetime.now())
    # Print the result
    print(optimized_params)
    print(fitness)


def evaluate_parameter_values(values, filename):
    """
    Evaluates the parameter values
    :param values:
    :param filename:
    :return:
    """
    # Get the optimization input
    opt_input = experiment_input.get_experiment_data_from_file(filename)
    # Get the variable parameters
    var_params, ratio_indices = ga_input_output.get_variable_parameters(opt_input)
    # Get the fixed parameters
    fixed_params = opt_input
    # Get the reference spectra
    reference_spectra = ga_input_output.get_reference_spectra(opt_input)
    # Get the bounds (+100% and -100%) of the variable parameters
    bounds = ga_input_output.get_bounds(opt_input)
    # Create the optimization object
    optimization_object_test = OptimizationObject(values, fixed_params, reference_spectra, ratio_indices)
    # Evaluate the objective function
    f = optimization_object_test.evaluate()
    # Print the result
    print(f)
    return f


def get_simulated_spectra(values, filename):
    """
    Gets the simulated spectra
    :param values:
    :param filename:
    :return:
    """
    # Get the optimization input
    opt_input = experiment_input.get_experiment_data_from_file(filename)
    # Get the variable parameters
    var_params, ratio_indices = ga_input_output.get_variable_parameters(opt_input)
    # Get the fixed parameters
    fixed_params = opt_input
    # Get the reference spectra
    reference_spectra = ga_input_output.get_reference_spectra(opt_input)
    # Create the optimization object
    optimization_object_test = OptimizationObject(values, fixed_params, reference_spectra, ratio_indices)
    # Simulate the spectra
    simulated_spectra = optimization_object_test.simulate_spectra_return_all()
    return simulated_spectra


def run_experiment(filename, logger, strategy):
    """
    Runs the experiment
    :param filename:
    :param logger:
    :param strategy:
    :return:
    """
    global global_logger
    global_logger = logger
    # Get the optimization input
    opt_input = experiment_input.get_experiment_data_from_file(filename)
    # Get the variable parameters
    var_params, ratio_indices = ga_input_output.get_variable_parameters(opt_input)
    # Get the fixed parameters
    fixed_params = opt_input
    # Get the reference spectra
    reference_spectra = ga_input_output.get_reference_spectra(opt_input)
    # Get the bounds (+100% and -100%) of the variable parameters
    bounds = ga_input_output.get_bounds(opt_input)
    # Get de parameters
    de_parameters = ga_input_output.get_de_parameter_dict_from_opt(opt_input)
    # Optimize the spectra
    optimized_params = optimize_spectra(reference_spectra, fixed_params, bounds, de_parameters, ratio_indices, strategy)

    # Normalize the ratios
    for ratio_indice in ratio_indices:
        temp = 0
        for i in ratio_indice:
            temp += optimized_params[i]
        for i in ratio_indice:
            optimized_params[i] /= temp

    # Log end iteration
    global iteration
    logger.log_message(f"End iteration: {iteration}")
    iteration = 0
    logger.log_message(f"Final solution: {optimized_params}")
    global fitness
    logger.log_message(f"Fitness: {fitness}")
    fitness = []


def optimize_single_spectrum(opt_input):
    """
    Optimize a single spectrum for the server
    :param opt_input:
    :return:
    """
    opt_input = json.loads(opt_input)
    # Get the variable parameters
    var_params, ratio_indices = ga_input_output.get_variable_parameters(opt_input)
    # Get the fixed parameters
    fixed_params = opt_input
    # Get the reference spectra
    reference_spectra = ga_input_output.get_reference_spectra(opt_input)
    # Get the bounds (+100% and -100%) of the variable parameters
    bounds = ga_input_output.get_bounds(opt_input)
    print("Bounds: ", bounds)
    # Get de parameters
    de_parameters = ga_input_output.get_de_parameter_dict_from_opt(opt_input)
    # Set maximum iterations
    de_parameters['endGeneration'] = de_parameters['endGeneration']/(len(var_params)*100)
    print("Termination at generation: ", de_parameters['endGeneration'])
    # Start time
    start_time = datetime.datetime.now()
    # Optimize the spectra
    optimized_params, objective_value = optimize_spectra(reference_spectra, fixed_params, bounds, de_parameters, ratio_indices)
    # Elapsed time
    elapsed_time = datetime.datetime.now() - start_time
    # Target
    target = ga_input_output.set_variable_parameters(fixed_params, optimized_params, ratio_indices)['target']
    # Create the response
    response = ga_input_output.create_single_opt_response_object(target, optimized_params, elapsed_time.total_seconds(), objective_value)
    return response


# # Get ../../files/input/opt_input.json
# with open("../../files/input/opt_input.json", "r") as file:
#     opt_input = file.read()
#     print(optimize_single_spectrum(opt_input))


