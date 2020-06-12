import extra_lib.metamodel as mmodel
import numpy as np
import matplotlib.pyplot as plt
from ga import *
from ga import ajuste_da_populacao

test = mmodel.metamodel()
test.cuda_status()
test.plot_correlations()
test.plot_distributions()

test.fit()
test.model_peformance()

valores_de_x = np.array([1, 1, 1, 1, 1])

print(test.predict([1, 1, 1, 1, 1]))

print(test.predict(np.array([1, 1, 1, 1, 1])))

pesos_da_equacao = len(valores_de_x)

solucao_por_populacao = 5
acasalamento = 4

# Definindo o tamanho da população.
tam_populacao = (solucao_por_populacao,
                 pesos_da_equacao)  # A população terá o cromossomo solucao_por_populacao em que cada cromossomo possui genes pesos_da_equacao.
# Cria a população inicial
nova_populacao = np.random.uniform(low=1, high=12.0, size=tam_populacao)
print(nova_populacao)

melhores = []
geracoes = 1000
for geracao in range(geracoes):
    print("Geracao : ", geracao)
    # Medir o ajuste de cada cromossomo na população. A operação é para ser "genérica"
    ajuste = ajuste_da_populacao(valores_de_x, nova_populacao)
    print("Ajuste")
    print(ajuste)

    melhores.append(np.max(np.sum(nova_populacao * valores_de_x, axis=1)))
    # O melhor da geração
    print("Melhor local : ", np.max(np.sum(nova_populacao * valores_de_x, axis=1)))

    # Escolhendo os melhores pais
    pais = escolhe_pais(nova_populacao, ajuste,
                           acasalamento)
    print("Pais")
    print(pais)

    # Cruzar para montar a nova geração
    varios_cruzamentos = cruzamento(pais,
                                       tam_descendencia=(tam_populacao[0] - pais.shape[0], pesos_da_equacao))
    print("Cruzamento")
    print(varios_cruzamentos)

    # Mutação para adicionar mudanças
    descendencia_mutacao = mutacao(varios_cruzamentos, num_mutacao=2)
    print("Mutacao")
    print(descendencia_mutacao)

    # Criando a nova população com base nos pais e na descendência.
    nova_populacao[0:pais.shape[0], :] = pais
    nova_populacao[pais.shape[0]:, :] = descendencia_mutacao

# Obtendo a melhor combinação após iterar, finalizando todas as gerações.
# Inicialmente, o ajuste é calculado para cada solução na geracao final.

ajuste = adjust(valores_de_x,nova_populacao)
os_melhores = np.where(ajuste == np.max(ajuste))

print("Melhor combinacao para os X: ", nova_populacao[os_melhores, :])
print("Melhor resultado de Y: ", ajuste[os_melhores])
