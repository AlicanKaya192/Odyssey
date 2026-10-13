# Naive Bayes ile Sınıflandırma

05'te her kelimenin hangi sınıfı ne kadar işaret ettiğini log oranla ölçtük.
**Naive Bayes** bu fikri bir sınıflandırıcıya çeviriyor: bir belgedeki
bütün kelimelerin işaretlerini toplayıp en olası sınıfı seçiyor. Metin
sınıflandırmanın en eski ve hâlâ en hızlı yöntemlerinden biri; az veriyle
şaşırtıcı derecede iyi çalışır. Bu bölüm Naive Bayes'i NumPy ile sıfırdan
yazıyor, scikit-learn'ün `MultinomialNB`'siyle birebir karşılaştırıyor ve
yumuşatmanın, kelime çiftlerinin etkisini ölçüyor.

## Bayes kuralı

Bir belge $d$ verildiğinde, sınıfı $c$ olma olasılığı:

$$P(c \mid d) \propto P(c) \prod_{w \in d} P(w \mid c)$$

- $P(c)$ **önsel olasılık** (prior): veride bu sınıfın payı. Yorumların
  çoğu olumlu olduğu için olumlunun önseli büyük.
- $P(w \mid c)$ kelimenin o sınıfın metinlerinde geçme olasılığı.
- $\propto$ "orantılı" demek: bütün sınıflar için aynı olan paydayı
  hesaplamaya gerek yok; en büyük olanı seçmek yetiyor.

**"Naif"** (naive) varsayım şu: sınıf bilindiğinde kelimeler birbirinden
bağımsız. Bu açıkça yanlış ("not" ile "good" birbirine bağlı), ama yöntem
yine de iyi çalışır, çünkü sınıflandırma için olasılıkların tam doğru
olması değil, en büyüğün doğru sınıf olması yeter.

## Eğitim ve test verisi

```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = CountVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)
print(A.shape, B.shape)
print({str(c): int((y_train == c).sum()) for c in sorted(set(y_train))})
```

```text
(1500, 326) (500, 326)
{'negative': 295, 'neutral': 217, 'positive': 988}
```

- `train_test_split` yorumların %75'ini eğitime, %25'ini teste ayırıyor.
  `stratify=labels` iki parçada da sınıf oranlarının aynı kalmasını
  sağlıyor; dengesiz veride önemli.
- Vektörleştirici **yalnızca eğitim** metinleriyle `fit` ediliyor (05, 06).
  Dağarcık 326 kelime.

## Sıfırdan Naive Bayes

Eğitim iki şeyi saymaktan ibaret: sınıfların payı ve her sınıfta her
kelimenin sayısı.

```python
classes = np.array(sorted(set(y_train)))
log_prior = np.log([(y_train == c).mean() for c in classes])
counts = np.array([
    np.asarray(A[y_train == c].sum(axis=0)).ravel() for c in classes])
smoothed = counts + 1
log_lik = np.log(smoothed / smoothed.sum(axis=1, keepdims=True))
print(classes.tolist(), log_prior.round(3).tolist())
print(log_lik.shape)
```

```text
['negative', 'neutral', 'positive'] [-1.626, -1.933, -0.418]
(3, 326)
```

- `log_prior` her sınıfın payının logaritması: olumlu −0,418 (%66), nötr
  −1,933 (%14,5).
- `counts` 3 × 326'lık bir tablo: her satır bir sınıf, her sütun bir kelime.
- **+1 (Laplace yumuşatması):** bir sınıfta hiç görülmemiş bir kelimenin
  olasılığı 0 olursa, o kelimeyi içeren her belge o sınıfa sıfır olasılık
  alır. +1 her kelimeye küçük bir pay bırakıyor (05'teki log oranla aynı
  fikir).
- `log_lik` $\log P(w \mid c)$: her satır kendi toplamına bölünüp
  logaritması alınıyor.

Tahmin, belgedeki kelimelerin log olasılıklarını toplayıp önseli eklemek:

```python
scores = np.asarray(B @ log_lik.T) + log_prior
pred = classes[scores.argmax(axis=1)]
print(round(float((pred == y_test).mean()), 3))
print(round(float((y_test == "positive").mean()), 3))
```

```text
0.866
0.66
```

- `B @ log_lik.T` her test belgesi için, her kelimenin sayısı çarpı o
  kelimenin log olasılığı, toplanmış hâli: formüldeki çarpım, log
  dünyasında toplama oldu.
- Doğruluk **%86,6**; her yoruma "olumlu" diyen taban çizgisi %66. 00'daki
  elle yazılmış kurallar %44,9'da kalmıştı.

## Neden logaritma?

```python
print(np.prod(np.full(400, 0.01)))
print(np.sum(np.log(np.full(400, 0.01))).round(1))
```

```text
0.0
-1842.1
```

400 kelimelik bir belgede her kelimenin olasılığı 0,01 olsa, çarpım
$10^{-800}$ olur; bilgisayarın en küçük ondalıklı sayısının çok altında.
Sonuç **0** çıkıyor ve bütün sınıflar eşit görünüyor (taşma, underflow).
Logaritmaların toplamı ise −1842,1 olarak sorunsuz duruyor. Olasılık
çarpımlarını her zaman log olarak toplarız.

