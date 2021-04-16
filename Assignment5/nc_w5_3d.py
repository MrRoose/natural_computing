import numpy as np
import matplotlib.pyplot as plt

weights = []
for error in np.arange(0.01, 1, 0.01):
    weight = np.log((1-error)/error)
    weights.append(weight)

plt.plot(list(np.arange(0, 1, 0.01)), weights)
plt.xlabel('Error rate (= 1 - p(correct)) base-learner')
plt.ylabel('Weight given to base learner')
plt.show()