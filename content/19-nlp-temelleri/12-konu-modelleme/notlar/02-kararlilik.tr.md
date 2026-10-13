Bir konu modelini farklı `random_state` ile yeniden eğitince aynı konuları
bulur mu? Dersteki ön işlemeyle NMF ve LDA'yı üç tohumla deneyelim ve her
konunun ilk üç kelimesine bakalım:

```python
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import (ENGLISH_STOP_WORDS,
                                             CountVectorizer, TfidfVectorizer)
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
settings = dict(stop_words=stop, token_pattern=r"[a-z]{2,}", min_df=5)
tfidf, counter = TfidfVectorizer(**settings), CountVectorizer(**settings)
X, C = tfidf.fit_transform(texts), counter.fit_transform(texts)
words = tfidf.get_feature_names_out()


def heads(model):
    return sorted(" ".join(words[r.argsort()[::-1][:3]])
                  for r in model.components_)


for seed in [0, 1, 2]:
    nmf = NMF(n_components=5, random_state=seed, max_iter=500).fit(X)
    lda = LatentDirichletAllocation(n_components=5, random_state=seed).fit(C)
    print(seed, "nmf", heads(nmf)[:2])
    print(seed, "lda", heads(lda)[:2])
```

```text
0 nmf ['account email address', 'app page error']
0 lda ['account log error', 'address account change']
1 nmf ['account email address', 'app page error']
1 lda ['account paid card', 'error login page']
2 nmf ['account email address', 'app page error']
2 lda ['account address wrong', 'account twice tried']
```

- **NMF** üç tohumda da aynı konuları buldu. scikit-learn'ün NMF'i
  varsayılan olarak başlangıcı rastgele değil, matrisin kendisinden (SVD ile)
  kuruyor; tohum bu yüzden sonucu değiştirmedi.
- **LDA** her tohumda farklı konular buldu. LDA rastgele bir başlangıçtan
  yola çıkıyor ve kısa, az kelimeli belgelerde farklı yerel çözümlere
  takılıyor.
- Konuları sıraladık (`sorted`), çünkü konu numaraları anlamsızdır: aynı
  konu bir çalıştırmada 0, ötekinde 3 olabilir. Konuları numarayla değil
  kelimeleriyle karşılaştır.

Bir konu modelinin sonucunu rapor etmeden önce birkaç tohumla çalıştır.
Her seferinde çıkan konular gerçek; bir kez çıkıp kaybolan konuya güvenme.
