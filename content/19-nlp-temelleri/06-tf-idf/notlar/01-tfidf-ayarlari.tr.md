`TfidfVectorizer`, `CountVectorizer`'ın bütün parametrelerini alır; bunlara
ek olarak ağırlıklandırmanın ayarları var.

| Parametre | Varsayılan | Ne yapar |
|---|---|---|
| `use_idf` | `True` | `False` olursa yalnızca TF + normalleştirme |
| `smooth_idf` | `True` | IDF formülündeki +1'ler; `False` olursa $\ln\frac{n}{\text{df}} + 1$ |
| `sublinear_tf` | `False` | TF yerine $1 + \ln(\text{tf})$: tekrarın etkisini yumuşatır |
| `norm` | `"l2"` | Satırları birim uzunluğa getirir; `"l1"` toplam 1, `None` normalleştirme yok |
| `min_df`, `max_df`, `ngram_range` | | `CountVectorizer`'daki gibi (04, 05) |

## sublinear_tf: tekrarı yumuşatmak

Dersteki yorumda "the" dört kez geçtiği için TF-IDF'te bile üçüncüydü.
`sublinear_tf=True` sayının kendisi yerine logaritmasını kullanır: 1 kez →
1, 4 kez → 2,39, 10 kez → 3,30.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
for sublinear in [False, True]:
    vectorizer = TfidfVectorizer(sublinear_tf=sublinear)
    X = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names_out()
    row = X[7].toarray().ravel()
    print(sublinear, [str(words[i]) for i in np.argsort(row)[::-1][:4]])
```

```text
False ['colour', 'love', 'the', 'buttons']
True ['colour', 'love', 'buttons', 'loud']
```

"the" listeden çıktı, yerine "loud" girdi. Uzun belgelerde (e-posta,
makale) bir kelimenin 20 kez geçmesi 2 kez geçmesinden on kat daha önemli
değildir; `sublinear_tf` bu yüzden uzun metinlerde sık kullanılır.

## Hangi ayarla başlamalı?

Metin sınıflandırmada sağlam bir başlangıç:

```text
TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
```

Sonra doğrulama verisiyle (09, 10) `min_df`, `ngram_range` ve
`sublinear_tf`'yi dene. Durak listesi çoğu zaman gerekmez: IDF sık
kelimeleri zaten bastırıyor.
