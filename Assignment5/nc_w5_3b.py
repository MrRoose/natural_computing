from scipy.special import binom
import numpy as np
import matplotlib.pyplot as plt


def prob_correct(weight_strong):
    # weight_strong has to be a float between 0 and 1. This will be the relative weight of the strong classifier.
    # The remaining weight 1 - w_strong, will be divided equally over the weak classifiers.

    p_strong = 0.75
    p_weak = 0.6

    weights_weak = (1 - weight_strong) / 10

    total_prob = 0

    # Strong = correct
    for i in range(10 + 1):
        val = weight_strong + i * weights_weak
        # If this contributes to a right prediction, we calculate its probability
        if val > 0.5:
            cur_prob = p_strong * binom(10, i) * (p_weak) ** i * (1 - p_weak) ** (10 - i)
            total_prob += cur_prob

    # Strong = incorrect
    for i in range(10 + 1):
        val = i * weights_weak
        # If this contributes to a right prediction, we calculate its probability
        if val > 0.5:
            cur_prob = (1 - p_strong) * binom(10, i) * (p_weak) ** i * (1 - p_weak) ** (10 - i)
            total_prob += cur_prob
    return total_prob


probs = []
for w_1 in np.arange(0, 1, 0.01):
    probs.append(prob_correct(w_1))

    if prob_correct(w_1) >= 0.8:
        print(w_1)

plt.plot(list(np.arange(0, 1, 0.01)), probs)
plt.xlabel('Weight of the strong classifier')
plt.ylabel('Probability of correctness of ensemble')
plt.show()