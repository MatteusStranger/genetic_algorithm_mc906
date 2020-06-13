import extra_lib.metamodel as mmodel
import numpy as np
import matplotlib.pyplot as plt

score = []  # melhor resultado da função objetiva
score_fit = []  # Armazena o melhor da geração
evolucao = []


def cromo(s0):
    """ Separa cromossomo em 4 partes"""
    vet = []
    vet.append(s0[0:5])
    vet.append(s0[5:10])
    vet.append(s0[10:15])
    vet.append(s0[15:20])
    vet.append(s0[20:])
    return vet


test = mmodel.metamodel()
test.cuda_status()
test.fit()
test.train_performance()
test.model_peformance()

s0 = np.random.randint(13,
                       size=25)

M = 1

for i in range(M):
    cromosome = []  # Guarda os cromossomos com crossover
    fit = []  # Guarda saída da função objetiva
    for j in range(len(s0)):
        v = cromo(s0)  # quebra em quatro partes
        for n in range(5):
            temp_max = test.predict(v[i])
            fit.append(temp_max)  # guarda função objetiva
        cromosome.append(s0)  # guarda o cromossomo

        if (np.median(fit) == np.max(fit)):
            # mutação se função obj negativa resultado repetido
            pos = np.random.randint(5)  # Escolhe uma das 4 variáveis
            np.random.shuffle(v[pos])  # Embaralha os bits de umas da variável
        s0 = list(v[0]) + list(v[1]) + list(v[2]) + list(v[3])  # junta partes
        s0 = np.roll(s0, -2)  # Faz crossover
        print(f'Novo s0 {s0}')

    nextGen = np.argmax(fit)  # Pega o melhor resultado para próxima geração
    score.append(np.max(fit))  # Armazena a melhor função obj
    score_fit.append(cromosome[nextGen])  # Armazena o melhor cromossomo

    if np.median(fit) == np.max(fit):
        # Se o resultado do melhor cromossomo repetir ele escolhe um aleatório
        # Stéfani: em vez de usar um aleatório, não é possível escolher o segundo melhor? Faz sentido?
        # Faz mutação em uma das posições do cromossomo
        s0 = cromosome[1]  # sorteia novo cromossomo
        # #Matteus Vargas: testando com o método de pegar o segundo melhor, que seria a posição 1 do array
        mutate = np.random.randint(len(s0))  # Escolhe uma posição para mutação
        s0[mutate] = 1 if s0[mutate] == 0 else 0  # Troca conteúdo
    else:
        s0 = cromosome[nextGen]

best = score_fit[np.argmax(score)]
best_varb = cromo(best)
print(f'Best cromosome {best_varb}')
