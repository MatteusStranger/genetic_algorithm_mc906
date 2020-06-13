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
new_populations = []
print(populations)


def fitness_score():
    global populations, best, best_cromossomo, scores
    scores = []
    for i in range(len(populations)):
        scores.append(test.predict(populations[i]))

    best = np.max(scores)
    best_cromossomo = populations[scores.index(best)]


def selectparent():
    global parents
    # global populations , parents
    parents = populations[0:2]


def crossover():
    global parents, pais
    pais = []
    cross_point = random.randint(0, 4)

    pais.append(tuple([parents[0][0:cross_point + 1] + parents[1][cross_point + 1:6]]))
    pais.append(tuple([parents[1][0:cross_point + 1] + parents[0][cross_point + 1:6]]))
    print(f'Pais {pais}')


def mutation():
    global populations, pais
    x = random.randint(0, 4)
    y = random.randint(0, 4)
    print(f'X {x} Y {y}')
    mae = pais[0][0]
    pai = pais[1][0]
    print(f'Mae {mae[y]}')
    print(f'Pai {pai[x]}')
    populations.append(mae)
    populations.append(pai)
    print(f'Populações {populations}')


for i in range(1):
    fitness_score()
    selectparent()
    crossover()
    mutation()

print("best score :")
print(best)
print("sequence........")
print(populations[0])
