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
    pupulationSize = results[0]['pupulationSize']
    alfa = results[0]['alfa']
    beta = results[0]['beta']
    numberOfGenerations = results[0]['numberOfGenerations']

    print(log)
    print('------------------ Algorithm Variables --------------')
    print('Population Size: ' + str(pupulationSize))
    print('Number of generations : ' + str(numberOfGenerations))
    print('Alfa: '+ str(alfa))
    print('Beta: '+ str(beta))
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')

    plt.plot([entry[0] for entry in log], [entry[2] for entry in log], 'k')
    plt.show()

if __name__ == "__main__":
    readResults(r"C:\Users\Adria\OneDrive\Documenti\GitHub\natcomp2021\results\Run_210719-153114\resultsGeneration_3.pickle")

