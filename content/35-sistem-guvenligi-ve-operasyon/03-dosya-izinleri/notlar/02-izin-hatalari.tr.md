İzin hatalarının çoğu kötü niyetten değil aceleden doğar: bir şey
çalışmıyordur, biri izni genişletir, iş çalışır ve izin öyle kalır. Bu not
en sık görülen hataları ve doğru karşılıklarını topluyor.

## "Çalışmıyor, 777 yapayım"

Bir program bir dosyayı okuyamıyorsa en kolay "çözüm" herkese her izni
vermektir. Çalışır, ama artık sistemdeki herkes o dosyayı değiştirebilir.
Doğrusu, programın **hangi kullanıcıyla** çalıştığını bulmak ve yalnızca
o kullanıcıya (ya da onun grubuna) gereken izni vermektir: çoğu zaman
`640` ya da `750` yeter.

## Gizli dosya geniş izinle

Anahtarlar, parola dosyaları, `.env` gibi sırlar içeren yapılandırmalar
`600` olmalıdır. Kopyalarken, arşivden çıkarırken ya da başka bir
bilgisayara taşırken izin değişebilir; bu yüzden sır içeren dosyaların
izni taşındıktan sonra yeniden denetlenir. Sırların nasıl saklanacağı Sır
Yönetimi bölümünün konusudur.

## Herkesin yazabildiği betik

Bir yönetici ya da zamanlanmış görev tarafından çalıştırılan bir betik
herkes tarafından yazılabiliyorsa, herhangi bir kullanıcı betiğin içine
kendi komutunu ekleyebilir ve o komut yöneticinin yetkisiyle çalışır.
Ayrıcalıklı olarak çalışan her dosya yalnızca sahibince (ve o sahip de
ayrıcalıklı olmalı) yazılabilir olmalıdır. Bu, bir sonraki bölümün konusu
olan yetki yükseltmenin en sık sebeplerinden biridir.

## Sahiplik de izin kadar önemli

`600` izinli bir dosya, sahibi yanlış kullanıcıysa yanlış kişiye açıktır.
Denetimde izin ile birlikte sahip ve grup da okunur.

## Denetim listesi

| Bulgu | Neden kötü? | Düzeltme |
|---|---|---|
| Dosya herkes tarafından yazılabilir (`o+w`) | Herkes içeriği değiştirebilir | `chmod o-w` |
| Sır içeren dosya grup ya da diğerlerince okunabilir | Sır sızar | `chmod 600` |
| Ayrıcalıklı çalışan betik başkalarınca yazılabilir | Yetki yükseltme | Sahibi ayrıcalıklı hesap, `755` ya da daha dar |
| Ortak klasörde yapışkan bit yok | Herkes başkasının dosyasını siler | Yapışkan bit ekle |
| Gereksiz setuid program | Yetki yükseltme kapısı | setuid bitini kaldır |

## Otomatik denetim

İzinleri tek tek elle kontrol etmek ölçeklenmez. Bir betik dosya listesini
ve izinlerini okur, yukarıdaki kuralları uygular ve bulguları raporlar.
Alıştırmalardaki `audit_files` bu fikrin oyuncak hâlidir: gerçek dosya
sistemine dokunmadan, verilen liste üzerinde çalışır.
