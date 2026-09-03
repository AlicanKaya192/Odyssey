# Makine Öğrenmesi Nedir?

Şimdiye kadar yazdığın her programda **kuralları sen yazdın.** "Not 50'nin
üstündeyse geçti" dedin, program da onu uyguladı.

Makine öğrenmesi bunu tersine çeviriyor: kuralı sen yazmıyorsun, **veriden
çıkarıyorsun.**

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Klasik programlama</h4>
      <p>Kuralı sen yazarsın, veriyi verirsin, sonuç çıkar.</p>
    </div>
    <div class="versus-side">
      <h4>Makine öğrenmesi</h4>
      <p>Veriyi <b>ve sonucu</b> verirsin, kural çıkar.</p>
    </div>
  </div>
  <figcaption>Fark girdide değil, neyin bilinmediğinde. Klasik programlamada sonuç bilinmiyor; makine öğrenmesinde kural bilinmiyor.</figcaption>
</figure>

## Ne zaman gerekiyor?

Bir e-postanın spam olup olmadığını anlatan kuralı yazmayı dene: "içinde
'kazandınız' geçiyorsa" dersin, ertesi gün 'kazandiniz' yazan bir e-posta
gelir. Yüzlerce kural yazarsın, hepsi eksik kalır.

Ama elinde spam olduğu bilinen on bin e-posta varsa, kuralı **onlardan**
çıkarabilirsin.

Ölçüt şu: **kuralı cümleyle yazabiliyorsan makine öğrenmesine gerek yok.**
KDV hesabı için model kurulmaz, formülü belli. Model, formülü olmayan ama
örneği bol olan işler için.

## Sözlük

Bu alanın kendi kelimeleri var ve hepsi tanıdık şeylerin yeni adı:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">örnek (sample)</span><span class="anat-body">tablodaki bir <b>satır</b> — bir ev, bir hasta, bir e-posta</span></div>
    <div class="anat-row"><span class="anat-label">özellik (feature)</span><span class="anat-body">tahminde kullanılan <b>sütun</b> — metrekare, yaş, kelime sayısı</span></div>
    <div class="anat-row"><span class="anat-label">hedef (target)</span><span class="anat-body">tahmin edilmek istenen sütun — fiyat, hastalık var/yok</span></div>
    <div class="anat-row"><span class="anat-label">model</span><span class="anat-body">özelliklerden hedefe giden, veriden çıkarılmış kural</span></div>
    <div class="anat-row"><span class="anat-label">eğitim (fit)</span><span class="anat-body">o kuralı veriden çıkarma işi</span></div>
    <div class="anat-row"><span class="anat-label">tahmin (predict)</span><span class="anat-body">kuralı yeni bir satıra uygulama</span></div>
  </div>
</figure>

Özellikler geleneksel olarak `X`, hedef `y` diye yazılıyor. Büyük harf
tesadüf değil: `X` bir **tablo** (çok sütun), `y` tek bir **sütun**.

## Üç öğrenme türü

**Gözetimli öğrenme (supervised).** Elinde doğru cevaplar var. Bin evin
metrekaresini **ve satış fiyatını** biliyorsun; model aradaki ilişkiyi
öğreniyor. Bu bölümün ve sonraki sekiz bölümün konusu bu.

**Gözetimsiz öğrenme (unsupervised).** Doğru cevap yok. Elinde müşteriler
var ama "doğru grup" diye bir şey yok; model benzeyenleri kendi kendine
kümeliyor. 10. bölümün konusu.

**Pekiştirmeli öğrenme (reinforcement).** Model deneyerek ve ödül alarak
öğreniyor — oyun oynayan, robot yürüten sistemler. Bu patikanın dışında.

## İki problem türü

Gözetimli öğrenmede hedefin **ne olduğu** yöntemi belirliyor:

| Hedef | Problem | Örnek |
|---|---|---|
| Sayı | **Regresyon** | Ev fiyatı, yarınki satış, sıcaklık |
| Kategori | **Sınıflandırma** | Spam mı değil mi, hangi tür, geçti mi kaldı mı |

Ayrım önemli çünkü **başarı ölçüsü** de değişiyor: regresyonda "kaç birim
yanıldın", sınıflandırmada "kaçını doğru bildin". İkisini karıştırmak en
sık yapılan başlangıç hatası.

Bazen sınır belirsiz: "kaç yıldız verecek" beş kategorili bir sınıflandırma
da sayılabilir, 1-5 arası bir regresyon da. Kararı sen veriyorsun ve
gerekçesini yazıyorsun.

## Asıl fikir: görmediği veriyle sınamak

Bir model eğitildiği veriyi ezberleyebiliyor. Bin evi ezberleyen bir model
o bin evde kusursuz, yeni bir evde işe yaramaz.

