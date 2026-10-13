scikit-learn'ün vektörleştiricilerinde n-gram ve dağarcık ayarları.

| Parametre | Ne yapar | Örnek |
|---|---|---|
| `ngram_range=(1, 2)` | Tek kelimeler ve ikililer | "not", "good", "not good" |
| `ngram_range=(2, 2)` | Yalnızca ikililer | "not good" |
| `analyzer="word"` | Kelime n-gram'ları (varsayılan) | |
| `analyzer="char"` | Harf n-gram'ları, kelime sınırını aşar | "t g" de bir parça |
| `analyzer="char_wb"` | Harf n-gram'ları, kelimenin içinde | " lo", "lov", "ove", "ve " |
| `min_df=2` | En az 2 belgede geçmeyeni atar | tek seferlik çiftler gider |
| `min_df=0.01` | Belgelerin en az %1'inde geçmeli (oran) | |
| `max_df=0.9` | Belgelerin %90'ından fazlasında geçeni atar | durak kelimesi gibi davranır |
| `max_features=1000` | En sık 1000 n-gram'ı tutar | sütun sayısına üst sınır |

## min_df ile dağarcığı budamak

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
for min_df in [1, 2, 5, 20]:
    vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=min_df).fit(texts)
    print(min_df, len(vectorizer.vocabulary_))
```

```text
1 2737
2 1573
5 901
20 454
```

Yalnızca bir belgede geçen n-gram'ları atmak (`min_df=2`) sütunların
%40'ından fazlasını götürüyor. Bunlar zaten tek bir örnekten öğrenilemezdi.
`min_df` değerini çok büyütmek ise nadir ama ayırt edici ifadeleri de
atar; doğru değeri doğrulama verisiyle seçeriz (09. ve 10. bölüm).

## Hangi n?

- **Kelime 1-2 gram:** sınıflandırmada en sık başlangıç; "not good" gibi
  olumsuzlamaları yakalar.
- **Kelime 3-gram ve üstü:** dağarcık patlar, nadiren kazanç getirir.
- **Harf 3-5 gram (`char_wb`):** yazım hatası, ek ve yabancı kelime çok
  olan metinlerde (tweet, ürün adı) iyi; Türkçe gibi eklemeli dillerde de
  işe yarar.
