# Word2Vec

PPMI ve SVD **saymaya** dayanıyordu: önce bütün birlikte geçmeleri say,
sonra matrisi sıkıştır. 2013'te Mikolov ve arkadaşlarının **Word2Vec**'i
başka bir yol açtı: vektörleri **tahmin ederek** öğrenmek. Bir kelimeye
bakıp çevresindeki kelimeleri tahmin etmeye çalışan küçük bir model kur;
modelin ağırlıkları kelime vektörleri olsun. Bu bölümde Word2Vec'in en
yaygın biçimini, **olumsuz örneklemeli atlamalı gram** (skip-gram with
negative sampling, SGNS) modelini NumPy ile sıfırdan yazıp eğiteceğiz ve
PPMI + SVD ile karşılaştıracağız.

## Eğitim çiftleri

Atlamalı gram her kelimeyi **merkez** alır ve penceresindeki her kelimeyle
bir (merkez, bağlam) çifti kurar. Model, merkezden bağlamı tahmin etmeye
çalışacak.

```python
from collections import Counter

import numpy as np
from corpus_data import make_corpus

sentences = [s.split() for s in make_corpus(20000)]
counts = Counter(w for s in sentences for w in s)
vocab = sorted(counts)
index = {w: i for i, w in enumerate(vocab)}


def skipgram_pairs(tokens, window=2):
    return [(tokens[i], tokens[j]) for i in range(len(tokens))
            for j in range(max(0, i - window), min(len(tokens), i + window + 1))
            if j != i]


print(skipgram_pairs("the cat chased the dog".split())[:4])
pairs = np.array([(index[a], index[b]) for s in sentences
                  for a, b in skipgram_pairs(s)])
print(pairs.shape)
```

```text
[('the', 'cat'), ('the', 'chased'), ('cat', 'the'), ('cat', 'chased')]
(321232, 2)
```

20 000 cümleden 321 232 çift çıktı. Birlikte geçme matrisini saymak yerine bu
çiftleri birer birer modele göstereceğiz.

## Model: iki tablo ve bir olasılık

Her kelimenin **iki** vektörü var: merkez olduğunda kullanılan `W_in`
satırı ve bağlam olduğunda kullanılan `W_out` satırı. Bir (merkez, bağlam)
çiftinin "gerçek çift" olma olasılığı, iki vektörün nokta çarpımının
**sigmoid**'i:

`P(gerçek | merkez, bağlam) = σ(v_merkez · u_bağlam)`, `σ(x) = 1 / (1 + e^-x)`

```python
dim = 20
rng = np.random.default_rng(0)
W_in = (rng.random((len(vocab), dim)) - 0.5) / dim
W_out = np.zeros((len(vocab), dim))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


v, u = W_in[index["cat"]], W_out[index["chased"]]
print(W_in.shape, W_out.shape)
print(sigmoid(v @ u))
```

```text
(166, 20) (166, 20)
0.5
```

- `W_in` küçük rastgele sayılarla, `W_out` sıfırla başlıyor (Word2Vec'in
  kendi kodundaki gibi). Başta her çift için olasılık tam 0,5: model hiçbir
  şey bilmiyor.
- Eğitim, gerçek çiftlerin olasılığını 1'e itecek şekilde vektörleri
  ayarlayacak. Sonunda `W_in`'in satırları kelime vektörlerimiz olacak.

## Olumsuz örnekleme

Yalnızca gerçek çiftleri gösterirsek model her olasılığı 1 yaparak "kazanır".
Ona **yanlış** çiftler de göstermek gerekir: her gerçek çift için
dağarcıktan rastgele K kelime (burada 5) çekip "bunlar bağlam değil" deriz.
Rastgele kelimeler sıklığa göre çekilir, ama sayımlar 0,75 kuvvetine
yükseltilir; böylece "the" biraz daha az, nadir kelimeler biraz daha çok
seçilir (önceki bölümün notundaki yumuşatma).

```python
freq = np.array([counts[w] for w in vocab], dtype=float)
noise = freq ** 0.75 / (freq ** 0.75).sum()
for word in ["the", "cat", "throne"]:
    share = counts[word] / freq.sum()
    print(word, round(share, 4), round(float(noise[index[word]]), 4))
```

```text
the 0.2039 0.0958
cat 0.0053 0.0062
throne 0.0014 0.0022
```

"the" tokenların %20,4'ü ama olumsuz örneklerin %9,6'sı; "throne" binde
1,4'ten binde 2,2'ye çıkıyor. Kayıp fonksiyonu:

`L = −log σ(v · u_bağlam) − Σ log σ(−v · u_olumsuz)`

İlk terim gerçek çiftin olasılığını büyütmek, ikincisi rastgele çiftlerin
olasılığını küçültmek ister.

## Eğitmek

