# Keşif Başvurusu

`import pandas as pd` yapıldığı ve tablonun `data` olduğu varsayılıyor.

## Sıra

| Adım | Çağrı | Ne sorar |
|---|---|---|
| 1 | `data.shape` | Kaç satır, kaç sütun |
| 2 | `data.dtypes` | Her sütun beklenen tipte mi |
| 3 | `data.head()` | İçeride gerçekte ne var |
| 4 | `data.isna().sum()` | Nerede boşluk var |
| 5 | `data.describe()` | Sayısal sütunların özeti |
| 6 | `data["sutun"].value_counts()` | Kategoriler dengeli mi |
| 7 | `data.groupby(...)` | Gruplar birbirinden farklı mı |
| 8 | `data.corr()` | Sütunlar birlikte mi hareket ediyor |

## İlk bakış

| Yazım | Ne verir |
|---|---|
| `data.shape` | `(satır, sütun)` demeti |
| `data.columns.tolist()` | Sütun adları |
| `data.dtypes.astype(str).tolist()` | Tipler, okunur liste hâlinde |
| `data.head(5)` / `data.tail(5)` | İlk / son beş satır |
| `data.sample(5)` | Rastgele beş satır |
| `len(data)` | Satır sayısı |

`sample()` `head()`'den daha dürüst bir bakış: veri tarihe göre sıralıysa
ilk beş satır yalnızca en eski kayıtları gösteriyor.

## Eksik değerler

| Yazım | Ne verir |
|---|---|
| `data.isna().sum()` | Sütun başına boş sayısı |
| `data.isna().sum().sum()` | Toplam boş sayısı |
| `data.isna().any(axis=1).sum()` | En az bir boşluğu olan satır sayısı |
| `(data.isna().mean() * 100).round(1)` | Sütun başına boş yüzdesi |
| `data.dropna(subset=["score"])` | Belirli sütunda boşu olan satırları at |

Yüzde, sayıdan daha anlamlı: 100 satırda 20 boş ile 100.000 satırda 20 boş
aynı şey değil.

## Sayısal özet

| Yazım | Ne verir |
|---|---|
| `data.describe()` | Sekiz satırlık özet tablo |
| `data["s"].mean()` / `.median()` | Ortalama / medyan |
| `data["s"].std()` | Standart sapma |
| `data["s"].quantile(0.25)` | Birinci çeyrek |
| `data["s"].min()` / `.max()` | Uçlar |
| `data["s"].idxmax()` | En büyüğün **etiketi** |
| `data["s"].skew()` | Çarpıklık; 0 simetrik |

`describe()` okunurken:

| Görülen | Anlamı |
|---|---|
| `mean` ile `50%` uzak | Dağılım çarpık, uç değer var |
| `std` küçük | Değerler birbirine yakın |
| `std` büyük | Yayılım geniş; iki farklı grup olabilir |
| `min` ya da `max` saçma | Veri hatası ya da farklı birim |
| `count` satır sayısından az | O sütunda eksik var |

## Kategorik özet

| Yazım | Ne verir |
|---|---|
| `data["c"].value_counts()` | Her değerden kaç tane |
| `data["c"].value_counts(normalize=True)` | Oran olarak |
| `data["c"].nunique()` | Kaç farklı değer |
| `data["c"].unique()` | Değerlerin kendisi |
| `data["c"].value_counts().head(10)` | En sık on değer |

`nunique()` satır sayısına eşitse o sütun bir kimlik (id) sütunudur;
gruplamada işe yaramıyor.

## Gruplar

| Yazım | Ne verir |
|---|---|
| `data.groupby("c")["s"].mean()` | Grup ortalamaları |
| `data.groupby("c")["s"].agg(["count", "mean"])` | **Birlikte** — doğru kullanım |
| `data.groupby("c")["s"].agg(["count", "mean", "std"])` | Yayılımla birlikte |
| `data.groupby(["c1", "c2"])["s"].mean()` | İki kırılım |
| `data.groupby("c")["s"].median()` | Aykırı değer varken |

**`count` olmadan ortalama okunmuyor.** Kaç kişiden hesaplandığını
bilmeden ortalama bir bilgi değil.

## İlişki

| Yazım | Ne verir |
|---|---|
| `data["a"].corr(data["b"])` | İki sütun arasında tek sayı |
| `data.corr(numeric_only=True)` | Bütün sayısal sütunların matrisi |
| `data.corr(numeric_only=True).round(2)` | Okunur hâli |
| `data.plot(kind="scatter", x="a", y="b")` | Gözle bakmak |

Korelasyonu okurken kaba bir ölçek:

| Değer | Yorum |
|---|---|
| 0.0 - 0.3 | Zayıf ya da yok |
| 0.3 - 0.7 | Orta |
| 0.7 - 1.0 | Güçlü |

İşaret yönü söylüyor: `-0.8` de güçlü, ters yönde.

**Korelasyona bakmadan önce dağılım grafiğine bak.** Eğri bir ilişki
varsa korelasyon 0 çıkabiliyor ve "ilişki yok" sanılıyor.

## Aykırı değerler

```python
q1 = data["score"].quantile(0.25)
q3 = data["score"].quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

outliers = data[(data["score"] < low) | (data["score"] > high)]
```

| Yazım | Ne yapar |
|---|---|
| `data["s"].quantile(0.25)` | Birinci çeyrek |
| `data["s"].nlargest(5)` | En büyük beş |
| `data["s"].nsmallest(5)` | En küçük beş |
| `ax.boxplot(data["s"])` | Kutu grafiği — aykırıları gösteriyor |

`nlargest` aykırıyı gözle görmenin en hızlı yolu: uçtaki değerler
diğerlerinden kopuksa fark ediliyor.

## Kırılım tabloları

| Yazım | Ne verir |
|---|---|
| `pd.crosstab(data["c1"], data["c2"])` | İki kategorinin çapraz sayımı |
| `pd.cut(data["age"], bins=[20, 30, 40, 60])` | Sayıyı aralığa çevirir |
| `data.pivot_table(values="s", index="c1", columns="c2")` | Özet tablo |

`pd.cut` sürekli bir sütunu kategoriye çeviriyor; yaş yerine yaş aralığıyla
gruplamak çoğu zaman daha okunaklı.

## Kontrol listesi

- [ ] Kaç satır, kaç sütun?
- [ ] Tipler doğru mu?
- [ ] Eksik değer var mı, yüzde kaç?
- [ ] `describe`'da ortalama ile medyan uzak mı?
- [ ] `min`/`max` mantıklı mı?
- [ ] Kategoriler dengeli mi?
- [ ] Gruplar arasında fark var mı — ve grup büyüklükleri ne?
- [ ] Sütunlar birlikte mi hareket ediyor?
- [ ] Aykırı değer var mı, sebebi ne?
- [ ] Bulguyu tek cümleyle nasıl yazarım?
