# PPMI ve SVD ile Kelime Vektörleri

Önceki bölümde birlikte geçme sayımları anlam sınıflarını ayırdı, ama "the"
gibi sık kelimeler her vektöre hâkimdi: "cat" ile "bread" 0,612 benzer
çıktı. Bu bölümde iki adım atacağız. Önce sayımları **PMI** ile
ağırlıklandırıp "beklenenden ne kadar sık?" sorusuna çevireceğiz; sık
kelimelerin etkisi kendiliğinden düşecek. Sonra **SVD** ile 166 sütunluk
vektörleri 20 sayıya sıkıştıracağız. Sonunda elimizde **yoğun kelime
vektörleri** (dense word vectors) olacak ve onlarla "king − man + woman"
gibi hesaplar yapabileceğiz.

## PMI: beklenenden ne kadar sık?

"cat" ile "the" 662 kez birlikte geçti, "cat" ile "chased" 154 kez. Ama
"the" zaten her yerde. Asıl soru: iki kelime **rastlantıyla beklenenden**
ne kadar sık birlikte geçiyor? **Noktasal karşılıklı bilgi** (PMI, pointwise
mutual information) bunu ölçer:

`PMI(w, c) = log( P(w, c) / (P(w) · P(c)) )`

İki kelime birbirinden bağımsız olsaydı birlikte görülme olasılıkları
`P(w) · P(c)` olurdu. PMI gerçek olasılığın buna oranının logaritması: 0
"bağımsız", pozitif "beklenenden sık", negatif "beklenenden seyrek". NLP
Temelleri'nin 04. bölümünde kelime çiftleri için gördüğün PMI ile aynı fikir.

```python
from collections import Counter

import numpy as np
from corpus_data import make_corpus

sentences = [s.split() for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                M[index[w], index[s[j]]] += 1
total = M.sum()
p_word = M.sum(axis=1) / total
p_context = M.sum(axis=0) / total


def pmi(w, c):
    joint = M[index[w], index[c]] / total
    return np.log(joint / (p_word[index[w]] * p_context[index[c]]))


with np.errstate(divide="ignore"):
    for w, c in [("cat", "chased"), ("cat", "the"), ("cat", "cooked")]:
        print(w, c, int(M[index[w], index[c]]), round(float(pmi(w, c)), 2))
```

```text
cat chased 154 2.33
cat the 662 0.75
cat cooked 0 -inf
```

- "cat" ile "the" 662 kez geçti ama PMI'ları yalnızca 0,75: "the" her
  kelimenin yanında olduğu için bu birliktelik pek bir şey söylemiyor.
- "cat" ile "chased" daha az geçti (154) ama PMI 2,33: rastlantının yaklaşık
  on katı (`e^2,33 ≈ 10`).
- Hiç birlikte geçmeyen çiftin PMI'ı eksi sonsuz (`log 0`). Sayılarla
  çalışabilmek için bunu düzelteceğiz.

## PPMI matrisi

**Pozitif PMI** (PPMI) negatif değerleri, sonsuz dahil, 0 yapar:
`PPMI = max(PMI, 0)`. Negatif PMI güvenilmez: "beklenenden seyrek" demek
için çok fazla veri gerekir. Bütün matrisi bir kerede hesaplayalım:

```python
with np.errstate(divide="ignore"):
    P = np.log((M / total) / np.outer(p_word, p_context))
P = np.maximum(P, 0)


def cosine(X, a, b):
    x, y = X[index[a]], X[index[b]]
    return round(float(x @ y / np.linalg.norm(x) / np.linalg.norm(y)), 3)


def neighbours(X, word, k=4):
    unit = X / np.linalg.norm(X, axis=1, keepdims=True)
    sims = unit @ unit[index[word]]
    return [vocab[i] for i in np.argsort(-sims)[1:k + 1]]


print(cosine(P, "cat", "dog"), cosine(P, "cat", "bread"))
for word in ["cat", "king", "paris"]:
    print(word, neighbours(P, word))
```

```text
0.995 0.033
cat ['cow', 'dog', 'rabbit', 'horse']
king ['queen', 'uncle', 'brother', 'man']
paris ['athens', 'vienna', 'berlin', 'rome']
```

- "cat" ile "dog" 0,995 benzer kaldı, ama "cat" ile "bread" 0,612'den
  0,033'e düştü. Ortak sık kelimeler artık benzerlik yaratmıyor; ayrım
  çok daha keskin.
- `np.outer(p_word, p_context)` her hücre için bağımsızlıkta beklenen
  olasılığı veriyor; bölme ve logaritma bütün matrise tek seferde
  uygulanıyor.

## SVD ile kısaltmak

