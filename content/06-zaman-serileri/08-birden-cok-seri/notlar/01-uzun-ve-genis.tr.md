## İki biçim arasında

```python
wide = long.pivot(index="date", columns="store", values="sales")     # uzun -> genis
long = wide.reset_index().melt(id_vars="date", var_name="store",
                               value_name="sales").dropna()         # genis -> uzun
```

| Araç | Ne zaman |
|---|---|
| `pivot` | Her (tarih, seri) çifti **en fazla bir kez** geçiyorsa |
| `pivot_table(..., aggfunc="sum")` | Çiftler tekrar ediyorsa; tekrarları özetliyor |
| `melt` | Geniş tabloyu uzuna çevirmek |
| `stack()` / `unstack()` | İndeks seviyeleriyle aynı iş |

`pivot` tekrarlanan çift görünce hata veriyor
(`Index contains duplicate entries`). Bu iyi bir şey: Bölüm 03'teki tekrar
sorunu burada kendini belli ediyor. Tekrarları önce çöz ya da bilerek
`pivot_table` kullan.

`melt` sonrası `dropna()`: geniş tablodaki `NaN` hücreler uzun tabloda boş
satır oluyor; çoğu zaman istenmiyor.

## Hangi biçim ne için

| İş | Uzun | Geniş |
|---|---|---|
| Dosyaya yazmak, veritabanı | ✓ | |
| Seri sayısı çok ya da değişken | ✓ | |
| Seri başına ek sütun (fiyat, stok) | ✓ | |
| Makine öğrenmesi için özellik tablosu | ✓ | |
| Serileri karşılaştırmak, korelasyon | | ✓ |
| Çizmek (her seri bir çizgi) | | ✓ |
| Seriler arası toplam, pay, sıra | | ✓ |
| Eksikleri görmek | | ✓ |

## Uzun biçimde seri başına işlemler

```python
g = long.groupby("store")["sales"]

long["lag1"] = g.shift(1)
long["lag7"] = g.shift(7)
long["change"] = g.diff()
long["growth"] = g.pct_change()
long["ytd"] = g.cumsum()
long["ma7"] = g.transform(lambda x: x.rolling(7).mean())
long["safe_ma7"] = g.transform(lambda x: x.shift(1).rolling(7).mean())
long["z"] = g.transform(lambda x: (x - x.mean()) / x.std())
```

**Önce sırala.** Bu işlemler her grubun içinde satır sırasına göre çalışıyor:
`long = long.sort_values(["store", "date"])`.

**`shift(7)` satır sayıyor.** C mağazasının pazar satırları yok; onun
`shift(7)`'si 7 gün değil 7 **açık gün** geriye gidiyor (8 takvim günü).
Takvime göre gecikme için önce her mağazayı tam takvime oturt:

```python
full = (long.set_index("date").groupby("store")["sales"]
        .apply(lambda x: x.asfreq("D")).reset_index())
```

## Seri başına yeniden örnekleme

```python
long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()
long.groupby(["store", pd.Grouper(key="date", freq="ME")])["sales"].agg(["sum", "mean"])
long.set_index("date").groupby("store")["sales"].resample("W").sum()
```

İlk ve üçüncü satır aynı sonucu veriyor. Tarih bir sütunsa `Grouper(key=...)`,
indeksteyse `resample`.

## Geniş biçimde seriler arası işlemler

```python
wide.sum(axis=1)                          # her gun: serilerin toplami
wide.mean(axis=1)                         # her gun: serilerin ortalamasi
wide.div(wide.sum(axis=1), axis=0)        # her gun: pay
wide.rank(axis=1, ascending=False)        # her gun: sira
wide.idxmax(axis=1)                       # her gun: en yuksek seri
wide.corr()                               # seriler arasi korelasyon
wide / wide.iloc[0] * 100                 # ilk gune gore endeks
wide.sub(wide.mean(axis=1), axis=0)       # gunluk ortalamadan sapma
```

`axis=1` "satır boyunca, sütunlar arasında" demek. `div` ve `sub` içinde
`axis=0` "her satırı kendi değeriyle" anlamına geliyor.

## Toplarken eksikler

| İfade | `NaN` olan seri |
|---|---|
| `wide.sum(axis=1)` | Atlanıyor (0 gibi) |
| `wide.sum(axis=1, min_count=4)` | Dört seri de yoksa sonuç `NaN` |
| `wide.mean(axis=1)` | Atlanıyor; ortalama **mevcut serilerin** |
| `wide.dropna().sum(axis=1)` | Yalnızca bütün serilerin olduğu günler |

Seri sayısı zamanla değişiyorsa toplam da ortalama da **karşılaştırılabilir
değil.** İki dürüst yol: sabit bir seri kümesiyle çalışmak ya da "mağaza
başına ortalama" gibi seri sayısından bağımsız bir ölçü kullanmak.

## Hiyerarşi

Seriler çoğu zaman iç içe: mağaza → şehir → bölge → toplam. Alt düzeylerin
toplamı üst düzeyi vermeli. Her düzey için ayrı tahmin yaparsan tahminler
birbirini tutmuyor (mağaza tahminlerinin toplamı, şehir tahminine eşit
çıkmıyor). Bu sorunun adı **hiyerarşik uzlaştırma**; en basit çözüm en alt
düzeyi tahmin edip yukarı toplamak.
