import extra_lib.metamodel as mmodel
import numpy as np

test = mmodel.metamodel()
test.cuda_status()
test.plot_correlations()
test.plot_distributions()

test.fit()  # test.train_performance())
test.model_peformance()

print(test.predict([1, 1, 1, 1, 1]))

print(test.predict(np.array([1, 1, 1, 1, 1])))



