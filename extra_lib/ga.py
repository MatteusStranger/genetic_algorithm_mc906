import random
import matplotlib.pyplot as plt
import extra_lib.monitor as monitor

# Instanciação das variáveis globais principais
best = -100000
high_bound = 12  # Limite superior, útil para estimar as gerações
populations = ([[random.randint(1, 12) for x in range(5)] for i in range(4)])
parents = []  # Pais nos crossovers
melhores_scores = []  # Eleição dos melhores fitness
melhores_cromossomos = []  # Eleição dos melhores cromossomos
crossover_results = []  # Resultado dos crossovers
scores = []
geracoes = []
melhores = []
mem = []
cpu = []


def setModel(model):
    global test
    test = model


def uso_recursos():
    global mem, cpu
    memoria, processador = monitor.monitor()
    mem.append(memoria)
    cpu.append(processador)


def fitness_score():
    global populations, best
    fit_value = []
    for i in range(len(populations)):
        fit_value.append(test.predict(populations[i]))
    fit_value, populations = zip(*sorted(zip(fit_value, populations), reverse=True))
    best = fit_value[0]
    melhores.append(best)


def selectparent():
    global parents
    # global populations , parents
    parents = populations[0:2]


def crossover(corte):
    global parents
    cross_point = corte
    parents = parents + tuple([(parents[0][0:cross_point + 1] + parents[1][cross_point + 1:6])])
    parents = parents + tuple([(parents[1][0:cross_point + 1] + parents[0][cross_point + 1:6])])


def mutation(taxa_mutacao):
    global populations, parents
    mute = random.randint(0, 100)
    if mute == taxa_mutacao:
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
    populations = parents


def plotar_grafico(geracoes, scores):
    global mem, cpu
    aux = []
    for i in range(len(melhores)):
        aux.append(float(melhores[i]))

    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.plot(geracoes, aux)
    plt.show()
    print("Monitoramos o uso de memória e cpu durante as gerações. "
          "Gostaria de ver os resultos em gráfico?")
    print()
    print("1 - Sim")
    print("0 - Nao")
    print()
    segue = int(input())

    if (segue == 1):
        plt.xlabel('Gerações')
        plt.ylabel('Memória')
        plt.plot(geracoes, mem)
        plt.show()

        plt.xlabel('Gerações')
        plt.ylabel('CPU')
        plt.plot(geracoes, cpu)
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


def execucao(modo):
    ajusta_populacao(populations)
    print(f'População inicial {populations}')

    if(modo == 2):
        print()
        print("Entre com a quantidade de gerações")
        M = int(input())
        print()
        print("O crossover padrão divide o cromossomo exatamente no meio. Nesse modo você pode escolher"
              "a posição de corte. Escolha um valor entre 0~4")
        corte = int(input())
        print()
        print("Defina a sua taxa de mutação. Esse valor corresponde as chances de uma geração sofrer mutação."
              "Isso é importante para alcançar uma boa solução"
              " Entre com um valor entre 0~100")
        taxa_mutacao = int(input())
    else:
        M = 2000
        corte = 2
        taxa_mutacao = 25

    for i in range(M):
        print()
        print(f'Geração {i}')
        print()
        geracoes.append(i)

        fitness_score()
        selectparent()
        crossover(corte)
        mutation(taxa_mutacao)
        uso_recursos()

    print()
    print(f"Melhor resultado : {best}")
    print()
    print()

    plotar_grafico(geracoes, melhores)
