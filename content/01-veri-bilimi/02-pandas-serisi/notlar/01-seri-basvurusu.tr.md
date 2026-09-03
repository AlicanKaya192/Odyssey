`import pandas as pd` yapıldığı varsayılıyor.

## Oluşturma

| Yazım | Ne yapar |
|---|---|
| `pd.Series([1, 2, 3])` | Listeden seri; index 0, 1, 2 |
| `pd.Series([1, 2], index=["a", "b"])` | Etiketli index |
| `pd.Series({"a": 1, "b": 2})` | Sözlükten; anahtarlar index oluyor |
| `pd.Series(5, index=["a", "b"])` | Hepsi aynı değer |
| `pd.Series(numpy_dizisi)` | NumPy dizisinden |

## Özellikler

| Yazım | Ne verir |
|---|---|
| `s.index` | Etiketler |
| `s.values` | Değerler (NumPy dizisi olarak) |
| `s.dtype` | Değerlerin tipi |
| `s.size` | Toplam hücre sayısı (**boşlar dâhil**) |
| `s.count()` | **Dolu** hücre sayısı |
| `s.name` | Serinin adı |
| `s.empty` | Boş mu |

`size` ile `count()` farklıysa eksik değer var demektir. Bu, bir seriye
bakarken ilk kontrol edilecek şey.

## Seçim

| Yazım | Ne seçer |
|---|---|
| `s["Ada"]` | Etikete göre tek değer |
| `s[["Ada", "Mina"]]` | Birden fazla etiket |
| `s.iloc[0]` | **Sıraya** göre ilk eleman |
| `s.iloc[1:3]` | Sıraya göre dilim |
| `s.loc["Ada"]` | Etikete göre (açık hâli) |
| `s[s > 80]` | Koşula göre |
| `s.head(3)` / `s.tail(3)` | İlk / son üç |

Index sayılardan oluşuyorsa `s[0]` kafa karıştırıyor: etiket mi sıra mı?
Bu yüzden `loc` (etiket) ve `iloc` (sıra) ayrımı var — bir sonraki bölümün
konusu.

## Toplulaştırma

| Yazım | Ne verir |
|---|---|
| `s.sum()` | Toplam |
| `s.mean()` | Ortalama |
| `s.median()` | Medyan |
| `s.std()` | Standart sapma |
| `s.min()` / `s.max()` | Uçlar |
| `s.idxmin()` / `s.idxmax()` | En küçüğün / en büyüğün **etiketi** |
| `s.describe()` | Sekiz sayı birden |
| `s.cumsum()` | Yürüyen toplam |

**Hepsi eksik değerleri atlıyor.** NumPy'da öyle değildi; oradaki `mean()`
tek bir `nan` yüzünden `nan` veriyordu.

NumPy'ın `argmax`'i sıra veriyordu, pandas'ın `idxmax`'i **etiket** veriyor:
`scores.idxmax()` sana doğrudan en yüksek notu alanın adını söylüyor.

## Eksik değerler

| Yazım | Ne yapar |
|---|---|
| `s.isna()` | Hangi hücreler boş (`True`/`False`) |
| `s.notna()` | Tersi |
| `s.isna().sum()` | Kaç tane boş |
| `s.dropna()` | Boşları atılmış **yeni seri** |
| `s.fillna(0)` | Boşlar sıfırla dolu **yeni seri** |
| `s.fillna(s.mean())` | Ortalamayla doldurulmuş |
| `s.ffill()` | Boşluğu bir üstteki değerle doldur |
| `s.bfill()` | Bir alttaki değerle doldur |

`fillna` ve `dropna` özgün seriyi **değiştirmiyor**; sonucu bir değişkene
almazsan kayboluyor.

Eski belgelerde `fillna(method="ffill")` yazımını görebilirsin; **pandas
3.0'da kaldırıldı**, artık `ffill()` ve `bfill()` ayrı metotlar.

## Kategorik değerler

| Yazım | Ne verir |
|---|---|
| `s.value_counts()` | Her değerden kaç tane, çoktan aza |
| `s.value_counts(normalize=True)` | Aynısı ama oran olarak |
| `s.unique()` | Tekrarsız değerler, **görülme sırasıyla** |
| `s.nunique()` | Kaç farklı değer |
| `s.isin(["Ankara", "Izmir"])` | Listedekilerden biri mi |

`np.unique` sıralıyordu, `Series.unique()` **sıralamıyor** — ilk görülme
sırasını koruyor. İki kütüphanenin aynı adlı iki fonksiyonu farklı
davranıyor.

## Dönüşüm ve sıralama

| Yazım | Ne yapar |
|---|---|
| `s.astype(int)` | Tip değiştirir |
| `s.sort_values()` | Değere göre sıralı **yeni seri** |
| `s.sort_values(ascending=False)` | Büyükten küçüğe |
| `s.sort_index()` | Etikete göre sıralı |
| `s.tolist()` | Python listesine çevirir |
| `s.to_dict()` | Sözlüğe çevirir |
| `s.reset_index(drop=True)` | Index'i 0'dan yeniden numaralar |

## Her elemana bir işlem

| Yazım | Ne yapar |
|---|---|
| `s * 2` | Vektörel — en hızlısı, tercih edilen |
| `s.apply(fonksiyon)` | Her elemana fonksiyonu uygular |
| `s.map({"a": 1, "b": 2})` | Sözlükle değer değiştirir |
| `s.round(2)` | Yuvarlar |

`apply` esnek ama yavaş: arkada Python döngüsü dönüyor. Vektörel bir
karşılığı varsa onu kullan.

## Metin serileri

| Yazım | Ne yapar |
|---|---|
| `s.str.lower()` | Hepsini küçük harfe |
| `s.str.strip()` | Baştaki ve sondaki boşlukları atar |
| `s.str.contains("An")` | İçeriyor mu |
| `s.str.len()` | Uzunluklar |
| `s.str.split(",")` | Böler |

`.str` olmadan çalışmıyor: `s.lower()` diye bir şey yok, çünkü `s` bir metin
değil, metinlerden oluşan bir seri.
