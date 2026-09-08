Kurulumda takılırsan buraya bak. Sorunlar sık görülen sırayla yazılı.

## "ODBC sürücüsü bulunamadı"

Odyssey sunucuya `ODBC Driver 18 for SQL Server` ile bağlanıyor. Bu mesaj
o sürücünün kurulu olmadığını söylüyor.

Kontrol: Başlat menüsüne **ODBC** yaz, "ODBC Veri Kaynakları (64 bit)"
uygulamasını aç, **Sürücüler** sekmesine geç. Listede sürücünün adı
görünmeli.

Yoksa
<https://learn.microsoft.com/tr-tr/sql/connect/odbc/download-odbc-driver-for-sql-server>
sayfasındaki **x64** bağlantısından kur, sonra **Odyssey'i kapatıp aç.**
Yeni kurulan sürücüyü çalışan bir program görmüyor.

## "SQL Server'a ulaşılamadı"

Sürücü var ama sunucu cevap vermiyor. Üç ihtimal:

**Sunucu çalışmıyor.** Başlat menüsüne `services.msc` yaz. Açılan listede
**SQL Server (SQLEXPRESS)** satırını bul. Durum sütununda "Çalışıyor"
yazmıyorsa satıra sağ tıklayıp **Başlat** de.

Aynı satıra çift tıklayıp **Başlangıç türü** kutusunu **Otomatik** yaparsan
bilgisayarı her açtığında kendiliğinden başlar.

**Instance adı farklı.** Odyssey `.\SQLEXPRESS`, `(localdb)\MSSQLLocalDB`,
`.` ve `localhost` adreslerini deniyor. Kurulumda `Basic` yerine `Custom`
seçip başka bir ad yazdıysan bulamaz. En kolayı kurulumu tekrarlayıp
`Basic` seçmek.

**Kurulum yarım kalmış.** Kurulum penceresini erken kapattıysan servis hiç
oluşmamış olabilir. Yükleyiciyi tekrar çalıştır.

## Kurulum "yeniden başlatma bekleniyor" diyor

Windows'ta bekleyen bir güncelleme varsa SQL Server kurulumu başlamıyor.
Bilgisayarı yeniden başlat, sonra yükleyiciyi tekrar çalıştır.

## Kurulum ".NET Framework" istiyor

Eski Windows sürümlerinde çıkıyor. Yükleyicinin verdiği bağlantıdan kur,
sonra kurulumu tekrarla.

## SSMS açılıyor ama bağlanamıyor

SSMS'in bağlantı penceresinde üç kutu var:

- **Server name**: `.\SQLEXPRESS` — baştaki nokta "bu bilgisayar" demek.
- **Authentication**: `Windows Authentication`. Kullanıcı adı ve parola
  istemiyor; Windows hesabınla giriyorsun.
- **Encryption**: `Optional`. Varsayılan `Mandatory` olduğunda yerel
  kurulumlarda sertifika hatası veriyor.

## Odyssey çalışıyor ama SSMS çalışmıyor (ya da tersi)

İkisi aynı sunucuya bağlanıyor, yani biri çalışıyorsa sunucu ayakta
demektir. Sorun diğerinin ayarında.

- Yalnızca SSMS bağlanıyorsa: ODBC sürücüsü eksik.
- Yalnızca Odyssey bağlanıyorsa: SSMS'in bağlantı penceresindeki üç kutuyu
  yukarıdaki gibi doldur.

## Alıştırma veritabanlarını silmek

Odyssey her alıştırma için `Odyssey_` önekli bir veritabanı açıyor. Silmen
gereken bir durum yok; yer kaplamasını istemiyorsan SSMS'te sağ tıklayıp
silebilirsin. Odyssey bir dahaki çalıştırmada yenisini kurar.
