# Kelime Torbası

Bir model sayılardan oluşan bir tablo ister: her satır bir örnek, her sütun
bir özellik. Metni böyle bir tabloya çevirmenin en eski ve hâlâ en çok
kullanılan yolu **kelime torbası** (bag of words): her belge, dağarcıktaki
her kelimenin o belgede kaç kez geçtiğini sayan bir satır olur. Sıra
unutulur; geriye yalnızca bir torba dolusu kelime kalır. Bu bölüm kelime
torbasını önce elle, sonra scikit-learn'ün `CountVectorizer`'ı ile kuruyor,
eğitimde görülmemiş kelimelere ne olduğunu gösteriyor ve torbanın kendisinden
hangi kelimelerin hangi sınıfı işaret ettiğini çıkarıyor.

## Elle bir kelime torbası

```python
docs = ["the battery is great", "the battery died", "great price great sound"]
vocab = sorted({w for d in docs for w in d.split()})
print(vocab)
for d in docs:
    words = d.split()
    print([words.count(w) for w in vocab])
```

```text
['battery', 'died', 'great', 'is', 'price', 'sound', 'the']
[1, 0, 1, 1, 0, 0, 1]
[1, 1, 0, 0, 0, 0, 1]
[0, 0, 2, 0, 1, 1, 0]
```

- **Dağarcık** (vocabulary) bütün belgelerdeki farklı kelimelerin sıralı
  listesi: 7 kelime. Her kelime bir sütun.
- Her belge 7 sayılık bir satır: "great price great sound" satırında
  "great" sütunu 2, "price" ve "sound" 1, öbürleri 0.
- Satırların hepsi aynı uzunlukta. Metinler farklı uzunlukta olsa da tablo
  düzgün: model için gereken de bu.

## CountVectorizer

scikit-learn aynı işi parçalama, küçük harf ve seyrek matrisle birlikte
yapıyor:

```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)
print(vectorizer.get_feature_names_out().tolist())
print(X.toarray().tolist())
print(vectorizer.vocabulary_["great"], X.shape)
```

```text
['battery', 'died', 'great', 'is', 'price', 'sound', 'the']
[[1, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 0, 0, 1], [0, 0, 2, 0, 1, 1, 0]]
2 (3, 7)
```

- `fit` dağarcığı öğrenir, `transform` belgeleri sayar; `fit_transform`
  ikisini birden yapar. scikit-learn'ün bütün dönüştürücüleri gibi.
- `get_feature_names_out()` sütunların adları, `vocabulary_` kelimeden sütun
  numarasına sözlük: "great" 2. sütun (sıfırdan sayınca).
