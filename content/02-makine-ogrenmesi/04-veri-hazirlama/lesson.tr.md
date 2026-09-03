# Modele Veri Hazırlamak

Şimdiye kadarki dosyalar temizdi: bütün sütunlar sayı, hiç eksik değer yok.
Gerçek veri böyle değil.

Bu bölümde üç sorun ve bir kural var. Kural üçünden de önemli.

## Kural: önce ayır, sonra dokun

Hazırlığın her adımı veriden bir şey **öğreniyor**: ortalama, standart
sapma, kategori listesi. O bilgi bütün veriden çıkarılırsa, modelin
görmemesi gereken test satırları hesaba giriyor.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Yanlış sıra</h4>
      <p>Bütün veriyi hazırla → sonra ayır.<br>Test verisinin bilgisi eğitime <b>sızıyor</b>.</p>
    </div>
    <div class="versus-side">
      <h4>Doğru sıra</h4>
      <p>Ayır → hazırlığı <b>eğitimde öğren</b> → ikisine de uygula.<br>Test el değmemiş kalıyor.</p>
    </div>
  </div>
  <figcaption>Buna veri sızıntısı deniyor. Test skoru olduğundan yüksek çıkıyor ve model gerçekte o kadar iyi değil.</figcaption>
</figure>

Bu bölümdeki her işlem bu kurala uyuyor. Kuralı bilmeden yapılan hazırlık,
ölçümü sessizce bozuyor.

## Sorun 1: eksik değerler

```
ValueError: Input contains NaN
```

sklearn eksik değerle çalışmıyor (birkaç ağaç tabanlı model dışında). İki
seçenek var: **doldur** ya da **at**.

```python
print(df.isna().sum())
# age        0
# km         0
# engine    14
# fuel       0
# ...
```

120 satırın 14'ünde motor hacmi yok.

**Atmak** en kolayı ama pahalı: 120 satırın 14'ünü atmak verinin sekizde
birini kaybetmek demek. Az veride bu lüks yok.

**Doldurmak** daha yaygın. Sayısal sütunlarda ortalama ya da medyan,
kategorik sütunlarda en sık görülen değer.

```python
fill_value = X_train["engine"].mean()      # yalnizca EGITIM'den
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})
```

**Dikkat:** ortalama **eğitim** verisinden hesaplanıyor ve **aynı sayı** ikisine
de uygulanıyor. Bütün veriden hesaplamak sızıntı olur.

Bu örnekte iki ortalama arasında neredeyse fark yok — **1.458** ve
**1.457**. Kural farkın büyüklüğüyle ilgili değil: ölçümün dürüst olup
olmadığıyla ilgili. Bugün 0.001 olan fark, başka bir veride 0.3 olabiliyor.

**Ortalama mı medyan mı:** aykırı değer varsa medyan. Ortalama tek bir uç
kayıttan etkilenirken medyan etkilenmiyor.

## Sorun 2: metin sütunları

```
ValueError: could not convert string to float: 'diesel'
```

Model sayıyla çalışıyor. `fuel` sütununda `petrol`, `diesel`, `lpg` var —
bunlar modele böyle giremiyor.

**Akla ilk gelen yol yanlış:** `petrol=0, diesel=1, lpg=2` demek. Bu, model
için `lpg`'yi `petrol`'ün iki katı ve `diesel`'i tam ortası yapıyor. Öyle
bir sıra yok.

Doğru yol **one-hot kodlama**: her kategori kendi sütunu oluyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">önce</span><span class="anat-body">tek sütun: <code>fuel</code> = petrol / diesel / lpg</span></div>
    <div class="anat-row"><span class="anat-label">sonra</span><span class="anat-body">üç sütun: <code>fuel_petrol</code>, <code>fuel_diesel</code>, <code>fuel_lpg</code> — her satırda yalnızca biri 1</span></div>
  </div>
  <figcaption>Kategoriler arasında sıra yokken sıra uydurmamanın yolu: her birine kendi sütununu vermek.</figcaption>
</figure>

```python
encoded = pd.get_dummies(df, columns=["fuel", "gearbox"])
```

Beş sütun sekize çıkıyor: `age`, `km`, `engine`, `fuel_petrol`,
`fuel_diesel`, `fuel_lpg`, `gearbox_manual`, `gearbox_auto`.

**Sonuç:** bu iki sütunu modele eklemek hatayı **32.58'den 16.42'ye**
düşürüyor. Yakıt türü ve vites gerçekten fiyatı belirliyormuş; sayısal
olmadıkları için dışarıda kalmışlardı.

**Ne zaman sıra uydurmak doğru:** kategoride gerçek bir sıra varsa.
`düşük < orta < yüksek` ya da `ilkokul < lise < üniversite` için
`0, 1, 2` doğru — buna **sıralı (ordinal)** kodlama deniyor. Sıra
yoksa one-hot.

**Bir tuzak:** çok kategorili sütunlar (şehir, ürün kodu) one-hot ile
yüzlerce sütun üretiyor. Az veride bu, özellik sayısını örnek sayısına
yaklaştırıyor ve model ezberlemeye başlıyor.

**pandas 3 ayrıntısı:** metin sütunlarını bulmak için eski öğretilerde
`df.dtypes == "object"` geçiyor. pandas 3'te metin sütunları artık
`object` değil; o kontrol **boş liste** veriyor. Çalışan yol:

