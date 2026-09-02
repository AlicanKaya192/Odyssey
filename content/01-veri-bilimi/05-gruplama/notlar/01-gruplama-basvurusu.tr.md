# Gruplama Başvurusu

`data` bir DataFrame.

## Temel gruplama

| Yazım | Ne verir |
|---|---|
| `data.groupby("city")["score"].mean()` | Şehir başına ortalama — seri |
| `data.groupby("city")["score"].sum()` | Toplam |
| `data.groupby("city")["score"].count()` | **Dolu** hücre sayısı |
| `data.groupby("city").size()` | **Bütün** satır sayısı |
| `data.groupby("city")["score"].min()` / `.max()` | Uçlar |
| `data.groupby("city")["score"].median()` | Medyan |
| `data.groupby("city")["score"].std()` | Standart sapma |
| `data.groupby("city")["name"].nunique()` | Grup başına farklı değer |
| `data.groupby("city")["score"].first()` / `.last()` | İlk / son satır |

Gruplar **alfabetik sıralanıyor**. Sonuç sıralamasını değiştirmek için
`sort=False` verebiliyorsun; büyük veride biraz hızlandırıyor.

## Birden fazla hesap

| Yazım | Ne verir |
|---|---|
| `.agg(["count", "mean", "max"])` | Üç sütunlu tablo |
| `.agg(kisi=("name", "count"), ort=("score", "mean"))` | Adlandırılmış sütunlar |
| `.agg({"score": "mean", "age": "max"})` | Sütun başına farklı hesap |
| `.describe()` | Grup başına sekiz sayı |

Adlandırılmış biçim (`yeni_ad=("sütun", "hesap")`) rapor üretirken en
okunaklısı.

## Birden fazla anahtar

| Yazım | Ne verir |
|---|---|
| `data.groupby(["city", "grade"])["score"].mean()` | Çok seviyeli index |
| `... .reset_index()` | Seviyeleri sütuna çevirir |
| `... .unstack()` | İkinci anahtarı sütun yapar (pivot gibi) |
| `data.groupby("city", as_index=False)` | Anahtar sütun olarak kalır |

## Pivot tablo

| Yazım | Ne yapar |
|---|---|
| `pivot_table(index="city", columns="grade", values="score")` | Varsayılan hesap: ortalama |
| `..., aggfunc="sum"` | Hesabı değiştirir |
| `..., aggfunc=["mean", "count"]` | Birden fazla hesap |
| `..., fill_value=0` | Boş hücreleri doldurur |
| `..., margins=True` | Satır ve sütun toplamlarını ekler |

`pivot_table` ile `groupby(...).unstack()` aynı sonucu veriyor; ilki daha
okunaklı.

## Grup sonucuyla çalışmak

Sonuç bir seri ya da tablo; seride öğrendiğin her şey geçerli.

| Yazım | Ne yapar |
|---|---|
| `.sort_values(ascending=False)` | Büyükten küçüğe sıralar |
| `.idxmax()` | En yüksek değerli **grubun adı** |
| `.head(3)` | İlk üç grup |
| `.round(2)` | Yuvarlar |
| `.to_dict()` | Sözlüğe çevirir |
| `.reset_index()` | Normal tabloya çevirir |

## transform ve filter

| Yazım | Ne yapar |
|---|---|
| `data.groupby("city")["score"].transform("mean")` | Grup ortalamasını **her satıra** yazar |
| `data.groupby("city")["score"].transform("rank")` | Grup içi sıra |
| `data.groupby("city").filter(lambda g: len(g) > 2)` | Yalnızca büyük grupların satırları |

`transform` tabloyu **aynı boyda** bırakıyor; `agg` küçültüyor. Grup
ortalamasıyla satırı karşılaştıracaksan `transform` gerekiyor.

## Sayma kalıpları

```python
# Her kategoriden kac tane
data["city"].value_counts()

# Ayni sey groupby ile
data.groupby("city").size()

# Iki kategorinin kesisimi
data.groupby(["city", "grade"]).size()

# Kategori basina yuzde
data["city"].value_counts(normalize=True) * 100
```

`value_counts()` tek sütun için daha kısa; `groupby` başka hesaplar da
gerektiğinde.

## Sık kullanılan kalıplar

```python
# En yuksek ortalamali sehir
data.groupby("city")["score"].mean().idxmax()

# Grup basina en iyi kisi
data.loc[data.groupby("city")["score"].idxmax()]

# Grup ortalamasinin ustundekiler
mean_by_city = data.groupby("city")["score"].transform("mean")
data[data["score"] > mean_by_city]

# Rapor tablosu
data.groupby("city").agg(
    kisi=("name", "count"),
    ortalama=("score", "mean"),
    en_yuksek=("score", "max"),
).round(1).sort_values("ortalama", ascending=False)
```

İkinci kalıp işe yarıyor: `idxmax()` grup başına birer **satır etiketi**
veriyor, `loc` de o satırların tamamını getiriyor.

## Eksik değerler

| Durum | Davranış |
|---|---|
| Anahtar sütunu eksikse | Satır **hiçbir gruba girmiyor**, sessizce düşüyor |
| `dropna=False` | Eksik anahtar `NaN` adlı bir grup oluyor |
| Hesaplanan sütun eksikse | `mean` ve `sum` atlıyor, `count` saymıyor |

Gruplamadan önce anahtar sütununda `isna().sum()` çalıştırmak iyi bir
alışkanlık — yoksa toplamın neden tutmadığını uzun süre arıyorsun.
