`pipe`'ı iki adımlı bir Pipeline olarak kur: `"tfidf"` adıyla
`TfidfVectorizer()`, `"model"` adıyla `LogisticRegression(max_iter=1000)`.
Bütün yorumlarla eğit. `predict_labels(sentences)` ham cümle listesini alıp
tahminleri düz liste olarak döndürsün.

**Beklenen çıktı:**

```
['positive', 'negative']
```
