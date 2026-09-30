## Denetim listesi

```python
raw["date"].is_monotonic_increasing        # sirali mi?
raw["date"].duplicated().sum()             # ayni tarih birden cok mu?
raw["sales"].isna().sum()                  # acik eksik
(raw["sales"] <= 0).sum()                  # kilik degistirmis eksik olabilir

full = raw.groupby("date")["sales"].sum().asfreq("D")
full.isna().sum()                          # gercek eksik sayisi
full.isna().mean()                         # eksik orani
```

Beklenen satır sayısını kendin hesapla ve karşılaştır:
`len(pd.date_range(start, end, freq="D"))`.

## Yöntemler

| Yöntem | Kod | Ne zaman | Risk |
|---|---|---|---|
| Sıfır | `fillna(0)` | Eksik = gerçekten sıfır (kapalı gün) | Bilinmeyeni sıfır saymak |
| Son değer | `ffill()` | Değer değişene kadar geçerli (fiyat, stok, durum) | Mevsimi siler; uzun boşlukta bayat |
| Sonraki değer | `bfill()` | Yalnızca serinin başını doldururken | Geleceği kullanır |
| Doğrusal | `interpolate()` | Yavaş ve düzgün değişen ölçüm (sıcaklık) | Mevsimi siler; geleceği kullanır |
| Zamana göre | `interpolate(method="time")` | Düzensiz aralıklı indeks | Aynı |
| Geçen mevsim | `fillna(s.shift(m))` | Mevsimsel seri | Trend varsa biraz düşük kalır |
| İki mevsimin ortalaması | `shift(m)` ve `shift(-m)` ortalaması | Mevsimsel seri, geçmişi temizlerken | Geleceği kullanır |
| Mevsim konumu ortalaması | `groupby(...).transform("mean")` | Trendsiz mevsimsel seri | Trendi yok sayar |
| Hareketli ortanca | `fillna(s.rolling(7, center=True, min_periods=1).median())` | Gürültülü, mevsimsiz | Geleceği kullanır |
| Model | STL / ARIMA ile | Uzun ya da çok sayıda boşluk | Karmaşık; aşırı güven |

`interpolate()` varsayılan olarak satırları **eşit aralıklı** sayar. İndeks
düzensizse `method="time"` gerçek zaman farkını kullanır.

## `limit` ve kısa boşluk kalıbı

```python
s.ffill(limit=2)                     # her bosluktan en cok 2 hucre
s.interpolate(limit=3)               # ayni; uzun boslugun ilk 3'unu de doldurur
s.interpolate(limit_area="inside")   # yalnizca iki dolu deger arasini
```

"Yalnızca `n` ya da daha kısa boşlukları doldur":

```python
missing = s.isna()
run_id = (missing != missing.shift()).cumsum()
run_length = missing.groupby(run_id).transform("sum")

short = missing & (run_length <= n)
result = s.where(~short, s.interpolate())
```

## Geriye bakan ve ileriye bakan

| Geriye bakan (sızıntı yok) | İki yöne bakan (geleceği kullanır) |
|---|---|
| `ffill()` | `bfill()` |
| `fillna(s.shift(m))` | `interpolate()` |
| Geriye dönük `rolling(...).mean()` | `center=True` pencereler |
| | `shift(-m)` içeren her şey |

Geçmiş bir raporu temizlerken iki yöne bakmak serbest ve daha isabetli. Bir
tahmin modelini sınarken (Bölüm 15) yalnızca sol sütun.

## Toplamlar ve ortalamalar

`sum()` ve `mean()` `NaN`'ı **atlar**. Sonuç:

- Eksik günü olan bir ayın **toplamı** düşük çıkar (eksik gün sıfır sayılmış
  gibi).
- **Ortalama** ise yalnızca mevcut günlerden hesaplanır; eksik günler rastgele
  değilse (hep pazar eksikse) yanlı olur.

Yeniden örneklerken eksik günü olan dönemi boş bırakmak için:

```python
monthly = full.resample("MS").sum(min_count=28)
```

`min_count`: dönemde en az bu kadar dolu değer yoksa sonuç `NaN`.

## İşaretleme

```python
frame = pd.DataFrame({
    "sales": filled,
    "was_missing": full.isna(),
})

frame["was_missing"].groupby(frame.index.month).sum()     # ay basina doldurulan
frame.loc[~frame["was_missing"], "sales"].mean()          # yalnizca gercek gunler
```

Makine öğrenmesi modelinde (Bölüm 19) `was_missing` bir özellik olarak da
verilebilir: eksikliğin kendisi bilgi taşıyabilir.

## Ne zaman doldurma

- Boşluk, mevsimin boyundan uzunsa ve elinde yalnızca bir iki tur veri varsa.
- Verinin %5–10'undan fazlası eksikse.
- Eksik olan, tahmin etmeye çalıştığın **hedefin** kendisiyse ve o dönemde
  modeli değerlendireceksen.
- Eksikliğin nedeni bilinmiyorsa: önce nedeni bul.

Bu durumlarda seçenekler: boşluğu bırakıp onu kabul eden yöntem kullanmak
(statsmodels'in durum uzayı modelleri `NaN`'ı kendisi ele alır), daha kaba
sıklığa geçmek, ya da seriyi boşluğun sonrasından başlatmak.
