Doğruluk tek bir sayı: kaç tahminin tuttuğunu söylüyor ama **hangi** hataların
yapıldığını söylemiyor. Hataları anlamanın en basit yolu, her (doğru etiket,
tahmin) çiftini saymak.

```python
from collections import Counter

pairs = Counter((r["label"], predict(r["text"])) for r in reviews)
for label in ["positive", "neutral", "negative"]:
    row = [pairs[(label, guess)] for guess in ["positive", "neutral", "negative"]]
    print(label.ljust(8), row, sum(row))
```

```text
positive [528, 687, 103] 1318
neutral  [28, 239, 22] 289
negative [79, 183, 131] 393
```

Bu, dersteki `predict` kuralının hata tablosu. Her satır bir **doğru**
etiket, sütunlar sırasıyla kuralın `positive`, `neutral`, `negative`
tahmini. Köşegen (sol üstten sağ alta: 528, 239, 131) doğru tahminler;
toplamları 898, dersteki sayı.

## Tablo ne söylüyor?

- **Olumlu yorumların 687'sine "nötr" denmiş.** Sorun en çok burada: olumlu
  yorumların çoğu listemizdeki kelimeleri hiç içermiyor ("It does the job",
  "Much better"), skor 0 kalıyor.
- **Olumlu yorumların 103'üne "olumsuz" denmiş.** Bunların çoğu olumsuzlama:
  "not bad", "not fragile".
- **Olumsuz yorumların 183'üne "nötr" denmiş.** "would not buy", "Returned
  it" gibi cümleler hiçbir listede değil.
- Nötr yorumlarda kural iyi görünüyor (289'un 239'u), ama bu bir başarı
  değil: kural, emin olmadığı her şeye zaten "nötr" diyor.

Son madde önemli: bir sınıfta yüksek isabet, modelin o sınıfa her şeyi
yığmasından da gelebilir. Bunu ölçen kavramlara (**kesinlik** ve **duyarlılık**,
precision ve recall) 09. bölümde bakacağız. Bu tabloya da orada asıl adıyla
**karışıklık matrisi** (confusion matrix) diyeceğiz.

## Alışkanlık

Her model denemesinden sonra yalnızca doğruluğa bakma:

1. Hata tablosunu çıkar.
2. En büyük hata hücresinden birkaç örnek oku.
3. Hatanın sebebini adlandır (olumsuzlama, eksik kelime, yazım hatası).

Hangi yöntemi deneyeceğine bu sebepler karar verir.
