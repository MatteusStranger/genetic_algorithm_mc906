import numpy as np
import extra_lib.metamodel as hospitalModel
import matplotlib.pyplot as plt
import extra_lib.monitor as monitor


class ag_asex:
    def __init__(self):
        self.mem = []
        self.cpu = []
        self.mm = hospitalModel.metamodel()
        self.mm.fit()
        self.exp = np.arange(4)
        self.low_bounds = np.array([1, 1, 1, 1, 1])
        self.high_bounds = np.array([3, 4, 5, 6, 12])
        self.quantizations = (self.high_bounds - self.low_bounds) / (
                2 ** 4 - 1
        )  # quantização
        self.fc = (
            lambda x, exp, _type: np.sum(x * 2 ** exp) * self.quantizations[_type]
                                  + self.low_bounds[_type]
        )  # decoficação

        self.fy = (
            lambda x1, x2, x3, x4, x5: 1.113 * self.fc(x2, self.exp, 1).astype(int)
                                       + 0.701
                                       * self.fc(x2, self.exp, 1).astype(int)
                                       * self.fc(x3, self.exp, 2).astype(int)
                                       + 0.207
                                       * self.fc(x2, self.exp, 1).astype(int)
                                       * self.fc(x5, self.exp, 4).astype(int)
                                       + 0.021
                                       * self.fc(x1, self.exp, 0).astype(int)
                                       * self.fc(x5, self.exp, 4).astype(int)
                                       - 0.435 * self.fc(x2, self.exp, 1).astype(int) ** 2
                                       - 0.013
                                       * self.fc(x2, self.exp, 1).astype(int)
                                       * self.fc(x5, self.exp, 4).astype(int) ** 2
                                       - 0.092
                                       * self.fc(x2, self.exp, 1).astype(int)
                                       * self.fc(x3, self.exp, 2).astype(int) ** 2
                                       - 1
                                       + 1 / self.fc(x4, self.exp, 3).astype(int)
        )
        self.fm = lambda x1, x2, x3, x4, x5: self.mm.predict(
            [
                self.fc(x1, self.exp, 0).astype(int),
                self.fc(x2, self.exp, 1).astype(int),
                self.fc(x3, self.exp, 2).astype(int),
                self.fc(x3, self.exp, 3).astype(int),
                self.fc(x4, self.exp, 4).astype(int),
            ]
        )[0][0]

    def setModel(self, model):
        self.mm = model

    def getModel(self):
        return self.mm

    def agOptim(self, fitness, with_plot=False):
        print("Entre com a quantidade de gerações:")
        M = int(input())
        print()

        print("Informe o valor da autorreprodução (valor negativo):")
        self_reproduction = int(input())
        print()

        def uso_recursos(self):
            memoria, processador = monitor.monitor()
            self.mem.append(memoria)
            self.cpu.append(processador)

        s0 = np.array(
            [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        )  # Estado inicial
        score = []  # melhor resultado da função fitness
        score_fit = []  # Armazena o melhor da geração

        def cromo(s0):
            """ Separa cromossomo em 5 partes"""
            vet = []
            vet.append(s0[0:4])
            vet.append(s0[4:8])
            vet.append(s0[8:12])
            vet.append(s0[12:16])
            vet.append(s0[16:])
            return vet

        for i in range(M):
            cromosome = []  # Guarda os cromossomos com crossover
            fit = []  # Guarda saída da função objetiva
            for j in range(len(s0) // 2 + 1):  # Rotaciona até dar uma volta completa
                v = cromo(s0.copy())  #quebra em quatro partes
                temp_max = fitness(
                    v[0], v[1], v[2], v[3], v[4]
                )  # Retorna a função fitness
                fit.append(temp_max)  # guarda resultado fitness
                cromosome.append(s0.copy())  # guarda o cromossomo
                if (np.min(temp_max) < 0) | (j%2 == 0):
                    # aplica mutacao para evitar função obj negativa e cromossomo repetido
                    pos = np.random.randint(4)  # Escolhe uma das 5 variáveis
                    np.random.shuffle(
                        v[pos]
                    )  # Embaralha os bits de umas da variável (muda numero)
                s0 = (
                        list(v[0]) + list(v[1]) + list(v[2]) + list(v[3]) + list(v[4])
                )  # junta partes
                s0 = np.roll(s0, self_reproduction)  # Gera novos indiduos com mesmo cromossomo
            score.append(np.max(fit))  # Armazena a melhor resultado da geracao
            score_fit.append(cromosome[np.argmax(fit)])  # Armazena o melhor cromossomo
            if i%2 == 0:  # Aumenta a taxa de mutação para 50%
                s0 = cromosome[np.random.randint(len(fit))]  # pega outro cromossomo diferente para self.explorar outro espaco
            else:
                s0 = cromosome[np.argmax(fit)]  # Pega o melhor resultado

            uso_recursos(self)

        best = score_fit[np.argmax(score)]  # pega melhor cromossomo
        best_varb = cromo(best)  # quebra em 5 variaveis binaria
        best_value = fitness(
            best_varb[0], best_varb[1], best_varb[2], best_varb[3], best_varb[4]
        )  # Converte para funcao fitness para decimal
        best_var = [
            self.fc(best_varb[0], self.exp, 0).astype(int),
            self.fc(best_varb[1], self.exp, 1).astype(int),
            self.fc(best_varb[2], self.exp, 2).astype(int),
            self.fc(best_varb[3], self.exp, 3).astype(int),
            self.fc(best_varb[4], self.exp, 4).astype(int),
        ]  # Converte em 5 variaveis
        print(
            f"Best value: {best_value} best cromosome {best} best combination of variables {best_var}"
        )

        if with_plot:
            plt.plot(score)
            plt.show()

            print("Monitoramos o uso de memória e cpu durante as gerações. "
                  "Gostaria de ver os resultos em gráfico?")
            print()
            print("1 - Sim")
            print("0 - Nao")
            print()
            segue = int(input())

            if (segue == 1):
                plt.ylabel('Memória')
                plt.plot(self.mem)
                plt.show()

                plt.ylabel('CPU')
                plt.plot(self.cpu)
                plt.show()

        # print(np.max(score))

# Como chamar agOptim(nome da funcao)
# variable = ag_asex()
# Usar a rede neural
# variable.agOptim(variable.fm ,with_plot=True)
# Usar equacao
# variable.agOptim(variable.fy)
# definir rede neural diferente
# variable.setModel(test)

# Exemplo de uso
# ag1 = ag_asex()
# ag1.agOptim(ag1.fm)
# ag1q.agOptim(ag1.fy)
