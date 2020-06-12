import numpy


def adjust(valores_de_x, nova_populacao):
    print()
    print(f'Nova população {nova_populacao}')
    print()
    ajuste = numpy.sum(nova_populacao, valores_de_x)  # , axis=1)
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
