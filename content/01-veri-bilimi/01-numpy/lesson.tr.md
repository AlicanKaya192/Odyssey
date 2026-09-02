# NumPy Dizileri

Önceki bölümde ortalamayı elle hesapladın, döngüyle filtreledin, sözlüklerle
grupladın. Hepsi çalışıyordu. Şimdi aynı işleri **döngü yazmadan** yapmayı
öğreneceksin.

NumPy'ın tek bir veri yapısı var: **dizi** (array). Bu bölüm o yapıyı ve
onunla ne yapıldığını anlatıyor.

```python
import numpy as np
```

`np` kısaltması bir gelenek. Herkes böyle yazıyor; sen de böyle yaz, kodunu
okuyan herkes ne olduğunu anlasın.

## Neden liste değil?

İki listenin elemanlarını çarpmak istiyorsun:

```python
a = [1, 2, 3, 4]
b = [2, 3, 4, 5]

result = []
for i in range(len(a)):
    result.append(a[i] * b[i])

print(result)
```

```text
[2, 6, 12, 20]
```

Aynı iş NumPy ile:

```python
a = np.array([1, 2, 3, 4])
b = np.array([2, 3, 4, 5])

print(a * b)
```

```text
[ 2  6 12 20]
```

Döngü yok, `append` yok, boş liste yok. Buna **vektörel işlem** deniyor:
işlemi tek tek elemanlara değil, dizinin tamamına söylüyorsun.

İki sebeple böyle:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Kısa</h4>
      <p>Beş satır bire iniyor. Yazması kolay, okuması kolay, hata yapması zor.</p>
    </div>
    <div class="versus-side">
      <h4>Hızlı</h4>
      <p>Döngü Python'da değil, altta C'de dönüyor. Milyonlarca elemanda fark saniyelerle ölçülüyor.</p>
    </div>
  </div>
</figure>

Hız neden geliyor? Çünkü **dizi tek tipte veri tutuyor.** Python listesi her
eleman için ayrı bir nesne, ayrı bir tip bilgisi tutuyor; dizi ise "hepsi
`int64`" deyip yan yana duran ham sayıları saklıyor.

## Dizi oluşturmak

En yaygın yol bir listeden çevirmek:

```python
numbers = np.array([3, 7, 1, 9])
print(numbers)
```

```text
[3 7 1 9]
```

Sıfırdan üretmenin de yolları var:

```python
print(np.zeros(4, dtype=int))
print(np.arange(0, 10, 2))
print(np.linspace(0, 1, 5))
```

```text
[0 0 0 0]
[0 2 4 6 8]
[0.   0.25 0.5  0.75 1.  ]
```

`arange` **adımı** alıyor (sıfırdan ona kadar ikişer), `linspace` **kaç
parça** istediğini alıyor (sıfırla bir arasında beş sayı). İkisi sık
karıştırılıyor: `arange` bitişi dışarıda bırakıyor, `linspace` içeriye
alıyor.

## Dizinin özellikleri

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix.ndim)    # kac boyut
print(matrix.shape)   # her boyutta kac eleman
print(matrix.size)    # toplam eleman
print(matrix.dtype)   # icindeki tip
```

```text
2
(2, 3)
6
int64
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ndim</span><span class="anat-body">boyut sayısı — 1 vektör, 2 tablo, 3 ve üstü daha derin yapılar</span></div>
    <div class="anat-row"><span class="anat-label">shape</span><span class="anat-body">bir demet: <code>(satır, sütun)</code>. En çok kullandığın özellik bu</span></div>
    <div class="anat-row"><span class="anat-label">size</span><span class="anat-body">toplam hücre sayısı — <code>shape</code> değerlerinin çarpımı</span></div>
    <div class="anat-row"><span class="anat-label">dtype</span><span class="anat-body">bütün elemanların ortak tipi</span></div>
  </div>
</figure>

## Tek tip olmanın sonucu

Diziye farklı tipler koyarsan NumPy hepsini **ortak bir tipe çeviriyor**:

```python
mixed = np.array([1, 2.5, 3])
print(mixed.dtype)
print(mixed)
```

```text
float64
[1.  2.5 3. ]
```

