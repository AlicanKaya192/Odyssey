# Karar Ağaçları

KNN "bu kayda en çok kim benziyor" diye soruyordu. Karar ağacı bambaşka bir
şey soruyor: **"hangi soruyu sorarsam grubu en iyi ayırırım?"**

Uzaklık yok, komşu yok. Yalnızca eşikler ve dallar var.

## Ağaç bir soru dizisi

Model şuna benziyor:

```
visits <= 18.5 ?
├── evet -> income <= 137500 ?
│          ├── evet -> ayrilir
│          └── hayir -> kalir
└── hayir -> ...
```

Yeni bir müşteri geldiğinde kök soruya cevap veriyorsun, o dala iniyorsun,
sonraki soruya cevap veriyorsun ve bir **yaprağa** varıyorsun. Yaprağın
etiketi tahmin.

**Bu yapının iki sonucu var:**

- **Model okunabiliyor.** Doğrusal regresyonun katsayıları soyut; ağacın
  kuralları cümleye çevrilebiliyor: "ayda 18'den az giriyor ve geliri
  137.500'ün altındaysa ayrılıyor."
- **Kural keskin.** 18.5 ziyaret ile 18.6 ziyaret arasında model için bir
  uçurum var; gerçekte yok. Ağaçların basamaklı yapısı buradan geliyor.

## Bölünme nasıl seçiliyor

Ağaç her adımda şunu yapıyor: **bütün özellikleri ve bütün olası eşikleri
deniyor**, her birinin grubu ne kadar iyi ayırdığını ölçüyor ve en iyisini
seçiyor.

"İyi ayırmak" bir sayıyla ölçülüyor: **safsızlık** (impurity).

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">gini = 0</span><span class="anat-body">grupta tek bir sınıf var — <b>saf</b></span></div>
    <div class="anat-row"><span class="anat-label">gini = 0.5</span><span class="anat-body">iki sınıf yarı yarıya — <b>en karışık</b></span></div>
    <div class="anat-row"><span class="anat-label">iyi bölünme</span><span class="anat-body">iki alt grubun safsızlığı, bölünmeden öncekinden <b>düşük</b></span></div>
  </div>
  <figcaption>Ağaç her adımda safsızlığı en çok düşüren soruyu seçiyor. Gelecekteki adımlara bakmıyor — buna "açgözlü" deniyor.</figcaption>
</figure>

`gini` yerine `entropy` de kullanılabiliyor; sonuçlar genelde çok yakın
çıkıyor. Regresyonda ölçü değişiyor: safsızlık yerine **varyans** (MSE)
düşürülüyor.

**Açgözlü olması bir sınır:** ağaç o anki en iyi bölünmeyi seçiyor, iki adım
sonrasını hesaba katmıyor. Bazen "şimdi biraz kötü ama sonra çok iyi" bir
bölünme kaçırılıyor.

## Ağacı okumak

Eğitilmiş bir ağacın kuralları metne dökülebiliyor:

```python
from sklearn.tree import export_text
print(export_text(model, feature_names=list(X.columns)))
```

```
|--- visits <= 18.50
|   |--- income <= 137500.00
|   |   |--- class: 1
|   |--- income >  137500.00
|   |   |--- class: 0
|--- visits >  18.50
|   |--- income <= 41500.00
|   |   |--- class: 0
|   |--- income >  41500.00
|   |   |--- class: 0
```

**Alt taraftaki iki yaprağa dikkat et: ikisi de `class: 0`.**

Bölünme etiketi değiştirmiyor. O zaman ağaç neden bölmüş?

Çünkü ağaç **etiketi** değil **safsızlığı** en iyiliyor. Sol yaprakta 20
kayıt var ve dağılım 11'e 9 (gini 0.495, neredeyse en karışık hâl); sağ
yaprakta 75 kayıt var ve dağılım 74'e 1 (gini 0.026, neredeyse saf).
İkisinin de çoğunluğu aynı sınıf ama **güven düzeyleri** bambaşka.

Bu ayrım `predict_proba` çağırdığında ortaya çıkıyor: soldaki yaprak %55
diyor, sağdaki %99.

## Ölçekleme hiçbir şey değiştirmiyor

Bölüm 06'da ölçeklemeyi atlamak KNN'i taban çizginin altına düşürmüştü:
0.64'e karşı 0.92. Aynı veride ağaç:

```
agac, olceklemesiz   0.80
agac, olcekli        0.80
```

