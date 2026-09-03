# İlk Model

Önceki bölümde bir modelin ne olduğunu, veriyi neden ikiye ayırdığımızı ve
taban çizginin ne işe yaradığını konuştuk. Eşiği döngüyle arayıp bir model
de eğittin.

Şimdi aynı işi kütüphaneyle yapacaksın. Değişen şey fikir değil, yazdığın
satır sayısı: elle yirmi satırda yaptığın arama, üç satıra iniyor.

## sklearn'in üç adımı

Makine öğrenmesi kütüphanesinin adı **scikit-learn**, kodda `sklearn` diye
geçiyor. İçindeki her model aynı üç adımı taşıyor.

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1 · kur</b><br><code>LinearRegression()</code></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>2 · öğren</b><br><code>fit(X, y)</code></span>
    <span class="arrow">→</span>
    <span class="node ok"><b>3 · tahmin et</b><br><code>predict(X_new)</code></span>
  </div>
  <figcaption>Doğrusal regresyon, karar ağacı, KNN — hepsi bu üçünü taşıyor. Model değiştirmek çoğu zaman ilk satırı değiştirmek demek.</figcaption>
</figure>

Sekiz evin metrekaresi ve fiyatı elimizde olsun:

```python
from sklearn.linear_model import LinearRegression

areas = [50, 60, 70, 80, 90, 100, 110, 120]
prices = [155, 178, 205, 228, 250, 278, 300, 325]

model = LinearRegression()
model.fit([[a] for a in areas], prices)

print(model.predict([[95]]))   # [264.16666667]
```

Üç satır. Modelin 95 metrekarelik bir ev için söylediği rakam **264**.

Bu sayı veride yok — 90 var, 100 var, 95 yok. Model aradaki kuralı çıkardı
ve o kuralı hiç görmediği bir girdiye uyguladı. Bölüm boyunca peşinde
olduğumuz şey buydu.

## Modelin öğrendiği şey iki sayı

`fit` bittiğinde model bir şey öğrenmiş oluyor ve o şeye bakabiliyorsun:

```python
print(model.coef_[0])     # 2.4285714285714284
print(model.intercept_)   # 33.35714285714289
```

Öğrendiği kural şu:

```
fiyat = 2.43 x metrekare + 33.36
```

**`coef_` eğim, `intercept_` kesişim.** Metrekare bir birim artınca fiyatın
ne kadar arttığını `coef_` söylüyor: 2.43. Sıfır metrekarelik bir evin
"fiyatı" ise `intercept_` — anlamsız bir sayı, ama doğrunun nereden
geçtiğini belirliyor.

Önceki bölümde eşiği döngüyle arıyordun. `fit` de tam olarak bunu yapıyor:
hatayı en aza indiren eğim ve kesişimi arıyor. Farkı, aramayı döngüyle
değil doğrudan hesapla yapması.

**Alt çizgi bir kural:** `coef_` ve `intercept_` sonunda alt çizgi
taşıyor. sklearn'de bu, "bu değer **eğitimden sonra** oluştu" demek.
`fit` çağrılmadan onlara bakarsan hata alıyorsun — çünkü henüz yoklar.

## `X` iki boyutlu olmak zorunda

Yukarıdaki `[[a] for a in areas]` gözünü tırmalamış olabilir. Neden düz
liste değil de her sayı ayrı bir listede?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">X</span><span class="anat-body">bir <b>tablo</b>: her satır bir örnek, her sütun bir özellik → iki boyutlu</span></div>
    <div class="anat-row"><span class="anat-label">y</span><span class="anat-body">tek bir <b>sütun</b>: her örneğin doğru cevabı → tek boyutlu</span></div>
  </div>
  <figcaption>Tek özellikle çalışsan bile X bir tablo. Tek sütunlu bir tablo yine tablodur.</figcaption>
</figure>

sklearn her zaman bir **tablo** bekliyor, çünkü modeller çok özellikle
çalışabilsin diye yazılmışlar. Tek özellik, tek sütunlu bir tablo demek.

pandas tarafında bu ayrım köşeli parantez sayısıyla yapılıyor:

```python
X = df[["area"]]   # DataFrame — tablo, iki boyutlu   dogru
X = df["area"]     # Series    — sutun, tek boyutlu   hata
y = df["price"]    # y icin Series dogru
```

Tek parantez yazıp `fit` çağırırsan sklearn şunu söylüyor:

```
ValueError: Expected 2D array, got 1D array instead
```

**Bu hatayı herkes görüyor.** Gördüğünde çevirisi hazır olsun: "X'i tablo
olarak vermemişsin."

## Gerçek veriyle: ayır, eğit, ölç

