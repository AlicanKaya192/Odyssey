# Pandas Serileri

NumPy dizisi bir şeyi bilmiyordu: **elemanların adını.** Notların
`[82, 74, 91]` diye duruyordu ama hangisi kimin, dizi bunu tutmuyordu.

pandas'ın çözümü **seri** (Series): bir NumPy dizisi ve yanında ona eşlik
eden **etiketler**.

```python
import pandas as pd
```

`pd` de tıpkı `np` gibi bir gelenek.

## İlk seri

```python
scores = pd.Series([82, 74, 91, 68])
print(scores)
```

```text
0    82
1    74
2    91
3    68
dtype: int64
```

Sol sütun **index** (dizin), sağ sütun **değerler**. Index vermezsen pandas
0'dan başlayan sayılar koyuyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">index</span><span class="anat-body">etiketler — sayı, metin, tarih olabilir</span></div>
    <div class="anat-row"><span class="anat-label">values</span><span class="anat-body">asıl veri; altında bir NumPy dizisi duruyor</span></div>
    <div class="anat-row"><span class="anat-label">dtype</span><span class="anat-body">değerlerin ortak tipi — NumPy'dan gelen kural</span></div>
    <div class="anat-row"><span class="anat-label">name</span><span class="anat-body">serinin adı; bir tabloya girdiğinde sütun adı oluyor</span></div>
  </div>
</figure>

## Etiketli index

Asıl güç burada:

```python
scores = pd.Series([82, 74, 91], index=["Ada", "Kerem", "Mina"])
print(scores)
print(scores["Mina"])
```

```text
Ada      82
Kerem    74
Mina     91
dtype: int64
91
```

Artık "üçüncü eleman" demene gerek yok, adıyla çağırıyorsun. NumPy'da bunu
yapabilmek için ayrı bir isim dizisi tutup indeksleri eşleştirmen
gerekiyordu.

Sözlükten de kurulabiliyor — anahtarlar index oluyor:

```python
population = pd.Series({"Ankara": 5, "Izmir": 4})
print(population)
```

```text
Ankara    5
Izmir     4
dtype: int64
```

## NumPy'dan gelenler

Seri bir NumPy dizisinin üstünde durduğu için vektörel işlemler aynen
çalışıyor:

```python
scores = pd.Series([82, 74, 91], index=["Ada", "Kerem", "Mina"])

print(scores + 5)
print(scores.mean())
print(scores[scores > 80])
```

```text
Ada      87
Kerem    79
Mina     96
dtype: int64
82.33333333333333
Ada     82
Mina    91
dtype: int64
```

Dikkat: koşullu seçimde **etiketler de geliyor.** Sonuç yalnızca sayılar
değil, kimin hangi notu aldığı.

## Hizalama: serinin asıl numarası

İki seriyi topladığında pandas **sıraya değil etikete** bakıyor:

```python
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["z", "y", "x"])

print(a + b)
```

```text
x    31
y    22
z    13
dtype: int64
```

`b` ters sırada duruyor ama sonuç doğru: `x` ile `x`, `y` ile `y` toplandı.
NumPy olsaydı hizaya bakmadan sırayla toplardı ve **sessizce yanlış** sonuç
verirdi.

Buna **hizalama** (alignment) deniyor ve pandas'ın en değerli özelliği.
İki farklı kaynaktan gelen veriyi birleştirirken sıraların tutmasını
beklemek zorunda kalmıyorsun.

Etiket bir tarafta yoksa sonuç `NaN` oluyor:

```python
a = pd.Series([1, 2], index=["x", "y"])
b = pd.Series([10, 20], index=["y", "z"])

print(a + b)
```

```text
x     NaN
y    12.0
z     NaN
dtype: float64
```

Bu bir hata değil, bilgi: `x` yalnızca birinde var, `z` yalnızca ötekinde.
pandas uydurmak yerine "bilinmiyor" diyor.

## Eksik değerler: NumPy'dan farklı

Burası dikkat isteyen bir yer.

```python
values = pd.Series([80.0, None, 90.0])

print(values.mean())
```

```text
85.0
```

