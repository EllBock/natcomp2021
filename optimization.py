import json
import multiprocessing

from pygmo.core import de1220, algorithm, population
import os
import time
import pygmo as pg
from parametersKeys import parameters, minimumValue,maximumValue
TEMP_FOLDER_PATH = 'ExampleRun17071638/temp'
TEMP_PARAMETERS_FILE = os.path.join(TEMP_FOLDER_PATH, 'parameters')
results_path = None


def writeXtoJson(x):

    parametersdict = dict(zip(parameters, x))
    jsonPath = os.path.join(results_path,'temp','parameters.json')

    with open(jsonPath,'w') as f:
         json.dump(parametersdict, f)

def start_torcs(config_file):
    # print(f"Launch TORCS using {config_file}.")

    # Change the current working directory
    os.chdir(TORCSDIR)

    # Start TORCS
    command = f'wtorcs -t 100000 -r {config_file}'
    ret = os.system(command)

    return ret


def start_client(port, warmup, track, results=None):
    # print("Launch Client (warmup mode).")
    command = f'python2 client.py -p {port} -t {track} -f {} '

    if warmup:
        command += '-s 0 '
    else:
        command += '-s 2 '

    if results:
        command += f'-R {results}'

    ret = os.system(command)
    return ret


def executeGame(race_config, warmup_config, port):
    # Warm up phase
    track_name = race_config.split('')[0]
    trackinfo_file = os.path.join[TEMP_FOLDER_PATH, track_name + '.trackinfo']
    client = multiprocessing.Process(target=start_client, args=(port, True, trackinfo_file, 'results/useless'))
    # TODO: Se non viene passato nulla a results, non salvarlo perchè non serve.
    client.start()

    torcs = multiprocessing.Process(target=start_torcs, args=(warmup_config, ))
    torcs.start()

    client.join()
    torcs.join()
    if not os.path.isfile(trackinfo_file):
        raise Exception(f'Error: {trackinfo_file} was not created.')


     # creating multiple processes
    client = multiprocessing.Process(target=start_client, args=(TRACK, ))
    client.start()
    # Actual game execution

    for i in range(2):
        result1_file = os.path.join(TEMP_FOLDER_PATH, track_name + '_' +str(i) +'.csv')
        client = multiprocessing.Process(target=start_client, args=(port, False, trackinfo_file, result1_file ))
        client.start()

        torcs = multiprocessing.Process(target=start_torcs, args=(race_config, ))
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

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):

        new_default_parameter = writeXtoJson(x)

        #3001
        #first = multiprocessing.Process(target=executeGame, args=('forza_3001.xml','forza_warmup_3001.xml', 3001))

        #3002
        second = multiprocessing.Process(target=executeGame, args=('cgtrack2_3002.xml','cgtrack2_warmup_3002.xml', 3002))

        #3003
        third = multiprocessing.Process(target=executeGame, args=('etrack3_3003.xml','cgtrack2_warmup_3002.xml', 3003))

        #3004
        fourth = multiprocessing.Process(target=executeGame, args=('wheel1_3004.xml','cgtrack2_warmup_3002.xml', 3004))

        #first.start()
        #second.start()
        #third.start()
        #fourth.start()

        #first.join()
        #second.join()
        #third.join()
        #fourth.join()

        #fitness = computefitness()

        return [sum(x * x)]

    # Deve ritornare una coppia di np array contenente il minimo e massimo valore che i parametri possono assumere
    # I due array sono ordinati rispetto all'ordine dei parametri passati alla funzione di fitness.
    # The problem dimension will be inferred by the return value of the get_bounds function.
    def get_bounds(self):
        return (minimumValue, maximumValue)

    ############# Altri metodi sono opzionali



if __name__ == "__main__":

    currentTime = time.strftime("%y%m%d-%H%M%S")
    results_path = os.path.join('results', 'Run_'+ currentTime)

    if not os.path.exists(os.path.join(results_path,'temp')):
        os.makedirs(os.path.join(results_path,'temp'))


    allowedVariants = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                       18]  # Default [2, 3, 7, 10, 13, 14, 15, 16]

    # Initialize the problem
    problem = optimizationProblem()
    pgOptimizationProblem = pg.problem(problem)
    print(pgOptimizationProblem)

    # Initialize the algorithm
    algo = algorithm(de1220(gen=200, variant_adptv=2, allowed_variants=allowedVariants))
    algo.set_verbosity(1)

    # Run the algorithm
    pop = population(pgOptimizationProblem, 10**2)
    pop = algo.evolve(pop)

    # Take the results
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')
    uda = algo.extract(de1220)
    log = uda.get_log()

    best_fitness = pop.get_f()[pop.best_idx()]
    print(best_fitness)
