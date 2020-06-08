import numpy

def ajuste_da_populacao(valores_de_x, nova_populacao):
    print()
    print(f'Nova população {nova_populacao}')
    print()
    ajuste = numpy.divide(nova_populacao, valores_de_x)#, axis=1)
    print()
    print(f'Ajuste {ajuste}')
    print()
    return ajuste


def escolhe_pais(nova_populacao, ajuste, acasalamento):
    # Selecionar os melhores indivíduos da geração atual como pais para produzir o cruzamento da próxima geração.
    pais = numpy.empty((acasalamento, nova_populacao.shape[1]))
    for selecao_de_pais in range(acasalamento):
        ajuste_pai = numpy.where(ajuste == numpy.max(ajuste))
        ajuste_pai = ajuste_pai[0][0]
        pais[selecao_de_pais, :] = nova_populacao[ajuste_pai, :]
        ajuste[ajuste_pai] = -99999999999
    return pais


def cruzamento(pais, tam_descendencia):
    cruzamento = numpy.empty(tam_descendencia)
    # O ponto em que o cruzamento ocorre entre dois pares. Geralmente, está no centro.
    momento_de_cruzar = numpy.uint8(tam_descendencia[1] / 2)

    for k in range(tam_descendencia[0]):
        mae = k % pais.shape[0]

        pai = (k + 1) % pais.shape[0]
        # O novo cruzamento terá sua primeira metade de seus genes extraídos para mãe.
        cruzamento[k, 0:momento_de_cruzar] = pais[mae, 0:momento_de_cruzar]
        # O novo cruzamento terá sua segunda metade de seus genes extraídos com pai.
        cruzamento[k, momento_de_cruzar:] = pais[pai, momento_de_cruzar:]
    return cruzamento


def mutacao(varios_cruzamentos, num_mutacao=1):
    conta_mutacao = numpy.uint8(varios_cruzamentos.shape[1] / num_mutacao)
    # As mudanças são aleatórias.
    for idx in range(varios_cruzamentos.shape[0]):
        gene_idx = conta_mutacao - 1
        for mutation_num in range(num_mutacao):
            # O valor aleatório a ser adicionado ao gene.
            random_value = numpy.random.uniform(-1.0, 1.0, 1)
            varios_cruzamentos[idx, gene_idx] = varios_cruzamentos[idx, gene_idx] + random_value
            gene_idx = gene_idx + conta_mutacao
    return varios_cruzamentos


# Entradas da equação. Esses são os valores de X1,X2,X3,X4. O que vamos procurar são os pesos

valores_de_x = [3, 1, 4, 4, 1]
pesos_da_equacao = len(valores_de_x)

solucao_por_populacao = 5
acasalamento = 4

# Definindo o tamanho da população.
tam_populacao = (solucao_por_populacao,
                 pesos_da_equacao)  # A população terá o cromossomo solucao_por_populacao em que cada cromossomo possui genes pesos_da_equacao.
# Cria a população inicial
nova_populacao = numpy.random.uniform(low=1, high=12.0, size=tam_populacao)
print(nova_populacao)

melhores = []
geracoes = 1
for geracao in range(geracoes):
    print("Geracao : ", geracao)
    # Medir o ajuste de cada cromossomo na população. A operação é para ser "genérica"
    ajuste = ajuste_da_populacao(valores_de_x, nova_populacao)
    print("Ajuste")
    print(ajuste)

    melhores.append(numpy.max(numpy.sum(nova_populacao * valores_de_x, axis=1)))
    # O melhor da geração
    print("Melhor local : ", numpy.max(numpy.sum(nova_populacao * valores_de_x, axis=1)))

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

ajuste = ajuste_da_populacao(valores_de_x, nova_populacao)
os_melhores = numpy.where(ajuste == numpy.max(ajuste))

print("Melhor combinacao para os X: ", nova_populacao[os_melhores, :])
print("Melhor resultado de Y: ", ajuste[os_melhores])
