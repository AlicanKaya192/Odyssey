import numpy as np
from ab_data import make_population

users = make_population()
true_p = users["bought"].mean()
sample = users["bought"].sample(n=1000, random_state=32)
# 1) Örneklemdeki payı (p_hat) 4 basamakla yazdır.
# 2) Standart hatasını sqrt(p_hat * (1 - p_hat) / n) 4 basamakla yazdır.
# 3) Tahminin gerçekten kaç standart hata uzakta olduğunu
#    ((p_hat - true_p) / se) 2 basamakla yazdır.
