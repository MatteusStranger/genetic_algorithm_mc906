import numpy as np
import matplotlib.pyplot as plt

# Setup inicial
low_bound = 1  # Limite inferior
high_bound = 12  # Limite superior
exp = np.arange(4)  # Exponente de 0 até 4 (4 bits de precisão)
quantization = (high_bound - low_bound) / (2 ** 4 - 1)  # quantização
fc = lambda x, exp: np.sum(x * 2 ** exp) * quantization + low_bound  # decoficação
fy = lambda x1, x2, x3, x4: 5 * fc(x1, exp) - 3 * fc(x2, exp) * fc(x3, exp) \
                            + fc(x3, exp) - 2 * fc(x4, exp)  # função objetiva
#Matteus Vargas: o fy é o cara que preciso ficar modificando. Só preciso entender melhor os detalhes aqui

s0 = np.random.randint(2, size=16) #Matteus Vargas: deixei a população inicial aleatória. Vou trocar isso para entrada do usuário
print(f'População inicial (random) {s0}')
# s0 = np.array([0, 1, 1, 0,
#              1, 1, 0, 0,
#             1, 0, 1, 1,
#            0, 0, 0, 1])  # Estado inicial

M = 1000  # Numero de geração #Matteus Vargas: quero deixar esse valor aberto, só preciso achar uma forma de parada
score = []  # melhor resultado da função objetiva
score_fit = []  # Armazena o melhor da geração


def cromo(s0):
    """ Separa cromossomo em 4 partes"""
    vet = []
    vet.append(s0[0:4])
    vet.append(s0[4:8])
    vet.append(s0[8:12])
    vet.append(s0[12:])
    return vet

#Matteus Vargas: vou arrumar uma maneira de particionar as operações de GA em defs e colocar em outro arquivo. Deixar esse só para elaborar a função em si

for i in range(M):
    cromosome = []  # Guarda os cromossomos com crossover
    fit = []  # Guarda saída da função objetiva
    variables = []  # Guarda a saída de cada variável
    for j in range(len(s0) // 2 + 1):  # Rotaciona até dar uma volta completa
        v = cromo(s0)  # quebra em quatro partes
        temp_max = fy(v[0], v[1], v[2], v[3])  # Retorna a função objetiva
        fit.append(temp_max)  # guarda função objetiva
        cromosome.append(s0)  # guarda o cromossomo
        variables.append([fc(v[0], exp), fc(v[1], exp),
                          fc(v[2], exp), fc(v[3], exp)])  # Guarda variáveis
        if (np.min(temp_max) < 0) | (np.median(fit) == np.max(fit)):
            # mutação se função obj negativa resultado repetido
            pos = np.random.randint(4)  # Escolhe uma das 4 variáveis
            np.random.shuffle(v[pos])  # Embaralha os bits de umas da variável
        s0 = list(v[0]) + list(v[1]) + list(v[2]) + list(v[3])  # junta partes
        s0 = np.roll(s0, -2)  # Faz crossover
    nextGen = np.argmax(fit)  # Pega o melhor resultado para próxima geração
    score.append(np.max(fit))  # Armazena a melhor função obj
    score_fit.append(cromosome[nextGen])  # Armazena o melhor cromossomo
    if np.median(fit) == np.max(fit):
        # Se  resultado do melhor cromossomo repetir ele escolhe um aleatório
        # Faz mudatação em uma das posições  do cromossomo
        s0 = cromosome[np.random.randint(len(fit))]  # sorteia novo cromossomo
        mutate = np.random.randint(len(s0))  # Escolhe uma posição para mutação
        s0[mutate] = 1 if s0[mutate] == 0 else 0  # Troca conteúdo
    else:
        s0 = cromosome[nextGen]

best = score_fit[np.argmax(score)]
best_varb = cromo(best)
best_value = fy(best_varb[0], best_varb[1], best_varb[2], best_varb[3])
best_var = [fc(best_varb[0], exp), fc(best_varb[1], exp), fc(best_varb[2], exp), fc(best_varb[3], exp)]
print(f'Best value: {best_value} best cromosome {best} best combination of variables {best_var}')
plt.plot(score)
plt.savefig('graphics.png')
