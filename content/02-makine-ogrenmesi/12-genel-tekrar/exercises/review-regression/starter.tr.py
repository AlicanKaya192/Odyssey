# Ice aktarmalari yaz: pandas, ColumnTransformer, SimpleImputer, Pipeline,
# OneHotEncoder, StandardScaler, LinearRegression, DecisionTreeRegressor,
# RandomForestRegressor, KFold, cross_val_score, train_test_split,
# mean_absolute_error, root_mean_squared_error, r2_score.
# Veriyi oku, X ve y'yi al, ayir (regresyonda stratify yok).


# On isleyiciyi uret: sayisal sutunlara medyan + olcekleme,
# metin sutunlarina OneHotEncoder(handle_unknown="ignore").


# Taban cizgi: her seye egitim ortalamasi. MAE, RMSE ve R2 tek satirda.


# Uc modeli sirayla ele al: linear, tree, forest.
# Her biri icin tek satir: ad, CV MAE, CV yayilimi, test MAE, test R2.
# scoring="neg_mean_absolute_error" negatif donuyor.


# CV kazanani ile test kazanani yan yana (en dusuk MAE kazaniyor).
