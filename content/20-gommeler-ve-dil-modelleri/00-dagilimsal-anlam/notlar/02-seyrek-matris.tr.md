Küçük dünyamızda matris 166 × 166 = 27 556 hücre. Gerçek bir dil için ne
olur?

```python
from collections import Counter

from corpus_data import make_corpus
from scipy import sparse

sentences = [s.split() for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
pairs = Counter()
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                pairs[index[w], index[s[j]]] += 1
rows, cols = zip(*pairs)
M = sparse.csr_matrix((list(pairs.values()), (rows, cols)),
                      shape=(len(vocab), len(vocab)))
print(M.nnz, round(M.nnz / (M.shape[0] * M.shape[1]), 3))
dense_bytes = M.shape[0] * M.shape[1] * 8
sparse_bytes = M.data.nbytes + M.indices.nbytes + M.indptr.nbytes
print(dense_bytes, sparse_bytes)
print(round(100_000 ** 2 * 8 / 1e9), "GB")
```

```text
2306 0.084
220448 28340
80 GB
```

- Hücrelerin yalnızca yaklaşık %8'i dolu: çoğu kelime çifti hiç birlikte
  geçmiyor. **Seyrek matris** (sparse) yalnızca dolu hücreleri ve
  yerlerini saklar.
- Bu küçük örnekte bile seyrek biçim yoğun biçimin sekizde biri kadar yer
  tutuyor. 100 000 kelimelik bir dağarcığın yoğun matrisi 80 GB olurdu; her
  kelime dağarcığın yalnızca küçük bir kısmıyla birlikte geçtiği için
  gerçek dilde dolu hücre oranı daha da düşüktür.
- NLP Temelleri'nde `CountVectorizer` de seyrek matris döndürüyordu; aynı
  sebepten. `Counter` ile çiftleri sayıp `csr_matrix`'e vermek, büyük bir
  külliyatta birlikte geçme matrisini kurmanın olağan yolu.
