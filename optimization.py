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

    with open(track + '.trackinfo', 'r')as f:
        lines = f.readlines()
        for l in lines:
            data = l.strip().split(' ')
            if len(data) < 4:
                return True

    return False


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


def executeGame(race_config, warmup_config, port, config_path, resultsPath):

    tempFolder = os.path.join(resultsPath, 'temp')
    tempParametersFile = os.path.join(tempFolder, 'parameters.json')

    # Warm up phase
    # print("*********************WARM UP PHASE")
    track_name = race_config.split('-')[0]
    client = multiprocessing.Process(target=start_client, args=(port, True, tempFolder, track_name, tempParametersFile, track_name+'_warmup.csv'))
    # TODO: Se non viene passato nulla a results, non salvarlo perchè non serve.
    client.start()

    warmup_config_path = os.path.join(config_path, warmup_config)
    torcs = multiprocessing.Process(target=start_torcs, args=(warmup_config_path, ))
    torcs.start()

    client.join()
    torcs.join()

    trackinfo_file = os.path.join(tempFolder, track_name+'.trackinfo')
    if not os.path.isfile(trackinfo_file):
        raise Exception(f'Error: {trackinfo_file} was not created.')

    # Actual game execution
    for i in range(2):
        # print(f"************************RACING PHASE {i+1}")
        result_file = track_name + '_' +str(i) +'.csv'
        client = multiprocessing.Process(target=start_client, args=(port, False, tempFolder, track_name, tempParametersFile, result_file))
        client.start()

        race_config_path = os.path.join(config_path, race_config)
        torcs = multiprocessing.Process(target=start_torcs, args=(race_config_path, ))
        torcs.start()

        # Waiting until TORCS finishes
        torcs.join()
        if torcs.exitcode == 1: #TORCS_ERROR
            client.kill()
            raise Exception("Cannot start TORCS, (cannot bind socket). Aborting...")

        # Waiting until client finishes
        client.join()





class optimizationProblem:

    def __init__(self, resultsPath):
        self.resultsPath = resultsPath
        self.resultsFileNames = ['cgtrack2_0.csv','cgtrack2_1.csv', 'etrack3_0.csv', 'etrack3_1.csv', 'forza_0.csv', 'forza_1.csv' , 'wheel1_0.csv' , 'wheel1_1.csv' ]
        self.alfa = 0.05
        self.beta = 150

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):
        start = time.time()

        writeXtoJson(x)

        #3001
        first = multiprocessing.Process(target=executeGame, args=('forza-inferno-0.xml','forza-solo-0.xml', 3001, config.FORZADIR, self.resultsPath))

        #3002
        second = multiprocessing.Process(target=executeGame, args=('cgtrack2-inferno-1.xml','cgtrack2-solo-1.xml', 3002, config.CGTRACKDIR, self.resultsPath))

        #3003
        third = multiprocessing.Process(target=executeGame, args=('etrack3-inferno-2.xml','etrack3-solo-2.xml', 3003, config.ETRACKDIR,self.resultsPath))

        #3004
        fourth = multiprocessing.Process(target=executeGame, args=('wheel1-inferno-3.xml','wheel1-solo-3.xml', 3004, config.WHEELDIR, self.resultsPath))

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
    numberOfGenerations = 1
    populationSize = 7 # Circa 3 volte la dimensionalità del problema (47)
    snakeoilPopSize = math.floor(populationSize * 0.80)  # circa 80 % della total population
    randomPopulationSize = populationSize - snakeoilPopSize # circa 20 % della total population


    # Initialize the algorithm
    algo = algorithm(de1220(gen=numberOfGenerations, variant_adptv=IDEvariant,ftol=-float("Inf")))
    algo.set_verbosity(1)

    # Run the algorithm
    pop = population(pgOptimizationProblem, randomPopulationSize)

    # Populate the remaining population with snakeoils default parameters
    snakeoilParameters = defaultSnakeOilParameters.values()

    for i in range(snakeoilPopSize):
        pop.push_back(snakeoilParameters)

    # Start the evolution
    pop = algo.evolve(pop)

    # Take the results
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')
    uda = algo.extract(de1220)
    log = uda.get_log()

    best_fitness = pop.get_f()[pop.best_idx()]
    print(best_fitness)

    savedDictionary = {}

    savedDictionary['log'] = log
    savedDictionary['pop'] = pop
    parametersdict = dict(zip(parameters, pop.champion_x))
    parametersdict.update(notOptimzedParameters)
    savedDictionary['best_parameters'] = parametersdict
    jsonPath = os.path.join(resultsPath, "champion.json")
    writeXtoJson(pop.champion_x, filename=jsonPath)
    savedDictionary['pupulationSize'] = populationSize
    savedDictionary['numberOfGenerations'] = numberOfGenerations

    savedDictionary['alfa'] = 0.05
    savedDictionary['beta'] = 150


    with open('finalPopulation.pickle','wb') as f:
        pickle.dump(savedDictionary, f)


