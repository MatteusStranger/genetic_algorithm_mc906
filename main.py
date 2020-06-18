import extra_lib.metamodel as mmodel
import numpy as np
import extra_lib.ag_asex as ag_asex
import extra_lib.ga as ga
from timeit import Timer
import tools.report as r

r.clear_report()
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
    ga.setModel(test)
    print()
    print("Temos dois modos para rodar o código: execução e teste")
    print(
        "No primeiro modo o código será executado de modo default, como foi concebido inicialmente pelos desenvolvedores")
    print(
        "No segundo modo serão pedidas algumas entradas do usuário a fim de fazermos testes de parâmetros. Aqui a população inicial deixará de ser aleatória e será "
        "definida manualmente por padrão")
    print()
    print("1 - Execução")
    print("2 - Teste")

    modo = int(input())

    t = Timer(lambda: ga.execucao(modo))
    tempo = t.timeit(number=1)
    print(f"Tempo gasto para executar a reprodução sexuada {tempo:0.4f}s")

    # ########################## Reprodução assexuada #####################################
    # print(
    #     '-------------------------------------- Instanciando executando a reprodução asexuada --------------------------------------')
    #
    # ag1 = ag_asex.ag_asex()
    # ag1.setModel(test)
    # t = Timer(lambda: ag1.agOptim(ag1.fm, with_plot=True))
    # tempo = t.timeit(number=1)
    # print(f"Tempo gasto para executar a reprodução asexuada {tempo:0.4f}s")
