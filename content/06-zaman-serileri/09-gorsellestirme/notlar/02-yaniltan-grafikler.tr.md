Bir grafik yanlış sayı içermeden de yanlış bir şey söyleyebiliyor. Zaman
serisinde en sık görülen altı yol ve her birinin düzeltmesi.

## 1. İki ayrı dikey eksen

`ax.twinx()` ile aynı grafiğe farklı ölçekte iki seri koymak mümkün. Sorun
şu: iki eksenin aralığını **sen** seçiyorsun, ve aralıkları ayarlayarak iki
çizgiyi istediğin kadar üst üste ya da ayrı gösterebilirsin. Aynı veriyle
"birlikte hareket ediyorlar" da "ilgisizler" de çizilebiliyor.

Düzeltme: iki seriyi **endeksle** (ikisi de 100'den başlasın) ya da **alt
alta iki panel** çiz. İlişkiyi görmek istiyorsan saçılım grafiği ve
korelasyon.

## 2. Kesilmiş dikey eksen

Ekseni 280'den başlatıp 300'de bitirirsen %3'lük bir oynama uçurum gibi
görünür. Çubuk grafikte çubuğun **boyu** değeri anlattığı için eksen sıfırdan
başlamalı. Çizgi grafikte sıfır zorunlu değil, ama aralığı seçtiğini bil ve
okuyana düzeyi hissettir (yüzde değişimi yaz, ya da sıfırlı bir küçük panel
ekle).

## 3. Seçilmiş zaman aralığı

Aynı seri, başlangıç tarihine göre "yükseliyor" ya da "düşüyor" görünebilir.
Aralık ayından başlayan bir grafik hep düşüş gösterir; Mayıs'tan başlayan
hep yükseliş.

Düzeltme: en az bir tam mevsim döngüsünü (tercihen iki) göster; başlangıç ve
bitişi neden orada seçtiğini söyleyebilmelisin. Mevsimsel seride iki nokta
arasını karşılaştırırken aynı mevsimi karşılaştır.

## 4. Aşırı düzleştirme

365 günlük hareketli ortalama her seriyi sakin ve kararlı gösterir. Kırılma,
aykırı gün, oynaklıktaki artış düz çizginin altında kaybolur.

Düzeltme: ham seriyi silik de olsa arkada tut; pencere boyunu başlığa ya da
lejanta yaz. Geriye dönük ortalamanın dönüm noktalarını geç gösterdiğini
unutma (Bölüm 07).

## 5. Doğrusal eksende büyüyen seri

Yüzdeyle büyüyen bir seride doğrusal eksen son yılları abartır, ilk yılları
düz çizgiye sıkıştırır. 100'den 200'e çıkış ile 1000'den 2000'e çıkış aynı
büyüme (iki katı), ama doğrusal eksende ikincisi on kat daha dik.

Düzeltme: `ax.set_yscale("log")`. Tersi de bir hata: logaritmik eksen mutlak
farkları gizler; bütçe, stok gibi **miktarın kendisinin** önemli olduğu yerde
doğrusal eksen doğru.

## 6. Birleştirilmiş boşluklar

Eksik günler satır olarak yoksa çizgi iki komşu noktayı birleştirir ve veri
kesintisiz görünür. Beş günlük bir kesinti düz bir çizgi parçası olarak
"ölçülmüş" gibi durur.

Düzeltme: çizmeden önce `asfreq`; çizgi kopsun.

## Yayınlamadan önce

1. Başlık ne gösterildiğini söylüyor mu? ("Günlük satış, 2022–2024")
2. Dikey eksenin **birimi** yazıyor mu?
3. Sıklık belli mi (günlük, haftalık ortalama, aylık toplam)?
4. Düzleştirme varsa pencere boyu yazıyor mu?
5. Çubuk grafiğin ekseni sıfırdan başlıyor mu?
6. Eksik veri çizgiyle birleştirilmiş mi?
7. Başlangıç ve bitiş tarihi gerekçeli mi?
8. Renkler renk körü biri için de ayırt edilebilir mi? Çizgi türünü ya da
   işareti de değiştir.
9. Grafik tek bir soruyu mu cevaplıyor? İkiyse iki grafik.
