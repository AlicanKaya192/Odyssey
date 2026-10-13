# Bitirme: Destek Talebi Sınıflandırıcı

Bu modülde öğrendiklerini tek bir projede birleştiriyoruz. Görev: bir
mağazanın destek ekibine gelen talepleri **beş kategoriye** (hesap, fatura,
iade, kargo, teknik) ayıran, içinden sipariş numarasını çeken ve acil
olanları işaretleyen bir sistem. Adımlar gerçek bir projedeki sırayla:
veriye bak, taban çizgisini ölç, ön işlemeyi kur, modeli seç, hataları
incele, ikinci görevi (öncelik) dene ve hepsini tek bir fonksiyona bağla.

## Veri ve taban çizgisi

```python
import re
from collections import Counter

import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_tickets

tickets = make_tickets(4000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
for name, count in Counter(labels.tolist()).most_common():
    print(name, count)
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
print(len(X_train), len(X_test), round((y_test == "shipping").mean(), 3))
```

```text
shipping 1163
technical 1005
account 819
billing 624
refund 389
3000 1000 0.291
```

- Sınıflar dengesiz: kargo iadenin üç katı. Bu yüzden ölçü olarak doğruluğun
  yanında **macro F1** kullanacağız (09).
- Bölme `stratify` ile: test verisinde her sınıfın oranı bütün veridekiyle
  aynı.
- Taban çizgisi: her talebe "kargo" demek %29,1 doğru. Her model bunu
  açıkça geçmeli.

## Ön işleme: maskelemek

Taleplerde sipariş numaraları, tutarlar, e-postalar, tarihler ve hata
kodları var. Her numara dağarcığa ayrı bir kelime olarak giriyor
(`ord`, `27246`...) ve hiçbiri iki kez görülmüyor. 14'teki kurallarla bunları
**ortak bir yer tutucuya** çevirelim:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

MASKS = [(r"\bORD-\d+\b", " ordernum "), (r"\$[\d,]+(?:\.\d{2})?", " amount "),
         (r"\S+@\S+", " email "), (r"\b\d{4}-\d{2}-\d{2}\b", " date "),
         (r"\bE\d{3,4}\b", " errcode ")]


def mask(text):
    for pattern, placeholder in MASKS:
        text = re.sub(pattern, placeholder, text)
    return " ".join(text.lower().split())


print(mask("Refund $12.49 for ORD-27246 to ana7@example.com!"))
for preprocessor in [None, mask]:
    pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=preprocessor,
                                               ngram_range=(1, 2))),
                     ("model", LinearSVC())]).fit(X_train, y_train)
    pred = pipe.predict(X_test)
    size = len(pipe.named_steps["tfidf"].vocabulary_)
    print(preprocessor is not None, size, round((pred == y_test).mean(), 3),
          round(f1_score(y_test, pred, average="macro"), 3))
```

```text
refund amount for ordernum to email
False 7117 0.966 0.96
True 1951 0.976 0.971
```

- Maskeleme dağarcığı dörtte birine indirdi. Binlerce tek seferlik numara
  yerine "ordernum" gibi bir yer tutucu birçok talepte geçiyor ve model ona
  bir ağırlık öğrenebiliyor: "ordernum" geçmesi kargo ya da iade
  olasılığını artırıyor (14'teki tablo).
- Doğruluk da biraz arttı. Ama asıl kazanç sağlamlık: yeni bir sipariş
  numarası modelin hiç görmediği bir kelime değil artık.
- `mask` küçük harfe de çeviriyor; 10'daki notta gördüğün gibi
  `preprocessor` verince varsayılan küçük harf yapılmıyor.

## Modeli seçmek

Ayarları çapraz doğrulamayla arayalım; test verisine yalnızca en sonda bir
kez bakacağız:

```python
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=mask)),
                 ("model", LinearSVC())])
grid = GridSearchCV(pipe, {"tfidf__ngram_range": [(1, 1), (1, 2)],
                           "tfidf__min_df": [1, 2],
                           "model__C": [0.3, 1, 3]}, cv=5, scoring="f1_macro")
grid.fit(X_train, y_train)
print(grid.best_params_)
pred = grid.predict(X_test)
print(round(grid.best_score_, 3), round((pred == y_test).mean(), 3),
      round(f1_score(y_test, pred, average="macro"), 3))
```

```text
{'model__C': 3, 'tfidf__min_df': 1, 'tfidf__ngram_range': (1, 2)}
0.968 0.977 0.972
```

- 12 ayar × 5 kat = 60 model. En iyisi kelime çiftleri ve `C=3`.
- Test macro F1 0,972, çapraz doğrulamadaki 0,968'e çok yakın. Bu veride
  arama iyimserliği küçük; yine de son sayı testten.
- Taban çizgisinin %29,1'inden %97,7'ye. Ama talepler kalıplardan üretildi;
  gerçek taleplerde bu kadar yüksek sonuç beklenmez. Yöntem aynı kalır.

## Hata analizi

Yüzde 97,7 iyi; peki kalan %2,3 nerede?

```python
import textwrap

from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, pred, digits=3))
print(confusion_matrix(y_test, pred, labels=grid.classes_))
wrong = [(t, a, b) for t, a, b in zip(X_test, y_test, pred) if a != b]
print(len(wrong))
for text, true, guess in wrong[:3]:
    print(true, "->", guess)
    print(textwrap.fill(text, 76, initial_indent="  ", subsequent_indent="  "))
