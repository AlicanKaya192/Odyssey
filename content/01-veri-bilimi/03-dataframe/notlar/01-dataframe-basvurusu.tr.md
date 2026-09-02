# DataFrame Başvurusu

`import pandas as pd` yapıldığı varsayılıyor. `data` bir DataFrame.

## Oluşturma

| Yazım | Ne yapar |
|---|---|
| `pd.DataFrame({"a": [1, 2], "b": [3, 4]})` | Sözlükten; anahtarlar sütun adı |
| `pd.DataFrame([{"a": 1}, {"a": 2}])` | Sözlük listesinden; her sözlük bir satır |
| `pd.DataFrame(liste, columns=["a", "b"])` | Liste listesinden |
| `pd.read_csv("dosya.csv")` | CSV dosyasından |
| `series.to_frame()` | Seriden tek sütunlu tablo |

## İlk bakış

| Yazım | Ne verir |
|---|---|
| `data.shape` | `(satır, sütun)` |
| `len(data)` | Satır sayısı |
| `data.columns` | Sütun adları |
| `data.index` | Satır etiketleri |
| `data.dtypes` | Her sütunun tipi |
| `data.head(5)` / `data.tail(5)` | İlk / son satırlar |
| `data.info()` | Sütun, tip, dolu sayısı, bellek — hepsi bir arada |
| `data.describe()` | Sayısal sütunların özeti |
| `data.sample(3)` | Rastgele üç satır |

`info()` bir veriyi ilk açtığında en çok işe yarayan çağrı: eksik değerleri
ve yanlış tipleri tek ekranda gösteriyor.

## Sütun seçmek

| Yazım | Ne döndürür |
|---|---|
| `data["score"]` | **Seri** |
| `data[["score"]]` | Tek sütunlu **DataFrame** |
| `data[["name", "score"]]` | İki sütunlu DataFrame |
| `data.select_dtypes("number")` | Yalnızca sayısal sütunlar |

## Sütun eklemek ve çıkarmak

| Yazım | Ne yapar |
|---|---|
| `data["yeni"] = data["a"] + data["b"]` | Hesaplanmış sütun ekler |
| `data["sabit"] = 0` | Sabit değerli sütun ekler |
| `data.drop(columns=["a"])` | Sütun atılmış **yeni tablo** |
| `data.rename(columns={"a": "b"})` | Sütun adı değiştirilmiş yeni tablo |
| `data.columns = ["x", "y"]` | Bütün adları değiştirir (yerinde) |

## Satır işlemleri

| Yazım | Ne yapar |
|---|---|
| `data.sort_values("score")` | Bir sütuna göre sıralı yeni tablo |
| `data.sort_values("score", ascending=False)` | Büyükten küçüğe |
| `data.sort_values(["city", "score"])` | Önce şehre, sonra nota göre |
| `data.drop_duplicates()` | Tekrar eden satırları atar |
| `data.reset_index(drop=True)` | Index'i 0'dan numaralar |
| `data.set_index("name")` | Bir sütunu index yapar |

## Index

| Yazım | Ne yapar |
|---|---|
| `data.set_index("name")` | `name` sütunu index olur |
| `data.reset_index()` | Index sütuna döner |
| `data.reset_index(drop=True)` | Index atılır, yenisi 0'dan |
| `data.index.name` | Index'in adı |

Index satırların adı. Sıralamada, filtrelemede ve birleştirmede satırların
kimliğini o taşıyor.

## Toplulaştırma

| Yazım | Ne verir |
|---|---|
| `data["score"].mean()` | Tek sütunun ortalaması |
| `data.mean(numeric_only=True)` | Her sayısal sütunun ortalaması |
| `data.sum(numeric_only=True)` | Toplamlar |
| `data["score"].max()` | En büyük değer |
| `data["score"].idxmax()` | En büyüğün **satır etiketi** |
| `data.loc[data["score"].idxmax()]` | En yüksek notu alan **satırın tamamı** |
| `data.count()` | Sütun başına dolu hücre sayısı |
| `data.nunique()` | Sütun başına farklı değer sayısı |

Son ikisi eksik veriyi ve kategorik sütunları görmenin hızlı yolu.

## Eksik değerler

| Yazım | Ne yapar |
|---|---|
| `data.isna()` | Hücre hücre `True`/`False` |
| `data.isna().sum()` | **Sütun başına** kaç eksik |
| `data.dropna()` | Eksik içeren satırları atar |
| `data.dropna(subset=["score"])` | Yalnızca o sütuna bakarak atar |
| `data.fillna(0)` | Bütün boşlukları doldurur |
| `data.fillna({"score": 0})` | Sütun sütun farklı değerle doldurur |

`data.isna().sum()` bir veriyi ilk açtığında yazılan ikinci çağrı — hangi
sütunda ne kadar boşluk olduğunu tek bakışta gösteriyor.

## Tip dönüşümü

| Yazım | Ne yapar |
|---|---|
| `data["a"].astype(int)` | Tamsayıya çevirir (**kırpar**, yuvarlamaz) |
| `data["a"].astype(float)` | Ondalığa çevirir |
| `data["a"].astype(str)` | Metne çevirir |
| `pd.to_numeric(data["a"], errors="coerce")` | Çevrilemeyenleri `NaN` yapar |
| `pd.to_datetime(data["date"])` | Tarihe çevirir |

`to_numeric` CSV'den gelen kirli sayı sütunlarında kurtarıcı: bozuk
değerleri patlamak yerine `NaN` yapıyor, sen de onları sayabiliyorsun.

## Kaydetme

| Yazım | Ne yapar |
|---|---|
| `data.to_csv("out.csv", index=False)` | CSV'ye yazar |
| `data.to_dict("records")` | Sözlük listesine çevirir |
| `data.values` | NumPy dizisine çevirir |

`index=False` demezsen dosyaya bir de index sütunu yazılıyor ve dosyayı
tekrar okuduğunda `Unnamed: 0` diye bir sütun çıkıyor.