Sekiz satırlık listede test kümesi yoktu. Gerçek bir dosyada bütün akış
kuruluyor:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("homes.csv")
X = df[["area"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
prediction = model.predict(X_test)

print(mean_absolute_error(y_test, prediction))   # 18.5
```

Birkaç ayrıntı:

- **`train_test_split` dört şey döndürüyor** ve sırası sabit:
  `X_train, X_test, y_train, y_test`. Sırayı karıştırmak sessiz bir hata —
  kod çalışıyor, sonuç saçmalıyor.
- **`test_size=0.25`** verinin dörtte birini teste ayırıyor. 0.2 ile 0.3
  arası yaygın; azı ölçümü güvenilmez, çoğu eğitimi zayıflatıyor.
- **`random_state=42`** ayrımı sabitliyor. Vermezsen her çalıştırmada
  başka bir sonuç çıkıyor ve "iyileştim mi, şansım mı yaver gitti"
  ayırt edilemiyor. 42 bir gelenek, sihirli bir sayı değil.
- Bölme **rastgele**, baştan kesme değil. Dosya metrekareye göre sıralıysa
  ilk %75'i almak eğitimi küçük evlere, testi büyüklere ayırırdı.

## Ölçüm tek başına bir şey söylemiyor

`18.5` ne demek? İyi mi kötü mü?

Önceki bölümün cevabı burada işe yarıyor: **taban çizgiye bak.**

```python
baseline = y_train.mean()
baseline_mae = mean_absolute_error(y_test, [baseline] * len(y_test))

print(baseline_mae)   # 82.29
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Taban çizgi</h4>
      <p>Her eve <b>312.87</b> diyor.<br>Ortalama hata: <b>82.29</b></p>
    </div>
    <div class="versus-side">
      <h4>Model</h4>
      <p>Metrekareye bakıp söylüyor.<br>Ortalama hata: <b>18.50</b></p>
    </div>
  </div>
  <figcaption>Hata %77 azaldı. "18.5 iyi mi" sorusunun cevabı buradan geliyor, sayının kendisinden değil.</figcaption>
</figure>

Model taban çizgiyi geçti; öğrendiği bir şey var. Geçemeseydi, üç satırlık
kod ortalamadan daha kötü tahmin ediyor olurdu ve atılması gerekirdi.

**Sıralamayı bozma:** taban çizgi modelden **önce** kurulur. Sonra
kurulduğunda, modelin sayısını görmüş oluyorsun ve "olsa olsa şu kadardır"
diye kendini kandırman kolaylaşıyor.

## İkinci özellik

Elimizdeki dosyada `age` sütunu da var — evin yaşı. Ekleyelim:

```python
X = df[["area", "age"]]
```

Kodun geri kalanı **aynı**. Tek değişen, `X`'in iki sütunlu olması.

```
tek ozellik   MAE 18.50
iki ozellik   MAE  7.13
```

Hata yarıdan fazla düştü. Model artık iki katsayı öğrendi:

```python
print(model.coef_)   # [ 2.77 -3.35]
```

**Katsayının işareti bir şey anlatıyor:** metrekare artınca fiyat artıyor
(+2.77), yaş artınca fiyat düşüyor (-3.35). Sayılar veriden çıktı, kimse
modele "eski evler daha ucuzdur" demedi.

Ama iki uyarı:

- **Katsayı sebep söylemiyor.** "Yaş fiyatı düşürüyor" değil, "yaşı büyük
  olan evlerin fiyatı düşük çıkıyor" doğru cümle. Önceki modülün kuralı
  burada da geçerli.
- **Katsayılar birbiriyle kıyaslanamaz.** 3.35 > 2.77 diye "yaş daha
  önemli" denmiyor: metrekare 45 ile 165 arasında geziniyor, yaş 0 ile 30
  arasında. Katsayı, sütunun **birimine** bağlı. Kıyaslamak için önce
  ölçeklemek gerekiyor — 4. bölümün konusu.

## Bir sayı daha: `score`

Her sklearn modelinde `score` var. Regresyonda **R²** döndürüyor:

```python
print(model.score(X_test, y_test))   # 0.943
```

R² kabaca "hedefteki değişkenliğin ne kadarını açıklayabildin" demek.
1'e yakın iyi, 0 taban çizgi kadar, negatif taban çizgiden **kötü**.

MAE ile arasındaki fark pratik: MAE hedefin biriminde konuşuyor ("ortalama
18.5 bin lira yanılıyorum"), R² birimsiz bir oran. Rapora ikisi birden
yazılıyor — biri anlaşılır, öteki karşılaştırılabilir.

## Bütün akış tek yerde

<figure class="fig">
  <div class="flow">
    <span class="node"><b>oku</b><br><code>read_csv</code></span>
    <span class="arrow">→</span>
    <span class="node"><b>ayır</b><br><code>train_test_split</code></span>
    <span class="arrow">→</span>
    <span class="node"><b>taban çizgi</b><br><code>y_train.mean()</code></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>eğit</b><br><code>fit</code></span>
    <span class="arrow">→</span>
    <span class="node ok"><b>ölç</b><br><code>mean_absolute_error</code></span>
  </div>
  <figcaption>Bu sıra bundan sonraki bütün bölümlerde aynı kalıyor. Değişen yalnızca dördüncü kutunun içindeki model.</figcaption>
</figure>

Doğrusal regresyon yerine karar ağacı kurmak istesen, değişecek tek satır
bu:

```python
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()
```

Geri kalan her şey — ayırma, eğitme, ölçme — olduğu gibi kalıyor. İşte bu
yüzden sklearn'in üç adımını bir kez öğrenmek yetiyor.

## Bu bölümde neyi atladık

Dürüst olmak gerekirse birkaç şeyin üstünden geçtik:

- **Doğrusal regresyon her veriye uymaz.** Fiyat metrekareyle düz bir
  doğru boyunca artmıyorsa bu model yetersiz kalıyor. 7. ve 8. bölümde
  eğri ilişkileri yakalayan modeller var.
- **Eksik değer ve metin sütunları modele giremiyor.** Dosyamız temizdi;
  gerçek veri olmuyor. 4. bölümün konusu.
- **Tek bir ayrımın sonucu şansa bağlı.** `random_state=42` yerine 7
  yazsan MAE değişir. Daha güvenilir ölçüm için çapraz doğrulama var —
  5. bölüm.

Şimdilik elinde çalışan bir akış var ve o akış taban çizgiyi geçiyor. Geri
kalanı bunun üstüne biniyor.
