# Keşifçi Veri Analizi

Buraya kadar teker teker araç öğrendin: seçmek, filtrelemek, gruplamak,
temizlemek, çizmek. **Keşifçi veri analizi** (EDA) bu araçların hangi sırayla
ve neden kullanıldığını anlatan şey.

Tek cümleyle: eline yeni bir veri geldiğinde ne yapacağını bilmek.

## Bu bir adım değil, bir döngü

Yeni başlayanlar EDA'yı "analizden önceki hazırlık" sanıyor. Öyle değil.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Soru</b><br>neyi merak ediyorum</span>
    <span class="arrow">→</span>
    <span class="node"><b>Bak</b><br>tablo, sayı, grafik</span>
    <span class="arrow">→</span>
    <span class="node"><b>Bulgu</b><br>ne gördüm</span>
    <span class="arrow">→</span>
    <span class="node"><b>Yeni soru</b></span>
  </div>
  <figcaption>Her bulgu yeni bir soru doğuruyor. Döngü, sorular bitince değil, cevaplar bir hikâye anlatmaya başlayınca duruyor.</figcaption>
</figure>

"Ortalama not 71" bir bulgu. Ama hemen ardından şu geliyor: kimin notu
düşük? Neden? Az mı çalışmışlar, yoksa başka bir şey mi var?

Bu bölümde bir veriyi baştan sona bu gözle gezeceğiz.

## Veri

```python
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir", "Ankara", "Bursa", "Izmir"],
    "age": [24, 31, 28, 45, 22, 38, 52, 27],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11],
    "score": [88, 62, 82, 45, 91, 70, 51, 84],
})
```

Sekiz kişi: şehir, yaş, çalışma saati ve sınav notu.

Gerçekte satır sayısı yüz binlerce olabiliyor, ama **bakılan sıra
değişmiyor.**

## 1. Adım: boyut ve tipler

```python
print(data.shape)
print(data.dtypes.astype(str).tolist())
```

```text
(8, 4)
['str', 'int64', 'int64', 'int64']
```

İlk soru "kaç satır, kaç sütun". İkincisi "her sütun beklediğim tipte mi".

Bir sayı sütunu `str` görünüyorsa temizlenmemiş demektir — önceki bölümün
konusu. Analize başlamadan önce bunu görmen gerekiyor, ortalama alırken
değil.

## 2. Adım: gözle bak

```python
print(data.head(3))
```

```text
     city  age  hours  score
0  Ankara   24     12     88
1   Izmir   31      5     62
2  Ankara   28      9     82
```

Bu adım atlanıyor ama en ucuz olanı. Üç satır bakmak "bu sütunda neler var"
sorusunun cevabını, hiçbir istatistik vermeden veriyor.

## 3. Adım: eksik değer var mı

```python
print(data.isna().sum().tolist())
```

```text
[0, 0, 0, 0]
```

Bu veride yok. Olsaydı iki soru gelirdi: **kaç tane** ve **neden**.

İkincisi asıl önemli olan. Anket verisinde gelir sütunu boşsa, o kişiler
rastgele dağılmıyor olabilir — genelde yüksek gelirliler cevaplamıyor. O
zaman eksikleri atmak veriyi sistematik olarak çarpıtıyor.

## 4. Adım: describe

```python
print(data.describe())
```

```text
             age     hours      score
count   8.000000   8.00000   8.000000
mean   33.375000   7.87500  71.625000
std    10.662853   4.35685  17.459647
min    22.000000   2.00000  45.000000
25%    26.250000   4.50000  59.250000
50%    29.500000   8.00000  76.000000
75%    39.750000  11.25000  85.000000
max    52.000000  14.00000  91.000000
```

Bu tabloyu **okumayı** öğrenmek, EDA'nın yarısı. Üç şeye bakılıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">mean ↔ 50%</span><span class="anat-body">ortalama ile medyan uzaksa dağılım çarpık; uç değer var</span></div>
    <div class="anat-row"><span class="anat-label">std</span><span class="anat-body">yayılım — küçükse herkes benziyor, büyükse iki farklı grup olabilir</span></div>
    <div class="anat-row"><span class="anat-label">min / max</span><span class="anat-body">mantıklı mı? yaş 0 ya da 200 ise veri hatası var</span></div>
  </div>
