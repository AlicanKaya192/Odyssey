Veri bilimiyle ilgili bir yazı okurken ya da bir kütüphanenin belgesine
bakarken sürekli karşına çıkacak kelimeler. Hepsini şimdi ezberlemene gerek
yok; tıkandığında buraya dön.

## Verinin şekli

| Terim | Ne demek |
|---|---|
| **Kayıt / satır** (record, row) | Bir varlık hakkındaki bilgilerin tamamı: bir öğrenci, bir sipariş, bir gün |
| **Değişken / sütun** (feature, column) | Bütün kayıtlarda ölçülen aynı özellik: not, şehir, fiyat |
| **Gözlem** (observation) | Kayıt ile aynı şey. İstatistik tarafından gelen ad |
| **Veri kümesi** (dataset) | Satır ve sütunların tamamı; bir tablo |
| **Boyut** (shape) | Kaç satır, kaç sütun. `(800, 5)` = 800 kayıt, 5 özellik |

Aynı şeye üç farklı ad verilmesi kafa karıştırıyor ama sebebi var: veri
bilimi istatistik, veritabanı ve yazılım dünyalarının kesişiminde duruyor ve
her biri kendi kelimesini getirdi.

## Değişken türleri

Bir sütunun **ne tür** değer tuttuğu, ona ne yapabileceğini belirliyor.

| Tür | Örnek | Ne yapılır |
|---|---|---|
| **Sayısal** (numeric) | not, fiyat, yaş | ortalama, toplam, fark |
| **Kategorik** (categorical) | şehir, cinsiyet, sınıf | sayma, gruplama |
| **Sıralı** (ordinal) | düşük / orta / yüksek | sırası var ama farkı ölçülemez |
| **Tarih** (datetime) | 2026-03-14 | aralık, gün farkı, aya göre gruplama |
| **Metin** (text) | yorum, açıklama | arama, uzunluk, ayrıştırma |

**Sık yapılan hata:** posta kodu ya da öğrenci numarası sayısal görünüyor
ama kategorik. Ortalama posta kodu diye bir şey yok.

## Özet istatistikler

Bir sayısal sütunu tek bir cümleye indiren ölçüler:

| Ölçü | Ne söyler |
|---|---|
| **Ortalama** (mean) | Toplamın kayıt sayısına bölümü |
| **Medyan** (median) | Sıraladığında tam ortadaki değer |
| **Mod** (mode) | En çok tekrar eden değer |
| **En küçük / en büyük** (min / max) | Uçlar |
| **Standart sapma** (std) | Değerlerin ortalamadan ne kadar uzağa yayıldığı |

**Ortalama ile medyan neden ikisi birden var?** Çünkü ortalama uç değerlerden
etkileniyor. Beş kişinin maaşı 30, 32, 35, 33 ve 900 bin ise ortalama 206
bin çıkıyor — kimsenin maaşı o değil. Medyan 33 bin diyor ve durumu doğru
anlatıyor.

Bir sütuna baktığında ortalama ile medyan **birbirinden çok uzaksa**, orada
uç değerler var demektir.

## Veri kalitesi

| Terim | Ne demek |
|---|---|
| **Eksik değer** (missing / NaN) | Hücre boş. Sıfır değil, "bilinmiyor" |
| **Aykırı değer** (outlier) | Diğerlerinden çok uzak değer. Hata da olabilir, gerçek de |
| **Tekrar eden kayıt** (duplicate) | Aynı satır iki kez girilmiş |
| **Tutarsızlık** | Aynı şeyin farklı yazımı: `"Ankara"`, `"ankara"`, `"ANKARA"` |

Bunların hepsi gerçek veride var. "Temiz veri" diye bir şey yok; temizlenmiş
veri var.

## İşlemler

| Terim | Ne demek |
|---|---|
| **Filtreleme** (filter) | Koşula uyan satırları seçmek |
| **Seçim** (selection) | Belirli sütunları almak |
| **Gruplama** (group by) | Satırları bir sütuna göre kümelere ayırmak |
| **Toplulaştırma** (aggregation) | Her grubu tek bir sayıya indirmek |
| **Birleştirme** (join / merge) | İki tabloyu ortak bir sütun üzerinden yan yana koymak |
| **Sıralama** (sort) | Satırları bir sütuna göre dizmek |

Bu altı işlem veri işlerinin neredeyse tamamını kaplıyor. SQL'de de aynıları
var (`WHERE`, `SELECT`, `GROUP BY`, `JOIN`, `ORDER BY`) — isimleri bile
benziyor, çünkü aynı fikirler.

## Dosya biçimleri

| Biçim | Ne zaman |
|---|---|
| **CSV** | Virgülle ayrılmış düz metin. Her yerde açılıyor, en yaygın |
| **Excel** (.xlsx) | Birden fazla sayfa, biçimlendirme. İş dünyasında yaygın |
| **JSON** | İç içe yapılar için. API'lerden genelde bu geliyor |
| **Parquet** | Sıkıştırılmış, sütun tabanlı. Büyük veride hızlı |
| **SQL** | Veritabanından sorguyla çekilen |

Başlangıçta CSV yeter. `Dosya İşlemleri` bölümünde okuduğun düz metin
dosyaları aslında bunun basit hâliydi.

## Kütüphaneler

| Kütüphane | Ne için |
|---|---|
| **NumPy** | Sayı dizileri, matematik, hız |
| **pandas** | Tablolar: okuma, temizleme, gruplama |
| **Matplotlib** | Grafik çizme |
| **scikit-learn** | Makine öğrenmesi modelleri |

pandas NumPy'ın üstüne kurulu; Matplotlib ikisiyle de çalışıyor.
scikit-learn bir sonraki patikanın konusu.