Kaybın türevi basit: gerçek çift için puanın türevi `σ(s) − 1`, olumsuz
çift için `σ(s)`. Çiftleri 256'lık gruplar hâlinde işleyip her grupta üç
tabloyu türevin tersi yönünde biraz kaydırıyoruz (gradyan inişi; ML
Algoritmaları'nın 04. bölümü). Öğrenme oranı eğitim boyunca doğrusal
olarak azalıyor.

```python
def train(dim=20, negatives=5, epochs=5, lr=0.05, batch=256, seed=0):
    rng = np.random.default_rng(seed)
    W_in = (rng.random((len(vocab), dim)) - 0.5) / dim
    W_out = np.zeros((len(vocab), dim))
    losses = []
    for epoch in range(epochs):
        step = lr * (1 - epoch / epochs)
        order = rng.permutation(len(pairs))
        total = 0.0
        for start in range(0, len(pairs), batch):
            c, o = pairs[order[start:start + batch]].T
            neg = rng.choice(len(vocab), size=(len(c), negatives), p=noise)
            v, u_pos, u_neg = W_in[c], W_out[o], W_out[neg]
            s_pos = sigmoid((v * u_pos).sum(axis=1))
            s_neg = sigmoid(np.einsum("bkd,bd->bk", u_neg, v))
            total -= np.log(s_pos).sum() + np.log(1 - s_neg).sum()
            g_pos, g_neg = (s_pos - 1)[:, None], s_neg[:, :, None]
            grad_v = g_pos * u_pos + (g_neg * u_neg).sum(axis=1)
            np.add.at(W_out, o, -step * g_pos * v)
            np.add.at(W_out, neg, -step * g_neg * v[:, None, :])
            np.add.at(W_in, c, -step * grad_v)
        losses.append(round(float(total / len(pairs)), 3))
    return W_in, W_out, losses


W_in, W_out, losses = train()
print(losses)
```

```text
[2.351, 1.985, 1.756, 1.565, 1.438]
```

- Kayıp her turda düşüyor: model gerçek çiftleri rastgele çiftlerden
  ayırmayı öğreniyor.
- `np.add.at` gerekli: aynı kelime bir grupta birden çok kez geçebilir
  (özellikle "the"); `W_in[c] -= ...` yazsaydık tekrarlanan satırların
  güncellemelerinden yalnızca biri kalırdı.
- `einsum("bkd,bd->bk", ...)` her çiftin K olumsuz vektörüyle merkez
  vektörünün nokta çarpımlarını tek seferde alıyor.

## Sonuç

```python
def unit(W):
    return W / np.linalg.norm(W, axis=1, keepdims=True)


def neighbours(E, word, k=4):
    sims = E @ E[index[word]]
    return [vocab[i] for i in np.argsort(-sims)[1:k + 1]]


def analogy(E, a, b, c):
    sims = E @ (E[index[b]] - E[index[a]] + E[index[c]])
    for w in (a, b, c):
        sims[index[w]] = -np.inf
    return vocab[int(np.argmax(sims))]


E = unit(W_in)
for word in ["cat", "bread", "paris"]:
    print(word, neighbours(E, word))
print(analogy(E, "man", "king", "woman"), analogy(E, "paris", "france", "rome"))
```

```text
cat ['sheep', 'mouse', 'dog', 'cow']
bread ['cake', 'soup', 'cheese', 'rice']
paris ['lisbon', 'athens', 'berlin', 'vienna']
queen italy
```

- Komşular yine sınıf sınıf ve `king − man + woman` yine "queen". Bu kez
  hiçbir matris saymadık; vektörler çiftleri tahmin etmeye çalışırken
  ortaya çıktı.
- `france − paris + rome` de "italy". Ama tek örnek yanıltabilir; bir
  sonraki blokta bütün teste bakacağız.

## İki tablo birlikte

`W_out`'u attık; ama o da bir kelime vektörü tablosu. Word2Vec'i
kullananların bir alışkanlığı iki tabloyu toplamak. Benzetme testinde
deneyelim:

```python
from corpus_data import CAPITALS, GENDER_PAIRS


def score(E):
    gender = sum(analogy(E, m1, f1, m2) == f2 for m1, f1 in GENDER_PAIRS
                 for m2, f2 in GENDER_PAIRS if m1 != m2)
    caps = list(CAPITALS.items())
    capital = sum(analogy(E, c1, k1, c2) == k2 for c1, k1 in caps
                  for c2, k2 in caps if c1 != c2)
    return gender, capital


print("W_in", score(unit(W_in)))
print("W_in + W_out", score(unit(W_in + W_out)))
```

```text
W_in (28, 5)
W_in + W_out (29, 56)
```

- `W_in` tek başına başkentlerde zayıf: 56'da 5 (PPMI + SVD 24 bulmuştu).
  İki tablo birlikte 56'nın 56'sını buluyor.
- Neden? `W_in`'deki benzerlik "aynı bağlamlarda geçmek"tir: "paris" ile
  "rome" benzer. `W_out`, bir kelimenin **bağlam olarak** nasıl
  göründüğünü tutar; `W_in` ile `W_out`'un çarpımı "birlikte geçmek"
  demektir: "paris" ile "france". Toplam iki türü birleştiriyor ve başkent
  ilişkisi tam olarak "birlikte geçen" iki kelimenin ilişkisi.
- Bu ölçümün küçük bir dünyada olduğunu unutma; gerçek gömmelerde toplamın
  etkisi daha küçüktür. Ama hangi tablonun "kelime vektörü" olduğu da bir
  seçimdir ve ölçülmeye değer.

## Özet

- Word2Vec vektörleri sayarak değil, merkez kelimeden bağlamı tahmin
  ederek öğrenir. Atlamalı gram her (merkez, bağlam) çiftini bir örnek
  yapar.
- Olumsuz örnekleme her gerçek çifte K rastgele "yanlış" çift ekler;
  rastgele kelimeler sıklığın 0,75 kuvvetiyle çekilir.
- Eğitim bir sigmoid ve gradyan inişi: kayıp 2,351'den 1,438'e indi.
  Tekrarlanan satırlar için `np.add.at`.
- Komşular ve `king − man + woman = queen` sayma yöntemindeki gibi çıktı.
  `W_in + W_out` başkent benzetmelerinin hepsini buldu.
