Naive Bayes'in iki güçlü yanı var: az veriyle çabuk öğrenir ve öğrendiği şey
okunabilir. İkisini de ölçelim:

```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = CountVectorizer().fit(X_train)
nb = MultinomialNB().fit(vectorizer.transform(X_train), y_train)
words = vectorizer.get_feature_names_out()
log_prob = dict(zip(nb.classes_, nb.feature_log_prob_))
diff = log_prob["negative"] - log_prob["positive"]
print([str(words[i]) for i in np.argsort(diff)[::-1][:5]])
print([str(words[i]) for i in np.argsort(diff)[:5]])
for n in [50, 100, 200, 500, 1500]:
    model = MultinomialNB().fit(vectorizer.transform(X_train[:n]), y_train[:n])
    print(n, round(model.score(vectorizer.transform(X_test), y_test), 3))
```

```text
['terrible', 'honest', 'hate', 'of', 'waste']
['works', 'no', 'expected', 'well', 'totally']
50 0.738
100 0.816
200 0.842
500 0.864
1500 0.866
```

## Model ne öğrendi?

`feature_log_prob_` her sınıf için $\log P(w \mid c)$ tablosu (derste elle
hesapladığımız `log_lik`). İki sınıfın farkı, kelimenin hangi sınıfı ne kadar
işaret ettiği:

- Olumsuz için: "terrible", "honest", "hate", "of", "waste".
- Olumlu için: "works", **"no"**, "expected", "well", "totally".

"no"nun olumlu yorumları işaret etmesi şaşırtıcı görünüyor: veride "I
expected it to be bad, but no" kalıbı var. 05'teki ders yine geçerli: model
anlamı değil birlikteliği öğrenir. Bu yüzden öğrenilen kelimelere **mutlaka
bak**; tuhaf bir kelime çoğu zaman verideki bir kalıbı ya da bir sızıntıyı
gösterir.

## Ne kadar veri gerekiyor?

Son satırlar **öğrenme eğrisi**: eğitim verisi büyüdükçe test doğruluğu.

- 50 yorumla %73,8: taban çizgisini (%66) şimdiden geçiyor.
- 200 yorumla %84,2, 500 yorumla %86,4; 1500 yorumla %86,6. Eğri 500'den
  sonra düzleşiyor.

Düzleşen eğri "daha çok veri bu modele yardım etmeyecek" demek. Daha iyisi
için modeli ya da özellikleri değiştirmek gerekir (kelime çiftleri %88,8'e
çıkarmıştı; 09'da doğrusal modeller). Öğrenme eğrisi, veri toplamaya mı yoksa
modele mi emek vereceğine karar vermenin en ucuz yolu.
