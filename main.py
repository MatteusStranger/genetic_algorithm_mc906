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
populations = ([[random.randint(1, 12) for x in range(5)] for i in range(4)])
print()
parents = []
new_populations = []
melhores_scores = []
melhores_cromossomos = []
print(f'População inicial: {populations}')


def fitness_score():
    global populations, best, melhores_scores, melhores_cromossomos
    fit_value = []
    for i in range(len(populations)):
        fit_value.append(test.predict(populations[i]))
    print(fit_value)

    fit_value, populations = zip(*sorted(zip(fit_value, populations), reverse=True))
    best = fit_value[0]
    print()
    print(f'Melhor Fitness da geração {best}')
    print(f'Melhor cromossomo da geração {populations[0]}')
    melhores_scores.append(best)
    melhores_cromossomos.append(populations[0])


def selectparent():
    global parents
    # global populations , parents
    parents = populations[0:2]
    print()
    print(f'Pais selecionados {parents}')


def crossover():
    global parents

    cross_point = random.randint(0, 4)
    parents = parents + tuple([(parents[0][0:cross_point + 1] + parents[1][cross_point + 1:6])])
    parents = parents + tuple([(parents[2][0:cross_point + 1] + parents[1][cross_point + 1:6])])
    print()
    print(f'Crossover: {parents}')


def mutation():
    global populations, parents
    print(f'População antiga pós-crossover: {populations}')
    mute = random.randint(0, 49) # Taxa de mutação

    print(f'População 64 {populations}')
    if mute == 20:
        x = random.randint(0, 3)
        y = random.randint(0, 4)
        parents[x][y] = random.randint(1,12)
    populations = parents
    print()
    print(f'População pós-mutação: {populations}')


M = 1
for i in range(M):
    print()
    print(f'Geração {i}')
    fitness_score()
    selectparent()
    crossover()
    mutation()

print()
print(f'Melhores fitness {melhores_scores}')
print()
print(f'Melhores cromossomos {melhores_cromossomos}')
print()
print("best score :")
print(best)
print()
print("sequence........")
print(populations[0])
print()
