Bu modül kavramları kurdu. Patikada sırada üç modül var; her biri buradaki
bir fikri derinleştiriyor.

## Kriptografi

Burada `hashlib` ve `hmac`'i kullandık ama içlerini açmadık. Kriptografi
modülü özet fonksiyonlarının, simetrik ve asimetrik şifrelemenin, dijital
imzanın ve sertifikaların nasıl çalıştığını küçük, ölçülen örneklerle
anlatıyor. Kimlik Yönetimi bölümündeki imzalı jetonun gerçek hâli oradaki
konuların birleşimi.

## Ağ ve Web Güvenliği

Saldırı yüzeyinin en büyük parçası çoğu zaman ağ ve web uygulamalarıdır.
Bu modül güvenlik duvarlarını, HTTPS'i ve OWASP'ın listelediği sık web
açıklarını (enjeksiyon, bozuk erişim denetimi, oturum hataları) anlatıyor.
Yetkilendirme bölümündeki "karar sunucuda verilir" ilkesi orada her
örnekte karşına çıkacak.

## Sistem Güvenliği ve Operasyon

Önlemler alındıktan sonra sistemlerin nasıl sertleştirildiği, kayıtların
nasıl izlendiği ve bir olay olunca ne yapıldığı. Zararlı Yazılım
bölümündeki "bulaşınca ne yapılır?" sırası orada bir olay müdahale planına
dönüşüyor; NIST CSF'nin Detect, Respond ve Recover işlevleri de bu
modülün konusu.

## Çalışırken

- Kavramları gördüğün sistemlerde ara: okulunun ya da kullandığın bir
  uygulamanın giriş akışı hangi faktörleri kullanıyor, hangi standartla
  tek oturum açılıyor?
- Kendi küçük projelerinde tehdit modellemenin dört sorusunu sor.
- Öğrendiğin teknikleri yalnızca kendi sistemlerinde ya da açıkça izin
  verilmiş alıştırma ortamlarında dene. İzinsiz deneme suçtur.
