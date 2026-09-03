# KNN

Bölüm 00'da bir alıştırmada en yakın komşuyu elle bulmuştun. O alıştırmanın
adı vardı: **KNN**, yani K-En Yakın Komşu.

Bu bölümde onu gerçek veride kullanacaksın — ve bu modelin ötekilerden ne
kadar farklı çalıştığını göreceksin.

## Öğrenmeyen model

sklearn'in üç adımı burada da aynı: kur, `fit`, `predict`. Ama `fit`'in
içinde olan şey bambaşka.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Öteki modeller</h4>
      <p><code>fit</code> uzun sürer, kural çıkarılır.<br><code>predict</code> hızlıdır: formülü uygula.</p>
    </div>
    <div class="versus-side">
      <h4>KNN</h4>
      <p><code>fit</code> anında biter: veri <b>saklanır</b>.<br><code>predict</code> pahalıdır: her satıra uzaklık ölçülür.</p>
    </div>
  </div>
  <figcaption>Bu yüzden KNN'e "tembel" model deniyor. Maliyet eğitimden tahmin anına kayıyor.</figcaption>
</figure>

Doğrusal regresyon eğitimden sonra iki sayı tutuyordu (`coef_`,
`intercept_`) ve veriyi unutuyordu. KNN hiçbir şey öğrenmiyor: **bütün
eğitim verisini saklıyor** ve her tahminde ona bakıyor.

Pratik sonucu: eğitim verisi büyüdükçe KNN'in **tahmini** yavaşlıyor. Bir
milyon satırlık veride her tahmin bir milyon uzaklık hesabı demek.

## Tahmin nasıl üretiliyor

Üç adım:

1. Yeni noktanın **her eğitim satırına** uzaklığını hesapla.
2. En yakın **k** tanesini al.
3. Sınıflandırmada **oy çokluğu**, regresyonda **ortalama**.

Uzaklık genelde Öklid: farkların karelerinin toplamının karekökü.

Sekiz noktalı küçük bir örnekte, yeni bir nokta için en yakınlar şöyle
sıralanıyor:

```
uzakliklar: [0.71, 1.0, 2.92, 3.61, 4.03, 4.24, 4.3, 4.61]

k=1  ['A']                     -> A
k=3  ['A', 'B', 'B']           -> B
k=5  ['A', 'B', 'B', 'A', 'B'] -> B
```

**Cevap `k` ile değişiyor.** `k=1` A diyor, `k=3` B. Aynı veri, aynı nokta,
farklı sonuç. Demek ki `k` küçük bir ayrıntı değil, modelin kendisi.

## Ölçekleme burada zorunlu

Bölüm 04'te ölçeklemenin bazı modelleri etkilediğini, bazılarını
etkilemediğini görmüştük. KNN etkilenenlerin başında geliyor ve etki
tahmin edebileceğinden büyük.

Müşteri verisinde üç sütun var: `age` (18-70), `income` (12.000-200.000),
`visits` (1-50).

```
taban cizgi (en sik sinif)      0.70
KNN, olceklemesiz               0.64
KNN, olcekli                    0.92
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Ölçeklemesiz</h4>
      <p>Doğruluk <b>0.64</b><br>Taban çizginin <b>altında</b> — hiçbir şey öğrenmeyen bir satır bundan iyi.</p>
    </div>
    <div class="versus-side">
      <h4>Ölçekli</h4>
      <p>Doğruluk <b>0.92</b><br>Taban çizgiyi açık farkla geçiyor.</p>
    </div>
  </div>
  <figcaption>Aynı model, aynı veri, aynı k. Tek fark sütunların ortak bir ölçeğe getirilmesi.</figcaption>
</figure>

**Neden bu kadar sert:** uzaklık hesabında `income` sütunundaki iki müşteri
arasındaki fark 100.000 olabiliyor; `visits` sütunundaki fark en fazla 49.
Karelerinin toplamında ikincisi görünmüyor bile.

Ölçeklemesiz KNN aslında **yalnızca gelire bakıyor.** Öteki iki sütun
modele verilmiş ama kullanılmıyor.

**Bu, ölçeklemeyi unutmanın modeli taban çizginin altına düşürebildiği
anlamına geliyor** — yani model kurmamış olmaktan daha kötü bir sonuç.

```python
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