**Birebir aynı.** Tek bir ondalık bile oynamıyor.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>KNN</h4>
      <p>Uzaklık hesaplıyor.<br>Sütunların ölçeği <b>her şeyi</b> değiştiriyor: 0.64 → 0.92</p>
    </div>
    <div class="versus-side">
      <h4>Ağaç</h4>
      <p>"Bu değer eşikten büyük mü" diye soruyor.<br>Ölçek eşiği kaydırıyor, <b>cevabı değiştirmiyor</b>: 0.80 → 0.80</p>
    </div>
  </div>
  <figcaption>Ölçekleme "her zaman yapılır" bir adım değil; hangi modelin neye baktığına bağlı.</figcaption>
</figure>

Sebebi basit: `income <= 137500` sorusu ölçeklendikten sonra
`income_scaled <= 0.42` oluyor. Eşik değişiyor, **sıralama** değişmiyor — ve
ağaç yalnızca sıralamayla ilgileniyor.

Aynı sebeple ağaçlar aykırı değerlere de dayanıklı: bir kayıt 100 kat büyük
olsa bile hâlâ "eşikten büyük" grubunda, o kadar.

## Derinlik: tanıdık bir düğme

```
derinlik   egitim   test
       1    0.807    0.820
       2    0.880    0.960
       3    0.933    0.800
       5    0.993    0.880
       8    1.000    0.880
    none    1.000    0.880
```

Bölüm 05'te aynı tabloyu görmüştün: **eğitim doğruluğu 1.000'e tırmanıyor**,
test doğruluğu takılıp kalıyor. Sınırsız derinlikte ağaç her kaydı ayrı bir
yaprağa koyup ezberliyor.

**Test sütunu yine zıplıyor:** 0.82 → 0.96 → 0.80 → 0.88. 50 kayıtlık bir
test kümesinde tek bir kayıt 0.02 oynatıyor ve bu tablo gürültüyle dolu.

Bu yüzden derinlik buradan seçilmiyor. Çapraz doğrulamayla:

```
derinlik   CV ort   CV std
       1    0.753    0.062
       2    0.827    0.049
       3    0.773    0.057
       5    0.813    0.086
    none    0.820    0.091
```

En iyi **derinlik 2** (0.827) ve yayılımı da en küçük (0.049). Bu sefer
seçim rahat: fark yayılıma göre anlamlı ve seçilen değer testte de en iyi
(0.96).

**Bölüm 06'daki durumun tersi.** Orada bütün `k` değerleri gürültü
aralığındaydı ve çapraz doğrulama ayırt edemiyordu; burada ayırt ediyor.
Aynı araç, iki farklı sonuç — bu yüzden **her seferinde yayılıma bakmak**
gerekiyor.

**İkinci düğme: `min_samples_leaf`.** Bir yaprakta en az kaç kayıt olacağını
söylüyor. Derinliği sınırlamadan da ezberi engelliyor: yaprakta en az 5
kayıt zorunluysa tek bir kaydı ezberleyen dal oluşamıyor.

## Özellik önemi

Ağaç, hangi sütunun ne kadar işe yaradığını söyleyebiliyor:

```python
for name, value in zip(X.columns, model.feature_importances_):
    print(name, round(value, 3))
```

```
age      0.169
income   0.398
visits   0.433
```

Bu sayılar, o sütunla yapılan bölünmelerin safsızlığı ne kadar düşürdüğünü
anlatıyor ve toplamları 1.

**Ama üç tuzağı var:**

**1. Önem sebep demek değil.** Önceki modüllerin kuralı burada da geçerli.
"En önemli değişken `visits`" cümlesi, ziyaret sayısını artırmanın müşteriyi
tuttuğu anlamına gelmiyor.

**2. İlişkili sütunlar önemi paylaşıyor.** İki sütun birbirinin neredeyse
aynısıysa ağaç birini seçiyor, öteki sıfıra yakın önem alıyor. "Bu sütun
işe yaramıyor" sonucu çıkarılıyor — oysa yalnızca ikizi seçilmiş.

**3. Çok değerli sütunlar şişiyor.** Sürekli sayısal bir sütunda binlerce
olası eşik var; kategorik bir sütunda birkaç tane. Ağaç ilkinde tesadüfen
iyi bir bölünme bulmakta daha şanslı ve önemi olduğundan yüksek çıkıyor.

