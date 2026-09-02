# Gruplama ve Toplulaştırma

İlk bölümde şehirlere göre ortalama notu hesaplamak için on satır yazmıştın:
iki sözlük, bir döngü, bir bölme. Şimdi o on satırın tek satırlık karşılığını
öğreneceksin.

```python
data.groupby("city")["score"].mean()
```

Bu bölümün konusu bu satır ve etrafındakiler.

Örneklerde şu tablo kullanılıyor:

```python
data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "grade": ["A", "B", "A", "C", "B", "A"],
    "score": [82, 74, 91, 68, 88, 76],
})
```

## Böl, hesapla, birleştir

`groupby` üç adımlı bir işlem:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Böl</b><br>satırları anahtara göre kümelere ayır</span>
    <span class="arrow">→</span>
    <span class="node"><b>Hesapla</b><br>her küme için bir sayı üret</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Birleştir</b><br>sonuçları tek tabloda topla</span>
  </div>
  <figcaption>Sen yalnızca "neye göre" ve "ne hesaplansın" diyorsun; üç adımın hepsini pandas yapıyor.</figcaption>
</figure>

```python
print(data.groupby("city")["score"].mean())
```

```text
city
Ankara    87.0
Bursa     68.0
Izmir     75.0
Name: score, dtype: float64
```

Sonuç bir **seri**: index gruplar, değerler hesaplanan sayı. Gruplar
kendiliğinden **alfabetik sıralanıyor**.

Okuma sırası soldan sağa: *"`data`'yı `city`'ye göre grupla, `score`
sütununu al, ortalamasını hesapla."*

## Hangi hesap?

Seride ne varsa burada da var:

```python
print(data.groupby("city")["score"].count())
print(data.groupby("city").size())
```

```text
city
Ankara    3
Bursa     1
Izmir     2
Name: score, dtype: int64
city
Ankara    3
Bursa     1
Izmir     2
dtype: int64
```

İkisi benziyor ama farklılar: **`count()` dolu hücreleri**, **`size()` bütün
satırları** sayıyor. Eksik değer varsa ikisi ayrışıyor.

`sum`, `min`, `max`, `median`, `std`, `nunique` — hepsi aynı şekilde
çalışıyor.

## Birden fazla hesap: agg

```python
print(data.groupby("city")["score"].agg(["count", "mean", "max"]))
```

```text
        count  mean  max
city
Ankara      3  87.0   91
Bursa       1  68.0   68
Izmir       2  75.0   76
```

Sonuç artık bir **tablo**: satırlar gruplar, sütunlar hesaplar.

Sütunlara kendi adını vermek ve farklı sütunlardan hesap yapmak da mümkün:

```python
print(data.groupby("city").agg(
    kisi=("name", "count"),
    ortalama=("score", "mean"),
))
```

```text
        kisi  ortalama
city
Ankara     3      87.0
Bursa      1      68.0
Izmir      2      75.0
```

Yazım şu: `yeni_ad=("hangi sütun", "hangi hesap")`. Rapor üretirken en çok
kullanacağın biçim bu.

## İki anahtara göre gruplamak

```python
print(data.groupby(["city", "grade"])["score"].mean())
```

```text
city    grade
Ankara  A        86.5
        B        88.0
Bursa   C        68.0
Izmir   A        76.0
        B        74.0
Name: score, dtype: float64
```

Index'te iki seviye var — buna **çok seviyeli index** deniyor. Boş görünen
hücreler bir öncekiyle aynı demek, tekrar yazılmıyor.

Bu yapıyla çalışmak biraz zahmetli; genelde düzleştiriliyor:

```python
print(data.groupby(["city", "grade"])["score"].mean().reset_index())
```

`reset_index()` seviyeleri sütuna çeviriyor ve elinde normal bir tablo
kalıyor.

## Grup sonucu index oluyor

`groupby` sonucunda anahtar **index'e** taşınıyor. Sütun olarak kalmasını
istiyorsan:

```python
print(data.groupby("city", as_index=False)["score"].mean())
```

```text
     city  score
0  Ankara   87.0
1   Bursa   68.0
2   Izmir   75.0
```

Sonucu başka bir tabloyla birleştirecekseniz ya da dosyaya yazacaksanız bu
biçim daha kullanışlı.

