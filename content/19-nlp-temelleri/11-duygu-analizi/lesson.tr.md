# Duygu Analizi

**Duygu analizi** (sentiment analysis) bir metnin olumlu mu olumsuz mu
olduğunu bulmak. 08 ve 09'da bunu sınıflandırma olarak yaptık: etiketli
yorumlardan model öğrendik ve %91,6'ya ulaştık. Bu bölüm madalyonun öbür
yüzü: hiç etiketli veri olmadan, yalnızca bir **duygu sözlüğü** (lexicon)
ve birkaç kuralla ne kadar gidilebilir? Sonra iki yolu aynı test verisinde
karşılaştıracağız ve bir yorumun **neyini** beğenip neyini beğenmediğini
bulacağız: görüş yönü (aspect) bazında duygu.

## Sözlük tabanlı duygu

En basit fikir: olumlu kelimeleri +1, olumsuz kelimeleri −1 say, toplamın
işaretine bak.

```python
import re

import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from text_data import make_reviews

POSITIVE = {"good", "solid", "comfortable", "reliable", "sturdy", "nice",
            "quiet", "great", "excellent", "perfect", "fantastic",
            "impressive", "love", "loves", "worth", "better", "well", "needed"}
NEGATIVE = {"bad", "weak", "flimsy", "poor", "uncomfortable", "loud",
            "fragile", "terrible", "awful", "useless", "disappointing", "hate",
            "worse", "waste", "broke", "damaged", "late", "returned",
            "stopped", "never"}
TOKEN = re.compile(r"[a-z']+|[.,!?]")


def plain_score(text):
    words = TOKEN.findall(text.lower())
    return sum((w in POSITIVE) - (w in NEGATIVE) for w in words)


def to_label(score):
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)


def evaluate(name, score):
    pred = np.array([to_label(score(t)) for t in X_test])
    macro = f1_score(y_test, pred, average="macro")
    print(name, round((pred == y_test).mean(), 3), round(macro, 3))
    return pred


print(plain_score("The strap is great but the screen is weak."))
evaluate("plain", plain_score)
```

```text
0
plain 0.636 0.57
```

- Sözlüğü kendimiz yazdık: 18 olumlu, 20 olumsuz kelime. Hiç eğitim yok;
  eğitim verisini yalnızca karşılaştırma için ayırdık.
- "great" +1, "weak" −1: toplam 0, yani nötr. Karışık bir cümle için makul.
- Doğruluk %63,6. Taban çizgisinin (hep "olumlu", %65,9) bile altında. Ama
  sözlük taban çizgisi gibi tek sınıfa yığılmıyor: macro F1 0,57.

## Olumsuzlama

"Not worth the money" sözlüğe göre olumlu: "worth" +1. **Olumsuzlama**
(negation) kuralı: "not", "can't", "never" gibi bir kelimeden sonraki
birkaç kelimenin işaretini çevir. Noktalama işareti bu etkiyi keser.

```python
NEGATORS = {"not", "can't", "never", "no", "don't", "didn't"}


def negated_score(text, window=3):
    total, left = 0, 0
    for word in TOKEN.findall(text.lower()):
        if word in ".,!?":
            left = 0
            continue
        if word in NEGATORS:
            left = window
            continue
        value = (word in POSITIVE) - (word in NEGATIVE)
        if left:
            value = -value
            left -= 1
        total += value
    return total


print(negated_score("Not worth the money."))
print(negated_score("The lid is not bad at all."))
lexicon_pred = evaluate("negation", negated_score)
```

```text
-1
1
negation 0.754 0.691
```

- `left` olumsuzlayıcıdan sonra kaç kelimenin daha etkileneceğini sayıyor
  (pencere 3). "not bad" artık +1.
- Tek kural doğruluğu %63,6'dan %75,4'e çıkardı. 09'da kelime çiftlerinin
  ("not good") modele kattığının sözlükteki karşılığı bu.
- Pencere kaba bir yaklaşım: "not only good but great" gibi cümlelerde
  yanılır. Gerçek sistemler (VADER gibi) olumsuzlamayı, güçlendiricileri
  ("very") ve büyük harfi ayrı kurallarla ele alır; hepsi elle yazılmış
  kurallardır.

## "But"tan sonrası

Gerçek yorumlarda "ama"dan sonraki kısım çoğu zaman asıl hükmü taşır: "Ekranı
güzel ama pili bir günde bitiyor." Bu yüzden bazı sözlük yöntemleri "but"tan
sonrasını daha ağır sayar. Deneyelim:

```python
def but_score(text, weight=2):
    lower = text.lower()
    if " but " not in lower:
        return negated_score(lower)
    head, tail = lower.rsplit(" but ", 1)
    return negated_score(head) + weight * negated_score(tail)


evaluate("but x2", but_score)
```

```text
but x2 0.726 0.661
```