Üçüncü tuzağın uç örneği: veriye **müşteri numarası** koyarsan ağaç onunla
her kaydı ayırabiliyor ve o sütun en önemli görünüyor.

## Ağaçların asıl zayıflığı: kararsızlık

Aynı veriden birkaç satır çıkarıp ağacı yeniden eğitirsen **bambaşka bir
ağaç** çıkabiliyor. Kök bölünmesi bile değişebiliyor.

Sebebi açgözlülük: ilk bölünme bir eşiğe kıl payı karar veriyor ve o karar
değişince altındaki her şey değişiyor. Küçük bir veri değişikliği, ağacın
tamamını yeniden şekillendiriyor.

**Bu, tek bir ağacın güvenilirliğini düşürüyor.** Model bugün "en önemli
sütun `visits`" diyor, on satır sonra "en önemli sütun `income`" diyebiliyor.

Çözüm bir sonraki bölümde: **çok sayıda ağaç kurup ortalamasını almak.**
Rastgele orman ve gradyan artırma tam olarak bunu yapıyor ve kararsızlığı
bir dezavantajdan avantaja çeviriyor.

## Ağaç mı KNN mi

Aynı veride üç modelin sonucu:

```
taban cizgi           0.70
karar agaci (d=3)     0.80
KNN (k=25, olcekli)   0.92
```

**Bu veride KNN kazanıyor.** Ağaç taban çizgiyi geçiyor ama KNN'in
gerisinde kalıyor.

Bu, ağaçların kötü olduğu anlamına gelmiyor — veriye bağlı. Ağaçlar
basamaklı kurallarla çalışıyor; sınır düzgün ve eğriyse basamaklarla taklit
etmek zorunda kalıyorlar. Bölüm 05'te de aynısını görmüştük: araba
verisinde ağacın hatası 64, doğrusal regresyonunki 16.5'ti.

**Model seçimi ölçüm işi.** Hangisinin kazanacağı verinin şekline bağlı ve
bunu önceden bilmenin yolu yok.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Ağaç iyi olduğunda</h4>
      <p>Kurallar keskin ve basamaklı<br>Kategorik sütunlar çok<br>Yorumlanabilirlik önemli<br>Ölçekleme yapılamıyor</p>
    </div>
    <div class="versus-side">
      <h4>KNN iyi olduğunda</h4>
      <p>Sınırlar düzgün ve eğri<br>Az sayıda sayısal özellik<br>Yerel benzerlik anlamlı<br>Veri küçük</p>
    </div>
  </div>
  <figcaption>İkisi de sınırın şekli hakkında varsayım yapmıyor ama farklı şekilleri farklı kolaylıkla yakalıyorlar.</figcaption>
</figure>

## Ağacın avantajları

| Avantaj | Neden |
|---|---|
| Ölçekleme gerekmiyor | Sıralamaya bakıyor, uzaklığa değil |
| Aykırı değere dayanıklı | Uç değer yalnızca "eşiğin üstünde" |
| Okunabilir | Kurallar cümleye çevrilebiliyor |
| Kategorik ve sayısal birlikte | Aynı ağaçta ikisi de olabiliyor |
| Etkileşimleri yakalıyor | "Genç **ve** az giren" gibi birleşik kurallar doğal |

Son satır önemli: doğrusal regresyon her sütuna ayrı katsayı veriyor ve
"genç olmak" ile "az girmek" birleşince ne olduğunu ayrıca söylemek
gerekiyor. Ağaç bunu kendiliğinden kuruyor, çünkü dallar zaten iç içe
koşullar.

## Bu bölümde neyi atladık

- **Budama (pruning).** `ccp_alpha` parametresiyle ağaç önce büyütülüp sonra
  gereksiz dalları kesiliyor; derinlik sınırlamaktan daha esnek bir yol.
- **Regresyon ağaçları.** `DecisionTreeRegressor` aynı mantıkla çalışıyor,
  yalnızca yaprakta sınıf yerine **ortalama** duruyor ve safsızlık yerine
  varyans düşürülüyor.
- **Kategorik sütunların doğrudan işlenmesi.** sklearn hâlâ kodlama
  istiyor; bazı kütüphaneler (LightGBM gibi) kategoriyi doğrudan alabiliyor.

Bir sonraki bölüm, bu bölümün zayıflığını çözüyor: tek bir ağacın
kararsızlığı, **çok sayıda ağacın** ortalamasında kayboluyor.