`fit` eğitimde, `transform` ikisinde. Bölüm 04'ün kuralı burada da geçerli.

## `k` neyi ayarlıyor

`k` bir **hiperparametre**: model öğrenmiyor, sen seçiyorsun. Ve doğrudan
karmaşıklığı ayarlıyor.

```
 k   egitim   test
 1    1.000   0.820
 3    0.940   0.860
 5    0.940   0.920
 9    0.927   0.900
15    0.920   0.880
25    0.927   0.920
```

**`k=1`'de eğitim doğruluğu 1.000.** Şaşırtıcı değil: her eğitim noktasının
kendine en yakın komşusu kendisidir. Model eğitim verisini kusursuz
biliyor ve testte 0.820'ye düşüyor — bölüm 05'in aşırı öğrenme tablosunun
ders kitabı örneği.

`k` büyüdükçe eğitim doğruluğu düşüyor, test doğruluğu önce yükseliyor.
Çok büyük `k` ise sınırları bulanıklaştırıyor: `k` bütün veri sayısına
eşit olsaydı model her şeye en sık sınıfı derdi — yani taban çizgiye
dönerdi.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">küçük k</span><span class="anat-body">gürültüye duyarlı; tek bir aykırı komşu kararı değiştiriyor</span></div>
    <div class="anat-row"><span class="anat-label">büyük k</span><span class="anat-body">sınırlar bulanıklaşıyor; küçük gruplar kayboluyor</span></div>
    <div class="anat-row"><span class="anat-label">k = n</span><span class="anat-body">model taban çizgiye dönüşüyor: her şeye en sık sınıf</span></div>
  </div>
  <figcaption>Tek sayı seçmek yaygın bir alışkanlık: ikili sınıflandırmada oylar eşit kalmıyor.</figcaption>
</figure>

## `k` nasıl seçilir — ve bir tuzak

Bölüm 05'in kuralı: hiperparametre **çapraz doğrulamayla** seçilir, test
kümesine bakılarak değil.

Eğitim tarafında çapraz doğrulama sonuçları:

```
 k   CV ort   CV std
 1    0.913    0.040
 3    0.893    0.039
 5    0.900    0.052
 7    0.873    0.057
 9    0.880    0.062
15    0.893    0.053
25    0.880    0.054
```

En yüksek ortalama `k=1`'de: 0.913. Seçim tamam gibi görünüyor.

**Ama yayılıma bak: 0.040.** En iyi ile en kötü arasındaki fark 0.040
(0.913 - 0.873) ve yayılım da 0.040. Yani **bütün k değerleri birbirinin
gürültü aralığında.** Çapraz doğrulama burada hiçbirini ayırt edemiyor.

Bu durumda ne yapılır? Bölüm 05'in cümlesi: "farkın yayılımdan büyük olması
gerekiyor." Değilse seçim başka ölçütle yapılıyor — ve KNN'de o ölçüt
belli: **daha büyük `k` daha sağlam**, çünkü tek bir komşuya bağlı değil.

Test kümesinde ne olduğuna bakalım:

```
CV kazanani  k=1   ->  test 0.820
gurultu icinde en buyuk k=25  ->  test 0.920
```

**Naif seçim on puan kaybettiriyor.** `k=1` çapraz doğrulamada kıl payı
öndeydi ve o kıl payı gürültüydü.

Bu, çapraz doğrulamanın işe yaramadığı anlamına gelmiyor. Tersine: yayılımı
da verdiği için "bu fark anlamsız" diyebildik. Ortalamaya tek başına
baksaydık `k=1`'i seçip yanılacaktık.

## Karar sınırı

`k`'nın ne yaptığını en iyi gösteren şey, modelin çizdiği **sınır**.

İki özellikli bir modelde (`income` ve `visits`) düzlemin her noktası için
tahmin üretip renklendirdiğimizde şunu görüyoruz:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>k = 1</h4>
      <p>Sınır <b>parçalı</b>: tek tek noktaların etrafında adacıklar var. Model her aykırı kaydı ciddiye almış.</p>
    </div>
    <div class="versus-side">
      <h4>k = 15</h4>
      <p>Sınır <b>düzgün</b>: tek bir eğri. Aykırı kayıtlar çoğunluk içinde eriyor.</p>
    </div>
  </div>
  <figcaption>İkisinin de test doğruluğu 0.90. Aynı sayı, bambaşka iki model — sayı tek başına modeli anlatmıyor.</figcaption>