Bu yüzden veri **ikiye ayrılıyor**:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Bütün veri</b></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>Eğitim</b><br>model bunu görüyor</span>
    <span class="arrow">+</span>
    <span class="node ok"><b>Test</b><br>model bunu hiç görmüyor</span>
  </div>
  <figcaption>Test verisi sınav gibi: sorular önceden verilirse not, bilgiyi değil ezberi ölçer.</figcaption>
</figure>

```python
records = [("Ada", 62), ("Kerem", 78), ("Mina", 91), ("Deniz", 45)]

split = int(len(records) * 0.75)
train, test = records[:split], records[split:]

print(len(train), len(test))
```

```text
3 1
```

Gerçekte bunu elle yapmıyorsun (`train_test_split` var, bir sonraki
bölümde), ama ne yaptığını bilerek kullanman gerekiyor.

**Kural:** modelin başarısı **yalnızca** test verisinde ölçülür. Eğitim
verisindeki başarı, öğrencinin cevap anahtarıyla girdiği sınavın notu.

## Taban çizgi olmadan sayı bir şey söylemiyor

Modelin "%80 doğru" demesi iyi mi? Cevap, hiç model kurmadan ne kadar
doğru olacağına bağlı.

Yüz e-postanın 80'i normal, 20'si spam olsun. "Hepsi normal" diyen, tek
satırlık, hiçbir şey öğrenmeyen bir program da **%80 doğru** oluyor.

Bu yüzden her işe **taban çizgiyle** başlanıyor:

| Problem | Taban çizgi |
|---|---|
| Regresyon | Her şeye eğitim verisinin **ortalamasını** söyle |
| Sınıflandırma | Her şeye **en sık görülen** sınıfı söyle |

Modelin taban çizgiyi geçemiyorsa ortada model yok. Bu iki satır, aylarca
uğraşılmış bir projenin boşa gittiğini ilk günden gösterebiliyor.

## Öğrenmek aslında ne demek

"Öğrenme" kelimesi olduğundan gizemli duruyor. Çoğu model için yaptığı iş
şu: **hatayı en küçük yapan sayıları aramak.**

Notlara bakıp "kaçtan yukarısı geçti" kuralını çıkarmak isteseydin,
eşiği 30'dan 100'e kadar dener ve en çok doğruyu vereni seçerdin. Doğrusal
regresyonun yaptığı da bu — yalnızca aradığı sayı bir eşik değil, bir eğim
ve bir kesişim.

Yani model bir sihir değil, **aranmış bir parametre**.

## Neyi yapamıyor

- **Veride olmayanı bilemiyor.** Ev fiyatını etkileyen şey konumsa ve
  konum sütunu yoksa, model onu icat edemiyor.
- **Sebep söylemiyor.** Önceki modülün kuralı burada da geçerli: model
  birlikte hareket eden şeyleri buluyor, sebebi değil.
- **Geçmişi tekrarlıyor.** Geçmişte taraflı kararlar varsa model onları
  öğreniyor ve sürdürüyor.
- **Veriden iyi olamıyor.** Kirli, eksik, dengesiz bir veriyle iyi model
  çıkmıyor. Önceki modülün tamamı bu yüzden vardı.

## Sıra

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>soru ve veri</span>
    <span class="arrow">→</span>
    <span class="node"><b>2</b><br>ayır</span>
    <span class="arrow">→</span>
    <span class="node"><b>3</b><br>taban çizgi</span>
    <span class="arrow">→</span>
    <span class="node"><b>4</b><br>model kur</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>5</b><br>testte ölç</span>
  </div>
  <figcaption>Üçüncü adım atlanıyor ve sonra dördüncü adımın iyi mi kötü mü olduğu anlaşılmıyor.</figcaption>
</figure>

## Özet

- Klasik programlamada **kuralı sen yazıyorsun**, makine öğrenmesinde
  **kural veriden çıkıyor**.
- Kuralı cümleyle yazabiliyorsan modele gerek yok.
- **Özellikler `X`**, **hedef `y`**. Hedef sayıysa regresyon, kategoriyse
  sınıflandırma.
- Üç öğrenme türü: gözetimli (cevaplar var), gözetimsiz (yok),
  pekiştirmeli (deneyerek).
- **Başarı yalnızca modelin görmediği veride ölçülüyor.**
- **Taban çizgi olmadan başarı sayısı okunmuyor**: dengesiz bir veride
  hiçbir şey öğrenmeyen bir program da %80 doğru olabiliyor.
- Öğrenmek çoğu zaman **hatayı en küçük yapan parametreleri aramak**.
- Model veride olmayanı bilemiyor, sebep söylemiyor ve geçmişi
  tekrarlıyor.
