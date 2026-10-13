Zipf yasası metin tablolarının neredeyse tamamen sıfır olacağını söylüyordu.
Ölçelim:

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
X = CountVectorizer(ngram_range=(1, 2)).fit_transform(texts)
cells = X.shape[0] * X.shape[1]
print(X.shape, X.nnz, round(X.nnz / cells, 4))
dense_mb = cells * 8 / 1e6
sparse_mb = (X.data.nbytes + X.indices.nbytes + X.indptr.nbytes) / 1e6
print(round(dense_mb, 1), round(sparse_mb, 2))
```

```text
(2000, 2737) 52089 0.0095
43.8 0.63
```

- Tablo 2000 satır × 2737 sütun = 5,5 milyon hücre; bunların yalnızca
  52 089'u sıfırdan farklı (`nnz`, number of non-zeros). **Doluluk %0,95.**
- Bütün hücreleri saklamak 43,8 MB tutardı; scikit-learn yalnızca sıfır
  olmayanları ve yerlerini saklıyor: 0,63 MB.

## Seyrek matris nasıl saklanır?

scikit-learn metin tablolarını SciPy'nin **CSR** (compressed sparse row)
biçiminde döndürür. Üç dizi:

| Dizi | İçinde ne var |
|---|---|
| `data` | Sıfır olmayan değerler |
| `indices` | Her değerin sütun numarası |
| `indptr` | Her satırın `data` içinde nerede başladığı |

Bunu bilmek için iki pratik sebep var:

1. **`X.toarray()` deme.** Seyrek matrisi düz (dense) diziye çevirmek bütün
   sıfırları belleğe yazar; büyük veride bellek biter.
2. **Seyrek matrisle çalışan model seç.** Lojistik regresyon, doğrusal SVM ve
   Naive Bayes seyrek girdiyi doğrudan alır; bazı modeller (ör. pek çok ağaç
   uygulaması) düz diziye çevirir ve yavaşlar.

Satırları ve sütunları seçmek seyrek matriste de çalışır: `X[0]` ilk
belgenin satırı, `X[:, 5]` beşinci sütun. `X[0].nnz` ilk belgede kaç farklı
n-gram geçtiğini verir.
