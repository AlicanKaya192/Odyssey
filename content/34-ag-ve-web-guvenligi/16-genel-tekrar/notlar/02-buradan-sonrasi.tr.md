Bu modül isteklerin ağda nasıl korunduğunu ve web uygulamalarının sık
açıklarını anlattı. Patikanın son modülü bunların arkasındaki sistemlere
ve günlük işletmeye bakıyor.

## Sistem Güvenliği ve Operasyon

- **Bellek ve işletim sistemi:** bir programın belleği nasıl bozulur,
  işletim sistemi bunu nasıl sınırlar; dosya izinleri ve yetki
  yükseltme. Buradaki "en az yetkili veritabanı kullanıcısı" fikri orada
  işletim sistemi hesaplarına uygulanıyor.
- **Güvenli yazılım geliştirme:** bu modüldeki savunmaların (parametreli
  sorgu, kodlama, izin listesi) bir ekipte kod incelemesiyle ve
  bağımlılık denetimiyle nasıl alışkanlık hâline geldiği.
- **Sır yönetimi:** API anahtarları, imza sırları ve oturum imza anahtarı
  kodun içine değil nereye konur, nasıl yenilenir.
- **Kayıt, izleme ve olay müdahalesi:** Kimlik Doğrulama Hataları
  bölümündeki "kaynak başına izleme" ve OWASP'ın kayıt kategorisi orada
  saldırı tespitine, sonra bir olay müdahale planına dönüşüyor.

## Çalışırken

- Kendi küçük web projelerinde bu bölümün "bir isteğin yolu" sırasını
  uygula: oturum, köken ve jeton, sahiplik, parametreli sorgu, kodlanmış
  çıktı.
- Tarayıcının geliştirici araçlarında kendi sitenin cevap başlıklarına ve
  çerez özelliklerine bak; Başlık Şablonu notuyla karşılaştır.
- OWASP'ın web ve API listelerini ve hile sayfalarını (Cheat Sheet
  Series) başvuru olarak kullan; listeler birkaç yılda bir güncellenir.
- Öğrendiğin teknikleri yalnızca kendi sistemlerinde ya da açıkça izin
  verilmiş alıştırma ortamlarında dene. İzinsiz deneme suçtur.
