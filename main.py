import extra_lib.metamodel as mmodel
import numpy as np
import extra_lib.ag_asex as ag_asex
import extra_lib.ga as ga
from timeit import Timer

print()
print(
    "Matias Vargas Maekawa Fernandes Moraes e Silva (MVMFMS) é um diretor de hospital que visa atender o máximo de pacientes possível em sua unidade hospitalar.")
print("Para isso, ele precisa saber quantos funcionarios ele deverá contratar e qual o seu ganho com isso.")
print(
    "A sua equipe técnica projetou uma solução que toma a quantidade de recepcionistas, técnicos, médicos, enfermeiras na sala de tratamento e enfermeiras na sala de emergência, sendo representadas respectivamente pelas variáveis x1, x2, x3, x4, x5.")
print("Este problema é baseado em um caso real definido no trabalho de Ahmed e Alkhamis (2009).")
print("Será agora instanciado um metamodelo, baseado em redes neurais, que consome um dataset coletado para este caso.")
print("Esse metamodelo é usado como função de fitness no algoritmo genético")
print("Para deixar as coisas mais interessantes, MVMFMS dividiu sua equipe em duas partes")
print("A primeira parte desenvolveu um esquema clássico de Algoritmo Genético, com crossover e mutação")
print("Já a segunda equipe buscou uma abordagem assexuada. Ambos serão executados à seguir")
print("Spoiler: mais interessante que o resultado, foi o caminho percorrido")
print("Enjoy")
print()
print("Pressione 1 para continuar e 0 para abortar")
print()
segue = int(input())

if (segue == 1):
    print('-------------------------------------- Instanciando o metamodelo --------------------------------------')
    test = mmodel.metamodel()
    test.cuda_status()
    test.fit()
    print()
    print(
        '-------------------------------------- Instanciando executando a reprodução sexuada --------------------------------------')
    ############################ Reprodução sexuada ########################################
    test.model_peformance()
    ga.setModel(test)
    # ga.execucao()

    t = Timer(lambda: ga.execucao())
    tempo = t.timeit(number=1)
    print(f"Tempo gasto para executar a reprodução sexuada {tempo:0.4f}s")

    ########################## Reprodução assexuada #####################################
    print(
        '-------------------------------------- Instanciando executando a reprodução asexuada --------------------------------------')
    exp = np.arange(4)
    low_bounds = np.array([1, 1, 1, 1, 1])
    high_bounds = np.array([3, 4, 5, 6, 12])
    quantizations = (high_bounds - low_bounds) / (2 ** 4 - 1)  # quantização
    fc = lambda x, exp, _type: np.sum(x * 2 ** exp) * quantizations[_type] + low_bounds[_type]  # decoficação
    fy = lambda x1, x2, x3, x4, x5: 1.113 * fc(x2, exp, 1).astype(int) + 0.701 * fc(x2, exp, 1).astype(int) * fc(x3,
                                                                                                                 exp,
                                                                                                                 2).astype(
        int) + 0.207 * fc(x2, exp, 1).astype(int) * fc(x5, exp, 4).astype(int) + 0.021 * fc(x1, exp, 0).astype(
        int) * fc(x5, exp, 4).astype(int) - \
                                    0.435 * fc(x2, exp, 1).astype(int) ** 2 - 0.013 * fc(x2, exp, 1).astype(int) * fc(
        x5, exp, 4).astype(int) ** 2 - 0.092 * fc(x2, exp, 1).astype(int) * fc(x3, exp, 2).astype(int) ** 2
    fm = lambda x1, x2, x3, x4, x5: test.predict(
        [fc(x1, exp, 0).astype(int), fc(x2, exp, 1).astype(int), fc(x3, exp, 2).astype(int), fc(x3, exp, 3).astype(int),
         fc(x4, exp, 4).astype(int)])[0][0]

    ag1 = ag_asex.ag_asex()
    ag1.setModel(test)
    t = Timer(lambda: ag1.agOptim(fm, with_plot=True))
    tempo = t.timeit(number=1)
    print(f"Tempo gasto para executar a reprodução asexuada {tempo:0.4f}s")

