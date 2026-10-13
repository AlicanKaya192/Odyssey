Dört normalleştirme aracı, ne yaptıkları ve bedelleri.

| Yöntem | Ne yapar | Örnek | Bedeli | Ne zaman |
|---|---|---|---|---|
| Durak kelimeleri | Sık, tek başına anlamsız kelimeleri atar | "the", "is" gider | Olumsuzluk ve şiddet kelimeleri de gidebilir | Konu bulma, arama; duygu analizinde dikkatli |
| Kök bulma | Ekleri kurallarla keser | "loves" → "love" | Tutarsız kökler, fazla/az kesme | Hızlı ve kaba birleştirme |
| Lemmatisation | Sözlükteki temel biçim | "was" → "be" | Sözlük ve dil bilgisi ister, yavaş | Doğruluk önemliyse |
| Yer tutucu | Değişken bilgiyi tek token yapar | ORD-48213 → `<order>` | Bilginin kendisi kaybolur | Sınıflandırma; bilgi çıkarmada değil |

## Olumsuzlukları koruyan durak listesi

Hazır listeyi kullanacaksan olumsuzluk ve şiddet kelimelerini listeden
çıkar:

```python
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

KEEP = {"not", "no", "never", "nor", "very", "too"}
STOP = ENGLISH_STOP_WORDS - KEEP
print(len(STOP))
tokens = "the fit is not good at all".split()
print([t for t in tokens if t not in STOP])
```

```text
312
['fit', 'not', 'good']
```

`ENGLISH_STOP_WORDS` bir `frozenset`; `-` ile fark alınca yeni bir küme
çıkıyor, asıl liste değişmiyor. "not" artık kaldı: "fit not good".

## scikit-learn'de

| Parametre | Ne yapar |
|---|---|
| `CountVectorizer(stop_words="english")` | Hazır İngilizce listeyi kullanır (olumsuzluklar dahil siler) |
| `CountVectorizer(stop_words=list(STOP))` | Kendi listeni verir |
| `CountVectorizer(lowercase=False)` | Büyük harfi korur |
| `CountVectorizer(tokenizer=fonksiyon)` | Kendi parçalayıcın; içinde kök bulma da yapabilirsin |
| `CountVectorizer(preprocessor=fonksiyon)` | Parçalamadan önce metne uygulanır (temizlik, yer tutucu) |

## Sıra

Temizlik → yer tutucu → parçalama → küçük harf → durak kelimeleri → kök
bulma. Yer tutucu parçalamadan **önce** gelir: e-posta ve tutar daha
dağılmadan yakalanmalı.
