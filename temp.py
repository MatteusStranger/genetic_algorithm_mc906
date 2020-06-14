import matplotlib.pyplot as plt
import random
import extra_lib.metamodel as mmodel

test = mmodel.metamodel()
test.cuda_status()
test.fit()
# test.train_performance()
test.model_peformance()

best = -100000
populations = ([[random.randint(1, 12) for x in range(5)] for i in range(4)])
# fm = lambda x1, x2, x3, x4, x5: mmodel.predict([x1, x2, x3, x4, x5])[0][0]
parents = []
new_populations = []
melhores = []
geracoes = []


def fitness_score():
    global populations, best
    fit_value = []
    fit_score = []
    for i in range(len(populations)):
        fit_value.append(test.predict(populations[i]))
    fit_value, populations = zip(*sorted(zip(fit_value, populations), reverse=True))
    best = fit_value[0]
    melhores.append(best)


def selectparent():
    global parents
    # global populations , parents
    parents = populations[0:2]



def crossover():
    global parents
    cross_point = random.randint(0, 3)
    parents = parents + tuple([(parents[0][0:cross_point + 1] + parents[1][cross_point + 1:6])])
    parents = parents + tuple([(parents[1][0:cross_point + 1] + parents[0][cross_point + 1:6])])


def mutation():
    global populations, parents
    mute = random.randint(0, 49)
    if mute == 25:
        x = random.randint(0, 3)
        y = random.randint(0, 4)

        if (y == 0):
            parents[x][y] = random.randint(1, 3)  # 1 - parents[x][y]
        if (y == 1):
            parents[x][y] = random.randint(1, 4)  # 1 - parents[x][y]
        if (y == 2):
            parents[x][y] = random.randint(1, 5)  # 1 - parents[x][y]
        if (y == 3):
            parents[x][y] = random.randint(1, 6)  # 1 - parents[x][y]
        if (y == 4):
            parents[x][y] = random.randint(1, 12)  # 1 - parents[x][y]
    print(f'Mutação {parents}')
    populations = parents


def plotar_graficos(geracoes, melhores):
    aux = []
    for i in range(len(melhores)):
        aux.append(float(melhores[i]))

    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.plot(geracoes, aux)
    plt.show()


def ajusta_populacao(populations):
    for i in range(4):
        for x in range(5):
            if (x == 0 and (populations[i][x] not in range(1, 3))):
                populations[i][x] = random.randint(1, 3)
            if (x == 1 and (populations[i][x] not in range(1, 4))):
                populations[i][x] = random.randint(2, 4)
            if (x == 2 and (populations[i][x] not in range(1, 5))):
                populations[i][x] = random.randint(3, 5)
            if (x == 3 and (populations[i][x] not in range(1, 6))):
                populations[i][x] = random.randint(4, 6)
            if (x == 4 and (populations[i][x] not in range(1, 12))):
                populations[i][x] = random.randint(10, 12)


ajusta_populacao(populations)

for i in range(2000):
    geracoes.append(i)
    fitness_score()
    selectparent()
    crossover()
    mutation()

# print("best score :")
# print(best)
# print("sequence........")
# print(populations[0])

plotar_graficos(geracoes, melhores)
