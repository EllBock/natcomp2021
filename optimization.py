import json
import math
import multiprocessing
import pickle

import numpy as np
from pygmo.core import de1220, algorithm, population
import os
import time
import pygmo as pg
from parametersKeys import parameters, minimumValue,maximumValue,notOptimzedParameters, defaultSnakeOilParameters
import config
import utils



def malformed_trackinfo(track):

   # with open(track + '.trackinfo', 'r')as f:
   #     lines = f.readlines()
   #     for l in lines:
   #         data = l.strip().split(' ')
   #         if len(data) < 4:
   #             return True

    return True


def writeXtoJson(x, filename=None):

    parametersdict = dict(zip(parameters, x))
    parametersdict.update(notOptimzedParameters)
    if filename is None:
        jsonPath = os.path.join(resultsPath,'temp','parameters.json')
    else:
        jsonPath = filename
    with open(jsonPath,'w') as f:
         json.dump(parametersdict, f)


def start_torcs(config_file):
    # print(f"Launch TORCS using {config_file}.")

    # Change the current working directory
    os.chdir(config.TORCSDIR)

    # Start TORCS
    command = f'wtorcs -t 100000 -r {config_file}'
    # print('TORCS - ' + command)
    ret = os.system(command)

    return ret


def start_client(port, warmup, tempFolder, trackname, tempParametersFile, results):
    # print("Launch Client (warmup mode).")
    os.chdir(tempFolder)
    command = f'python2 {config.CLIENTPATH} -p {port} -f {tempParametersFile} -R {results}'

    if warmup:
        command += f' -s 0 -t {trackname}'
    else:
        if not malformed_trackinfo(trackname):
            command += f' -s 2 -t {trackname}'

    # print('CLIENT - ' + command)
    ret = os.system(command)
    return ret


def executeGame(warmup_config, warmup_port,race_config, race_port, config_path, resultsPath):

    tempFolder = os.path.join(resultsPath, 'temp')
    tempParametersFile = os.path.join(tempFolder, 'parameters.json')

    # print("*********************WARM UP PHASE")
    track_name = race_config.split('-')[0]


    # Start TORCS warmup
    # warmup_config_path = os.path.join(config_path, warmup_config)
    # torcs_warmup = multiprocessing.Process(target=start_torcs, args=(warmup_config_path, ))
    # torcs_warmup.start()

    # Start TORCS race
    race_config_path = os.path.join(config_path, race_config)
    torcs_race = multiprocessing.Process(target=start_torcs, args=(race_config_path, ))
    torcs_race.start()

    # Start warmup client
    #client = multiprocessing.Process(target=start_client, args=(warmup_port, True, tempFolder, track_name, tempParametersFile, track_name+'_warmup.csv'))
    # TODO: Se non viene passato nulla a results, non salvarlo perchè non serve.
    # client.start()

    # client.join()
    # torcs_warmup.join()

    # trackinfo_file = os.path.join(tempFolder, track_name+'.trackinfo')
    # if not os.path.isfile(trackinfo_file):
    #    raise Exception(f'Error: {trackinfo_file} was not created.')

    # Actual game execution
    # print(f"************************RACING PHASE ")
    result_file = track_name + '.csv'
    client = multiprocessing.Process(target=start_client, args=(race_port, False, tempFolder, track_name, tempParametersFile, result_file))
    client.start()

    # Waiting until TORCS finishes
    torcs_race.join()

    if torcs_race.exitcode == 1: #TORCS_ERROR
        client.kill()
        raise Exception("Cannot start TORCS, (cannot bind socket). Aborting...")

    # Waiting until client finishes
    client.join()