- `X` seyrek bir matris (04'ün notu); küçük örnekte `toarray()` ile
  görebiliyoruz, büyük veride bunu yapma.

## Dağarcıkta olmayan kelime

Vektörleştirici bir kez `fit` edildi; yeni bir metinde **hiç görmediği**
kelimeler gelirse?

```python
new = vectorizer.transform(["the camera is great but the zoom died"])
print(new.toarray().tolist())
analyze = vectorizer.build_analyzer()
tokens = analyze("the camera is great but the zoom died")
print([w for w in tokens if w in vectorizer.vocabulary_])
```

```text
[[0, 1, 1, 1, 0, 0, 2]]
['the', 'is', 'great', 'the', 'died']
```

"camera", "but" ve "zoom" dağarcıkta yok; **hiçbir uyarı vermeden atıldılar**.
Bunlara **dağarcık dışı** (out of vocabulary, OOV) kelimeler denir. Model
yeni bir ürünün adını, yeni bir hatayı, yeni bir argoyu hiç göremez.
Dağarcığı her zaman **yalnızca eğitim verisiyle** `fit` et ve test verisine
yalnızca `transform` uygula; bütün veriyle `fit` etmek test verisinin
kelimelerini eğitime sızdırır (ML Kütüphaneleri'ndeki veri sızıntısının aynısı).

## Torba sırayı bilmez

```python
pair = ["the battery is great", "great is the battery"]
a, b = vectorizer.transform(pair).toarray()
print(a.tolist(), b.tolist(), (a == b).all())
```

```text
[1, 0, 1, 1, 0, 0, 1] [1, 0, 1, 1, 0, 0, 1] True
```

İki cümlenin vektörü birebir aynı. "dog bites man" ile "man bites dog" da
aynı torbaya düşer. Çoğu sınıflandırma görevinde bu kayıp şaşırtıcı derecede
az önemlidir: bir yorumun olumlu mu olumsuz mu olduğu çoğu zaman hangi
kelimelerin geçtiğinden anlaşılır. Sıra önemliyse 04'teki n-gram'lar ya da
ikinci modüldeki dizi modelleri gerekir.

## Sayı mı, var-yok mu?

```python
text = ["great great great price"]
counts = CountVectorizer().fit_transform(text).toarray()
flags = CountVectorizer(binary=True).fit_transform(text).toarray()
print(counts.tolist(), flags.tolist())
```

```text
[[3, 1]] [[1, 1]]
```

`binary=True` sayı yerine yalnızca var (1) ya da yok (0) yazar. Kısa
metinlerde (yorum, tweet, başlık) bir kelimenin üç kez geçmesi çoğu zaman bir
kez geçmesinden fazla bilgi taşımaz; ikili torba daha iyi çalışabilir.
Hangisinin daha iyi olduğunu doğrulama verisinde ölçeriz.

## Hangi kelimeler hangi sınıfı işaret ediyor?

Kelime torbası yalnızca modele girdi değil, kendi başına bir inceleme
aracıdır. Her kelimenin olumsuz yorumlardaki payını olumlu yorumlardaki
payıyla karşılaştıralım:

```python
import numpy as np
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
words = vectorizer.get_feature_names_out()
pos = np.asarray(X[labels == "positive"].sum(axis=0)).ravel() + 1
neg = np.asarray(X[labels == "negative"].sum(axis=0)).ravel() + 1
log_ratio = np.log((neg / neg.sum()) / (pos / pos.sum()))
for i in np.argsort(log_ratio)[::-1][:6]:
    print(words[i], int(neg[i] - 1), int(pos[i] - 1), round(log_ratio[i], 2))
print("---")
for i in np.argsort(log_ratio)[:4]:
    print(words[i], int(neg[i] - 1), int(pos[i] - 1), round(log_ratio[i], 2))
```

```text
terrible 15 0 3.91
hate 73 13 2.8
worse 71 13 2.78
honest 42 8 2.7
box 63 13 2.66
damaged 63 13 2.66
---
works 3 207 -2.81
expected 2 147 -2.76
well 8 426 -2.72
too 4 231 -2.7
```

- `X[labels == "positive"]` olumlu yorumların satırları; `sum(axis=0)` her
  sütunun toplamı, yani her kelimenin olumlu yorumlarda kaç kez geçtiği.
- **+1 eklemek** (yumuşatma, smoothing) bir sınıfta hiç geçmeyen kelimenin
  oranını sıfıra bölmekten kurtarıyor. "terrible" olumlu yorumlarda hiç
  geçmiyor; +1 olmasa oran sonsuz olurdu.
- **Log oran** pozitifse kelime olumsuz yorumlarda daha sık: "terrible",
  "hate", "worse", "damaged". Negatifse olumlu yorumlarda: "works", "well".
- İki kelime dikkat çekici: **"honest"** olumsuzu, **"expected"** olumluyu
  işaret ediyor. Kendi başlarına ikisi de duygusuz kelimeler. Veride
  "not good, to be honest" ve "I expected it to be bad, but no" kalıpları
  var. Model kelimelerin **anlamını** değil, hangi sınıfla **birlikte**
  geçtiklerini öğrenir. Bu hem gücü hem tehlikesi: kalıp değişirse
  öğrenilen ilişki bozulur.

Bu hesap 08. bölümdeki Naive Bayes sınıflandırıcısının kalbidir; orada aynı
oranları toplayıp karar vereceğiz.

## Uzun belge, büyük sayılar

```python
lengths = np.asarray(X.sum(axis=1)).ravel()
print(lengths.min(), lengths.max(), round(lengths.mean(), 1))
```

```text
3 38 15.0
```

Satır toplamları 3 ile 38 kelime arasında. Uzun bir yorumun sayıları kısa
bir yorumunkinden büyük olur; iki belgeyi karşılaştırırken uzunluk anlamı
bastırabilir. Bir sonraki bölümün konusu TF-IDF, hem bunu hem de her belgede
geçen sık kelimelerin ağırlığını düzeltiyor.

## Özet

- Kelime torbası her belgeyi dağarcıktaki kelimelerin sayılarından oluşan
  bir satıra çevirir; sıra unutulur.
- `CountVectorizer`: `fit` dağarcığı öğrenir, `transform` sayar; sonuç seyrek
  matris.
- Dağarcıkta olmayan kelimeler sessizce atılır. Dağarcığı yalnızca eğitim
  verisiyle kur.
- `binary=True` var-yok torbası; kısa metinlerde sayıdan iyi olabilir.
- Sınıflara göre kelime toplamları ve +1 yumuşatmalı log oran, hangi
  kelimenin hangi sınıfı işaret ettiğini gösterir. Model anlamı değil
  birlikteliği öğrenir.