Tamsayılar ondalığa dönüştü. Ters yönde ise **veri kaybı** oluyor:

```python
values = np.array([1, 2, 3])
values[0] = 9.7
print(values)
```

```text
[9 2 3]
```

`9.7` sessizce `9` oldu — dizinin tipi `int64` ve ondalık kısım atıldı. Hata
yok, uyarı yok. Bu, NumPy'da en sık düşülen tuzaklardan biri.

## Yeniden şekillendirme

Aynı veriyi farklı bir düzende görmek:

```python
flat = np.arange(6)
print(flat)
print(flat.reshape(2, 3))
```

```text
[0 1 2 3 4 5]
[[0 1 2]
 [3 4 5]]
```

Eleman sayısı tutmak zorunda: altı elemanı `(2, 3)` yapabilirsin, `(2, 4)`
yapamazsın — `ValueError` alırsın.

## Seçim

Tek boyutta listeyle aynı:

```python
values = np.array([10, 20, 30, 40, 50])

print(values[0])
print(values[-1])
print(values[1:4])
```

```text
10
50
[20 30 40]
```

İki boyutta virgülle: `[satır, sütun]`.

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix[0, 2])   # birinci satir, ucuncu sutun
print(matrix[1])      # butun ikinci satir
print(matrix[:, 0])   # butun satirlarin ilk sutunu
```

```text
3
[4 5 6]
[1 4]
```

`matrix[0][2]` de çalışıyor ama `matrix[0, 2]` hem daha kısa hem daha hızlı:
ilki önce bir ara dizi üretiyor.

## Dilim bir kopya değil

Bu, listeden gelen alışkanlığı bozan bir davranış:

```python
values = np.array([1, 2, 3, 4, 5])
part = values[1:3]
part[0] = 99

print(values)
```

```text
[ 1 99  3  4  5]
```

`part` yeni bir dizi değil, aynı verinin üstünde bir **pencere** (view).
Onu değiştirince özgün dizi de değişiyor. Python listesinde böyle olmuyor;
`liste[1:3]` gerçek bir kopya veriyor.

Kopya istiyorsan açıkça isteyeceksin:

```python
part = values[1:3].copy()
```

Bunun sebebi hız: milyon elemanlı bir diziden dilim alırken veriyi
kopyalamamak büyük bir kazanç. Ama farkında olmadan özgün veriyi bozmak da
kolay.

## Fancy index

Bir dizi indeksle birden fazla eleman seçmek:

```python
values = np.array([10, 20, 30, 40, 50])
picked = values[[0, 3, 4]]
print(picked)
```

```text
[10 40 50]
```

Dilimden farkı: buradaki seçim **sıralı olmak zorunda değil** ve sonuç
gerçek bir kopya.

## Koşullu seçim

En çok kullanacağın şey bu. Bir karşılaştırma yaptığında NumPy sana
`True`/`False`'lardan oluşan bir dizi veriyor:

```python
scores = np.array([45, 82, 91, 60, 74])

print(scores > 70)
```

```text
[False  True  True False  True]
```

Bu diziyi köşeli parantezin içine koyunca **yalnızca `True` olanlar**
geliyor:

```python
print(scores[scores > 70])
print(scores[scores > 70].mean())
```

```text
[82 91 74]
82.33333333333333
```

Bu iki satır, önceki bölümde on satırla yaptığın işin karşılığı.

Birden fazla koşulu birleştirmek için `&` ve `|` kullanılıyor, `and` ve `or`
değil — ve **parantez zorunlu**:

```python
print(scores[(scores > 50) & (scores < 90)])
```

```text
[82 60 74]
```

`and` yazarsan `ValueError` alıyorsun: Python tek bir doğruluk değeri
bekliyor, elindeyse beş tane var.

## Matematik ve toplulaştırma

Bütün dizi üzerinde tek seferde:

```python
values = np.array([3, 7, 1, 9])

