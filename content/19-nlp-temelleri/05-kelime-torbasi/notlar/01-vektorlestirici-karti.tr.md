`CountVectorizer`'ın en çok kullanılan parçaları.

## Metotlar ve nitelikler

| Ad | Ne yapar |
|---|---|
| `fit(metinler)` | Dağarcığı öğrenir |
| `transform(metinler)` | Metinleri öğrenilmiş dağarcıkla sayar (seyrek matris) |
| `fit_transform(metinler)` | İkisi birden; yalnızca eğitim verisinde |
| `get_feature_names_out()` | Sütun adları (kelimeler), sütun sırasıyla |
| `vocabulary_` | Kelime → sütun numarası sözlüğü |
| `build_analyzer()` | Metni nasıl parçaladığını gösteren fonksiyon |
| `inverse_transform(X)` | Satırlardan o belgede geçen kelimelere geri dönüş |

## Parametreler

| Parametre | Varsayılan | Not |
|---|---|---|
| `lowercase` | `True` | Büyük harfi korumak için `False` |
| `token_pattern` | en az iki karakterlik kelimeler | tek harfler ve "n't" düşer (02) |
| `stop_words` | `None` | `"english"` olumsuzlukları da siler (03) |
| `ngram_range` | `(1, 1)` | `(1, 2)` ikilileri ekler (04) |
| `min_df`, `max_df` | `1`, `1.0` | seyrek ve çok sık sütunları atar |
| `max_features` | `None` | en sık k kelimeyle sınırlar |
| `binary` | `False` | sayı yerine var-yok |

## max_features ve geri dönüş

```python
from sklearn.feature_extraction.text import CountVectorizer

docs = ["the battery is great", "the battery died", "great price great sound"]
vectorizer = CountVectorizer(max_features=4)
X = vectorizer.fit_transform(docs)
print(vectorizer.get_feature_names_out().tolist())
print(vectorizer.inverse_transform(X[2:3])[0].tolist())
```

```text
['battery', 'died', 'great', 'the']
['great']
```

`max_features=4` yalnızca en sık 4 kelimeyi tuttu; "price" ve "sound"
düştü. Üçüncü belgeye geri dönünce yalnızca "great" kaldı: belge artık
"great price great sound" değil. Dağarcığı daraltmak her zaman bir şey
götürür; ne götürdüğüne `inverse_transform` ile bakabilirsin.
