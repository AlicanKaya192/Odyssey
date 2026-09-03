# Ice aktarmalari yaz: GridSearchCV, StratifiedKFold, LogisticRegression
# ve accuracy_score de gerekiyor.
# Veriyi hazirla, ayir ve pipeline'i kur.


# StratifiedKFold kur.


# Iki parametreli izgarayi tanimla:
#   prepare__num__impute__strategy: ["median", "mean"]
#   model__C: [0.01, 0.1, 1, 10]


# GridSearchCV ile ara. Her nokta icin tek satir: strateji, C, CV ortalamasi.


# En iyi ayarlari ve o ayarin CV skorunu yazdir.


# Aramanin test dogrulugu ile ayarsiz pipeline'in test dogrulugu yan yana.
