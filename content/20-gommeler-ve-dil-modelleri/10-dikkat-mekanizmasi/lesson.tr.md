# Dikkat Mekanizması

RNN bilgiyi adım adım taşır: üç kelime gerideki bir özneyi hatırlamak için
bilgi üç kez gizli duruma yazılıp okunmalı ve her adımda biraz kaybolur.
**Dikkat mekanizması** (attention) başka bir yol önerir: sonraki kelimeye
karar verirken **bütün önceki kelimelere doğrudan bak** ve hangisinin ne
kadar önemli olduğunu öğren. Uzaklık artık sorun değil; her kelime tek
adımda erişilebilir. Bu fikir 2014'te makine çevirisinde ortaya çıktı
(Bahdanau ve arkadaşları) ve transformer'ın temeli oldu. Bu bölümde dikkati
önce küçük bir örnekle anlayacak, sonra öğrenen bir dikkat modeli kuracağız.

## Yumuşak sözlük araması

Python sözlüğünde bir anahtarla tam olarak bir değere ulaşırsın. Dikkat bunun
**yumuşak** hâli: bir **sorgu** (query) bütün **anahtarlarla** (key)
karşılaştırılır, benzerlikler softmax ile ağırlığa çevrilir ve **değerlerin**
(value) ağırlıklı ortalaması alınır.

```python
import numpy as np


def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


keys = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])
values = np.array([[10.0], [20.0], [30.0]])
query = np.array([1.0, 0.2])
scores = keys @ query / np.sqrt(len(query))
weights = softmax(scores)
print(scores.round(3), weights.round(3))
print((weights @ values).round(2))
```

```text
[0.707 0.141 0.594] [0.406 0.231 0.363]
[19.57]
```

- Sorgu ilk anahtara en çok benziyor; en büyük ağırlığı o alıyor, ama öteki
  ikisi de pay alıyor. Sonuç değerlerin karışımı.
- Her şey türevlenebilir: sorgu, anahtarlar ve değerler öğrenilebilir.
  Sert bir "en iyisini seç" kararı türevlenemezdi.

## Neden √d'ye bölüyoruz?

Puanları vektör boyunun kareköküne böldük. Bunu yapmasak ne olur? Rastgele
vektörlerde nokta çarpımın büyüklüğü boyutla büyür:

```python
rng = np.random.default_rng(0)
for d in [4, 64, 512]:
    q = rng.normal(size=(1000, d))
    k = rng.normal(size=(1000, 10, d))
    s = np.einsum("nd,nkd->nk", q, k)
    raw = softmax(s).max(axis=1).mean()
    scaled = softmax(s / np.sqrt(d)).max(axis=1).mean()
    print(d, round(float(s.std()), 1), round(float(raw), 3), round(float(scaled), 3))
```

```text
4 2.0 0.493 0.305
64 7.9 0.875 0.322
512 22.8 0.952 0.322
```

- 512 boyutta puanların standart sapması 22,8: softmax neredeyse bütün
  ağırlığı tek bir anahtara veriyor (ortalama en büyük ağırlık 0,952).
  Böyle "sert" bir softmax'ın türevleri çok küçüktür ve öğrenme durur.
- `√d`'ye bölmek puanları her boyutta aynı ölçeğe getiriyor: en büyük
  ağırlık 0,32 civarında kalıyor. Transformer'ın "ölçekli nokta çarpım
  dikkati" (scaled dot-product attention) adı buradan geliyor.

## Öğrenen bir dikkat modeli

Şimdi dikkatin uzaklık sorununu çözdüğünü görelim. Görev: bir cümlenin
başından zamire kadar olan kısmını alıp gelen zamirin erkek ("he", "his")
mi kadın ("she", "her") mı olacağını tahmin etmek. "the queen smiled and
___" cümlesinde cevap üç kelime geride.