class optimizationProblem:

    def __init__(self, resultsPath):
        self.resultsPath = resultsPath
        self.resultsFileNames = ['cgtrack2.csv', 'etrack3.csv', 'forza.csv', 'wheel1.csv']
        #self.resultsFileNames = [ 'forza.csv' ]
        self.alfa = 0.05
        self.beta = 150

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):

        start = time.time()

        writeXtoJson(x)

        first = multiprocessing.Process(target=executeGame, args=('forza-solo-0.xml', 3001, 'forza-inferno-9.xml', 3010, config.FORZADIR, self.resultsPath))
        second = multiprocessing.Process(target=executeGame, args=('cgtrack2-solo-1.xml', 3002, 'cgtrack2-inferno-8.xml',3009, config.CGTRACKDIR, self.resultsPath))
        third = multiprocessing.Process(target=executeGame, args=('etrack3-solo-2.xml', 3003, 'etrack3-inferno-7.xml', 3008, config.ETRACKDIR,self.resultsPath))
        fourth = multiprocessing.Process(target=executeGame, args=('wheel1-solo-3.xml', 3004, 'wheel1-inferno-6.xml', 3007, config.WHEELDIR, self.resultsPath))

        first.start()
        second.start()
        third.start()
        fourth.start()

        first.join()
        second.join()
        third.join()
        fourth.join()


        fitness = self.computefitness()


        # end time
        end = time.time()
        # total time taken
        print(f"Runtime of the program is {end - start}")
        return fitness

    # Deve ritornare una coppia di np array contenente il minimo e massimo valore che i parametri possono assumere
    # I due array sono ordinati rispetto all'ordine dei parametri passati alla funzione di fitness.
    # The problem dimension will be inferred by the return value of the get_bounds function.
    def get_bounds(self):
        return (minimumValue, maximumValue)

    ############# Altri metodi sono opzionali

    def computefitness(self):
        # leggere i file csv e prelevare il danno, il tempo fuoripista, e la velocità media
        tempDirectory = os.path.join(self.resultsPath,'temp')
        score_list = np.array([])
        for filename in self.resultsFileNames:
            d = utils.csv_to_column_dict(os.path.join(tempDirectory, filename))
            d = utils.calculate_race_time(d)
            offroad = utils.calculate_offroad_time(d)
            score = d['distRaced'][-1] / d['raceTime'][-1] - self.alfa * d['damage'][-1] - self.beta * offroad / d['raceTime'][-1]
            score_list = np.append(score_list, score)

        fitness = - np.average(score_list)


        return np.array([fitness])


def initializeDirectory():

    # Create directory to save the results of the optimization
    currentTime = time.strftime("%y%m%d-%H%M%S")
    resultsPath = os.path.join('results', 'Run_' + currentTime)

    if not os.path.exists(os.path.join(resultsPath, 'temp')):
        os.makedirs(os.path.join(resultsPath, 'temp'))

    return os.path.abspath(resultsPath)


if __name__ == "__main__":

    #Create directory for results
    resultsPath = initializeDirectory()

    # Initialize the problem
    problem = optimizationProblem(resultsPath)
    pgOptimizationProblem = pg.problem(problem)
    print(pgOptimizationProblem)

    # Algorithm parameters
    IDEvariant = 2
    numberOfGenerations = 100
    SINGLE_GENERATION = 1
    populationSize = 23 # Circa 3 volte la dimensionalità del problema (47)
    snakeoilPopSize = math.floor(populationSize * 0.80)  # circa 80 % della total population
    randomPopulationSize = populationSize - snakeoilPopSize # circa 20 % della total population


    # Initialize the algorithm
    algo = algorithm(de1220(gen=SINGLE_GENERATION, variant_adptv=IDEvariant,ftol=-float("Inf"), memory=True))
    algo.set_verbosity(1)

    # Run the algorithm
    pop = population(pgOptimizationProblem, randomPopulationSize)

    # Populate the remaining population with snakeoils default parameters\
    x_snakeoil = []

    for key in parameters:
        x_snakeoil.append(defaultSnakeOilParameters[key])

    for i in range(snakeoilPopSize):
        pop.push_back(x_snakeoil)

    # Start the evolution
    for i in range(1, numberOfGenerations + 1):

        pop = algo.evolve(pop)

        uda = algo.extract(de1220)
        log = uda.get_log()
        print(f'Iterazione {i} - {log[0]}')
        savedDictionary = {}
        picklePath = os.path.join(resultsPath, f'resultsGeneration_{i}.pickle')
        jsonPath = os.path.join(resultsPath, f"championOfGeneration_{i}.json")
        savedDictionary['algorithm'] = algo
        savedDictionary['pop'] = pop
        parametersdict = dict(zip(parameters, pop.champion_x))
        parametersdict.update(notOptimzedParameters)
        savedDictionary['best_parameters'] = parametersdict
        writeXtoJson(pop.champion_x, filename=jsonPath)
        savedDictionary['pupulationSize'] = populationSize
        savedDictionary['numberOfGenerations'] = numberOfGenerations
        savedDictionary['alfa'] = problem.alfa
        savedDictionary['beta'] = problem.beta


        with open(picklePath, 'wb') as f:
            pickle.dump(savedDictionary, f)