```python
text_columns = df.select_dtypes(exclude="number").columns.tolist()
```

## Sorun 3: ölçek farkı

`km` sütunu 10.000 ile 300.000 arasında, `engine` 1.0 ile 2.0 arasında
geziniyor. İkisi de sayı, ama aynı dünyada değiller.

Mesafeye bakan bir model için bu ölümcül:

```
KNN, olceklemesiz   MAE 171.49
KNN, olcekli        MAE  51.48
```

**Üç kat fark.** Ölçeklemesiz KNN aslında yalnızca `km`'ye bakıyor; `engine`
sütunundaki 1.0 ile 2.0 farkı, `km`'deki 250.000 farkın yanında yok
hükmünde.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)                       # sadece EGITIM'den ogren
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**`fit` eğitimde, `transform` ikisinde.** Bu üç satır, bölümün kuralının
koda dökülmüş hâli. `fit_transform`'u test verisine uygulamak sık yapılan
bir hata ve tam olarak sızıntı demek.

### Hangi model ölçekleme istiyor

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Etkileniyor</h4>
      <p>KNN, doğrusal modeller (düzenlileştirmeliyse), kümeleme, sinir ağları<br><b>Mesafe ya da ağırlık büyüklüğü kullananlar</b></p>
    </div>
    <div class="versus-side">
      <h4>Etkilenmiyor</h4>
      <p>Karar ağacı, rastgele orman, gradyan artırma<br><b>Eşiklerle çalışanlar</b></p>
    </div>
  </div>
  <figcaption>Ağaçlar "km 150.000'den büyük mü" diye soruyor; sütunun ölçeği bu soruyu değiştirmiyor.</figcaption>
</figure>

Aynı veride doğrusal regresyon ölçeklemeden **hiç etkilenmiyor**:

```
dogrusal regresyon, olceklemesiz   MAE 34.63
dogrusal regresyon, olcekli        MAE 34.63
```

Birebir aynı. Model katsayıyı sütunun ölçeğine göre ayarlıyor.

**Yine de ölçeklemenin bir faydası var:** katsayılar ölçeklenmiş veride
karşılaştırılabilir hâle geliyor. Bölüm 01'de "3.35 > 2.77 diye yaş daha
önemli denmez" demiştik — ölçekledikten sonra denebiliyor.

**İki ölçekleyici:**

| Ölçekleyici | Ne yapıyor | Ne zaman |
|---|---|---|
| `StandardScaler` | Ortalamayı 0, standart sapmayı 1 yapıyor | Varsayılan seçim |
| `MinMaxScaler` | Her şeyi 0-1 aralığına sıkıştırıyor | Sınırlı aralık gerekiyorsa |

## Sızıntı küçük olmak zorunda değil

Bu bölümün örneklerinde sızıntının etkisi küçük çıkıyor: ölçeklemeyi bütün
veride yapmak MAE'yi 51.48'den 51.69'a taşıyor, neredeyse hiçbir şey.

Bu, kuralın gevşek olduğu anlamına gelmiyor. Sızıntının büyüklüğü **ne
sızdığına** bağlı ve bazen sonuç tamamen uydurma çıkıyor.

Şöyle bir deney: 80 satır, 300 sütun ve **tamamı rastgele sayı**. Hedefle
hiçbir ilişkisi yok. Doğru kurulan bir model burada hiçbir şey bulamamalı.

```
sizintili secim   R2   0.442
temiz secim       R2  -0.273
```

**Temiz sonuç negatif** — doğru olan bu, çünkü öğrenilecek bir şey yok.

**Sızıntılı sonuç 0.442** — yani bir model varmış gibi görünüyor. Yapılan
tek şey, sütunları **bütün veriye bakarak** seçmekti: 300 rastgele sütun
arasından test verisiyle rastlantısal olarak uyuşan beşi seçiliyor ve
sonra o test verisinde ölçülüyor.

Bu sayı bir kâğıda yazılıp sunulabilir, kimse fark etmez. Model ise
hiçbir işe yaramaz.

## Sıra

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>oku</span>
    <span class="arrow">→</span>
    <span class="node acc"><b>2</b><br>AYIR</span>
    <span class="arrow">→</span>
    <span class="node"><b>3</b><br>eksikleri doldur</span>
    <span class="arrow">→</span>
    <span class="node"><b>4</b><br>kategorileri kodla</span>
    <span class="arrow">→</span>
    <span class="node"><b>5</b><br>ölçekle</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>6</b><br>eğit ve ölç</span>
  </div>
  <figcaption>İkinci kutu en başta duruyor. Ondan sonraki her adım eğitimde öğrenilip ikisine birden uygulanıyor.</figcaption>
</figure>

Bu sıra insanı zorluyor: aynı işlemi iki kümeye ayrı ayrı uygulamak,
dolduracak değeri saklamak, ölçekleyiciyi taşımak. Kodu dağıtıyor ve bir
adımı unutmak kolaylaşıyor.

**Bunun bir çözümü var: `Pipeline`.** Bütün hazırlık adımlarını modelle
birlikte tek nesnede topluyor ve sızıntıyı yapısal olarak imkânsız hâle
getiriyor. 11. bölümün konusu.

Şimdilik adımları elle yapmak gerekiyor — çünkü `Pipeline`'ın neyi
otomatikleştirdiğini bilmeden kullanmak, sızıntıyı görmeden geçmek demek.
