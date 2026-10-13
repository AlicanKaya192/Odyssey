# Doğrusal Modeller ve Değerlendirme

Naive Bayes her kelimenin ağırlığını sayarak buluyordu. **Doğrusal modeller**
(lojistik regresyon, doğrusal SVM) ağırlıkları **öğrenir**: hangi kelimenin
hangi sınıf için ne kadar önemli olduğunu, tahmin hatasını en aza indirecek
şekilde ayarlar. TF-IDF + lojistik regresyon metin sınıflandırmanın en güçlü
"ilk deneme"sidir ve çoğu zaman yeter. Bu bölüm üç modeli karşılaştırıyor,
ardından doğruluğun neden yetmediğini ve sınıf başına **kesinlik**,
**duyarlılık** ve **F1** ölçülerini anlatıyor.

## Doğrusal model metinde

Lojistik regresyon her sınıf için her kelimeye bir ağırlık verir. Bir
belgenin bir sınıftaki puanı, belgedeki kelimelerin TF-IDF değerleri çarpı
o sınıftaki ağırlıklarının toplamıdır (artı bir sabit). Puanlar softmax ile
olasılığa çevrilir ve en büyüğü seçilir. ML Algoritmaları'nda sıfırdan
yazdığın modelin aynısı; burada sütunlar kelimeler.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)
models = {"logistic": LogisticRegression(max_iter=1000),
          "svm": LinearSVC(), "naive bayes": MultinomialNB()}
for name, model in models.items():
    model.fit(A, y_train)
    print(name, round(model.score(B, y_test), 3))
```

```text
logistic 0.88
svm 0.888
naive bayes 0.852
```

- Lojistik regresyon %88, doğrusal SVM %88,8; aynı TF-IDF özellikleriyle
  Naive Bayes %85,2.
- `LinearSVC` sınıfları ayıran sınırla en yakın örnekler arasındaki payı
  büyütür; seyrek ve çok sütunlu metin verisinde çok iyi çalışır ve
  hızlıdır. Olasılık vermez (`predict_proba` yok).
- `max_iter=1000`: lojistik regresyon ağırlıkları adım adım ayarlar;
  varsayılan adım sayısı bazen yetmez ve uyarı verir.

## Doğruluk yetmez: karışıklık matrisi

%88 doğruluk her sınıf için %88 demek değil. Hangi sınıfın hangisiyle
karıştığını görmek için 00'daki hata tablosunun asıl adını kullanalım:
**karışıklık matrisi** (confusion matrix).

```python
from sklearn.metrics import confusion_matrix

lr = models["logistic"]
pred = lr.predict(B)
print(lr.classes_.tolist())
print(confusion_matrix(y_test, pred, labels=lr.classes_))
```

```text
['negative', 'neutral', 'positive']
[[ 75   2  21]
 [  6  49  17]
 [  2  12 316]]
```

- Satırlar **gerçek** sınıf, sütunlar **tahmin** (negative, neutral,
  positive sırasıyla). Köşegen doğru tahminler: 75, 49, 316.
- Olumsuz yorumların 21'i olumlu sanıldı; nötrlerin 17'si olumlu. Model
  emin olmadığında en büyük sınıfa, olumluya kayıyor.
- Olumlu yorumların 330'unun 316'sı doğru: doğruluğu yukarı çeken bu
  sınıf.

## Kesinlik, duyarlılık, F1

Her sınıf için iki soru sorulur:

- **Kesinlik** (precision): model "olumsuz" dediğinde ne kadar haklı?
  $\frac{\text{doğru olumsuz}}{\text{olumsuz denen hepsi}}$
- **Duyarlılık** (recall): gerçek olumsuzların ne kadarını yakaladı?
  $\frac{\text{doğru olumsuz}}{\text{gerçek olumsuzların hepsi}}$
- **F1** ikisinin harmonik ortalaması: $\frac{2PR}{P + R}$. Biri çok
  düşükse F1 de düşük olur.

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, pred, digits=3))
```

```text
              precision    recall  f1-score   support

    negative      0.904     0.765     0.829        98
     neutral      0.778     0.681     0.726        72
    positive      0.893     0.958     0.924       330

    accuracy                          0.880       500
   macro avg      0.858     0.801     0.826       500
weighted avg      0.878     0.880     0.877       500
```

- Olumsuz: kesinlik 0,904 (olumsuz dediğinde çoğunlukla haklı), duyarlılık
  0,765 (olumsuzların dörtte birini kaçırıyor).
