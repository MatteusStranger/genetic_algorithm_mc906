import extra_lib.metamodel as mmodel
import matplotlib.pyplot as plt
import numpy
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
populations = ([[random.randint(1, 12) for x in range(5)] for i in range(4)])  # População inicial
parents = []  # Pais nos crossovers
melhores_scores = []  # Eleição dos melhores fitness
melhores_cromossomos = []  # Eleição dos melhores cromossomos
crossover_results = []  # Resultado dos crossovers
scores = []
geracoes = []
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


def fitness_score():  # Aqui são eleitos os cromossomos com os melhores desempenhos de sua geração
    global populations, best, melhores_scores, melhores_cromossomos, scores, geracoes
    fit_value = []
    print()
    for i in range(len(populations)):
        fit_value.append(
            test.predict(populations[i]))  # Aqui é aplicada a predição com cada um dos cromossomos da população.
        # Seu resultado é guardado em uma lista

    print(f'Valores de fitness: {fit_value}')
    print()
    fit_value, populations = zip(*sorted(zip(fit_value, populations),
                                         reverse=True))  # Associa-se os melhores cromossomos aos seus scores, ordenado pelo score
    best = fit_value[0]  # Variável que guarda o melhor desempenho da geração
    print(
        f'População ordenada por score: {populations}')  # População ordenada pelo score, do melhor ao pior. Esse esquema será base para o crossover
    scores.append(best)
    melhores_scores.append(best)  # Guardam os scores ordenados
    melhores_cromossomos.append(populations[0])  # Guarda o melhor cromossomo da geração


def selectparent():  # Escolhem-se os pais
    global parents, populations
    parents.clear()
    # Nesse esquema, por ser uma população para, então fecham-se casais
    # O crossover se dá pelo cruzamento do melhor com o pior, do segundo melhor com o segundo pior

    parents.append(populations[0])
    parents.append(populations[3])
    parents.append(populations[1])
    parents.append(populations[2])
    print(f'Casais formados {parents}')
    print()


def crossover():
    global parents, crossover_results, populations
    cross_point = 2  # Ponto de corte no cromossomo
    crossover_results.clear()
    # Para formar novos filhos, pega-se a primeira metade da mãe e junta com a segunda metade do pai
    # O segundo filho, pegam as metades inversas, até serem formados 4 novos filhos, que
    # Irão substituir por completo a geração anterior, sem elitismo
    crossover_results.append(parents[0][0:cross_point + 1] + parents[1][cross_point + 1:])
    crossover_results.append(parents[0][cross_point + 1:] + parents[1][0:cross_point + 1])
    crossover_results.append(parents[2][0:cross_point + 1] + parents[3][cross_point + 1:])
    crossover_results.append(parents[2][cross_point + 1:] + parents[3][0:cross_point + 1])

    print()
    print(f'Crossover feito: {crossover_results}')


def mutation():
    global populations, crossover_results
    # O esquema de mutação funciona como um ajuste do crossover
    # Apelidado aqui de "correção genética", a mutação anda de gene em gene verificando se
    # O limite superior está correto. Caso não esteja, um novo valor, dentro do seu respectivo
    # limite é sorteado, permitindo que a regra dos limites seja mantida
    mute = random.randint(0, 100)
    if mute == 2:
        for i in range(4):
            for x in range(5):
                if (x == 0 and (crossover_results[i][x] not in range(1, 3))):
                    crossover_results[i][x] = random.randint(2, 3)

                if (x == 1 and (crossover_results[i][x] not in range(1, 4))):
                    crossover_results[i][x] = random.randint(3, 4)

                if (x == 2 and (crossover_results[i][x] not in range(1, 5))):
                    crossover_results[i][x] = random.randint(4, 5)

                if (x == 3 and (crossover_results[i][x] not in range(1, 6))):
                    crossover_results[i][x] = random.randint(5, 6)

                if (x == 4 and (crossover_results[i][x] not in range(1, 12))):
                    crossover_results[i][x] = random.randint(6, 12)

    populations = crossover_results
    print()
    print(f'População pós-mutação: {populations}')


def ajusta_populacao():
    global populations
    for i in range(4):
        for x in range(5):
            if (x == 0):
                populations[i][x] = random.randint(1, 3)
            if (x == 1):
                populations[i][x] = random.randint(2, 4)
            if (x == 2):
                populations[i][x] = random.randint(3, 5)
            if (x == 3):
                populations[i][x] = random.randint(4, 6)
            if (x == 4):
                populations[i][x] = random.randint(10, 12)


def plotar_grafico(geracoes, scores):
    global mem, cpu, pid
    aux = []
    for i in range(len(scores)):
        aux.append(float(scores[i]))

    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.plot(geracoes, aux)
    plt.show()
    print()
    print("Monitoramos o uso de memória e cpu ao longo das gerações, gostaria de ver os gráficos de desempenho?")
    print()
    print("1 - Sim")
    print("0 - Não")
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


if (segue == 1):
    M = generations()
    ajusta_populacao()  # O ajuste aqui serve para corrigir falhas que possa ter ocorrido na criação
    # da população inicial, em função dos limites superiores de cada variável
    for i in range(M):
        geracoes.append(i)
        print()
        print()
        print(
            f'-------------------------------------- Iniciando o AG, geração {i} --------------------------------------')
        print()
        print()
        print(f'População inicial da geração {i}: {populations}')
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
    melhores_scores, melhores_cromossomos = zip(*sorted(zip(melhores_scores, melhores_cromossomos), reverse=True))
    plotar_grafico(geracoes, scores)
    print(f'Melhor fitness {melhores_scores[0]}')
    print()
    print(f'Melhor cromossomo {melhores_cromossomos[0]}')
    print()
