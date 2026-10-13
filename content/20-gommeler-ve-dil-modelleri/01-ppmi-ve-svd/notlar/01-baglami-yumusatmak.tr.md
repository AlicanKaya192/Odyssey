PPMI'ın bilinen bir zayıflığı var: **nadir bağlam kelimeleri** PMI'ı şişirir.
Bir bağlam kelimesi az geçiyorsa `P(c)` küçüktür; onunla bir kez birlikte
görünmek bile büyük bir PMI verir. Word2Vec'in olumsuz örnekleme
dağılımından alınıp PPMI'a uygulanan bir hile (Levy, Goldberg ve Dagan,
2015) bunu yumuşatır: bağlam olasılıklarını hesaplarken sayımları `α = 0,75`
kuvvetine yükseltmek. Nadir kelimelerin payı biraz artar, `P(c)` o kadar
küçük kalmaz, PMI şişmez.

Üç vektör ailesini dersteki benzetme testinde karşılaştıralım: ham sayımların
SVD'si, PPMI'ın SVD'si ve yumuşatılmış PPMI'ın SVD'si (hepsi 20 boyut).

```python
import numpy as np
from corpus_data import CAPITALS, GENDER_PAIRS, make_corpus

sentences = [s.split() for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                M[index[w], index[s[j]]] += 1


def ppmi(alpha):
    p_word = M.sum(axis=1) / M.sum()
    smooth = M.sum(axis=0) ** alpha
    p_context = smooth / smooth.sum()
    with np.errstate(divide="ignore"):
        P = np.log((M / M.sum()) / np.outer(p_word, p_context))
    return np.maximum(P, 0)


def vectors(X, k=20):
    U, S, _ = np.linalg.svd(X)
    E = U[:, :k] * S[:k]
    return E / np.linalg.norm(E, axis=1, keepdims=True)


def analogy(E, a, b, c):
    sims = E @ (E[index[b]] - E[index[a]] + E[index[c]])
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


print("counts", score(vectors(M)))
print("ppmi", score(vectors(ppmi(1.0))))
print("ppmi 0.75", score(vectors(ppmi(0.75))))
```

```text
counts (27, 17)
ppmi (31, 24)
ppmi 0.75 (32, 25)
```

- Ham sayımların SVD'si en zayıfı: sık kelimeler yönlere hâkim oluyor.
- PPMI belirgin biçimde daha iyi; yumuşatma küçük bir adım daha ekliyor.
- Bu farklar küçük bir veride ve 112 soruluk bir testte ölçüldü; bir iki
  doğru cevap rastlantı olabilir. Gerçek çalışmalarda yumuşatmanın etkisi
  büyük külliyatlarda ve birçok testte ölçülmüştür. Kendi verinde de ölçmeden
  bir ayarı "iyileştirme" sayma.
