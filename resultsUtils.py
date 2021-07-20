import os.path
import pickle
import matplotlib.pyplot as plt
from pygmo import de1220

''' savedDictionary['log'] = log
    savedDictionary['pop'] = pop
    parametersdict = dict(zip(parameters, pop.champion_x))
    parametersdict.update(notOptimzedParameters)
    savedDictionary['best_parameters'] = parametersdict
    jsonPath = os.path.join(resultsPath, "champion.json")
    writeXtoJson(pop.champion_x, filename=jsonPath)
    savedDictionary['pupulationSize'] = populationSize
    savedDictionary['numberOfGenerations'] = numberOfGenerations
    savedDictionary['alfa'] = problem.alfa
    savedDictionary['beta'] = problem.beta'''

def takeResultsFromDirectory(directoryPath, numOfFiles):

    fitnessValues = []
    iterations = range(1, numOfFiles +1)

    for i in iterations:
        filePath = os.path.join(directoryPath,'resultsGeneration_'+str(i)+".pickle")
        results = []
        with (open(filePath, "rb")) as openfile:
            while True:
                try:
                    results.append(pickle.load(openfile))
                except EOFError:
                    break

        algo = results[0]['algorithm']
        uda = algo.extract(de1220)
        log = uda.get_log()
        fitnessValues.append(log[0][2])

def printResultsFromDirectory(directoryPath, numOfFiles):

    fitnessValues = []
    iterations = range(1, numOfFiles +1)

    for i in iterations:
        filePath = os.path.join(directoryPath,'resultsGeneration_'+str(i)+".pickle")
        results = []
        with (open(filePath, "rb")) as openfile:
            while True:
                try:
                    results.append(pickle.load(openfile))
                except EOFError:
                    break

        algo = results[0]['algorithm']
        uda = algo.extract(de1220)
        log = uda.get_log()
        fitnessValues.append(log[0][2])

    plt.plot(iterations, fitnessValues, 'k')
    plt.show()


def readResults(filepath):

    results = []
    with (open(filepath, "rb")) as openfile:
        while True:
            try:
                results.append(pickle.load(openfile))
            except EOFError:
                break

    pop = results[0]['pop']
    algo = results[0]['algorithm']
    uda = algo.extract(de1220)
    log = uda.get_log()
    pupulation_size = results[0]['pupulationSize']
    best_parameters = results[0]['best_parameters']
    alfa = results[0]['alfa']
    beta = results[0]['beta']
    number_of_generations = results[0]['numberOfGenerations']

    print(log)
    print('------------------ Algorithm Variables --------------')
    print('Population Size: ' + str(pupulation_size))
    print('Number of generations : ' + str(number_of_generations))
    print('Alfa: ' + str(alfa))
    print('Beta: ' + str(beta))
    print('Best parameters key,value are ' + best_parameters)
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')





if __name__ == "__main__":
    #readResults(r"C:\Users\Adria\OneDrive\Documenti\GitHub\natcomp2021\results\Run_210719-175212\resultsGeneration_100.pickle")
    printResultsFromDirectory(r"C:\Users\Adria\OneDrive\Documenti\GitHub\natcomp2021\results\Run_210719-175212",100)
