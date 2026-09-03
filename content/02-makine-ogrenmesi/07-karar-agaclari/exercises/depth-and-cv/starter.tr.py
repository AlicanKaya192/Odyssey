# Ice aktarmalari yaz: StratifiedKFold ve cross_val_score da gerekiyor.
# Dosyayi oku, X ve y'yi hazirla, ayir.


# BIRINCI BOLUM
# 1, 2, 3, 5, 8, None derinlikleri icin egitim ve test dogrulugunu olc,
# tek satir yazdir: derinlik, egitim, test. None yerine "none" yaz.


# IKINCI BOLUM
# StratifiedKFold kur (5 kat, shuffle=True, random_state=42).
# 1, 2, 3, 5, None derinlikleri icin YALNIZCA egitim verisinde capraz
# dogrula; her biri icin derinlik, ortalama, yayilim yazdir.
# En yuksek ortalamaya sahip derinligi sakla ve sonda yazdir.