</figure>

Burada `score` için ortalama 71.6, medyan 76. **Ortalama medyandan küçük**,
yani aşağıda birkaç düşük not ortalamayı çekiyor.

Bunu fark etmek yeni bir soru doğuruyor: kim o düşük notlular?

## 5. Adım: kategorik sütunlar

```python
print(data["city"].value_counts())
```

```text
city
Ankara    3
Izmir     3
Bursa     2
Name: count, dtype: int64
```

Bir kategorik sütunda ilk sorulan şey bu. İki şey birden görüyorsun: kaç
farklı değer var ve **dengeli mi**.

Dengesizlik önemli: bir grupta 2 kişi varsa o grubun ortalaması hakkında
söyleyebileceğin şey çok az.

## 6. Adım: grupları karşılaştır

Düşük notluları aramaya şehirden başlayalım:

```python
print(data.groupby("city")["score"].agg(["count", "mean"]))
```

```text
        count  mean
city
Ankara      3  80.0
Bursa       2  48.0
Izmir       3  79.0
```

Bursa 48, diğerleri 79-80. Fark büyük.

**Ama `count` sütununa bak: Bursa'da iki kişi var.** İki kişiden yola çıkıp
"Bursa'da notlar düşük" demek, iki kişiyi bir şehir sanmak oluyor.

`mean` ile `count`'u birlikte istemenin sebebi bu. Ortalamayı tek başına
görsen bu tuzağa düşerdin.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Bulgu</h4>
      <p>Bu veride Bursa'daki iki kişinin notu düşük.</p>
    </div>
    <div class="versus-side">
      <h4>İddia</h4>
      <p>Bursa'da notlar düşük.</p>
    </div>
  </div>
  <figcaption>İlki veriden okunuyor, ikincisi verinin söylemediği bir şey. Aradaki farkı korumak, analizde dürüstlüğün ta kendisi.</figcaption>
</figure>

## 7. Adım: sayısal sütunlar arasındaki ilişki

```python
print(round(data["hours"].corr(data["score"]), 2))
```

```text
0.98
```

**Korelasyon** iki sayısal sütunun birlikte hareket edip etmediğini -1 ile
+1 arasında bir sayıyla veriyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">+1'e yakın</span><span class="anat-body">biri artarken öteki de artıyor</span></div>
    <div class="anat-row"><span class="anat-label">0 civarı</span><span class="anat-body">doğrusal bir ilişki görünmüyor</span></div>
    <div class="anat-row"><span class="anat-label">-1'e yakın</span><span class="anat-body">biri artarken öteki azalıyor</span></div>
  </div>
</figure>

0.98 çok yüksek. Çalışma saati ile not birlikte hareket ediyor.

Bütün sayısal sütunları bir kerede karşılaştırmak da mümkün:

```python
print(data[["age", "hours", "score"]].corr().round(2))
```

```text
        age  hours  score
age    1.00  -0.89  -0.91
hours -0.89   1.00   0.98
score -0.91   0.98   1.00
```

Köşegen hep 1.00 — her sütun kendisiyle tam uyumlu. Tablonun alt ve üst
üçgeni aynı; bir kere okumak yetiyor.

Burada `age` ile `score` arasında -0.91 görünüyor: yaş arttıkça not
düşüyor. Ama `age` ile `hours` da -0.89. Yani yaşı büyük olanlar **daha az
çalışmış**. Notu düşüren yaş mı, çalışma saati mi? Bu veri bunu
söyleyemiyor.

**Korelasyon nedensellik değil.** Üç sütun birbirine karışmışken hangisinin
sebep olduğunu ayırmak ayrı bir iş.

## 8. Adım: aykırı değerler