Aynı veri NumPy'da `nan` veriyordu. **pandas eksik değerleri hesaplarken
kendiliğinden atlıyor.**

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>NumPy</h4>
      <p><code>mean()</code> sonucu <code>nan</code>. Atlamak için <code>nanmean</code> demen gerekiyor.</p>
    </div>
    <div class="versus-side">
      <h4>pandas</h4>
      <p><code>mean()</code> eksikleri atlıyor. Saydırmak istersen ayrıca söylüyorsun.</p>
    </div>
  </div>
  <figcaption>İki kütüphane aynı soruya farklı cevap veriyor. Hangisiyle çalıştığını bilmek gerekiyor — bu fark sessizce yanlış sonuç üretebiliyor.</figcaption>
</figure>

Kolaylık gibi görünüyor ama bir riski var: **kaç değerin eksik olduğunu fark
etmeyebiliyorsun.** Ortalama hesaplandı, sonuç geldi, ama belki yüz kaydın
seksen tanesi boştu.

Bu yüzden ortalamadan önce sayman gerekiyor:

```python
values = pd.Series([80.0, None, 90.0])

print(values.isna().sum())
print(values.count())
print(values.size)
```

```text
1
2
3
```

`count()` **dolu** hücreleri sayıyor, `size` hepsini. İkisi farklıysa
eksik değer var demektir.

## Eksikleri doldurmak ve atmak

```python
values = pd.Series([80.0, None, 90.0])

print(values.fillna(0).tolist())
print(values.dropna().tolist())
print(values.fillna(values.mean()).tolist())
```

```text
[80.0, 0.0, 90.0]
[80.0, 90.0]
[80.0, 85.0, 90.0]
```

Üçü de **yeni bir seri** döndürüyor; özgün seri değişmiyor. pandas'ta
neredeyse her metot böyle çalışıyor.

Hangisini seçeceğin veriye bağlı: sıfırla doldurmak "ölçüm sıfırdı" demek
oluyor ve ortalamayı aşağı çekiyor. Ortalamayla doldurmak ortalamayı
korumasa da bozmuyor. Atmak ise kaydı tamamen kaybediyor.

## Kategorik sütunlarda sayma

Metin tutan bir seride en çok gereken şey "hangisinden kaç tane var":

```python
cities = pd.Series(["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"])

print(cities.value_counts())
print(cities.nunique())
```

```text
Ankara    3
Izmir     1
Bursa     1
Name: count, dtype: int64
3
```

`value_counts()` çoktan aza sıralıyor. Bir veriyi ilk kez açtığında
kategorik sütunlara bu çağrıyı yapmak neredeyse refleks hâline geliyor.

## Hızlı bakış

```python
scores = pd.Series([82, 74, 91, 68])
print(scores.describe())
```

```text
count     4.000000
mean     78.750000
std       9.979145
min      68.000000
25%      72.500000
50%      78.000000
75%      84.250000
max      91.000000
dtype: float64
```

Tek çağrıda sekiz sayı: kaç dolu kayıt var, ortalama, standart sapma, en
küçük, çeyrekler ve en büyük. `50%` satırı **medyan**.

Ortalama ile medyan birbirinden uzaksa uç değer var demekti — burada 78.75
ve 78.0, yani veri dengeli.

## Seri, liste, dizi

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">liste</span><span class="anat-body">her tip karışabilir, döngüyle işlenir, etiket yok</span></div>
    <div class="anat-row"><span class="anat-label">NumPy dizisi</span><span class="anat-body">tek tip, vektörel işlem, etiket yok</span></div>
    <div class="anat-row"><span class="anat-label">pandas serisi</span><span class="anat-body">tek tip, vektörel işlem, <b>etiketli</b>, eksik değerleri biliyor</span></div>
  </div>
</figure>

Bir sonraki bölümde birden fazla seriyi yan yana koyup **DataFrame**
elde edeceksin — asıl tablo yapısı o.

## Özet

- **Seri** = değerler + **index**. Index olmadan bu bir NumPy dizisi olurdu.
- Index metin olabiliyor: `scores["Mina"]`.
- Vektörel işlemler NumPy'dan aynen geliyor, üstüne etiketler de taşınıyor.
- **Hizalama:** iki seri toplanırken sıraya değil **etikete** bakılıyor.
  Eşleşmeyen etiket `NaN` veriyor.
- **pandas eksik değerleri hesapta atlıyor**, NumPy atlamıyor. Bu yüzden
  `isna().sum()` ile kaç tane olduğunu görmek gerekiyor.
- `fillna`, `dropna` — ikisi de **yeni seri** döndürüyor.
- `value_counts()` kategorik sütunun ilk sorusu, `describe()` sayısal
  sütunun.
