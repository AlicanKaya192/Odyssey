import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
X = pd.DataFrame(rng.normal(size=(80, 300)),
                 columns=[f"c{i}" for i in range(300)])
y = pd.Series(rng.normal(size=80))

# Kalan ice aktarmalari yaz.


# SIZINTILI YOL
# Her sutunun hedefle mutlak korelasyonunu butun veride hesapla.
# En yuksek bes sutunu sec, SONRA ayir, egit, R2'yi yazdir.


# TEMIZ YOL
# Once ayir, korelasyonlari yalnizca egitimde hesapla, bes sutunu ona gore
# sec, egit, R2'yi yazdir.