</figure>

**Bu, tek bir ölçünün neden yetmediğinin görsel kanıtı.** İki model aynı
doğruluğu veriyor ama biri gürültüyü ezberlemiş, öteki genel eğilimi
yakalamış. Yeni veri geldiğinde ikisi çok farklı davranacak.

## Boyut laneti

KNN'in en ciddi sınırı: **özellik sayısı arttıkça uzaklık anlamını
kaybediyor.**

Sezgiye aykırı ama şöyle: çok boyutlu bir uzayda noktalar birbirinden
neredeyse **eşit** uzaklıkta oluyor. En yakın komşuyla en uzak komşu
arasındaki fark eriyor ve "en yakın" kelimesi anlamsızlaşıyor.

Pratik sonucu: elli sütunlu bir veride KNN genelde zayıf kalıyor. Üç beş
özellikte çok iyi çalışan yöntem, otuzda çöküyor.

Çözümler: özellik sayısını azaltmak, boyut indirgeme uygulamak (10. bölüm),
ya da bu sorundan etkilenmeyen bir modele geçmek — ağaçlar gibi.

## Regresyonda da çalışıyor

Aynı fikir sayısal hedefte de geçerli: en yakın `k` komşunun hedef
değerlerinin **ortalaması**.

```python
from sklearn.neighbors import KNeighborsRegressor
model = KNeighborsRegressor(n_neighbors=5)
```

Bölüm 04'te bunu görmüştün: araba verisinde ölçeklemesiz KNN 171.49,
ölçekli 51.48 veriyordu.

## Ağırlıklı oylama

Varsayılan olarak beş komşunun oyu eşit sayılıyor. Uzak komşunun oyunu
azaltmak da mümkün:

```python
KNeighborsClassifier(n_neighbors=5, weights="distance")
```

Mantıklı görünüyor ama **otomatik olarak daha iyi değil.** Bu veride:

```
weights="uniform"    0.92
weights="distance"   0.88
```

Daha kötü çıktı. Sebebi şu: mesafe ağırlığı çok yakın bir komşuya aşırı
güç veriyor ve model `k=1`'e yaklaşıyor — yani ezberlemeye.

Her ayar gibi bu da **denenerek** seçiliyor.

## KNN ne zaman iyi bir seçim

| İyi | Kötü |
|---|---|
| Az özellik (2-10 arası) | Çok özellik (boyut laneti) |
| Sınırlar karmaşık ve eğri | Çok büyük veri (tahmin yavaş) |
| Küçük ve orta veri | Eksik değer var (uzaklık hesaplanamıyor) |
| Hızlı bir taban çizgi gerekiyor | Yorumlanabilirlik önemli |

**Yorumlanabilirlik konusunda ilginç bir yanı var:** KNN neden öyle karar
verdiğini söyleyemiyor (katsayı yok, kural yok) ama **hangi komşulara
baktığını** gösterebiliyor. "Bu müşteriye ayrılacak dedim çünkü ona en
benzeyen beş müşterinin dördü ayrılmıştı" cümlesi kurulabiliyor — bazı
işlerde bu bir katsayıdan daha ikna edici.

## Bu bölümde neyi atladık

- **Farklı uzaklık ölçüleri.** Öklid varsayılan; `metric="manhattan"` ya da
  metin verisi için kosinüs benzerliği de kullanılıyor.
- **Hızlandırma.** sklearn `algorithm` parametresiyle KD-tree ve ball-tree
  kullanabiliyor; büyük veride tahmin süresini düşürüyor.
- **Eksik değer.** KNN uzaklık hesapladığı için eksik değerle çalışamıyor;
  önce doldurulması gerekiyor (bölüm 04).

Bir sonraki bölümde bambaşka bir yaklaşım var: uzaklığa değil **sorulara**
dayanan modeller — karar ağaçları.
