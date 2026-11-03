Bu modül kriptografinin nasıl çalıştığını küçük, ölçülen oyuncak
örneklerle gösterdi. Patikada sırada iki modül var; ikisi de buradaki
araçları gerçek sistemlerin içinde kullanıyor.

## Ağ ve Web Güvenliği

HTTPS bu modülün TLS El Sıkışması bölümünün uygulamadaki hâli. Ağ ve Web
Güvenliği modülü bağlantının çevresine bakıyor: ağ katmanları, güvenlik
duvarı, VPN, DNS; oturum ve çerezler (imzalı çerezler HMAC'in bir
kullanımı), sık web açıkları ve güvenlik başlıkları. Sertifikalar ve PKI
bölümündeki "doğrulamayı kapatma" kuralı orada güvenli API yazarken
karşına çıkacak.

## Sistem Güvenliği ve Operasyon

Anahtarın kendisi de bir varlık: nerede saklandığı, kimin erişebildiği,
sızınca ne yapıldığı. Sistem Güvenliği ve Operasyon modülü sırların ve
bağımlılıkların yönetimini, kayıt tutmayı, olay müdahalesini ve
yedeklemeyi anlatıyor; Sık Kriptografi Hataları bölümündeki "sızan sır"
adımları orada bir olay müdahale planının parçası.

## Gerçek kütüphanelerle çalışırken

- Derslerdeki oyuncak şifreleri, anahtarları ve eğrileri gerçek bir
  programda kullanma; yalnızca fikri göstermek içindiler.
- Kütüphanenin **üst düzey** işlevlerini seç (tek çağrıda AEAD, hazır
  parola özeti). Alt düzey parçaları (kip, dolgu, nonce) elle birleştirmek
  bu modüldeki hataların çoğunun kaynağı.
- Kütüphane bir uyarı ya da "kullanımdan kalktı" mesajı verirse
  görmezden gelme; çoğu zaman eski bir algoritmanın işareti.
- Varsayılanları sorgula: tekrar sayısı, anahtar boyu, TLS sürümü zamanla
  değişir; Hızlı Başvuru notundaki tablo bugünün önerisi.

## Çalışırken

- Kullandığın bir sitenin sertifikasını tarayıcıda aç: zinciri, tarihleri
  ve SAN listesini bu modüldeki adlarla oku.
- Bir projendeki ayarları Denetim Listesi notuyla gözden geçir.
