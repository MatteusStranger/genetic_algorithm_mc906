import extra_lib.metamodel as mmodel
import matplotlib.pyplot as plt
import random
import tools.monitor as monitor

# As próximas cinco linhas referem-se à criação, ajuste e treinamento da rede neural que
# serve como metamodelo para este problema. Sua operação de predição será o nosso fitness
print()
print(
    "Matias Vargas Maekawa Fernandes Moraes e Silva (MVMFMS) é um diretor de hospital que visa atender o máximo de pacientes possível em sua unidade hospitalar.")
print("Para isso, ele precisa saber quantos funcionarios ele deverá contratar e qual o seu ganho com isso.")
print(
    "A sua equipe técnica projetou uma solução que toma a quantidade de recepcionistas, técnicos, médicos, enfermeiras na sala de tratamento e enfermeiras na sala de emergência, sendo representadas respectivamente pelas variáveis x1, x2, x3, x4, x5.")
print("Este problema é baseado em um caso real definido no trabalho de Ahmed e Alkhamis (2009).")
print("Será agora instanciado um metamodelo, baseado em redes neurais, que consome um dataset coletado para este caso.")
print(
    "Em seguida, o algoritmo genético desenvolvido deverá maximizar as entradas a fim de definir os melhores valores possíveis para cada variável.")

print()
print("Pressione 1 para continuar e 0 para abortar")
print()
segue = int(input())

if (segue == 1):
    print('-------------------------------------- Instanciando o metamodelo --------------------------------------')
    test = mmodel.metamodel()
    test.cuda_status()
    test.fit()
    # test.train_performance()
    test.model_peformance()

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
pid = []


def uso_recursos():
    global mem, cpu, pid
    memoria, processador, processos = monitor.monitor()
    mem.append(memoria)
    cpu.append(processador)
    pid.append(processos)


def generations():
    return high_bound ** 3  # Estima uma quantidade suficientemente boa para a quantidade de gerações


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


ajusta_populacao(populations)
print(f'População inicial {populations}')
if (segue == 1):
    M = generations()
    for i in range(M):
        geracoes.append(i)
        print()
        print()
        print(
            f'-------------------------------------- Iniciando o AG, geração {i} --------------------------------------')
        print()
        print()
        print('-------------------------------------- Aplicando o fitness --------------------------------------')
        fitness_score()
        print()
        print('-------------------------------------- Selecionando os pais --------------------------------------')
        selectparent()
        print()
        print('-------------------------------------- Aplicando o crossover --------------------------------------')
        print()
        crossover()
        print('-------------------------------------- Aplicando a mutação --------------------------------------')
        mutation()
        print()
        uso_recursos()

    print()
    # Informa para o usuário os resultados
    print(f"Melhor resultado : {best}")
    print()
    print(f"Melhor cromossomos: {populations[0]}")
    print()

    plotar_grafico(geracoes, melhores)
