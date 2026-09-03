pandas kolaylık sağlarken sessizce karar veriyor. Aşağıdakiler o kararların
seni şaşırttığı yerler.

## 1. `s[0]` sıra değil, etiket arıyor

```python
s = pd.Series([10, 20, 30], index=[2, 0, 1])
print(s[0])
```

```text
20
```

İlk elemanı bekliyordun, `0` **etiketini** taşıyan elemanı aldın.

Index sayılardan oluştuğunda köşeli parantez belirsiz hâle geliyor. Bu
yüzden pandas iki açık yol veriyor:

```python
print(s.loc[0])    # etikete gore  -> 20
print(s.iloc[0])   # siraya gore   -> 10
```

**Kural:** sıra istiyorsan her zaman `iloc` yaz. Index'in ne olduğunu
düşünmek zorunda kalmıyorsun.

## 2. Sonucu atamazsan kayboluyor

```python
values = pd.Series([1.0, None, 3.0])
values.fillna(0)
print(values.isna().sum())
```

```text
1
```

`fillna` yeni bir seri döndürdü, sen onu bir yere koymadın, o da kayboldu.
Özgün seri hiç değişmedi.

```python
values = values.fillna(0)
```

pandas'ta neredeyse **her metot** böyle: `dropna`, `sort_values`, `astype`,
`round`, `replace`. Hepsi yeni bir nesne veriyor.

## 3. Hizalama beklemediğin sonucu verebiliyor

Hizalama çoğu zaman kurtarıcı ama bazen sürpriz:

```python
a = pd.Series([1, 2, 3])
b = pd.Series([1, 2, 3], index=[2, 1, 0])

print((a + b).tolist())
```

```text
[4, 4, 4]
```

`[2, 4, 6]` bekliyordun. pandas sıraya değil etikete baktı: 0 ile 0 (1+3),
1 ile 1 (2+2), 2 ile 2 (3+1).

**Ne zaman olur:** bir seriyi filtreleyip sonra başka bir seriyle işleme
soktuğunda. Filtreleme index'i koruyor, o yüzden aradaki numaralar eksik
kalıyor.

**Çözüm:** hizalama istemiyorsan index'i sıfırla ya da değerlerle çalış:

```python
print((a.values + b.values).tolist())      # [2, 4, 6]
print((a + b.reset_index(drop=True)).tolist())  # [2, 4, 6]
```

## 4. Eksik değerler sessizce atlanıyor

```python
scores = pd.Series([80.0, None, None, None, 90.0])
print(scores.mean())
print(scores.count())
```

```text
85.0
2
```

Ortalama geldi, sonuç makul görünüyor. Ama beş kaydın **üçü boştu** ve o
ortalama yalnızca iki sayıdan hesaplandı.

NumPy bu durumda `nan` verip seni uyarıyordu. pandas uyarmıyor — kolaylık
sağlıyor ama sorumluluğu sana bırakıyor.

**Alışkanlık hâline getir:** ortalama almadan önce `count()` ile `size`'ı
karşılaştır.

Eksikleri saydırmak istiyorsan söylüyorsun:

```python
print(scores.sum(skipna=False))   # nan
```

## 5. Boş seride ortalama `nan`

```python
empty = pd.Series([], dtype=float)
print(empty.mean())
```

```text
nan
```

Düz Python'da `sum([]) / len([])` sıfıra bölme hatası veriyordu; pandas
hata vermiyor, `nan` veriyor.

Bu, filtreden sonra sık karşına çıkıyor: hiçbir satır kalmadıysa ortalama
`nan` oluyor ve bunu fark etmezsen rapora `nan` yazıyorsun.

## 6. `None` koyunca tip ondalığa dönüyor

```python
print(pd.Series([1, 2, 3]).dtype)
print(pd.Series([1, None, 3]).dtype)
```

```text
int64
float64
```

Tamsayı tipi `NaN` tutamıyor, o yüzden pandas seriyi ondalığa çeviriyor.
Sonuç: `1` yerine `1.0` görüyorsun.

Geri çevirmek de eksik değer varken çalışmıyor:

```python
pd.Series([1.0, None, 3.0]).astype(int)
```

```text
IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer.
```

Önce boşlukları halletmen gerekiyor: `dropna()` ya da `fillna(...)`, sonra
`astype(int)`.

## 7. `Series.unique()` sıralamıyor

```python
cities = pd.Series(["Izmir", "Ankara", "Izmir", "Bursa"])
print(list(cities.unique()))
```

```text
['Izmir', 'Ankara', 'Bursa']
```

`np.unique` alfabetik sıralıyordu; `Series.unique()` **ilk görülme sırasını**
koruyor. Aynı adı taşıyan iki fonksiyon, iki farklı davranış.

Sıralı istiyorsan `sorted(cities.unique())` yazıyorsun.

## 8. `.str` olmadan metin metotları çalışmıyor

```python
cities.lower()
```

```text
AttributeError: 'Series' object has no attribute 'lower'
```

`cities` bir metin değil, **metinlerden oluşan bir seri**. Metotlar `.str`
üzerinden geliyor:

```python
print(cities.str.lower().tolist())
```

Aynı şey tarihler için `.dt`, kategoriler için `.cat` ile oluyor.

## 9. `apply` çalışıyor ama yavaş

```python
values.apply(lambda x: x * 2)   # calisir
values * 2                       # ayni sonuc, cok daha hizli
```

`apply` her eleman için Python fonksiyonunu çağırıyor; vektörel işlemin
bütün hız kazancını geri veriyor.

**Kural:** vektörel bir karşılığı varsa onu kullan. `apply` gerçekten
karmaşık, satır satır düşünmeyi gerektiren işler için.

## 10. `value_counts` eksikleri saymıyor

```python
s = pd.Series(["a", "b", None, "a"])
print(s.value_counts().sum())
print(s.size)
```

```text
3
4
```

Varsayılan olarak `NaN` sayılmıyor. Saymasını istiyorsan söylüyorsun:

```python
print(s.value_counts(dropna=False))
```

Kategorik bir sütunda "toplam kaç kayıt var" diye `value_counts().sum()`
yazarsan eksik olanları kaçırıyorsun.
