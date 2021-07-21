import json
import math
import multiprocessing
import pickle

import numpy as np
from pygmo.core import de1220, algorithm, population
import os
import time
import pygmo as pg
from parametersKeys import parameters, minimumValue, maximumValue, notOptimzedParameters, defaultSnakeOilParameters
import config
import utils
from resultsUtils import readPickleFile
import psutil

TIMEOUT_CLIENT = 120  # sec
TIMEOUT_SERVER = 5  # sec
SLEEPTIME = 0.2  # sec
RESUME = True

def writeXtoJson(x, filename=None):
    parametersdict = dict(zip(parameters, x))
    parametersdict.update(notOptimzedParameters)
    if filename is None:
        jsonPath = os.path.join(resultsPath, 'temp', 'parameters.json')
    else:
        jsonPath = filename
    with open(jsonPath, 'w') as f:
        json.dump(parametersdict, f)



def start_torcs(config_file):
    # Change the current working directory
    os.chdir(config.TORCSDIR)

    # Start TORCS
    command = f'wtorcs -t 100000 -r {config_file} 1>nul'
    ret = os.system(command)

    return ret


def start_client(port,tempFolder, tempParametersFile, results):
    # print("Launch Client (warmup mode).")
    os.chdir(tempFolder)

    command = f'python2 {config.CLIENTPATH} -p {port} -f {tempParametersFile} -R {results}'
    ret = os.system(command)
    return ret


def executeGame(race_config, race_port, config_path, resultsPath):
    ret = 0

    tempFolder = os.path.join(resultsPath, 'temp')
    tempParametersFile = os.path.join(tempFolder, 'parameters.json')

    track_name = race_config.split('-')[0]

    # Start TORCS race
    race_config_path = os.path.join(config_path, race_config)
    torcs_race = multiprocessing.Process(target=start_torcs, args=(race_config_path,))
    torcs_race.start()

    # Actual game execution
    result_file = track_name + '.csv'
    client = multiprocessing.Process(target=start_client,
                                     args=(race_port, tempFolder, tempParametersFile, result_file))

    client.start()

    # Waiting until client finishes

    client.join(timeout=TIMEOUT_CLIENT)
    if client.is_alive():
        print(f'Client hanged, terminating...')
        ret = 1

    client.terminate()
    client.join()

    torcs_race.join(timeout=TIMEOUT_SERVER)
    if torcs_race.is_alive():
        print(f'Torcs hanged, terminating... on port '+ race_port)
        ret = 2

    torcs_race.terminate()
    torcs_race.join()

    if torcs_race.exitcode == 1:  # TORCS_ERROR
        ret = 2

    exit(ret)


class optimizationProblem:

    def __init__(self, resultsPath,alfa,beta):
        self.resultsPath = resultsPath
        self.resultsFileNames = ['forza.csv', 'cgtrack2.csv', 'etrack3.csv', 'wheel1.csv']  # IN ORDINE DI PORTA!
        # self.resultsFileNames = [ 'forza.csv' ]
        self.alfa = alfa
        self.beta = beta

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):

        start = time.time()

        writeXtoJson(x)

        workers = []

        workers.append(multiprocessing.Process(target=executeGame,
                                               args=('forza-inferno-9.xml',
                                                     3010, config.FORZADIR, self.resultsPath)))
        workers.append(multiprocessing.Process(target=executeGame,
                                               args=('cgtrack2-inferno-8.xml',
                                                     3009, config.CGTRACKDIR, self.resultsPath)))
        workers.append(multiprocessing.Process(target=executeGame,
                                               args=('etrack3-inferno-7.xml',
                                                     3008, config.ETRACKDIR, self.resultsPath)))
        workers.append(multiprocessing.Process(target=executeGame,
                                               args=('wheel1-inferno-6.xml',
                                                     3007, config.WHEELDIR, self.resultsPath)))

        # Start all the workers
        for w in workers:
            w.start()

        # Wait for all the workers to finish
        for w in workers:
            w.join()

        retvalues = []
        for w in workers:
            retvalues.append(w.exitcode)

        fitness = self.computefitness(retvalues)

        # end time
        end = time.time()
        # total time taken
        print(f"Fitness : {fitness} computed in {end - start} seconds")

        return fitness

    # Deve ritornare una coppia di np array contenente il minimo e massimo valore che i parametri possono assumere
    # I due array sono ordinati rispetto all'ordine dei parametri passati alla funzione di fitness.
    # The problem dimension will be inferred by the return value of the get_bounds function.
    def get_bounds(self):
        return (minimumValue, maximumValue)

    def computefitness(self, retvalues):
        # leggere i file csv e prelevare il danno, il tempo fuoripista, e la velocità media
        temp_directory = os.path.join(self.resultsPath, 'temp')
        score_list = np.array([])

        print(f'Game execution returned {retvalues}')

        for i in range(len(retvalues)):
            filename = self.resultsFileNames[i]
            if retvalues[i] != 0:
                print(f"Skipped {filename} because client hanged")
                continue
            d = utils.csv_to_column_dict(os.path.join(temp_directory, filename))
            d = utils.calculate_race_time(d)
            offroad = utils.calculate_offroad_time(d)
            score = d['distRaced'][-1] / d['raceTime'][-1] - self.alfa * d['damage'][-1] - self.beta * offroad / \
                    d['raceTime'][-1]
            score_list = np.append(score_list, score)

        if score_list.shape[0] == 0:
            return np.array([float('inf')])

        fitness = - np.average(score_list)


        for proc in psutil.process_iter():
            if proc.name() == 'wtorcs.exe':
                print('Killing wtorcs.exe')
                proc.kill()
            if proc.name() == 'python2.exe':
                print('Killing python2.exe')
                proc.kill()


        return np.array([fitness])


