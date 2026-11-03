from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

test = make_experiment(n=12000, seed=46, lift=0.1)

# 1) Write the verdict function from this lesson (harm / ship /
#    not worth it / inconclusive, threshold 0.003).
# 2) Print the difference's 95% interval (confint_proportions_2indep, B
#    first) in points with 2 places, then print the decision.
