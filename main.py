import extra_lib.metamodel as mmodel
import numpy as np
import matplotlib.pyplot as plt
import random

test = mmodel.metamodel()
test.cuda_status()
test.fit()
test.train_performance()
test.model_peformance()

import random

best = -100000
low_bound = 1
high_bound = 12
populations = ([[random.randint(low_bound, high_bound) for x in range(5)] for i in range(4)])
print()
parents = []
new_populations = []
melhores_scores = []
melhores_cromossomos = []
crossover_results = []
geracoes = []


def generations():
    return high_bound ** 3


def fitness_score():
    global populations, best, melhores_scores, melhores_cromossomos
    fit_value = []
    for i in range(len(populations)):
        fit_value.append(test.predict(populations[i]))
    print(fit_value)

    fit_value, populations = zip(*sorted(zip(fit_value, populations), reverse=True))
    best = fit_value[0]
    print(f'População ordenada por score: {populations}')
    melhores_scores.append(best)
    melhores_cromossomos.append(populations[0])


def selectparent():
    global parents, populations
    parents.clear()
    parents.append(populations[0])
    parents.append(populations[3])
    parents.append(populations[1])
    parents.append(populations[2])
    print(f'Pais escolhidos {parents}')
    # global populations , parents


def crossover():
    global parents, crossover_results, populations
    cross_point = 2
    crossover_results.clear()
    crossover_results.append(parents[0][0:cross_point] + parents[1][cross_point:])
    crossover_results.append(parents[0][cross_point:] + parents[1][0:cross_point])
    crossover_results.append(parents[2][0:cross_point] + parents[3][cross_point:])
    crossover_results.append(parents[2][cross_point:] + parents[3][0:cross_point])

    print()
    print(f'Crossover: {crossover_results}')


def mutation():
    global populations, crossover_results
    print(f'População antiga pós-crossover: {crossover_results}')

    for i in range(len(crossover_results)):
        y = random.randint(0, 3)
        mute = random.randint(5, 12)
        crossover_results[i][y] = mute
        print(crossover_results[i][y])
    populations = crossover_results
    print()
    print(f'População pós-mutação: {populations}')


M = generations()
for i in range(M):
    print(f'População inicial: {populations}')
    print()
    print(f'Geração {i}')
    geracoes.append(i)
    fitness_score()
    selectparent()
    crossover()
    mutation()

print()
melhores_scores, melhores_cromossomos = zip(*sorted(zip(melhores_scores, melhores_cromossomos), reverse=True))
print(f'Melhor fitness {melhores_scores[0]}')
print()
print(f'Melhor cromossomo {melhores_cromossomos[0]}')
print()
