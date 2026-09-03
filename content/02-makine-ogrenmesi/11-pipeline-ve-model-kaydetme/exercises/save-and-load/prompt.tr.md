Eğitilmiş bir model bellekte duruyor. Program kapanınca gidiyor.

Bu alıştırmada pipeline'ı diske kaydedip geri yükleyecek ve **ham veriyle**
— eksik değerli ham veriyle — tahmin üreteceksin.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır, pipeline'ı kur ve eğit.
2. `joblib.dump` ile `model.joblib` olarak kaydet. Dosyanın 1000 bayttan
   büyük olup olmadığını yazdır.
3. `joblib.load` ile geri yükle.
4. Yüklenen modelin test kümesindeki tahminlerinin **orijinal modelinkiyle
   aynı** olup olmadığını yazdır.
5. Üç yeni aboneden oluşan bir `DataFrame` kur:
   - Bursa / basic / tenure 3 / monthly 140.0 / support 4
   - Izmir / pro / tenure 48 / monthly 45.0 / support 0
   - **şehri ve aylık ücreti bilinmeyen** / plus / tenure 20 / support 1
6. Yüklenen modelin bu üç satır için tahminlerini ve pozitif sınıf
   olasılıklarını ayrı satırlarda yazdır (olasılıklar üç ondalık).

**Beklenen çıktı:**

```
True
True
[1, 0, 0]
[0.993, 0.007, 0.466]
```

**Üçüncü satırın önemini kaçırma.** Ona ham bir sözlük verdin: `city` yok,
`monthly` yok. Ölçeklenmemiş sayılar, kodlanmamış metin.

Model çalıştı. Çünkü kaydedilen şey yalnızca katsayılar değil, **bütün
pipeline**:

- Sayısal sütunların eğitimde hesaplanan medyanı
- Metin sütunlarının eğitimde hesaplanan modu
- Kodlayıcının öğrendiği kategoriler
- Ölçekleyicinin ortalama ve standart sapması
- Model katsayıları ve sütun sırası

**Elle hazırlanmış bir modelde bu satır bir çökme olurdu** — ya da daha
kötüsü, medyanı yeniden hesaplayıp sessizce yanlış bir tahmin üretirdi.

**Olasılıklara bak:** birinci abone 0.993 (Bursa + basic + kısa süre + çok
destek çağrısı — dört risk faktörü birden), ikincisi 0.007 (Izmir + pro +
uzun süre + hiç destek), üçüncüsü 0.466 — **kararsız**, çünkü iki sütunu
eksik ve model onları ortalama değerlerle doldurdu.

Bu üçüncü sayı dürüst bir cevap: "bu abone hakkında yeterli bilgim yok."

**Dosyanın taşımadıkları:** kütüphane sürümleri, eğitim verisi, seçtiğin
karar eşiği ve ölçtüğün skorlar. Bunlar için dosyanın yanına bir metin
dosyası konuyor — ikinci ders notu bunun nasıl yazılacağını anlatıyor.
