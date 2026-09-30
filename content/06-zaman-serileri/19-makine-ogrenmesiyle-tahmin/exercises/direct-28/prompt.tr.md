28 günlük ufuk için doğrudan tahmin kur: yalnızca en az 28 gün eski
gecikmeler ve takvim. Bölüm 15'in düzeneğiyle sına.

Başlangıç kodunda `safe_features(full, calendar=True)` hazır: `lag28`,
`lag35`, `lag42`, `lag56`, iki düzey özelliği, haftanın günü kuklaları ve
(`calendar=True` ise) gün sayacı, Aralık tırmanışı ve Fourier terimleri.
`cuts` 13 kesim günü.

**Yapman gerekenler:**

1. `forecast(train, future_index, calendar)` fonksiyonunu yaz:
   - `full = train.reindex(train.index.union(future_index))`: gelecek
     tarihler `NaN` olarak eklenir.
   - `X = safe_features(full, calendar)`.
   - Eğitim satırları: `X.loc[train.index].dropna()`; hedef aynı tarihlerdeki
     `train`.
   - `LinearRegression` kur ve `X.loc[future_index]` için tahmin döndür.
2. 13 deneyde iki sürümü çalıştır: `calendar=True` ve `calendar=False`. Her
   deneyde test, kesimden sonraki 28 gün.
3. Her sürüm için ortalama MAE'yi ve en kötü deneyi iki ondalıkla
   `ad ortalama en_kötü` biçiminde alt alta yazdır (adlar: `with calendar`,
   `without`).
4. Takvimli sürümün mevsimsel naife (13 deneyde 17.95) göre becerisini iki
   ondalıkla yazdır.

**Beklenen çıktı:**

```
with calendar 10.64 16.93
without 18.98 41.35
0.41
```

Takvimli doğrusal model hatayı 10.6'ya indiriyor: aynı takvim bilgisini alan
ARIMA ile (10.23) başa baş. Takvimsiz sürüm ise mevsimsel naiften **kötü**.
Aynı model, aynı veri; fark yalnızca modele ne söylediğin. Gelecek satırlarını
`NaN` olarak ekleyip özellikleri tek seferde kurmak, eğitim ve tahmin
özelliklerinin aynı kodla üretilmesini sağlıyor: ikisi ayrışırsa en zor
bulunan hatalar oradan çıkar.