```

```text
              precision    recall  f1-score   support

     account      0.985     0.956     0.970       205
     billing      0.962     0.974     0.968       156
      refund      0.948     0.938     0.943        97
    shipping      0.980     0.993     0.986       291
   technical      0.988     0.992     0.990       251

    accuracy                          0.977      1000
   macro avg      0.973     0.971     0.972      1000
weighted avg      0.977     0.977     0.977      1000

[[196   5   4   0   0]
 [  2 152   1   1   0]
 [  0   1  91   3   2]
 [  1   0   0 289   1]
 [  0   0   0   2 249]]
23
account -> refund
  Hey there, Please reset the password for femi88@example.com. How long do
  refunds take to show on my card?
account -> billing
  Dear support, Please reset the password for gus53@example.com. Why did my
  card get charged $196.90 this month? Waiting for your answer.
shipping -> technical
  Hey there, My pcakage was delivered to the wrong address. The app crashes
  every time I open the order page. I paid with my credit card. Thanks.
```

- En zayıf sınıf iade (F1 0,943): en az örnekli sınıf ve fatura ile aynı
  kelimeleri kullanıyor ("card", "money", "charged").
- Karışıklık matrisinin köşegen dışındaki en büyük hücreleri hesap → fatura
  (5) ve hesap → iade (4).
- Örneklere bak: üç hatanın üçü de **iki konulu** talep. Şifre sıfırlama
  isteyen bir hesap talebi bir de "iadem ne zaman gelir?" diye soruyor.
  Kalan hatalara da tek tek baktığımızda 23 hatanın hepsinde talepte ikinci
  bir kategoriden bir cümle var (talepler üretilirken %15'ine böyle bir
  cümle ekleniyor).
- Bu hatalar modelin değil **görevin** sınırı: iki konulu bir talebi tek
  kategoriye koymak zaten tartışmalı. Çözüm daha iyi bir model değil, bir
  talebe birden fazla kategori verebilen (çok etiketli, multi-label) bir
  sistem ya da iki konulu talepleri insana yönlendirmek.

## İkinci görev: öncelik

Talepler ayrıca "high" ya da "normal" öncelikli. Önce bir kural, sonra bir
model deneyelim:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

priority = np.array([t["priority"] for t in tickets])
p_train, p_test = train_test_split(priority, test_size=0.25, random_state=0,
                                   stratify=labels)
rule = np.array(["high" if "urgent" in t.lower() else "normal" for t in X_test])
model = Pipeline([("tfidf", TfidfVectorizer(preprocessor=mask)),
                  ("model", LogisticRegression(max_iter=1000,
                                               class_weight="balanced"))])
guess = model.fit(X_train, p_train).predict(X_test)
for name, out in [("rule", rule), ("model", guess)]:
    print(name, round(precision_score(p_test, out, pos_label="high"), 3),
          round(recall_score(p_test, out, pos_label="high"), 3))
```

```text
rule 1.0 0.545
model 0.943 0.555
```

- "urgent" kuralı bulduğunda hep haklı (kesinlik 1,0) ama acil taleplerin
  ancak yarısını buluyor.
- Model daha iyisini yapamıyor: duyarlılık kurala yakın, kesinlik daha
  düşük. Sebep veride: acil taleplerin bir kısmı metinde hiçbir iz
  bırakmadan "high" etiketlenmiş (veri üretilirken taleplerin %10'u
  rastgele acil yapılıyor). Metinde olmayan bilgiyi hiçbir model metinden
  öğrenemez.
- Gerçek hayatta bu, etiketin başka bir kaynaktan (müşterinin üyelik türü,
  siparişin tutarı) geldiği anlamına gelir. Çözüm daha iyi bir metin modeli
  değil, o bilgiyi de modele vermek.

## Hepsini bağlamak

Son adım: bir talebi alıp kategori, sipariş numaraları ve aciliyeti tek
seferde döndüren bir fonksiyon.

```python
def route(text):
    return {"category": str(grid.predict([text])[0]),
            "orders": re.findall(r"\bORD-\d{5}\b", text),
            "urgent": "urgent" in text.lower()}


print(route("Hello, order ORD-55120 arrived damaged. This is urgent!"))
print(route("I cannot log in since Monday."))
```

```text
{'category': 'shipping', 'orders': ['ORD-55120'], 'urgent': True}
{'category': 'account', 'orders': [], 'urgent': False}
```

Bu fonksiyon bir web servisine ya da e-posta kutusunu dinleyen bir betiğe
konabilir. Modeli `joblib` ile kaydetmeyi (10'un ilk notu) ve maskeleme
fonksiyonunu bir modülde tutmayı unutma.

## Özet

- Taban çizgisi (%29,1) olmadan bir sonucun iyi olup olmadığı bilinmez.
- Veriye özgü gürültüyü maskelemek dağarcığı dörtte birine indirdi ve
  modeli yeni numaralara karşı sağlamlaştırdı.
- Ayarlar çapraz doğrulamayla seçildi, sonuç testte bir kez ölçüldü:
  %97,7, macro F1 0,972.
- Hata analizi zayıf sınıfı (iade) ve görevin kendi sınırını (iki konulu
  talepler) gösterdi.
- Öncelik etiketi kısmen metinde değildi; hiçbir metin modeli bunu
  aşamaz.
