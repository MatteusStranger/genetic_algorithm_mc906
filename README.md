# Institute of Computing - Unicamp

## Project 2 

### Authors

- Matteus Vargas (ra: 262885)
- Christian Maekawa (ra: 231867)
- Stéfani Fernandes (ra: 147939)
- Maisa Silva (ra: 181831)
- Giovane de Morais (ra: 192683)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

# Report
Complete project description can be found [here](./Final_Report.ipynb)

# Environment
You can use conda environment or Docker. Is possible to install our library and run with Google Colab. [Read here to install environment.](./env/README.md)  

# Context
This project is related with **Simulation**. To making a decision is common companies made simulations. **Optimization** because we are minimizing the time spend with simulations using metamodel and find maximal using **Genetic algorithms** to maximize our goal instead simulate all possible situations and **Operational Research** the big area that problem have relations. Simulations are critical because companies and universities have pilots that could cost very expensive if fails happens. To avoid this situation is common use software simulations. Some simulations expenses days, months, almost years, to compute a scenario and some cases the real situation not available yet. This problem is common in biology area. To simulate growth of some bacteria or some disease. Logistics use simulations to predict the worst situation.

The propose of this project is predicts the number of employees needs to cover affected area with disease to predict the number of patients we can heal. Was required to find the number of employees to maximize the number of patients served to cover the affected region. Maximize all parameter is not a solution because the employee has dependencies with each other, and we need to avoid unnecessary expenses with extra employees, idle time and bottleneck if possible.

Although, the project has strong relationship with simulation the scope of this project is Genetic algorithm. The project uses a dataset that was generated from [[1]](http://www.abepro.org.br/biblioteca/TN_STO_211_253_27544.pdf) that simulate a hospital model simulation. The description about how to model a simulated hospital was got from other article about how to create simulated hospital[[2]](https://www.sciencedirect.com/science/article/pii/S1877050912002827?via%3Dihub). Miranda [[1]](http://www.abepro.org.br/biblioteca/TN_STO_211_253_27544.pdf) based on  [[2]](https://www.sciencedirect.com/science/article/pii/S1877050912002827?via%3Dihub)  and create simulated hospital with software simulation. So, they generate the data that we use to create a metamodel. About creation of metamodel using artificial networking was reconstructed using python . Metamodel is a meta representation of the real model, all reproduction was compared with results obtained with articles.

Is out of scope explore about software simulation and metamodel. All settings were got from literature and tried to reproduce as close as possible.

The target about this project is about Genetic Algorithm. So was used the output from artificial network or metamodel equation as fitness function and applied many setting to find solution and share about discoveries. Other articles don't explore deep about results obtained with genetic algorithms.


## The problem addressed

Find the number of employees needed to maximize the number of patients served.

## The evolutionary model adopted
There are two evolutionary model with  sexual crossing over and other with assexual, auto-reproduction.

## Implementation specifics and restrictions

|Represetation | Decision variables                          | type    | Lower bound      | Upper bound    |
|:-------------|:-------------------------------------------:|:-------:|:----------------:|---------------:|
|x1            | Number of receptionists                     | Integer |        1         |       3        |
|x2            | Number of doctors                           | Integer |        1         |       4        |
|x3            | Number of laboratory technicians            | Integer |        1         |       5        |
|x4            | Number of nurses in the treatment room      | Integer |        1         |       6        |
|x5            | Number of nurses in the emergency room      | Integer |        1         |       12       |


## Variations on parameters

## Fitness function adopted
- Maximaze artificial network neural metamodel.

* population size 
* stop criteria
* selection technique
* crossover technique
* mutation technique
* replacement method
* mutation rate
* crossover rate

### References

[[1]](http://www.abepro.org.br/biblioteca/TN_STO_211_253_27544.pdf) DE CARVALHO MIRANDA, Rafael et al. **Otimização via simulação por metamodelagem: um estudo em casos da área médica**. Revista Produção Online, v. 16, n. 3, p. 1058-1078, 2016.

[[2]](https://www.sciencedirect.com/science/article/pii/S1877050912002827?via%3Dihub) CABRERA, Eduardo et al. **Simulation optimization for healthcare emergency departments**. Procedia Computer Science, v. 9, p. 1464-1473, 2012.