PPMI vektörleri hâlâ 166 sayı uzunluğunda ve çoğu 0. Gerçek bir dilde
yüz binlerce sütun olurdu. **SVD** (tekil değer ayrışımı, singular value
decomposition) matrisi `U · diag(S) · Vᵀ` biçiminde yazar; tekil değerler
(`S`) büyükten küçüğe sıralıdır. İlk k tanesini tutup gerisini atınca,
matrisin en çok bilgiyi taşıyan k yönünü korumuş oluruz. (ML Algoritmaları
modülündeki PCA'nın arkasında da SVD var.)

```python
U, S, Vt = np.linalg.svd(P)
energy = (S ** 2).cumsum() / (S ** 2).sum()
print([round(float(energy[k - 1]), 3) for k in [5, 10, 20, 50]])
k = 20
E = U[:, :k] * S[:k]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
print(E.shape)
for word in ["cat", "bread", "car"]:
    print(word, neighbours(E, word))
```

```text
[0.378, 0.593, 0.794, 0.948]
(166, 20)
cat ['cow', 'rabbit', 'mouse', 'horse']
bread ['rice', 'soup', 'cake', 'cheese']
car ['truck', 'tram', 'bus', 'bike']
```

- 20 boyut matrisin "enerjisinin" (tekil değerlerin karelerinin toplamı)
  %79,4'ünü tutuyor. Her kelime artık 20 sayılık **yoğun** bir vektör.
- Komşular aynı kaldı: hayvanlar, yiyecekler, taşıtlar. Bilgi 166 sütundan
  20'ye sıkıştı, ama anlam sınıfları korundu.
- Vektörleri birim uzunluğa getirdik; böylece nokta çarpım doğrudan
  kosinüs benzerliği oluyor.

## Benzetmeler

Yoğun vektörlerde bir fark bir **yön** taşıyabilir: "king" ile "queen"
arasındaki fark, "man" ile "woman" arasındaki farka benziyorsa,
`king − man + woman` hesabı "queen"e yakın düşer.

```python
from corpus_data import CAPITALS, GENDER_PAIRS


def analogy(E, a, b, c):
    """a : b :: c : ?  →  b - a + c vektörüne en yakın kelime."""
    target = E[index[b]] - E[index[a]] + E[index[c]]
    sims = E @ target
    for w in (a, b, c):
        sims[index[w]] = -np.inf
    return vocab[int(np.argmax(sims))]


def score(E):
    gender = sum(analogy(E, m1, f1, m2) == f2 for m1, f1 in GENDER_PAIRS
                 for m2, f2 in GENDER_PAIRS if m1 != m2)
    caps = list(CAPITALS.items())
    capital = sum(analogy(E, c1, k1, c2) == k2 for c1, k1 in caps
                  for c2, k2 in caps if c1 != c2)
    return gender, capital


print(analogy(E, "man", "king", "woman"))
print(analogy(E, "paris", "france", "rome"))
print(score(E), len(GENDER_PAIRS) * 7, len(CAPITALS) * 7)
```

```text
queen
italy
(31, 24) 56 56
```

- `king − man + woman` → "queen", `france − paris + rome` → "italy". Kimse
  "kraliçe kadın kraldır" ya da "Roma İtalya'nın başkentidir" demedi;
  bu ilişkiler yalnızca birlikte geçme sayımlarından çıktı.
- Ama her zaman değil: 56 cinsiyet benzetmesinin 31'i, 56 başkent
  benzetmesinin 24'ü doğru. Benzetme testi gömmelerin klasik ölçüsüdür ve
  gerçek gömmelerde de mükemmel değildir.
- Sorunun üç kelimesini adayların dışında tuttuk; yoksa en yakın kelime
  çoğu zaman sorudaki kelimelerden biri olur.

## Kaç boyut?

```python
for k in [2, 5, 10, 20, 50, 166]:
    Ek = U[:, :k] * S[:k]
    Ek = Ek / np.linalg.norm(Ek, axis=1, keepdims=True)
    print(k, score(Ek), analogy(Ek, "man", "king", "woman"))
```

```text
2 (12, 3) his
5 (27, 9) queen
10 (31, 23) queen
20 (31, 24) queen
50 (32, 18) queen
166 (32, 8) queen
```

- 2 boyut çok az: "king − man + woman" bile "his" çıkıyor.
- Başkent benzetmeleri 20 boyutta en iyisi (24) ve boyut arttıkça
  **düşüyor**: 166 boyutta, yani hiç kısaltmadan, yalnızca 8. Kesmek
  gürültüyü de atıyor; az sayıda güçlü yön ilişkiyi daha temiz taşıyor.
- Boyut bir ayar: gerçek gömmelerde genellikle 100 ile 300 arası seçilir ve
  bir görevde ölçülerek belirlenir.

## Özet

- PMI bir birlikteliğin rastlantıdan ne kadar sık olduğunu ölçer; sık
  kelimelerin ağırlığını kendiliğinden düşürür. PPMI negatifleri 0 yapar.
- PPMI ile "cat" ile "bread" benzerliği 0,612'den 0,033'e indi.
- SVD, PPMI matrisini az sayıda yoğun boyuta sıkıştırır; 20 boyut bilginin
  %79'unu tuttu ve anlam sınıflarını korudu.
- Yoğun vektörlerde farklar yön taşır: `king − man + woman ≈ queen`.
  Kısaltmak benzetmeleri iyileştirdi; boyut ölçülerek seçilir.