Kural **zarar verdi** (%75,4'ten %72,6'ya). Bu veride "But ..." cümlesi
yorumun sonuna eklenmiş **küçük bir itiraz**: puanı yorumun başı belirliyor.
Başka bir veriden gelen kural bu veriye taşınmıyor. Sözlük yöntemlerinin
zayıf yanı bu: kuralların her biri bir dil alışkanlığı hakkında tahmin, ve
tahmin ancak ölçülünce doğrulanır.

## Sözlük mü, model mi?

Aynı test verisinde 09'daki en iyi modelle karşılaştıralım. Olumsuzlama ve
ironi içeren yorumlara ayrıca bakalım:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LinearSVC())]).fit(X_train, y_train)
model_pred = pipe.predict(X_test)
print("model", round((model_pred == y_test).mean(), 3))
groups = {"negation": r"\bnot\b|can't",
          "sarcasm": r"great, the|just perfect|wonderful, it"}
for name, pattern in groups.items():
    idx = [i for i, t in enumerate(X_test) if re.search(pattern, t, re.I)]
    lex = (lexicon_pred[idx] == y_test[idx]).mean()
    mod = (model_pred[idx] == y_test[idx]).mean()
    print(name, len(idx), round(lex, 3), round(mod, 3))
```

```text
model 0.916
negation 127 0.827 0.984
sarcasm 17 0.765 1.0
```

- Model %91,6, sözlük %75,4. Olumsuzlama içeren 127 yorumda model %98,4,
  sözlük %82,7.
- İroni içeren 17 yorumda model hepsini bildi. Ama dikkat: bu yorumlar üç
  kalıptan geliyor ("Great, the ... broke"), model kalıbı ezberledi. Yeni
  bir ironi cümlesinde ne olduğunu ikinci notta ölçüyoruz.
- Sözlüğün asıl hatası olumlu yorumları nötr saymak: "Five stars for the
  strap" gibi sözlükte hiç kelimesi olmayan cümleler 0 alıyor.

Etiketli veri varsa model kazanır. Sözlük ne zaman işe yarar?

| Durum | Neden sözlük |
|---|---|
| Hiç etiketli veri yok | Başlamak için tek yol; sonra etiketleme için öneri üretir |
| Kararı açıklamak gerekiyor | Hangi kelimenin kaç puan verdiği tek tek görülür |
| Model eğitilen alanın dışına çıkılıyor | Model eğitildiği verinin kalıplarına bağlı |

Sözlük de alana bağlıdır: "loud" bir kulaklık için olumsuz, bir hoparlör için
olumlu olabilir; "unpredictable" bir filmin konusu için övgü, bir arabanın
direksiyonu için şikâyet.

## Görüş yönü bazında duygu

Bir yorum "kayış harika ama ekran zayıf" diyorsa tek bir etiket bilgiyi
kaybettirir. **Görüş yönü bazında duygu** (aspect-based sentiment) her
özellik için ayrı karar verir. Basit bir yol: yorumu cümlelere böl, içinde
özellik adı geçen cümleyi sözlükle puanla.

```python
from text_data import PRODUCTS


def aspect_scores(text, aspects):
    found = {}
    for sentence in re.findall(r"[^.!?]+", text.lower()):
        for aspect in aspects:
            if aspect in sentence:
                found[aspect] = found.get(aspect, 0) + negated_score(sentence)
    return found


aspects = PRODUCTS["sports watch"]
print(aspect_scores("The strap is great. The screen is weak.", aspects))
table = {a: [0, 0] for a in aspects}
for r in reviews:
    if r["product"] == "sports watch":
        for aspect, score in aspect_scores(r["text"], aspects).items():
            table[aspect][0] += score > 0
            table[aspect][1] += score < 0
for aspect, (good, bad) in table.items():
    print(f"{aspect:<13} +{good:<3} -{bad}")
```

```text
{'strap': 1, 'screen': -1}
strap         +29  -15
screen        +28  -7
battery       +20  -8
step counter  +22  -15
weight        +32  -12
```

- Spor saatinin yorumlarında her özellik için olumlu ve olumsuz yorum sayısı.
  Oranla en çok beğenilen ekran (28'e 7), en az beğenilen adım sayar (22'ye
  15).
- Bir mağaza için tek bir yıldız ortalamasından çok daha kullanışlı: hangi
  parçanın düzeltilmesi gerektiğini söylüyor.
- Yöntem kaba: "it" ile özelliğe dönen cümleyi ("It broke after a week")
  kaçırıyor, iki özellikli cümleye ikisine aynı puanı veriyor. Daha iyi
  yollar özelliği ve görüş kelimesini cümlenin yapısından eşleştirir.

## Özet

- Sözlük tabanlı duygu kelimelerin puanlarını toplar; eğitim gerektirmez.
- Olumsuzlama kuralı tek başına %63,6'yı %75,4'e çıkardı. "But"tan sonrasını
  ağır saymak bu veride zarar verdi: kuralları ölçmeden alma.
- Etiketli veri varsa model açık ara kazanır (%91,6). Sözlük etiket yokken,
  açıklama gerekirken ve alan değişirken işe yarar.
- Görüş yönü bazında duygu, yorumun neyi beğendiğini ayrı ayrı bulur.