```python
from corpus_data import GENDER_PAIRS, make_corpus

examples = []
for sentence in make_corpus(20000):
    words = sentence.split()
    for i, w in enumerate(words):
        if w in {"he", "his", "she", "her"} and i >= 2:
            examples.append((words[:i], int(w in {"she", "her"})))
vocab = sorted({w for prefix, _ in examples for w in prefix})
index = {w: i for i, w in enumerate(vocab)}
print(len(examples), examples[0])
```

```text
2257 (['the', 'prince', 'played', 'with'], 0)
```

Model çok basit: her kelimenin bir gömmesi (`E`), öğrenilen tek bir **sorgu**
vektörü (`q`) ve bir çıkış katmanı. Sorgu "cinsiyeti hangi kelime söylüyor?"
sorusunu temsil ediyor; her kelimenin gömmesi hem anahtar hem değer.

```python
rng = np.random.default_rng(0)
E = rng.normal(0, 0.1, (len(vocab), 16))
q = rng.normal(0, 0.1, 16)
w, b = np.zeros(16), 0.0


def attend(prefix):
    X = E[[index[t] for t in prefix]]
    a = softmax(X @ q)
    c = a @ X
    p = 1 / (1 + np.exp(-(w @ c + b)))
    return X, a, c, p


for epoch in range(3):
    total = 0.0
    for i in rng.permutation(len(examples)):
        prefix, y = examples[i]
        X, a, c, p = attend(prefix)
        total -= np.log(p if y else 1 - p)
        dz = p - y
        dc = dz * w
        da = X @ dc
        ds = a * (da - a @ da)
        dX = np.outer(a, dc) + np.outer(ds, q)
        w, b, q = w - 0.5 * dz * c, b - 0.5 * dz, q - 0.5 * ds @ X
        np.add.at(E, [index[t] for t in prefix], -0.5 * dX)
    print(epoch, round(float(total / len(examples)), 3))
```

```text
0 0.05
1 0.0
2 0.0
```

Geri hesap 08'deki ağdan tek bir yeni parça içeriyor: softmax'ın türevi
`a · (da − a · da)`. Kayıp ilk turda neredeyse sıfıra iniyor.

## Model nereye bakıyor?

```python
correct = 0
for male, female in GENDER_PAIRS:
    for word, y in [(male, 0), (female, 1)]:
        correct += (attend(["the", word, "smiled", "and"])[3] > 0.5) == y
print(correct, 2 * len(GENDER_PAIRS))
for prefix in [["the", "queen", "smiled", "and"], ["the", "boy", "smiled", "and"]]:
    _, a, _, p = attend(prefix)
    print(" ".join(f"{t}:{x:.2f}" for t, x in zip(prefix, a)), round(float(p), 2))
```

```text
16 16
the:0.00 queen:0.99 smiled:0.00 and:0.00 1.0
the:0.11 boy:0.42 smiled:0.24 and:0.22 0.0
```

- 16 kişi kelimesinin 16'sında zamir doğru. Uzaklık fark etmiyor: dikkat
  "queen"e üç kelime öteden tek adımda bakıyor.
- "the queen smiled and" cümlesinde ağırlığın 0,99'u "queen"de. Model
  hiç söylenmeden cinsiyeti taşıyan kelimeye bakmayı öğrendi.
- "the boy smiled and" cümlesinde ağırlık daha dağınık ama karar yine doğru:
  erkek kelimeler burada "varsayılan" gibi davranıyor. Dikkat ağırlıkları
  modelin kararını her zaman tam açıklamaz (birinci not).

## Özet

- Dikkat yumuşak bir sözlük araması: sorgu anahtarlarla karşılaştırılır,
  softmax ağırlıkları değerleri karıştırır.
- Puanlar `√d`'ye bölünür; yoksa büyük boyutta softmax sertleşir, öğrenme
  durur.
- Dikkat her kelimeye tek adımda erişir; uzak bağımlılıklar için bilgiyi
  adım adım taşımaya gerek kalmaz.
- Öğrenen küçük bir dikkat modeli zamir testinde 16/16 yaptı ve ağırlığını
  cinsiyeti taşıyan kelimeye verdi.
