## 1. Zincirli atama hiçbir şey yapmıyor

```python
data[data["a"] > 1]["b"] = 99
print(data["b"].tolist())
```

```text
[4, 5, 6]
```

Değer değişmedi. `data[data["a"] > 1]` **yeni bir tablo** üretti, atama ona
yapıldı, o tablo da hemen çöpe gitti.

pandas bunu fark ediyor ve `ChainedAssignmentError` uyarısı veriyor — ama
program çökmüyor, sadece istediğin olmuyor.

**Doğrusu tek adımda `loc` ile:**

```python
data.loc[data["a"] > 1, "b"] = 99
print(data["b"].tolist())
```

```text
[4, 99, 99]
```

**Kural:** bir tabloyu değiştirecekseniz köşeli parantezi **iki kez üst üste
kullanmayın**. Seçim ve atama tek bir `loc` çağrısında olmalı.

## 2. Atama kopya üretmiyor

```python
first = pd.DataFrame({"a": [1, 2]})
second = first
second["a"] = [9, 9]
print(first["a"].tolist())
```

```text
[9, 9]
```

`second = first` yeni bir tablo kurmuyor, **aynı tabloya ikinci bir ad**
veriyor. Birini değiştirince öteki de değişiyor.

Gerçek kopya istiyorsan: `second = first.copy()`.

Bu, NumPy'daki dilim/pencere meselesinin DataFrame hâli. Bir fonksiyona
tablo geçirirken de aynı risk var: fonksiyon tabloyu değiştirirse
çağıranın tablosu da değişiyor.

## 3. `data["x"]` ile `data[["x"]]` aynı şey değil

```python
type(data["score"])     # Series
type(data[["score"]])   # DataFrame
```

Tek köşeli parantez **seri**, çift köşeli parantez **tek sütunlu tablo**
veriyor.

Neden önemli: metotları farklı. Seride `str.lower()` var, tabloda yok.
Tabloda `shape` iki değer veriyor, seride bir.

Hangi noktada canını yakıyor: bir fonksiyon seri bekliyorken tablo
verdiğinde ya da tersi. Hata mesajı genelde `AttributeError` oluyor ve neden
olduğunu anlamak zaman alıyor.

## 4. `describe()` metin sütunlarını atlıyor

```python
data.describe()
```

Çıktıda yalnızca sayısal sütunlar var. İlk bakışta "sütunlarımın yarısı
kayboldu" gibi görünüyor ama kayıp yok — metin sütununun ortalaması diye
bir şey olmadığı için dışarıda bırakılıyor.

Metin sütunlarını da görmek istersen:

```python
data.describe(include="all")
```

Aynı sebeple `data.mean()` doğrudan çalışmıyor:

```text
TypeError: Cannot perform reduction 'mean' with string dtype
```

`data.mean(numeric_only=True)` demen gerekiyor.

## 5. `len(data)` satır sayısı, `data.size` hücre sayısı

```python
len(data)      # 3   satir
data.size      # 6   hucre (3 x 2)
data.shape     # (3, 2)
```

`size` NumPy'dan gelen bir isim ve **toplam hücre** demek. Satır sayısı
istiyorsan `len(data)` ya da `data.shape[0]`.

Serideyken `size` satır sayısıydı; tabloda anlamı değişiyor. Aynı adın iki
yapıda farklı davranması karıştırıyor.

## 6. Boş tabloda ortalama `nan`

```python
empty = data[data["score"] > 1000]
print(empty.shape)
print(empty["score"].mean())
```

```text
(0, 3)
nan
```

Filtre hiçbir satır bırakmadıysa hesaplar `nan` veriyor, hata değil.
Rapora `nan` yazmamak için filtreden sonra `shape[0]` ya da `empty` ile
kontrol etmek gerekiyor.

## 7. Sütun adlarındaki boşluklar

```python
list(pd.DataFrame({" a ": [1]}).columns)
```

```text
[' a ']
```

CSV'den gelen sütun adlarında baştaki ve sondaki boşluklar **korunuyor**.
`data["a"]` yazınca `KeyError` alıyorsun ve sebebi ekranda görünmüyor.

İlk iş olarak temizlemek iyi bir alışkanlık:

```python
data.columns = data.columns.str.strip()
```

Aynı şekilde büyük/küçük harf de birebir eşleşiyor: `"Score"` ile `"score"`
farklı sütunlar.

## 8. `append` artık yok

```python
data.append(other)
```

```text
AttributeError: 'DataFrame' object has no attribute 'append'
```

Eski öğreticilerde çok geçiyor ama **pandas 2.0'da kaldırıldı**. Yerine:

```python
pd.concat([data, other])
```

Zaten döngü içinde satır eklemek kötü bir fikirdi: her çağrı tabloyu baştan
kuruyordu. Doğrusu satırları bir listede toplayıp sonunda tek seferde tablo
kurmak.

## 9. Satır satır dolaşmak son çare

```python
for index, row in data.iterrows():
    ...
```

Çalışıyor ama her satır için bir **seri** nesnesi üretiyor ve çok yavaş.
Vektörel bir karşılığı varsa onu kullan:

```python
data["total"] = data["price"] * data["count"]   # dogru
```

`iterrows` yalnızca satırlar arasında gerçekten bağımlılık olan işler için
(bir öncekine bakarak karar vermek gibi).

## 10. Sütun sırası sözlükteki sıra

```python
list(pd.DataFrame({"z": [1], "a": [2]}).columns)
```

```text
['z', 'a']
```

pandas sütunları alfabetik sıralamıyor; sen nasıl yazdıysan öyle duruyor.
Belirli bir sıra istiyorsan açıkça seçiyorsun:

```python
data = data[["name", "city", "score"]]
```

Bu, bir tabloyu kaydetmeden ya da rapora koymadan önce yapılacak son
işlerden biri.
