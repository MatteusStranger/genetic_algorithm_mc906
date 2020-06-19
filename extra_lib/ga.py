import random
import matplotlib.pyplot as plt
import extra_lib.monitor as monitor
import tools.report as r

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


def define_snapshot(M, geracao):
    if ((geracao / M) in (0.25, 0, 4, 0.55, 0.7, 0.85, 0.95, 1)):
        return True
    else:
        return False


def setModel(model):
    global test
    test = model


def uso_recursos():
    global mem, cpu
    memoria, processador = monitor.monitor()
    mem.append(memoria)
    cpu.append(processador)


def fitness_score(snapshot):
    global populations, best, melhores_cromossomos
    fit_value = []
    for i in range(len(populations)):
        fit_value.append(test.predict(populations[i]))
    fit_value, populations = zip(*sorted(zip(fit_value, populations), reverse=True))
    best = fit_value[0]
    melhores.append(best)
    melhores_cromossomos.append(populations[0])
    if (snapshot == True):
        r.write_text(f'Melhor fitness {best}')


def selectparent(snapshot):
    global parents
    # global populations , parents
    parents = populations[0:2]
    if (snapshot == True):
        r.write_text(f'Pais selecionados {parents}')


def crossover(corte, snapshot):
    global parents
    cross_point = corte
    parents = parents + tuple([(parents[0][0:cross_point + 1] + parents[1][cross_point + 1:6])])
    parents = parents + tuple([(parents[1][0:cross_point + 1] + parents[0][cross_point + 1:6])])
    if (snapshot == True):
        r.write_text(f'Ponto de corte no cromossomo {cross_point}')
        r.write_text(f'Filhos {parents}')


def mutation(taxa_mutacao, snapshot):
    global populations, parents
    print(f'Populacao {parents}')
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

    print(f'Nova Populacao {parents}')
    if (snapshot == True):
        r.write_text(f'Taxa de mutação definida pelo usuário {taxa_mutacao}, taxa de mutação definida {mute}')
        r.write_text(f'Nova população {populations}')


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
    if (modo == 2):
        print()
        print("Gostaria de uma população fixa ou aleatória?")
        print("0 - Fixa")
        print("1 - Aleatória")
        pop = int(input())
        if pop == 0:
            global populations
            populations = [[3, 1, 3, 3, 10], [1, 3, 5, 2, 9], [2, 2, 3, 4, 12], [3, 2, 5, 6, 5]]
            print()
            print(f'População inicial {populations}')
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
        ajusta_populacao(populations)
        print(f'População inicial {populations}')
        M = 2000
        corte = 2
        taxa_mutacao = 25

    for i in range(M):
        print()
        print(f'Geração {i}')
        print()
        geracoes.append(i)
        snapshot = define_snapshot(M, i)
        if (snapshot):
            r.write_text()
            r.write_text(f"Snapshot da geração {i}")
        fitness_score(snapshot)
        selectparent(snapshot)
        crossover(corte, snapshot)
        mutation(taxa_mutacao, snapshot)
        uso_recursos()

    print()
    bests, melhores_crom = zip(*sorted(zip(melhores, melhores_cromossomos), reverse=True))
    print(f"Melhor resultado : {bests[0]}")
    print()
    print(f"Melhor Cromossomo : {melhores_crom[0]}")
    print()

    plotar_grafico(geracoes, melhores)
