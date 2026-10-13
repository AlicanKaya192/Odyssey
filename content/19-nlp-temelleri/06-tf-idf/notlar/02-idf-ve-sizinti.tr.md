IDF bir **istatistik**: bütün belgelere bakılarak öğreniliyor. Ölçekleyicinin
ortalaması gibi o da yalnızca eğitim verisinden öğrenilmeli. Bütün veriyle
`fit` edersek ne olur?

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
train, test = texts[:1000], texts[1000:]
right = TfidfVectorizer().fit(train)
leaky = TfidfVectorizer().fit(texts)
print(len(right.vocabulary_), len(leaky.vocabulary_))


def idf_of(vectorizer, word):
    return round(float(vectorizer.idf_[vectorizer.vocabulary_[word]]), 3)


print(idf_of(right, "bluetooth"), idf_of(leaky, "bluetooth"))
```

```text
288 350
4.382 4.524
```

- Doğru yol (yalnızca eğitim) 288 kelimelik bir dağarcık kurdu. Sızdıran
  yol 350: test verisinde olup eğitimde hiç görülmemiş **62 kelime** modele
  sütun olarak girdi.
- "bluetooth"un IDF'i de değişti (4,382 → 4,524): test belgeleri df'ye
  katıldı.

## Neden önemli?

Test verisi, modelin hiç görmediği yeni veriyi taklit eder. Dağarcık ya da
IDF test verisinden bir şey öğrenirse, test skoru gerçekte
göreceğinizden iyimser çıkar. Fark burada küçük görünebilir; ama bir
kelimenin yalnızca test verisinde geçtiği ve sınıfı ele verdiği durumlarda
(bir ürün adı, bir hata kodu) etkisi büyüktür.

## Doğru düzen

```text
vectorizer.fit(train)              # yalnızca eğitim
X_train = vectorizer.transform(train)
X_test = vectorizer.transform(test)
```

Ya da hepsini kendiliğinden doğru yapan bir **Pipeline** kullan; 10.
bölümün konusu. Çapraz doğrulamada (cross-validation) her katta
vektörleştiricinin yeniden `fit` edilmesi de ancak Pipeline ile kolay.
