Dağılımsal hipotez "benzer bağlam, benzer anlam" diyor. Ama "benzer anlam"
tam olarak ne demek? Sıfatlara bakalım:

```python
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
unit = M / np.linalg.norm(M, axis=1, keepdims=True)
for word in ["fast", "warm"]:
    sims = unit @ unit[index[word]]
    best = np.argsort(-sims)[1:4]
    print(word, [(vocab[i], round(float(sims[i]), 3)) for i in best])
```

```text
fast [('slow', 0.997), ('noisy', 0.993), ('new', 0.993)]
warm [('fresh', 0.999), ('sweet', 0.998), ('cold', 0.998)]
```

- "fast"in en yakın komşusu "slow"; "warm"ın komşuları arasında 0,998
  benzerlikle "cold" var.
  Zıt anlamlı kelimeler **aynı bağlamlarda** geçer: "the bus is fast" ve
  "the bus is slow" aynı kalıp. Bağlamdan bakınca neredeyse ayırt
  edilemezler.
- Dağılımsal benzerlik "aynı yerde kullanılabilir" demek, "aynı anlama
  gelir" değil. Eş anlamlıları, zıt anlamlıları ve aynı sınıfın üyelerini
  ("cat", "dog") birlikte yakalar.

## Bunun bedeli

- Duygu analizinde "good" ile "bad"in vektörleri yakınsa, yalnızca
  vektörlere bakan bir model ikisini karıştırabilir. Gerçek gömmelerde de
  bu bilinen bir sorundur; duygu için etiketli veriyle eğitim gerekir.
- Bir kelimenin birden çok anlamı varsa ("bank": banka ve nehir kıyısı) tek
  bir vektör ikisinin ortalaması olur. Bu modülün sonunda göreceğimiz
  **bağlamsal** gömmeler, kelimeye bulunduğu cümleye göre farklı vektör
  vererek bunu aşar.
