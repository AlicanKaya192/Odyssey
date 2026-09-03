# Topluluk Yöntemleri

Önceki bölüm bir zayıflıkla bitti: **tek bir ağaç kararsız.** Veriden birkaç
satır çıkarsan kök bölünmesi bile değişebiliyor.

Bu bölümün fikri şaşırtıcı derecede basit: **çok sayıda ağaç kur, hepsine
sor, çoğunluğa uy.**

## Önce kararsızlığı ölçelim

Eğitim verisinden her seferinde farklı bir %10'u çıkarıp ağacı yeniden
eğitelim:

```
agac  test skorlari: [0.92, 0.88, 0.78, 0.80, 0.80, 0.84]
kok esigi          : [16.5, 15.5, 16.5, 18.5, 28.5, 18.5]
```

**Skor 0.78 ile 0.92 arasında geziniyor** — 14 puanlık bir aralık. Veri
aynı veri, model aynı model; değişen yalnızca hangi satırların düştüğü.

Daha rahatsız edici olan ikinci satır: **kök bölünmesinin eşiği 15.5'ten
28.5'e çıkıyor.** Yani modelin kuralı da değişiyor. Dün "ayda 16'dan az
girenler" diyen model, bugün "28'den az girenler" diyor.

Aynı deneyde orman:

```
orman test skorlari: [0.90, 0.84, 0.86, 0.90, 0.90, 0.92]
```

**8 puanlık aralık, 14 yerine.** Aynı gürültü, yarı yarıya sönmüş.

## Fikir: torbalama (bagging)

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Eğitim verisi</b></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>N tane rastgele örneklem</b><br>her biri farklı satırlar</span>
    <span class="arrow">→</span>
    <span class="node"><b>N tane ağaç</b><br>her biri kendi örnekleminde</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Oy çokluğu</b></span>
  </div>
  <figcaption>Her ağaç veriyi biraz farklı görüyor, dolayısıyla biraz farklı yanılıyor. Ortalama alındığında yanılmalar birbirini söndürüyor.</figcaption>
</figure>

Örneklemler **yerine koyarak** çekiliyor: aynı satır bir örneklemde iki kez
görünebiliyor, başka birinde hiç görünmeyebiliyor. Buna **bootstrap**
deniyor ve "bagging" adı da buradan geliyor (bootstrap aggregating).

**Neden işe yarıyor:** tek bir ağacın hatası büyük ölçüde **rastgele** —
şu satır düştü diye eşik kaydı, bu satır girdi diye dal değişti. Rastgele
hatalar ortalama alındığında birbirini götürüyor. Sistematik hatalar
götürmüyor, ama onlar zaten model seçimiyle ilgili.

## Rastgele orman

Rastgele orman, torbalamaya **ikinci bir rastgelelik** ekliyor: her
bölünmede bütün özellikler değil, **rastgele seçilen bir alt kümesi**
deneniyor.

Bu tuhaf görünüyor — neden modeli kasıtlı olarak kısıtlayasın?

Çünkü kısıtlamazsan bütün ağaçlar **birbirine benziyor.** Veride çok güçlü
bir özellik varsa her ağaç kökte onu seçiyor ve ortalama alınacak bir
çeşitlilik kalmıyor. Özellikleri saklamak ağaçları birbirinden
farklılaştırıyor.

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
```

**Ölçekleme yine gerekmiyor** — içindekilerin hepsi ağaç.

## Kaç ağaç

```
agac sayisi   egitim   test
          1    0.947    0.720
          5    0.993    0.840
         25    1.000    0.900
        100    1.000    0.900
        300    1.000    0.900
```

**Tek ağaçla 0.72, 25 ağaçla 0.90.** Sonra düzleşiyor: 100 ve 300 ağaç aynı
sonucu veriyor.

**Buradaki en önemli şey ne olmadığı:** ağaç sayısını artırmak aşırı
öğrenmeye yol açmıyor. Eğitim doğruluğu 1.000'de sabit kalıyor ama test
doğruluğu **düşmüyor**. Her ağacın ezberi ötekilerin ezberiyle
kesişmediği için ortalama temiz kalıyor.

Yani `n_estimators` bir denge parametresi değil, bir **maliyet**
parametresi: daha çok ağaç = daha yavaş, belli bir noktadan sonra daha iyi
değil. 100-300 arası yaygın bir başlangıç.

## Artırma (boosting): farklı bir fikir

Ormanda ağaçlar **paralel** ve birbirinden habersiz. Artırmada ise
**sırayla** kuruluyorlar ve her yeni ağaç, öncekilerin **yanıldığı yerlere**
odaklanıyor.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Orman (torbalama)</h4>
      <p>Ağaçlar paralel, bağımsız.<br>Amaç: <b>varyansı düşürmek</b>.<br>Ağaçlar derin ve güçlü.</p>
    </div>
    <div class="versus-side">
      <h4>Artırma</h4>
      <p>Ağaçlar sırayla, birbirini düzeltiyor.<br>Amaç: <b>yanlılığı düşürmek</b>.<br>Ağaçlar sığ ve zayıf.</p>
    </div>
  </div>
  <figcaption>Biri "çok sayıda iyi tahmin ortalanırsa gürültü söner" diyor; öteki "her adımda kalan hatayı biraz daha azalt" diyor.</figcaption>
</figure>

```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(random_state=42)
```

Artırmanın kritik ayarı `learning_rate`: her ağacın düzeltmeye ne kadar
katkı vereceği. Küçük değer daha güvenli ama daha çok ağaç istiyor.
`n_estimators` ile birlikte ayarlanıyor.

**Artırma aşırı öğrenebiliyor** — ormandan farklı olarak. Ağaç sayısını
artırmak bir noktadan sonra test skorunu düşürüyor, çünkü model kalan
gürültüyü de düzeltmeye çalışıyor.

## Karşılaştırma — ve bir tuzak

Aynı veride üç model:

```
             test    CV ortalama   CV yayilim
