`results_rows(cs)` `GridSearchCV(LogisticRegression(), {"C": cs}, cv=5)`'i eğitim
verisinde çalıştırsın ve her aday için `[C, ortalama, sapma]` satırı
döndürsün (`cv_results_`'tan `params`, `mean_test_score`, `std_test_score`;
skorlar 3 basamak).

**Beklenen çıktı:**

```
[0.001, 0.733, 0.063]
[0.1, 0.831, 0.023]
[10.0, 0.822, 0.0]
```
