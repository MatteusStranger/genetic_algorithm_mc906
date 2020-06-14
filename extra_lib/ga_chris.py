import numpy as np
import metamodel as hospitalModel
import matplotlib.pyplot as plt
mm = hospitalModel.metamodel()
mm.fit()

exp=np.arange(4)
low_bounds = np.array([1,1,1,1,1])
high_bounds = np.array([3,4,5,6,12])
quantizations = (high_bounds - low_bounds) /(2**4-1) # quantização
fc = lambda x,exp,_type:np.sum(x*2**exp)*quantizations[_type] + low_bounds[_type] # decoficação

fy = lambda x1,x2,x3,x4,x5: 1.113*fc(x2,exp,1).astype(int) + 0.701*fc(x2,exp,1).astype(int)*fc(x3,exp,2).astype(int) + 0.207*fc(x2,exp,1).astype(int)*fc(x5,exp,4).astype(int) + 0.021*fc(x1,exp,0).astype(int)*fc(x5,exp,4).astype(int) - \
                            0.435*fc(x2,exp,1).astype(int)**2 - 0.013*fc(x2,exp,1).astype(int)*fc(x5,exp,4).astype(int)**2 -0.092*fc(x2,exp,1).astype(int)*fc(x3,exp,2).astype(int)**2
fm= lambda x1,x2,x3,x4,x5: mm.predict([fc(x1,exp,0).astype(int), fc(x2,exp,1).astype(int), fc(x3,exp,2).astype(int), fc(x3,exp,3).astype(int),fc(x4,exp,4).astype(int)])[0][0]
s0 = np.array([0,1,1,0, 
               1,1,0,0,
               1,0,1,1,
               0,0,0,1,
               0,0,0,0]) # Estado inicial
M = 2000 # Numero de geração
score = [] # melhor resultado da função objetiva
score_fit = [] # Armazena o melhor da geração

def cromo(s0):
    """ Separa cromossomo em 4 partes"""
    vet = []
    vet.append(s0[0:4])
    vet.append(s0[4:8])
    vet.append(s0[8:12])
    vet.append(s0[12:16])
    vet.append(s0[16:])
    return vet

for i in range(M):
    cromosome = [] # Guarda os cromossomos com crossover
    fit = [] # Guarda saída da função objetiva
    variables = [] # Guarda a saída de cada variável
    for j in range(len(s0)//2 + 1): # Rotaciona até dar uma volta completa
        v = cromo(s0.copy()) # quebra em quatro partes
        temp_max = fy(v[0],v[1],v[2],v[3],v[4]) # Retorna a função objetiva
        fit.append(temp_max) # guarda função objetiva
        cromosome.append(s0.copy()) # guarda o cromossomo
        variables.append([fc(v[0],exp,0),fc(v[1],exp,1),
                          fc(v[2],exp,2),fc(v[3],exp,3),fc(v[4],exp,4)])# Guarda variáveis
        if (np.min(temp_max) < 0) | (np.median(fit) == np.max(fit)): 
            # mutação se função obj negativa resultado repetido
            pos = np.random.randint(4) # Escolhe uma das 4 variáveis
            np.random.shuffle(v[pos]) # Embaralha os bits de umas da variável
        s0 = list(v[0]) + list(v[1]) + list(v[2]) + list(v[3]) + list(v[4]) # junta partes
        s0 = np.roll(s0,-2) # Faz crossover
    nextGen=np.argmax(fit) # Pega o melhor resultado para próxima geração
    score.append(np.max(fit)) # Armazena a melhor função obj
    score_fit.append(cromosome[nextGen]) # Armazena o melhor cromossomo
    if (np.median(score) == np.max(fit)):
        s0 = cromosome[np.random.randint(len(fit))]
    else:
        s0 = cromosome[np.argmax(fit)]
best = score_fit[np.argmax(score)]
best_varb = cromo(best)
best_value = fy(best_varb[0],best_varb[1],best_varb[2],best_varb[3],best_varb[4])
best_var = [fc(best_varb[0],exp,0).astype(int),fc(best_varb[1],exp,1).astype(int),fc(best_varb[2],exp,2).astype(int),fc(best_varb[3],exp,3).astype(int),fc(best_varb[4],exp,4).astype(int)]
print(f'Best value: {best_value} best cromosome {best} best combination of variables {best_var}')
plt.plot(score)
plt.show()
print(np.max(score))

s0 = np.array([0,1,1,0, 
               1,1,0,0,
               1,0,1,1,
               0,0,0,1,
               0,0,0,0]) # Estado inicial
M = 2000 # Numero de geração
score = [] # melhor resultado da função objetiva
score_fit = [] # Armazena o melhor da geração

for i in range(M):
    cromosome = [] # Guarda os cromossomos com crossover
    fit = [] # Guarda saída da função objetiva
    variables = [] # Guarda a saída de cada variável
    for j in range(len(s0)//2 + 1): # Rotaciona até dar uma volta completa
        v = cromo(s0.copy()) # quebra em quatro partes
        temp_max = fm(v[0],v[1],v[2],v[3],v[4]) # Retorna a função objetiva
        fit.append(temp_max) # guarda função objetiva
        cromosome.append(s0.copy()) # guarda o cromossomo
        variables.append([fc(v[0],exp,0),fc(v[1],exp,1),
                          fc(v[2],exp,2),fc(v[3],exp,3),fc(v[4],exp,4)])# Guarda variáveis
        if (np.min(temp_max) < 0) | (np.median(fit) == np.max(fit)): 
            # mutação se função obj negativa resultado repetido
            pos = np.random.randint(4) # Escolhe uma das 4 variáveis
            np.random.shuffle(v[pos]) # Embaralha os bits de umas da variável
        s0 = list(v[0]) + list(v[1]) + list(v[2]) + list(v[3]) + list(v[4]) # junta partes
        s0 = np.roll(s0,-2) # Faz crossover
    nextGen=np.argmax(fit) # Pega o melhor resultado para próxima geração
    score.append(np.max(fit)) # Armazena a melhor função obj
    score_fit.append(cromosome[nextGen]) # Armazena o melhor cromossomo
    if (np.median(score) == np.max(fit)):
        s0 = cromosome[np.random.randint(len(fit))] 
    else:
        s0 = cromosome[np.argmax(fit)]
best = score_fit[np.argmax(score)]
best_varb = cromo(best)
best_value = fm(best_varb[0],best_varb[1],best_varb[2],best_varb[3],best_varb[4])
best_var = [fc(best_varb[0],exp,0).astype(int),fc(best_varb[1],exp,1).astype(int),fc(best_varb[2],exp,2).astype(int),fc(best_varb[3],exp,3).astype(int),fc(best_varb[4],exp,4).astype(int)]
print(f'Best value: {best_value} best cromosome {best} best combination of variables {best_var}')
plt.plot(score)
plt.show()
print(np.max(score))