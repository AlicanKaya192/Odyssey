"Çok sayıda zayıf model bir araya gelince güçlü oluyor" cümlesi kulağa
sihir gibi geliyor. Değil; arkasında tek bir fikir var.

## İki tür hata

Bir modelin hatası ikiye ayrılıyor:

| Tür | Ne demek | Örnek |
|---|---|---|
| **Yanlılık** (bias) | Model sistematik olarak yanılıyor | Eğri ilişkiye düz çizgi çekmek |
| **Varyans** | Veri biraz değişince sonuç çok değişiyor | Derin bir ağacın kök eşiğinin kayması |

Bölüm 05'te bu ikisini görmüştün: yetersiz öğrenme yüksek yanlılık, aşırı
öğrenme yüksek varyans.

**Topluluk yöntemleri bu ikisine iki farklı yoldan saldırıyor.**

## Torbalama varyansı düşürüyor

Tek bir ağacın hatası büyük ölçüde rastgele: şu satır düştü diye eşik
kaydı, bu satır girdi diye dal değişti.

Rastgele hataların ortalaması alındığında **birbirini götürüyor.** Aynı
madeni parayı yüz kez atıp ortalamasını almak gibi: tek atışın sonucu
öngörülemez, yüz atışın ortalaması 0.5'e çok yakın.

Ölçülen sonuç:

```
agac  skorlari: [0.92, 0.88, 0.78, 0.80, 0.80, 0.84]  -> 14 puanlik aralik
orman skorlari: [0.90, 0.84, 0.86, 0.90, 0.90, 0.92]  ->  8 puanlik aralik
```

**Torbalama yanlılığa dokunmuyor.** Bütün ağaçlar aynı sistematik hatayı
yapıyorsa ortalamaları da o hatayı yapıyor. O yüzden torbalanan modeller
**derin** tutuluyor: yanlılıkları zaten düşük, azaltılması gereken şey
varyans.

## Bağımsızlık şart

Ortalamanın işe yaraması için hataların **birbirinden bağımsız** olması
gerekiyor. Bütün ağaçlar aynı hatayı yapıyorsa ortalama bir şey
düzeltmiyor.

Rastgele ormanın ikinci rastgeleliği (`max_features`) tam olarak bunun
için: her bölünmede özelliklerin bir alt kümesi saklanıyor ki ağaçlar
farklı yollardan gitsin.

Bu, sezgiye aykırı bir sonuç doğuruyor: **her ağacı tek başına zayıflatmak,
topluluğu güçlendiriyor.** Ağaçların tek tek doğruluğu düşüyor ama
aralarındaki bağımlılık daha çok düşüyor.

## Artırma yanlılığı düşürüyor

Artırmanın mantığı bambaşka. Ağaçlar sığ ve zayıf — tek başına bir ağaç
neredeyse hiçbir şey bilmiyor.

Ama sırayla kuruluyorlar ve her yeni ağaç, **kalan hataya** bakıyor:

```
tahmin = agac1 + lr * agac2 + lr * agac3 + ...
```

Her adımda hata biraz daha azalıyor. Yani topluluk, tek bir modelin
yakalayamayacağı karmaşıklığı **adım adım** kuruyor.

**Bu yüzden artırma aşırı öğrenebiliyor:** yeterince adım atarsan kalan
"hata" artık gürültüden ibaret oluyor ve model onu da düzeltmeye çalışıyor.
Ormanda böyle bir tehlike yok çünkü orada ağaçlar birbirini düzeltmiyor.

## Neden ağaçlar

Topluluk fikri her modelle çalışıyor ama ağaçlarla özellikle iyi çalışıyor:

- **Ağaçlar kararsız.** Ortalama alınacak çeşitlilik zaten var. Doğrusal
  regresyonun yüz tanesini ortalamak neredeyse aynı doğruyu veriyor —
  ortalanacak bir şey yok.
- **Ağaçlar ayarsız çalışıyor.** Ölçekleme, kodlama sırası, aykırı değer
  derdi yok.
- **Ağaçlar hızlı.** Yüzlercesini kurmak mümkün.

## Ne zaman işe yaramıyor

| Durum | Neden |
|---|---|
| Veri çok az | Bootstrap örneklemleri neredeyse aynı çıkıyor |
| İlişki gerçekten doğrusal | Doğrusal model zaten en iyisi; ağaçlar basamaklarla uğraşıyor |
| Tek bir özellik her şeyi belirliyor | Ağaçlar çeşitlenemiyor |
| Yorumlanabilirlik şart | Topluluk okunabilirliği tamamen kaybettiriyor |

Bölüm 05'te ölçülmüştü: araba verisinde ağacın hatası 64, doğrusal
regresyonunki 16.5'ti. Orada topluluk kurmak da kurtarmıyor — sorun ağaç
sayısında değil, ağacın veriye uymamasında.

## Kaba bir özet

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Model çok mu kararsız?</h4>
      <p>Aynı veriyle farklı sonuçlar, büyük eğitim-test uçurumu.<br><b>Torbalama / orman</b></p>
    </div>
    <div class="versus-side">
      <h4>Model çok mu basit?</h4>
      <p>Eğitimde de testte de kötü, örüntüyü yakalayamıyor.<br><b>Artırma</b></p>
    </div>
  </div>
  <figcaption>Teşhis bölüm 05'teki iki skor tablosundan geliyor; tedavi burada değişiyor.</figcaption>
</figure>

Pratikte ikisi de denenip **çapraz doğrulamayla** karşılaştırılıyor — çünkü
verinin hangi hataya daha yatkın olduğunu önceden bilmenin yolu yok.
