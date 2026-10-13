scikit-learn'de metin için üç Naive Bayes var; farkları kelimeyi nasıl
saydıkları.

| Sınıf | Girdi | Fikri | Ne zaman |
|---|---|---|---|
| `MultinomialNB` | Kelime sayıları (ya da TF-IDF) | Her kelime tekrarıyla sayılır | Varsayılan seçim |
| `ComplementNB` | Kelime sayıları | Her sınıfı, o sınıf **dışındaki** belgelerle öğrenir | Dengesiz sınıflar |
| `BernoulliNB` | Var-yok (0/1) | Kelimenin **geçmemesi** de bilgi | Kısa metinler |

## Karşılaştıralım

```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = CountVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)
for model in [MultinomialNB(), ComplementNB(), BernoulliNB()]:
    model.fit(A, y_train)
    pred = model.predict(B)
    neutral = round(float((pred[y_test == "neutral"] == "neutral").mean()), 3)
    print(type(model).__name__, round(model.score(B, y_test), 3), neutral)
```

```text
MultinomialNB 0.866 0.847
ComplementNB 0.846 0.861
BernoulliNB 0.864 0.819
```

- İkinci sayı genel doğruluk, üçüncüsü **nötr** yorumların ne kadarının nötr
  bulunduğu. Nötr en az örneği olan sınıf.
- `ComplementNB` genel doğrulukta biraz geride (%84,6) ama azınlık sınıfı
  nötrü en iyi o buluyor (%86,1). Dengesiz veride doğruluk tek başına
  yanıltıcı; 09'da sınıf başına ölçüleri (kesinlik, duyarlılık) göreceğiz.
- Üçü de birbirine yakın: Naive Bayes'te asıl kazanç türden değil,
  özelliklerden (kelime çiftleri, temizlik) gelir.

## TF-IDF ile Naive Bayes

`MultinomialNB` TF-IDF değerleriyle de çalışır (değerler negatif olmadığı
sürece). Kuramda sayılar için tasarlandı, ama uygulamada TF-IDF çoğu zaman
benzer ya da biraz daha iyi sonuç verir. Hangisinin iyi olduğunu
doğrulamayla seç.