- Nötr en zor sınıf: F1 0,726.
- **macro avg** sınıfların düz ortalaması: her sınıf eşit sayılır. **weighted
  avg** sınıf büyüklüğüyle ağırlıklı: büyük sınıf (olumlu) baskın. Dengesiz
  veride macro F1 (0,826) doğruluktan (0,880) daha dürüst bir özet.

## Az örnekli sınıfı güçlendirmek

`class_weight="balanced"` her sınıfın hatasını sınıfın büyüklüğüyle ters
orantılı ağırlıklandırır: az örnekli sınıftaki bir hata daha pahalıya gelir.

```python
balanced = LogisticRegression(max_iter=1000, class_weight="balanced")
balanced.fit(A, y_train)
print(classification_report(y_test, balanced.predict(B), digits=3))
```

```text
              precision    recall  f1-score   support

    negative      0.784     0.888     0.833        98
     neutral      0.652     0.806     0.720        72
    positive      0.947     0.861     0.902       330

    accuracy                          0.858       500
   macro avg      0.794     0.851     0.818       500
weighted avg      0.872     0.858     0.862       500
```

- Olumsuzun duyarlılığı 0,765 → 0,888, nötrünkü 0,681 → 0,806: azınlık
  sınıflar çok daha iyi yakalanıyor.
- Bedeli: kesinlikleri düştü (nötr 0,778 → 0,652) ve genel doğruluk 0,880 →
  0,858.

Hangisinin doğru olduğu göreve bağlı. Şikâyetleri kaçırmamak önemliyse
(olumsuz yorumu müşteri hizmetlerine yönlendirmek) duyarlılık; yanlış alarm
pahalıysa kesinlik. Bu bir **ödünleşim** (trade-off): birini artırmak
çoğu zaman öbürünü düşürür.

## Model ne öğrendi?

Lojistik regresyonun ağırlıkları (`coef_`) okunabilir: her sınıfın en büyük
ağırlıklı kelimeleri.

```python
words = vectorizer.get_feature_names_out()
for i, label in enumerate(lr.classes_):
    top = np.argsort(lr.coef_[i])[::-1][:5]
    print(label, [str(words[j]) for j in top])
```

```text
negative ['not', 'hate', 'worse', 'can', 'say']
neutral ['okay', 'fine', 'delivery', 'took', 'job']
positive ['but', 'totally', 'love', 'well', 'much']
```

- Olumsuz: "not", "hate", "worse"; ama **"can" ve "say"** de var. Veride "I
  can't say it is good" kalıbı geçiyor ve TF-IDF'in varsayılan parçalayıcısı
  "n't"yi atıyor (02): "can't" "can" oldu. Model olumsuzluğu "can" kelimesine
  yükledi.
- Nötr: "okay", "fine", "delivery took" ("Delivery took 16 days" nötr
  yorumlarda sık).
- Olumlu: "but" en başta: olumlu yorumlardaki "I expected ... but no"
  kalıbından.

Katsayılara bakmak hem modeli anlamanın hem de verideki tuhaflıkları
yakalamanın en ucuz yolu.

## Kelime çiftleriyle

```python
from sklearn.metrics import f1_score

bigrams = TfidfVectorizer(ngram_range=(1, 2)).fit(X_train)
A2, B2 = bigrams.transform(X_train), bigrams.transform(X_test)
for model in [LogisticRegression(max_iter=1000), LinearSVC()]:
    pred2 = model.fit(A2, y_train).predict(B2)
    accuracy = round(float((pred2 == y_test).mean()), 3)
    macro = round(f1_score(y_test, pred2, average="macro"), 3)
    print(type(model).__name__, accuracy, macro)
```

```text
LogisticRegression 0.898 0.846
LinearSVC 0.916 0.874
```

Doğrusal SVM kelime çiftleriyle %91,6 doğruluğa, 0,874 macro F1'e çıktı:
bu modülde şimdiye kadarki en iyi sonuç. 00'daki kurallar %44,9'daydı.

## Özet

- Doğrusal modeller her kelimeye her sınıf için bir ağırlık öğrenir. TF-IDF +
  lojistik regresyon ya da doğrusal SVM metin sınıflandırmanın güçlü
  başlangıcı.
- Karışıklık matrisi hangi sınıfın hangisiyle karıştığını gösterir;
  satırlar gerçek, sütunlar tahmin.
- Kesinlik "dediğinde haklı mı", duyarlılık "hepsini yakaladı mı"; F1 ikisinin
  harmonik ortalaması. Dengesiz veride macro F1'e bak.
- `class_weight="balanced"` azınlık sınıfların duyarlılığını artırır,
  kesinliği ve doğruluğu düşürür: göreve göre seç.
- Katsayılar okunabilir; verideki kalıpları ve parçalayıcının izlerini ("can")
  ortaya çıkarır.