def initializeDirectory():
    # Create directory to save the results of the optimization
    current_time = time.strftime("%y%m%d-%H%M%S")
    results_path = os.path.join('results', 'Run_' + current_time)

    if not os.path.exists(os.path.join(results_path, 'temp')):
        os.makedirs(os.path.join(results_path, 'temp'))

    return os.path.abspath(results_path)


def saveStateFile(resultsPath, i, algo, pop, populationSize, numberOfGenerations, problem,seed):
    saved_dictionary = {}  # Initial empty dictionary

    # Where to save the pickles and json files
    pickle_path = os.path.join(resultsPath, f'resultsGeneration_{i}.pickle')
    json_path = os.path.join(resultsPath, f"championOfGeneration_{i}.json")

    # Create the best parameters values dictionary
    parametersdict = dict(zip(parameters, pop.champion_x))
    parametersdict.update(notOptimzedParameters)

    # Save it to file
    writeXtoJson(pop.champion_x, filename=json_path)

    # Save other useful information
    saved_dictionary['algorithm'] = algo
    saved_dictionary['pop'] = pop
    saved_dictionary['best_parameters'] = parametersdict
    saved_dictionary['pupulationSize'] = populationSize
    saved_dictionary['numberOfGenerations'] = numberOfGenerations
    saved_dictionary['alfa'] = problem.alfa
    saved_dictionary['beta'] = problem.beta
    saved_dictionary['problem'] = problem
    saved_dictionary['seed'] = seed

    with open(pickle_path, 'wb') as f:
        pickle.dump(saved_dictionary, f)


if __name__ == "__main__":

    # Create directory for results
    resultsPath = initializeDirectory()

    # Algorithm parameters
    IDEvariant = 2  # IDE algorithm
    numberOfGenerations = 200  # Number of generations to evolve
    SINGLE_GENERATION = 1  # Parameters to handle the logging of the status parameter
    populationSize = 30  # Total population size
    snakeoilPopSize = math.floor(populationSize * 0.80)  # Size of the population composed by snakeoils parameters
    randomPopulationSize = populationSize - snakeoilPopSize  # Size of the population compsed by random parameters
    seed = 2
    alfa = 0.1  # 0.001 a 0.1
    beta = 10000  # 100 a 10000

    # Initialize the problem
    problem = optimizationProblem(resultsPath, alfa, beta)
    pgOptimizationProblem = pg.problem(problem)
    print(pgOptimizationProblem)

    # Initialize the algorithm
    algo = algorithm(de1220(gen=SINGLE_GENERATION, variant_adptv=IDEvariant, ftol=-float("Inf"), memory=True))
    algo.set_seed(seed)
    algo.set_verbosity(1)

    # Run the algorithm
    pop = population(pgOptimizationProblem, randomPopulationSize)

    # Populate the remaining population with snakeoils default parameters\
    x_snakeoil = []

    for key in parameters:
        x_snakeoil.append(defaultSnakeOilParameters[key])

    for i in range(snakeoilPopSize):
        pop.push_back(x_snakeoil)

    if RESUME:
        results = readPickleFile(r'C:\Users\giuli\OneDrive\Documenti\GitHub\natcomp2021\results\Run_210720-143026\resultsGeneration_32.pickle')
        pop = results[0]['pop']
        problem = results[0]['problem']
        algo = results[0]['algorithm']

    # Start the evolution
    for i in range(1, numberOfGenerations + 1):
        # Evolve the previous population
        pop = algo.evolve(pop)

        # Extract the results
        uda = algo.extract(de1220)
        log = uda.get_log()

        # Print the best fitness value of the ith iteration
        print(f'Iterazione {i} - {log[0]}')

        # Save the state of the parameters after the current iteration
        saveStateFile(resultsPath, i, algo, pop, populationSize, numberOfGenerations, problem,seed)
