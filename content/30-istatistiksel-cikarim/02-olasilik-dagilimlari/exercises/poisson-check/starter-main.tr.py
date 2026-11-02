from scipy import stats
from ab_data import make_population

users = make_population()
visits = users["visits"]
# 1) Her k = 0..5 için: k, gerçek pay ve Poisson modelinin pmf değeri
#    (ikisi de 3 basamak).
# 2) Son satırda ortalama ve varyans (2 basamak).
