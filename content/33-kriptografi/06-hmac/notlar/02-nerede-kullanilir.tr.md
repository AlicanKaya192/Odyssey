HMAC, iki tarafın bir anahtar paylaştığı her yerde mesajın değişmediğini
ve karşı taraftan geldiğini doğrulamak için kullanılır.

## Jetonlar ve oturumlar

Bir sunucunun verdiği oturum jetonu ya da API jetonu HMAC ile imzalanır.
Kullanıcı jetonun içindeki değerleri değiştirse bile (kendi rolünü
"admin" yapmak gibi) etiket tutmaz ve jeton reddedilir. Kimlik Yönetimi
ve Tek Oturum bölümündeki oyuncak JWT bunun küçük bir örneğiydi: önce
imza, sonra iddialar.

## Web kancaları (webhook)

Bir servis başka bir servise olay bildirdiğinde (ödeme alındı, sipariş
verildi), isteğin gövdesini ortak bir anahtarla HMAC'leyip etiketi bir
başlıkta gönderir. Alıcı etiketi doğrulamadan isteği işlememeli; yoksa
herkes sahte "ödeme alındı" bildirimi gönderebilir.

## API istekleri

Bazı API'ler her isteği (yöntem + yol + gövde + zaman damgası) HMAC'ler.
Zaman damgası, yakalanan bir isteğin sonradan **yeniden gönderilmesini**
(replay) zorlaştırır: sunucu çok eski zaman damgalı isteği reddeder.

## Dosya ve yapılandırma bütünlüğü

Bir yapılandırma dosyası ya da günlük, yanına bir HMAC etiketiyle
saklanırsa, dosyayı değiştiren ama anahtarı bilmeyen biri yakalanır. Düz
özet burada yetmez (saldırgan özeti de günceller); anahtar farkı yaratır.

## Dikkat edilecekler

- Anahtar gerçekten gizli ve yeterince uzun olmalı (en az 128 bit, rastgele).
- Her amaç için ayrı anahtar: şifreleme anahtarıyla MAC anahtarı aynı
  olmamalı.
- Etiketi her zaman `compare_digest` ile karşılaştır.
- Doğrulama başarısızsa mesaj hiç işlenmez; hata mesajı "neden" tutmadığını
  söylemez (saldırgana ipucu vermemek için).