## scikit-learn ile karşılaştır ve alpha

```python
from sklearn.naive_bayes import MultinomialNB

nb = MultinomialNB().fit(A, y_train)
print(round(nb.score(B, y_test), 3), bool((nb.predict(B) == pred).all()))
for alpha in [0.01, 0.1, 1, 10, 100]:
    model = MultinomialNB(alpha=alpha).fit(A, y_train)
    print(alpha, round(model.score(B, y_test), 3))
```

```text
0.866 True
0.01 0.868
0.1 0.872
1 0.866
10 0.862
100 0.682
```

- `MultinomialNB` bizim kodumuzla **bütün** tahminlerde aynı. Varsayılan
  `alpha=1` bizim +1'imiz.
- `alpha` yumuşatmanın gücü. 0,1 bu veride en iyisi (%87,2); 100 her kelimeye
  o kadar büyük pay bırakıyor ki kelimelerin farkı siliniyor ve model
  neredeyse önsele, yani taban çizgisine döndü (%68,2). `alpha` bir
  hiperparametre; doğru değeri test verisiyle değil doğrulama verisiyle
  seçeriz (10. bölüm).

## Tahminlere bakmak

```python
examples = ["the battery is great", "not good at all", "it broke after two days"]
for text in examples:
    probs = nb.predict_proba(vectorizer.transform([text]))[0]
    print(text, "->", nb.classes_[probs.argmax()], probs.round(2).tolist())
```

```text
the battery is great -> positive [0.25, 0.14, 0.62]
not good at all -> negative [0.74, 0.0, 0.26]
it broke after two days -> negative [0.93, 0.04, 0.03]
```

- `predict_proba` sınıf olasılıklarını `classes_` sırasıyla veriyor
  (negative, neutral, positive).
- "not good at all" olumsuz bulundu (%74): "not" ve "all" olumsuz yorumlarda
  sık geçiyor, "good"un olumlu işaretini bastırıyorlar. Naive Bayes
  olumsuzlamayı anlamıyor; kelimeleri tek tek sayıyor ve bu sefer şanslı.
- Naive Bayes'in olasılıkları genellikle **aşırı emin** çıkar (0,93 gibi):
  bağımsızlık varsayımı aynı bilgiyi birkaç kez sayıyor. Sınıflandırma için
  sorun değil, ama olasılığı doğrudan güven ölçüsü diye okuma.

## Kelime çiftleri

```python
bigrams = CountVectorizer(ngram_range=(1, 2)).fit(X_train)
nb2 = MultinomialNB().fit(bigrams.transform(X_train), y_train)
print(round(nb2.score(bigrams.transform(X_test), y_test), 3))
probs = nb2.predict_proba(bigrams.transform(["not good at all"]))[0]
print(nb2.classes_[probs.argmax()], probs.round(2).tolist())
```

```text
0.888
negative [0.99, 0.0, 0.01]
```

Kelime çiftleri eklenince doğruluk %88,8'e çıktı; "not good" artık tek bir
özellik ve model "not good at all"dan %99 emin. Naif varsayımın en büyük
zararını (kelimelerin birbirine bağlılığı) n-gram'lar kısmen geri alıyor.

## Destek talepleri

Aynı yöntem beş sınıflı talep verisinde:

```python
from text_data import make_tickets

tickets = make_tickets(2000)
t_texts = [t["text"] for t in tickets]
t_labels = np.array([t["category"] for t in tickets])
t_train, t_test, c_train, c_test = train_test_split(
    t_texts, t_labels, test_size=0.25, random_state=0, stratify=t_labels)
t_vec = CountVectorizer().fit(t_train)
t_nb = MultinomialNB().fit(t_vec.transform(t_train), c_train)
print(round(t_nb.score(t_vec.transform(t_test), c_test), 3))
print(round(float((c_test == "shipping").mean()), 3))
```

```text
0.928
0.296
```

%92,8 doğruluk; en sık sınıfı ("shipping") söyleyen taban çizgisi %29,6.
Sınıf sayısı arttıkça taban çizgisi düşer ve modelin katkısı daha net
görünür.

## Özet

- Naive Bayes: $P(c \mid d) \propto P(c) \prod P(w \mid c)$; sınıf biliniyorken
  kelimelerin bağımsız olduğu "naif" varsayımıyla.
- Eğitim saymaktır: sınıf payları ve sınıf başına kelime sayıları; +1
  (Laplace) görülmemiş kelimeye sıfır olasılık verilmesini önler.
- Olasılıkları çarpmak yerine logaritmalarını topla; yoksa sonuç 0'a taşar.
- Sıfırdan yazdığımız model `MultinomialNB` ile birebir aynı: yorumlarda
  %86,6, kelime çiftleriyle %88,8, taleplerde %92,8.
- `alpha` yumuşatmanın gücü; çok büyürse model önsele döner.
