## 1. Filtreden sonra index delik deşik

```python
data = pd.DataFrame({"name": ["Ada", "Kerem", "Mina"], "score": [82, 74, 91]})
high = data[data["score"] > 80]
print(high.index.tolist())
```

```text
[0, 2]
```

Seçilmeyen satırın numarası **atlanıyor**. Bu bilinçli: hangi satırın
nereden geldiğini kaybetmiyorsun.

Ama iki sonucu var:

- `high.loc[1]` artık `KeyError` veriyor — o etiket yok.
- Başka bir seriyle işlem yaparsan **hizalama** delikli index yüzünden
  beklemediğin `NaN`'lar üretiyor.

Numaraları sıfırlamak istiyorsan: `high.reset_index(drop=True)`.

## 2. `iloc[0]` ile `loc[0]` filtreden sonra farklı şeyler

```python
high.iloc[0]    # her zaman ilk satir
high.loc[0]     # "0" etiketli satir - yoksa KeyError
```

İlk satırı istiyorsan `iloc[0]`. `loc[0]` yalnızca `0` etiketi hâlâ
duruyorsa çalışıyor ve filtre onu atmış olabilir.

**Kural:** "ilk", "son", "üçüncü" diyorsan `iloc`; bir ada ya da koda göre
arıyorsan `loc`.

## 3. Parantezsiz `&`

```python
data[data["score"] > 70 & data["score"] < 90]
```

```text
ValueError: The truth value of a Series is ambiguous.
```

`&` operatörü `>` ve `<` işaretlerinden **önce** çalışıyor, o yüzden pandas
anlamsız bir şeyle karşılaşıyor.

Doğrusu her koşulu parantezle sarmak:

```python
data[(data["score"] > 70) & (data["score"] < 90)]
```

Burada hata alman şanslısın; bazı ifadelerde hata bile vermeden yanlış
sonuç çıkıyor.

## 4. `and` yerine `&`

```python
data[(data["a"] > 1) and (data["b"] < 5)]     # ValueError
data[(data["a"] > 1) & (data["b"] < 5)]       # dogru
```

`and` tek bir doğruluk değeri bekliyor; elinde satır sayısı kadar var.
NumPy'daki sebebin aynısı.

**İstisna:** `query` içinde `and` **çalışıyor**, çünkü orası Python değil:

```python
data.query("a > 1 and b < 5")
```

## 5. Boş sonuç sessizce geçiyor

```python
selected = data[data["score"] > 1000]
print(selected.shape)
print(selected["score"].mean())
```

```text
(0, 2)
nan
```

Hiçbir satır kalmadı ama hata yok. Ortalama `nan` çıkıyor ve raporuna
öyle yazılıyor.

Filtreden sonra kontrol etmek gerekiyor:

```python
if selected.empty:
    ...
```

`len(selected)` ya da `selected.shape[0]` de aynı işi görüyor.

## 6. Filtrelenmiş tablo bir kopya

```python
high = data[data["score"] > 80]
high["score"] = 0
print(data["score"].tolist())
```

```text
[82, 74, 91]
```

Özgün tablo değişmedi. pandas 3.0'da filtre sonucu gerçek bir **kopya**;
onu değiştirmek kaynağı etkilemiyor.

İyi haber gibi ama ters yönde tuzak: özgün tabloyu değiştirmek
istiyorsan filtre sonucuna atamak işe yaramıyor. Tek `loc` çağrısı
gerekiyor:

```python
data.loc[data["score"] > 80, "score"] = 0
```

## 7. Zincirli atama

```python
data[data["score"] > 80]["score"] = 0     # hicbir sey olmaz
data.loc[data["score"] > 80, "score"] = 0 # dogrusu
```

Bir öncekinin aynısı ama tek satırda yazıldığı için fark edilmesi daha zor.
Ara tablo üretiliyor, atama ona gidiyor, o da çöpe atılıyor.

**Kural:** değiştireceksen köşeli parantezi **iki kez üst üste kullanma**.

## 8. `between` iki ucu da alıyor

```python
pd.Series([1, 2, 3]).between(1, 3)
```

```text
[True, True, True]
```

`between(1, 3)` "1 ve 3 dâhil" demek. Python dilimlerine alışkınsan bunu
`1 <= x < 3` sanabiliyorsun.

Ucu dışarıda bırakmak istiyorsan söylemen gerekiyor:

```python
s.between(1, 3, inclusive="left")
```

## 9. `loc` dilimi bitişi içeri alıyor

```python
by_name.loc["Ada":"Mina"]     # Mina dahil
data.iloc[0:3]                # ucuncu satir haric
```

İki farklı kural, iki farklı araç. Aynı sayıda satır verirlerse tesadüf.

`loc` dilimi ayrıca **index sıralı değilse** beklenmedik sonuç veriyor —
sıralanmamış bir index'te "a'dan c'ye" ne demek belirsiz.

## 10. `str` metotları eksik değerlerde

```python
pd.Series(["Ada", None]).str.contains("A")
```

```text
[True, False]
```

Eksik değer `False` sayılıyor ve filtreden düşüyor. Çoğu zaman istediğin
bu, ama "eksik olanları da göreyim" diyorsan onları ayrıca kontrol etmen
gerekiyor:

```python
mask = data["name"].str.contains("A") | data["name"].isna()
```

## 11. Büyük/küçük harf birebir eşleşiyor

```python
data[data["city"] == "ankara"]     # bos doner
data[data["city"] == "Ankara"]     # dogru
```

Gerçek veride aynı şehir üç farklı yazımla geliyor. Karşılaştırmadan önce
tekilleştirmek iyi bir alışkanlık:

```python
data["city"] = data["city"].str.strip().str.title()
```

Ya da karşılaştırmayı harf duyarsız yapmak:

```python
data[data["city"].str.lower() == "ankara"]
```

## 12. `nlargest` beraberlikte ilkini alıyor

```python
data.nlargest(2, "score")
```

İki satırın notu aynıysa hangisinin geleceği **tabloya giriş sırasına**
bağlı. Sonuç kararlı ama "adil" değil.

Beraberliği kendin çözmek istiyorsan ikinci bir ölçüt veriyorsun:

```python
data.sort_values(["score", "age"], ascending=[False, True]).head(2)
```
