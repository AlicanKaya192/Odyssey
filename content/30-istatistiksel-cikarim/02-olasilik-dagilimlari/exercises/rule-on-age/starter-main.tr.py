from scipy import stats
from ab_data import make_population

users = make_population()
x = users["age"]
# k = 1, 2, 3 için tek satırda: k, normal dağılımın ortalamadan k sapma
# içine düşen payı ve yaşların gerçekte bu aralığa düşen payı (4 basamak).