print(values + 10)
print(values * 2)
print(values.sum())
print(values.mean())
print(values.min(), values.max())
print(values.argmax())
```

```text
[13 17 11 19]
[ 6 14  2 18]
20
5.0
1 9
3
```

`argmax` değerin kendisini değil **sırasını** veriyor: en büyük eleman
üçüncü indekste. "En yüksek notu kim aldı" sorusunda tam olarak bu gerekiyor.

## axis: hangi yönde?

İki boyutlu bir dizide "toplam" belirsiz bir istek — satırların mı,
sütunların mı?

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix.sum())
print(matrix.sum(axis=0))
print(matrix.sum(axis=1))
```

```text
21
[5 7 9]
[ 6 15]
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">axis yok</span><span class="anat-body">her şeyi topla, tek sayı çıkar</span></div>
    <div class="anat-row"><span class="anat-label">axis=0</span><span class="anat-body">satırlar boyunca in — <b>sütun</b> toplamları çıkar</span></div>
    <div class="anat-row"><span class="anat-label">axis=1</span><span class="anat-body">sütunlar boyunca git — <b>satır</b> toplamları çıkar</span></div>
  </div>
  <figcaption>Karıştırmamak için: axis, "hangisi kaybolacak" diye okunuyor. axis=0 satırları yok ediyor, geriye sütunlar kalıyor.</figcaption>
</figure>

Bir tabloda satırlar kayıt, sütunlar özellik olduğu için `axis=0` genelde
"her özelliğin ortalaması" demek — en çok kullanacağın hâli bu.

## Yayılma (broadcasting)

Farklı şekildeki dizilerle işlem yaparken NumPy küçük olanı **büyüğe
uyduruyor**:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bonus = np.array([10, 20, 30])

print(matrix + bonus)
```

```text
[[11 22 33]
 [14 25 36]]
```

`bonus` üç elemanlı, `matrix` iki satırlı. NumPy `bonus`'u her satıra ayrı
ayrı ekliyor. Bunu yapmak için bir döngü yazman gerekmiyor.

Kural şu: şekiller **sondan başa** karşılaştırılıyor ve her basamakta ya
eşit olmaları ya da birinin 1 olması gerekiyor. Uymuyorsa hata alıyorsun.

## Eksik değerler

Gerçek veride hücreler boş oluyor. NumPy'da bunun karşılığı `np.nan`:

```python
scores = np.array([80.0, np.nan, 90.0])

print(scores.mean())
print(np.nanmean(scores))
```

```text
nan
85.0
```

**Tek bir eksik değer bütün sonucu `nan` yapıyor.** Bu bilinçli: NumPy
"bilinmeyen bir sayıyla toplamın sonucu da bilinmiyor" diyor.

`nan` içeren dizilerde `nanmean`, `nansum`, `nanmax` kullanılıyor. Hangi
hücrelerin boş olduğunu `np.isnan` söylüyor:

```python
print(np.isnan(scores))
print(scores[~np.isnan(scores)])
```

```text
[False  True False]
[80. 90.]
```

`~` işareti "tersi" demek: `True` olanları değil, olmayanları seç.

Bir tuhaflık: `np.nan == np.nan` sonucu `False`. Bilinmeyen bir sayı başka
bir bilinmeyen sayıya eşit değil. Bu yüzden eşitlikle arayamıyorsun,
`isnan` gerekiyor.

## Özet

- NumPy'ın veri yapısı **dizi**: tek tipte, sabit boyutlu, hızlı.
- **Vektörel işlem:** `a * b` bütün diziyi çarpıyor, döngü gerekmiyor.
- `ndim`, `shape`, `size`, `dtype` — dizinin kimliği. En çok `shape`
  kullanılıyor.
- Tip tek: `int` diziye ondalık koyarsan **sessizce kırpılıyor**.
- **Dilim bir kopya değil**, aynı veriye açılan bir pencere. Kopya için
  `.copy()`.
- Koşullu seçim: `scores[scores > 70]`. Koşulları `&` ve `|` ile birleştir,
  parantezi unutma.
- `axis=0` sütun bazında, `axis=1` satır bazında sonuç veriyor.
- **Yayılma:** farklı şekiller uyduruluyor, döngü yazmadan.
- Eksik değer `np.nan`; bir tanesi bile ortalamayı `nan` yapıyor,
  `nanmean` ve `isnan` bunun içindir.
