import extra_lib.metamodel as mmodel
import numpy as np
import matplotlib.pyplot as plt
import random

test = mmodel.metamodel()
test.cuda_status()
test.fit()
test.train_performance()
test.model_peformance()

best = -100000
populations = ([[random.randint(1, 12) for x in range(5)] for i in range(4)])
parents = []
melhores_fitness = []
melhores_cromossomos = []
print(populations)


def fitness_score():
    global populations, best, best_cromossomo, scores, cromossomos, melhores_fitness, melhores_cromossomos
    cromossomos = []
    scores = []
    for i in range(len(populations)):
        scores.append(test.predict(populations[i]))

    best = np.max(scores)

    melhores_fitness.append(best)
    melhores_cromossomos.append(populations[scores.index(best)])

    worst = np.min(scores)
    print(f'Melhores scores linha 33: {melhores_fitness}')
    print(f'Melhores cromossomos linha 34: {populations[scores.index(best)]}')
    cromossomos.append(populations[scores.index(best)])
    cromossomos.append(populations[scores.index(worst)])
    # best_cromossomo = populations[scores.index(best)]


def selectparent():
    global parents, cromossomos
    # global populations , parents
    parents = cromossomos[0:2]
    print()
    print(f'Pais escolhidos: {parents}')


def crossover():
    global parents, pais
    pais = []
    cross_point = random.randint(0, 4)

    pais.append(tuple([parents[0][0:cross_point + 1] + parents[1][cross_point + 1:6]]))
    pais.append(tuple([parents[1][0:cross_point + 1] + parents[0][cross_point + 1:6]]))
    print()
    print(f'Crossover feito {pais}')
    print()


def mutation():
    global populations, pais

    print(f'Iniciando a mutação nos pais: {pais}')

    x = random.randint(0, 4)
    y = random.randint(0, 4)

    mae = pais[0][0]
    pai = pais[1][0]
    print()

    mae[y] = random.randint(1, 12)
    pai[x] = random.randint(1, 12)

    print(f'Mae mutante {mae}')
    print(f'Pai mutante {pai}')
    print()
    populations.append(mae)
    populations.append(pai)
    print(f'Nova população: {populations}')


M = 3
for i in range(M):
    print(f'Geração {i}')
    fitness_score()
    selectparent()
    crossover()
    mutation()
    print()
    print(f'Melhores scores da geração: {melhores_fitness}')
    print(f'Melhores cromossomos da geração: {melhores_cromossomos}')
    print()

print("best score :")
print(best)
print("sequence........")
print(populations[0])