taban        0.700
agac (d=2)   0.960      0.827        0.049
orman        0.900      0.867        0.063
artirma      0.880      0.873        0.053
```

**Test sütununa bakarsan ağaç kazanıyor: 0.96.** Ormanı da artırmayı da
geçiyor. O zaman bütün bu topluluk işi neye yarıyor?

**Yaramıyor — eğer o sayıya inanırsan.**

Bölüm 05'ten hatırla: 50 kayıtlık bir test kümesinde tek bir kayıt 0.02
oynatıyor. 0.96, derinlik taramasında gördüğümüz zıplamanın tepe noktası;
gerçek bir üstünlük değil, şanslı bir çekiliş.

**Çapraz doğrulama sütununa bak:** ağaç 0.827, orman 0.867, artırma 0.873.
Sıralama tersine dönüyor ve bu sefer **beş ölçümün ortalaması** konuşuyor.

Bu, modülün en çok tekrarlanan dersi: **tek bir sayı bir model hakkında
karar verdirmez.**

## Özellik önemi daha kararlı

Bölüm 07'de ağacın `age` sütununa 0.0 önem verdiğini görmüştük — derinlik 2
olduğu için sıra ona hiç gelmemişti. Orman:

```
agac  : age 0.000   income 0.454   visits 0.546
orman : age 0.232   income 0.344   visits 0.424
```

**Ormanda sıfır önem alan sütun yok.** Yüzlerce ağaç var ve her biri farklı
özellik alt kümeleriyle çalıştığı için `age` de defalarca deneniyor. Gerçek
katkısı ortaya çıkıyor.

**Bu, tek ağacın "bu sütun işe yaramıyor" demesinin neden güvenilmez
olduğunu gösteriyor.** Ormanın önem sıralaması hem daha kararlı hem daha
adil.

Yine de aynı uyarılar geçerli: **önem sebep demek değil**, ilişkili sütunlar
hâlâ önemi paylaşıyor ve çok değerli sütunlar hâlâ şişiyor.

## Bedava doğrulama: OOB

Torbalamanın hoş bir yan ürünü var. Her ağaç, eğitim verisinin yaklaşık
üçte birini **hiç görmüyor** (bootstrap örneklemine düşmeyen satırlar).
O satırlar o ağaç için bir test kümesi.

```python
model = RandomForestClassifier(n_estimators=200, oob_score=True,
                               random_state=42)
model.fit(X_train, y_train)
print(model.oob_score_)
```

```
agac sayisi   oob_score   test
         10      0.873    0.860
         50      0.880    0.880
        200      0.887    0.900
```

**OOB, ayrı bir doğrulama kümesi ayırmadan tahmin veriyor** ve test
skoruna oldukça yakın çıkıyor. Çapraz doğrulamanın ucuz alternatifi:
zaten eğitilen ağaçlardan hesaplanıyor, ek eğitim gerekmiyor.

Yine de test kümesinin yerini almıyor — OOB eğitim verisinden geliyor ve
son ölçüm hâlâ el değmemiş testte yapılıyor.

## Bedeli ne

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">hız</span><span class="anat-body">200 ağaç = 200 kat eğitim; tahmin de yavaşlıyor</span></div>
    <div class="anat-row"><span class="anat-label">okunabilirlik</span><span class="anat-body"><b>kaybediliyor</b> — 200 ağacın kuralını cümleye çeviremezsin</span></div>
    <div class="anat-row"><span class="anat-label">bellek</span><span class="anat-body">her ağaç ayrı ayrı saklanıyor</span></div>
  </div>
  <figcaption>Bölüm 07'nin en büyük avantajı burada gidiyor: tek bir ağacın kuralları paydaşa anlatılabiliyordu, ormanınki anlatılamıyor.</figcaption>
</figure>

Yorumlanabilirlik gerçekten gerekiyorsa iki yol var: tek bir sığ ağacı
**açıklama** olarak yanında sunmak, ya da özellik önemi ve kısmi bağımlılık
gibi araçlarla ormanı dolaylı anlatmak.

## Hangisi ne zaman

| Durum | Seçim |
|---|---|
| Hızlı, sağlam bir başlangıç | **Rastgele orman** |
| En yüksek doğruluk, ayar yapacak vaktin var | **Gradyan artırma** |
| Kuralı insana anlatman gerekiyor | **Tek ağaç** |
| Veri az ve ilişki doğrusal | **Doğrusal model** |
| Tahmin çok hızlı olmalı | Tek ağaç ya da doğrusal |

**Rastgele orman iyi bir varsayılan** çünkü ayar yapmadan da makul çalışıyor:
`n_estimators` yeterince büyük olsun, gerisi genelde iş görüyor. Gradyan
artırma daha yüksek tavan sunuyor ama `learning_rate`, `n_estimators` ve
derinliği birlikte ayarlamak gerekiyor.

## Bu bölümde neyi atladık

- **XGBoost, LightGBM, CatBoost.** Gradyan artırmanın daha hızlı ve daha
  güçlü uygulamaları; yarışmalarda ve sektörde en çok kullanılanlar.
  Ayrı kütüphaneler oldukları için burada yok.
- **`HistGradientBoostingClassifier`.** sklearn'in hızlı artırma sınıfı;
  büyük veride `GradientBoosting`'den çok daha hızlı ve **eksik değerle
  çalışabiliyor**.
- **Stacking.** Farklı türden modellerin tahminlerini başka bir modele
  girdi yapmak.

Bir sonraki bölüm bambaşka bir soruna bakıyor: sınıflardan biri verinin
%95'iyse ne oluyor?
