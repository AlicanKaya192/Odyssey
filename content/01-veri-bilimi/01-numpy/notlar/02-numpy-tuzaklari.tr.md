# NumPy Tuzakları

NumPy'ın çoğu hatası **hata vermiyor.** Program çalışıyor, sana bir sayı
veriyor ve o sayı yanlış oluyor. Aşağıdakiler en sık düşülenler.

## 1. Dilim özgün diziyi değiştiriyor

```python
values = np.array([1, 2, 3, 4, 5])
part = values[1:3]
part[0] = 99
print(values)
```

```text
[ 1 99  3  4  5]
```

Python listesinde böyle olmuyor; orada dilim gerçek bir kopya. NumPy'da
dilim aynı verinin üstünde bir **pencere**.

**Çözüm:** değiştireceksen `.copy()` iste.

```python
part = values[1:3].copy()
```

**Nasıl anlarım?** `part.base` özgün diziyi gösteriyorsa pencere,
`None` ise kopya.

Fancy index (`a[[0, 2]]`) ve koşullu seçim (`a[a > 5]`) zaten kopya
veriyor; yalnızca dilim pencere.

## 2. Tamsayı dizisine ondalık koymak

```python
values = np.array([1, 2, 3])
values[0] = 9.7
print(values)
```

```text
[9 2 3]
```

Ondalık kısım sessizce atıldı. Dizinin tipi `int64` ve NumPy tipi
değiştirmiyor — değeri kırpıyor.

**Çözüm:** diziyi baştan ondalık kur.

```python
values = np.array([1, 2, 3], dtype=float)
```

Bu, ortalama hesaplayıp geri yazarken sık başa geliyor: ortalamayı
`int` diziye yazarsan virgülden sonrası gidiyor.

## 3. `and` yerine `&`

```python
scores[scores > 50 and scores < 90]
```

```text
ValueError: The truth value of an array with more than one element is
ambiguous.
```

`and` tek bir doğruluk değeri bekliyor; elindeyse beş tane var.

**Çözüm:** `&` ve `|`, üstelik **parantezle**.

```python
scores[(scores > 50) & (scores < 90)]
```

Parantezi unutmak da sessiz bir hata: `&` karşılaştırmadan **önce**
çalışıyor ve bambaşka bir şey hesaplanıyor.

## 4. Tek bir `nan` her şeyi bozuyor

```python
scores = np.array([80.0, np.nan, 90.0])
print(scores.mean())
```

```text
nan
```

Bir tane eksik değer bütün ortalamayı `nan` yapıyor. Bu bilinçli: bilinmeyen
bir sayıyla toplamın sonucu da bilinmiyor.

**Çözüm:** `np.nanmean`, `np.nansum`, `np.nanmax`.

```python
print(np.nanmean(scores))   # 85.0
```

Ve bir tuhaflık: `np.nan == np.nan` sonucu `False`. Eksik değeri eşitlikle
arayamıyorsun, `np.isnan` gerekiyor.

```python
print(np.nan == np.nan)          # False
print(np.isnan(scores).sum())    # 1
```

## 5. `axis` ters anlaşılıyor

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.sum(axis=0))
```

Çoğu kişi `axis=0` deyince "satırları topla" bekliyor ama sonuç `[5 7 9]` —
yani **sütun** toplamları.

**Hatırlama yolu:** `axis`, "hangi boyut kaybolacak" demek. `axis=0` satır
boyutunu yok ediyor; geriye sütun başına birer sonuç kalıyor.

Emin olamıyorsan `shape`'e bak: `(2, 3)` bir dizide `axis=0` sonucu üç
elemanlı, `axis=1` sonucu iki elemanlı çıkıyor.

## 6. `arange` ondalıkla güvenilir değil

```python
print(np.arange(0, 1, 0.1).size)
```

```text
10
```

Burada 10 çıkıyor ama adım değerlerine göre bazen bir fazla eleman
gelebiliyor: ondalık sayılar ikilik tabanda tam saklanmıyor ve bitiş sınırı
kıl payı kaçıyor.

**Çözüm:** ondalık adım gerekiyorsa `linspace` kullan — o kaç eleman
istediğini soruyor, tahmin etmiyor.

```python
print(np.linspace(0, 1, 11))
```

## 7. `reshape` eleman sayısını değiştirmiyor

```python
np.arange(6).reshape(2, 4)
```

```text
ValueError: cannot reshape array of size 6 into shape (2,4)
```

`reshape` veriyi yeniden düzenliyor, çoğaltmıyor. 6 eleman `(2, 3)` ya da
`(3, 2)` olabiliyor, `(2, 4)` olamıyor.

Sütun sayısını hesaplatmak istiyorsan `-1` yaz: `a.reshape(2, -1)`.

## 8. Diziye eleman eklemek pahalı

```python
values = np.array([1, 2, 3])
values = np.append(values, 4)
```

Bu çalışıyor ama her çağrıda **diziyi baştan kuruyor**. Döngü içinde
kullanırsan yavaşlığın sebebi bu oluyor.

**Çözüm:** önce Python listesinde topla, sonunda bir kez diziye çevir.

```python
collected = []
for x in something:
    collected.append(x)

values = np.array(collected)
```

Dizinin boyutu sabit; NumPy'ın hızı buradan geliyor.

## 9. `a[0][2]` yerine `a[0, 2]`

İkisi de aynı sonucu veriyor ama `a[0][2]` önce bütün ilk satırı ayrı bir
dizi olarak üretiyor, sonra ondan seçiyor. `a[0, 2]` doğrudan hücreye
gidiyor.

Küçük dizilerde fark yok; büyük dizilerde ve döngü içinde var.

## 10. `argmax` değeri değil sırayı veriyor

```python
scores = np.array([45, 82, 91, 60])
print(scores.argmax())   # 2
print(scores.max())      # 91
```

`argmax` "kaçıncı", `max` "kaç". İkisi de gerekiyor: adları başka bir dizide
tutuyorsan `names[scores.argmax()]` sana en yüksek notu alanın adını
veriyor.
