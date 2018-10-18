from ast import literal_eval
import helloWorld as hW

def check(island):
    population = []
    with open('island_{0}.txt'.format(island), 'r') as f:
        for line in f:
            population.append(literal_eval(line))
    f.close()
    ant = population[0]
    stable = False
    for ind in range(len(population)):
        value = hW.evaluateIndividual(population[ind])
        if value >= 9600:
            stable = False
        if value < 9600:
            return True
    return stable