Aykırıyı gözle aramak yerine bir kural kullanılıyor. En yaygını **IQR
kuralı**:

```python
values = pd.Series([12, 15, 14, 13, 16, 15, 92])

q1 = values.quantile(0.25)
q3 = values.quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

print(q1, q3, iqr)
print(low, high)
print(values[(values < low) | (values > high)].tolist())
```

```text
13.5 15.5 2.0
10.5 18.5
[92]
```

`quantile(0.25)` verinin dörtte birinin altında kaldığı değer,
`quantile(0.75)` dörtte üçünün. Aradaki mesafeye **çeyrekler açıklığı**
(IQR) deniyor ve verinin orta yarısının ne kadar yayıldığını gösteriyor.

Bu aralığın 1.5 katı dışına çıkan değerler aykırı sayılıyor. `92` yakalandı.

Neden önemli olduğunu ortalamada görüyorsun:

```python
print(values.mean())
print(values.median())
```

```text
25.285714285714285
15.0
```

Tek bir değer ortalamayı 15'ten 25'e çıkardı. **Medyan kıpırdamadı.** Aykırı
değer şüphesi varken medyan daha güvenilir bir özet.

## Bulguyu cümleye çevirmek

Analizin sonunda bir tablo değil, **bir cümle** oluyor. İyi bir bulgu cümlesi
üç şey söylüyor: ne gördün, ne kadar güçlü, ve neyi söylemiyorsun.

> Sekiz kişilik bu veride çalışma saati ile not arasında güçlü bir ilişki
> var (korelasyon 0.98). Bursa'daki ortalama düşük görünüyor ama orada
> yalnızca iki kayıt var, bu yüzden şehir hakkında bir sonuç çıkarılamıyor.

Karşılaştır:

> Çalışmak notu artırıyor. Bursa'da eğitim kalitesi düşük.

İkincisi aynı veriden çıkarılmış gibi duruyor ama iki fazladan iddia
içeriyor: nedensellik ve iki kişilik bir gruptan bir şehre genelleme.

## Sıra

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1</b><br>shape, dtypes</span>
    <span class="arrow">→</span>
    <span class="node"><b>2</b><br>head</span>
    <span class="arrow">→</span>
    <span class="node"><b>3</b><br>isna</span>
    <span class="arrow">→</span>
    <span class="node"><b>4</b><br>describe</span>
    <span class="arrow">→</span>
    <span class="node"><b>5</b><br>value_counts</span>
    <span class="arrow">→</span>
    <span class="node"><b>6</b><br>groupby</span>
    <span class="arrow">→</span>
    <span class="node"><b>7</b><br>corr</span>
  </div>
  <figcaption>Ezberlenecek bir sıra değil, ama yeni bir veri açtığında nereden başlayacağını bilmek zaman kazandırıyor.</figcaption>
</figure>

Her adımda çıkan şey bir sonrakini yönlendiriyor. `describe`'da ortalama ile
medyan uzaksa aykırı değere bakıyorsun; `value_counts`'ta dengesiz bir grup
görüyorsan gruplamada dikkatli oluyorsun.

## Özet

- **EDA bir döngü:** soru → bak → bulgu → yeni soru.
- Sıra: `shape`/`dtypes` → `head` → `isna` → `describe` → `value_counts` →
  `groupby` → `corr`.
- **`describe` okunur:** ortalama ile medyanın farkı çarpıklığı, `std`
  yayılımı, `min`/`max` veri hatasını gösteriyor.
- **Grup ortalaması `count` olmadan okunmaz.** İki kişilik grup bir sonuç
  değil.
- **Korelasyon** birlikte hareketi ölçüyor, sebebi değil. Üçüncü bir sütun
  ikisini birden açıklıyor olabilir.
- **IQR kuralı** aykırı değeri kuralla buluyor: çeyrekler açıklığının 1.5
  katı dışı.
- Aykırı değer varken **medyan ortalamadan güvenilir**.
- Bulgu cümlesi neyi **söylemediğini** de söylüyor.
