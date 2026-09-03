# Ice aktarmalari yaz: numpy, SelectKBest, f_classif, cross_val_score,
# StratifiedKFold ve LogisticRegression de gerekiyor.
# Veriyi hazirla, ayir ve on islemeden gecir.


# 200 sutunluk rastgele gurultu uret (default_rng(7)) ve yanina ekle.
# Toplam sutun sayisini yazdir.


# YANLIS yol: butun egitim verisinde SelectKBest(f_classif, k=15) ile sec,
# sonra o 15 sutunda cross_val_score calistir. Ortalamayi yazdir.


# DOGRU yol: seciciyi ve modeli bir Pipeline'a koy, 209 sutunun tamamiyla
# cross_val_score calistir. Ortalamayi yazdir.


# Aradaki farki yazdir.


# Yanlis yolda secilen 15 sutunun kac tanesi gurultu?
