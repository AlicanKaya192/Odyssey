import numpy as np
from ab_data import make_novelty_test
# make_novelty_test(n=10000, seed=s) ile s = 200..219 arası 20 test kur.
# Her testte iki göreli artış (B / A - 1) hesapla:
#   yeni kullanıcıların 1. haftası, eski kullanıcıların 4. haftası.
# İkisinin 20 testteki ortalamasını aynı satırda 3 basamakla yaz.
# Hafta: (day - 1) // 7 + 1.
