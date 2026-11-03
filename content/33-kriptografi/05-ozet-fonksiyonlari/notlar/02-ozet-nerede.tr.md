Özet fonksiyonları her gün kullandığın birçok sistemin görünmeyen
parçasıdır. Nerede ne işe yaradığı, hangi özelliğin kullanıldığını
anlamayı kolaylaştırır.

## Bütünlük: "bu dosya değişti mi?"

İndirilen bir kurulum dosyasının yanında bir SHA-256 değeri yayımlanır.
Dosyayı indiren kişi kendi bilgisayarında özeti hesaplar ve karşılaştırır;
tutmazsa dosya yolda bozulmuş ya da değiştirilmiştir. Kullanılan özellik:
**belirlenimci** ve **çığ etkisi**.

## Parmak izi: "bu ikisi aynı mı?"

Büyük dosyaları karşılaştırmak yerine özetleri karşılaştırılır. Yedekleme
ve bulut depolama, aynı dosyayı iki kez saklamamak için özetleri kullanır
(kopya tespiti, deduplication). Sürüm kontrol sistemleri (Git) her dosyayı
ve her kaydı özetiyle adlandırır. Kullanılan özellik: **çakışmaya
dayanıklı**.

## Taahhüt: "önceden karar verdim ama sonra göstereceğim"

Bir değeri şimdi gizli tutup sonra açıklamak gerektiğinde, değerin özeti
önce yayımlanır. Sonra değer açıklanınca herkes özetini hesaplayıp
yayımlanana uyduğunu görür; yayımlayan araya değişiklik sokamaz. Kullanılan
özellik: **tek yönlü** ve **çakışmaya dayanıklı**.

## Yapı taşı: başka araçların içinde

- **HMAC** (sonraki bölüm) bir özet fonksiyonunu anahtarla sarar.
- **Parola özetleri** (Parolaları Saklamak) özeti yavaşlatıp tuzlar.
- **Dijital imza** (Dijital İmza bölümü) önce mesajın özetini alır, sonra
  onu imzalar: imza, uzun mesajın tamamını değil sabit boylu özetini işler.

## Nerede kullanılmaz?

- **Şifreleme yerine:** özet geri döndürülemez; gizli tutup sonra okuman
  gereken veriyi özetleyemezsin.
- **Düz parola saklama:** hızlı olması burada zarar; yavaş tuzlu özet
  gerekir.
- **Anahtarsız bütünlük kanıtı:** saldırgan veriyi ve özeti birlikte
  değiştirir; anahtarlı HMAC gerekir.
