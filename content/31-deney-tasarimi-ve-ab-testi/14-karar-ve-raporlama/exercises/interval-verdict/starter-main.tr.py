from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

test = make_experiment(n=12000, seed=46, lift=0.1)

# 1) Bu derste yazılan verdict fonksiyonunu yaz (harm / ship /
#    not worth it / inconclusive, eşik 0.003).
# 2) Farkın %95 aralığını (confint_proportions_2indep, önce B) puan olarak
#    2 basamakla yaz, sonra kararı yaz.