## Pivot tablo

İki anahtarlı gruplamanın **tablo hâli**:

```python
print(data.pivot_table(index="city", columns="grade", values="score", aggfunc="mean"))
```

```text
grade      A     B     C
city
Ankara  86.5  88.0   NaN
Bursa    NaN   NaN  68.0
Izmir   76.0  74.0   NaN
```

Satırlar bir anahtar, sütunlar öteki, hücreler hesap. Excel'deki pivot
tablonun aynısı.

`NaN` olan hücreler "bu kombinasyon veride yok" demek — Ankara'da C notu
alan kimse yok. Sıfır değil, **yok**. İkisini karıştırmamak gerekiyor; ama
sıfır görmek istiyorsan söyleyebiliyorsun:

```python
data.pivot_table(..., fill_value=0)
```

## Sıralamak ve en büyüğü bulmak

Grup sonucu da bir seri; ona da her şeyi yapabiliyorsun:

```python
averages = data.groupby("city")["score"].mean()

print(averages.sort_values(ascending=False))
print(averages.idxmax())
```

```text
city
Ankara    87.0
Izmir     75.0
Bursa     68.0
Name: score, dtype: float64
Ankara
```

`idxmax()` en yüksek ortalamalı **grubun adını** veriyor. "Hangi şehirde
satış en yüksek" sorusunun cevabı tam olarak bu iki satır.

## transform: grup sonucunu satırlara dağıtmak

Bazen grup ortalamasını **her satırın yanında** istiyorsun — mesela "bu
öğrenci kendi şehrinin ortalamasının üstünde mi?" sorusu için:

```python
data["city_mean"] = data.groupby("city")["score"].transform("mean")
print(data[["name", "city", "score", "city_mean"]])
```

```text
    name    city  score  city_mean
0    Ada  Ankara     82       87.0
1  Kerem   Izmir     74       75.0
2   Mina  Ankara     91       87.0
3  Deniz   Bursa     68       68.0
4    Efe  Ankara     88       87.0
5   Sila   Izmir     76       75.0
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>agg / mean</h4>
      <p>Grup başına <b>bir satır</b> döndürüyor. Tablo küçülüyor.</p>
    </div>
    <div class="versus-side">
      <h4>transform</h4>
      <p>Her satıra grubunun sonucunu yazıyor. Tablo <b>aynı boyda</b> kalıyor.</p>
    </div>
  </div>
</figure>

Artık karşılaştırma yapabiliyorsun:

```python
data["above_city"] = data["score"] > data["city_mean"]
```

## Eksik anahtarlar sessizce düşüyor

```python
d = pd.DataFrame({"g": ["a", "a", None], "v": [1, 2, 3]})
print(d.groupby("g")["v"].sum())
```

```text
g
a    3
Name: v, dtype: int64
```

Üçüncü satırın anahtarı boş olduğu için **hiçbir gruba girmedi** ve sonuçtan
tamamen kayboldu. Toplam 6 olması gerekirken 3 görünüyor.

Bu, sessiz hataların iyi bir örneği. Görmek istiyorsan:

```python
print(d.groupby("g", dropna=False)["v"].sum())
```

```text
g
a      3
NaN    3
Name: v, dtype: int64
```

**Alışkanlık:** gruplamadan önce anahtar sütununda `isna().sum()` çalıştır.

## Özet

- `groupby` üç adım: **böl, hesapla, birleştir.**
- Sonuç bir seri; anahtar **index'e** taşınıyor ve gruplar alfabetik
  sıralanıyor.
- `count()` dolu hücreleri, `size()` bütün satırları sayıyor.
- **`agg`** birden fazla hesap yapıyor;
  `yeni_ad=("sütun", "hesap")` biçimiyle rapor üretiliyor.
- `as_index=False` anahtarı sütun olarak bırakıyor.
- **`pivot_table`** iki anahtarlı gruplamanın tablo hâli; boş hücreler `NaN`.
- **`transform`** grup sonucunu her satıra dağıtıyor; tablo aynı boyda
  kalıyor.
- **Anahtarı eksik satırlar sessizce düşüyor.** `dropna=False` ile
  görünüyorlar.
