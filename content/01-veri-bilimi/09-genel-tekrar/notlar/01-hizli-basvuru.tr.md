# Hızlı Başvuru

Bütün modülün tek sayfası. `import numpy as np`, `import pandas as pd` ve
tablonun `data` olduğu varsayılıyor.

## NumPy

| Yazım | Ne yapar |
|---|---|
| `np.array([1, 2, 3])` | Listeden dizi |
| `np.arange(0, 10, 2)` | Adımla üretir |
| `np.linspace(0, 1, 5)` | Kaç parça olduğunu söyleyerek üretir |
| `a.shape` / `a.dtype` / `a.size` | Şekil, tip, eleman sayısı |
| `a.reshape(2, 3)` | Aynı veriyi farklı düzende |
| `a * 2`, `a + b` | Vektörel işlem — döngü yok |
| `a[a > 70]` | Koşullu seçim |
| `a.sum()` / `.mean()` / `.std()` | Toplulaştırma |
| `a.sum(axis=0)` | Sütun yönünde |
| `np.nanmean(a)` | Eksikleri atlayarak ortalama |

Dilim bir **kopya değil**: `a[1:3]` değiştirilirse özgün dizi de değişiyor.
Kopya için `.copy()`.

## Seri

| Yazım | Ne yapar |
|---|---|
| `pd.Series([1, 2], index=["a", "b"])` | Etiketli seri |
| `s["a"]` / `s.iloc[0]` | Etiketle / sırayla |
| `s[s > 80]` | Koşulla |
| `s.value_counts()` | Her değerden kaç tane |
| `s.unique()` / `s.nunique()` | Tekrarsız değerler / sayısı |
| `s.isna().sum()` | Kaç boş |
| `s.fillna(0)` / `s.dropna()` | Doldur / at |
| `s.str.strip()` / `s.str.lower()` | Metin işlemleri |
| `s.apply(fonksiyon)` | Her elemana |

İki seri toplanırken **etikete göre hizalanıyor**, sıraya göre değil.

## DataFrame

| Yazım | Ne yapar |
|---|---|
| `pd.DataFrame({...})` | Sözlükten tablo |
| `pd.read_csv("dosya.csv")` | Dosyadan |
| `data.shape` / `data.columns` / `data.dtypes` | Yapı |
| `data.head()` / `data.tail()` / `data.sample()` | Bakış |
| `data.describe()` | Sayısal özet |
| `data["a"]` | Tek sütun (seri) |
| `data[["a", "b"]]` | Birden çok sütun (tablo) |
| `data["yeni"] = ...` | Yeni sütun |
| `data.drop(columns=["a"])` | Sütun atar |
| `data.rename(columns={"a": "b"})` | Ad değiştirir |
| `data.to_csv("cikti.csv", index=False)` | Kaydeder |

## Seçim ve filtreleme

| Yazım | Ne seçer |
|---|---|
| `data.loc[0, "score"]` | Etiketle satır-sütun |
| `data.iloc[0, 2]` | Sırayla |
| `data.loc[data["score"] > 80]` | Koşulla |
| `data[(data["a"] > 1) & (data["b"] < 5)]` | İki koşul — **parantez şart** |
| `data[data["city"].isin(["Ankara"])]` | Listedekiler |
| `data[data["city"].str.contains("An")]` | Metin içeriyor mu |
| `data.sort_values("score", ascending=False)` | Sıralar |
| `data.nlargest(3, "score")` | En büyük üç |

`and`/`or` çalışmıyor; `&` ve `|` kullanılıyor ve her koşul parantez
içinde.

## Gruplama

| Yazım | Ne verir |
|---|---|
| `data.groupby("c")["s"].mean()` | Grup ortalaması |
| `data.groupby("c")["s"].agg(["count", "mean"])` | **Doğru kullanım** |
| `data.groupby(["c1", "c2"])["s"].mean()` | İki kırılım |
| `data.groupby("c").size()` | Grup büyüklükleri |
| `data.groupby("c")["s"].transform("mean")` | Her satıra kendi grup ortalaması |
| `data.pivot_table(values="s", index="c1", columns="c2")` | Özet tablo |
| `pd.crosstab(data["c1"], data["c2"])` | Çapraz sayım |

## Temizlik

| Yazım | Ne yapar |
|---|---|
| `data.columns.str.strip().str.lower()` | Sütun adları |
| `data["c"].str.strip().str.title()` | Metin tutarlılığı |
| `pd.to_numeric(data["c"], errors="coerce")` | Sayıya çevirir, olmayanı `NaN` yapar |
| `data.duplicated().sum()` | Kaç tekrar |
| `data.drop_duplicates(subset=["id"])` | Tekrarları atar |
| `data.dropna(subset=["score"])` | Belirli sütunda boş olanı atar |
| `data["c"].fillna(data["c"].median())` | Medyanla doldurur |
| `data["c"].replace(999, None)` | Gizli kodu boşa çevirir |

Sıra: **adlar → metin → tip → tekrar → eksik.**

## Görselleştirme

| Yazım | Ne çizer |
|---|---|
| `fig, ax = plt.subplots()` | Tuval ve çizim alanı |
| `ax.bar(x, y)` / `ax.barh(x, y)` | Dikey / yatay çubuk |
| `ax.plot(x, y, marker="o")` | Çizgi |
| `ax.scatter(x, y)` | Dağılım |
| `ax.hist(values, bins=10)` | Histogram |
| `ax.set_title(...)` / `set_xlabel` / `set_ylabel` | Etiketler — **zorunlu** |
| `ax.set_ylim(0, 100)` | Eksen aralığı |
| `fig.savefig("c.png", dpi=150, bbox_inches="tight")` | Kaydeder |
| `plt.close(fig)` | Tuvali kapatır |

Odyssey içinde `matplotlib.use("Agg")` satırı gerekiyor.

| Ne göstereceksin | Hangi grafik |
|---|---|
| Kategorileri karşılaştır | Çubuk |
| Zaman içinde değişim | Çizgi |
| Bir sütunun dağılımı | Histogram |
| İki sütun arasındaki ilişki | Dağılım |

## Keşif sırası

1. `data.shape` — ölçek
2. `data.dtypes` — tipler doğru mu
3. `data.head()` — içeride ne var
4. `data.isna().sum()` — boşluklar
5. `data.describe()` — ortalama, medyan, uçlar
6. `data["c"].value_counts()` — kategoriler dengeli mi
7. `data.groupby(...).agg(["count", "mean"])` — gruplar farklı mı
8. `data.corr(numeric_only=True)` — sütunlar birlikte mi hareket ediyor

## Aykırı değer

```python
q1 = data["score"].quantile(0.25)
q3 = data["score"].quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

outliers = data[(data["score"] < low) | (data["score"] > high)]
```

## Hatırlanacak kurallar

- pandas metotları **yeni bir nesne döndürüyor**; sonucu bir değişkene al.
- Zincirleme atama yerine `loc` ile tek adımda yaz.
- Grup ortalaması `count` olmadan okunmaz.
- Korelasyon nedensellik değil.
- Çubuk grafikte eksen sıfırdan başlar.
- Ham veri korunur, kopyayla çalışılır.
