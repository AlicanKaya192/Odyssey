# Ice aktarmalari yaz: StratifiedKFold, cross_val_score,
# LogisticRegression, KNeighborsClassifier, RandomForestClassifier,
# GradientBoostingClassifier, roc_auc_score, average_precision_score.
# Veriyi hazirla ve ayir (followup_calls yok, stratify=y).


# StratifiedKFold kur.


# Dort modeli sirayla ele al: logreg, knn, forest, boosting.
# Her biri icin tek satir: ad, CV ortalama precision, CV yayilimi,
# test ROC AUC, test ortalama precision.
# Capraz dogrulamada scoring="average_precision".


# Ortalama precision'in taban cizgisi (pozitif orani).


# CV kazanani.
