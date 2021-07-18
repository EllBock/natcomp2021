import json
import multiprocessing

from pygmo.core import de1220, algorithm, population
import os
import time
import pygmo as pg
from parametersKeys import parameters, minimumValue,maximumValue
import config


def malformed_trackinfo(track):

    with open(track + '.trackinfo', 'r')as f:
        lines = f.readlines()
        for l in lines:
            data = l.strip().split(' ')
            if len(data) < 4:
                return True

    return False

def writeXtoJson(x):

    parametersdict = dict(zip(parameters, x))
    jsonPath = os.path.join(resultsPath,'temp','parameters.json')

    with open(jsonPath,'w') as f:
         json.dump(parametersdict, f)

def start_torcs(config_file):
    # print(f"Launch TORCS using {config_file}.")

    # Change the current working directory
    os.chdir(config.TORCSDIR)

    # Start TORCS
    command = f'wtorcs -t 100000 -r {config_file}'
    print('TORCS - ' + command)
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

    print('CLIENT - ' + command)
    ret = os.system(command)
    return ret


def executeGame(race_config, warmup_config, port, config_path, resultsPath):

    tempFolder = os.path.join(resultsPath, 'temp')
    tempParametersFile = os.path.join(tempFolder, 'parameters.json')

    # Warm up phase
    print("*********************WARM UP PHASE")
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
        print(f"************************RACING PHASE {i+1}")
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


def computefitness():


    pass


class optimizationProblem:

    def __init__(self, resultsPath):
        self.resultsPath = resultsPath

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):

        new_default_parameter = writeXtoJson(x)

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

        print('Fatto')
        #fitness = computefitness()

        return [sum(x * x)]

    # Deve ritornare una coppia di np array contenente il minimo e massimo valore che i parametri possono assumere
    # I due array sono ordinati rispetto all'ordine dei parametri passati alla funzione di fitness.
    # The problem dimension will be inferred by the return value of the get_bounds function.
    def get_bounds(self):
        return (minimumValue, maximumValue)

    ############# Altri metodi sono opzionali

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
    #print(pgOptimizationProblem)

    # Algorithm parameters
    IDEvariant = 2
    numberOfGenerations = 200
    pupulationSize = 380 # Circa 8 volte la dimensionalità del problema (47)
    allowedVariants = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                       18]  # Default [2, 3, 7, 10, 13, 14, 15, 16]

    # Initialize the algorithm
    algo = algorithm(de1220(gen=numberOfGenerations, variant_adptv=IDEvariant, allowed_variants=allowedVariants))
    algo.set_verbosity(1)

    # Run the algorithm
    pop = population(pgOptimizationProblem, pupulationSize)
    pop = algo.evolve(pop)

    # Take the results
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')
    uda = algo.extract(de1220)
    log = uda.get_log()

    best_fitness = pop.get_f()[pop.best_idx()]
    print(best_fitness)
