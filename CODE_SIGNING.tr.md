[English](CODE_SIGNING.md) | **Türkçe**

# Kod imzalama politikası

Odyssey'in Windows kurulum dosyaları ve program dosyaları, Windows'un
yayıncıyı tanıyabilmesi için kod imzasıyla imzalanacak. Açık kaynak
projeleri ücretsiz imzalayan [SignPath Foundation](https://signpath.org)
programına başvurduk. Proje onaylanana kadar sürümler **imzasız**; Windows
"Windows kişisel bilgisayarınızı korudu" uyarısı gösterebilir ya da
Akıllı Uygulama Denetimi kurulum dosyasını engelleyebilir.

Onaydan sonra:

> Ücretsiz kod imzası [SignPath.io](https://about.signpath.io) tarafından
> sağlanır, sertifika [SignPath Foundation](https://signpath.org)'a aittir.

Sertifika SignPath Foundation adına verildiği için Windows yayıncı olarak
**SignPath Foundation** gösterir.

## Neler imzalanır

Yalnızca bu deponun açık kaynak kodundan, GitHub'ın sunucularında,
[yayın iş akışıyla](.github/workflows/release.yml) derlenen dosyalar:

1. Paketlenmiş uygulama: `Odyssey.exe` ve içindeki çalıştırılabilir
   dosyalar (`.dll`, `.pyd`).
2. Bu imzalı dosyalardan derlenen kurulum dosyaları:
   `Odyssey-X.Y.Z-setup.exe` ve fark kurulumları
   `Odyssey-X.Y.Z-patch-A.B.C.exe`.

Kişisel bir bilgisayarda derlenen hiçbir dosya imzalanmaz. Her imza isteği
imza atılmadan önce elle onaylanır.

## Ekip ve roller

| Rol | Kim | Anlamı |
|---|---|---|
| Yazar | [Alican Kaya](https://github.com/AlicanKaya192) | Kaynak kodu doğrudan yazar ve değiştirir. |
| İnceleyici | [Alican Kaya](https://github.com/AlicanKaya192) | Dışarıdan gelen her katkıyı (pull request) birleştirmeden önce inceler. |
| Onaylayıcı | [Alican Kaya](https://github.com/AlicanKaya192) | Her sürüm için imza isteğini onaylar. |

Ekipteki herkes GitHub'da ve SignPath'te iki adımlı doğrulama kullanır.

## Gizlilik

Odyssey çevrimdışı çalışır. İlerlemeniz, kodlarınız, notlarınız ve
ayarlarınız bilgisayarınızda, `%APPDATA%\Odyssey` klasöründe kalır ve hiçbir
yere yüklenmez. Kullanım verisi toplanmaz; hesap ya da bize ait bir sunucu
yoktur.

Program yalnızca aşağıdakiler için ağa bağlanır ve hiçbirinde kişisel veri
göndermez:

- **Sürüm denetimi.** Açılışta (ve açık kaldıkça üç saatte bir) GitHub'a
  (`api.github.com`) yeni bir sürüm çıkıp çıkmadığını sorar ve deponun
  yıldız sayısını gösterir. Ayarlar › Güncelleme'den kapatılır; kapalıyken
  program iki isteği de yapmaz.
- **Güncellemeyi indirmek,** yalnızca **Güncelle**'ye bastığınızda,
  GitHub'ın sürüm sayfasından.
- **Discord durumu.** Discord masaüstü uygulaması açıksa Odyssey, hangi
  ekranda ya da bölümde olduğunuzu bilgisayarınızdaki Discord uygulaması
  üzerinden Discord durumunuzda gösterir. Notlarınızın adı ve içeriği asla
  gönderilmez. Ayarlar › Görünüm'den kapatılır.
- **Tıkladığınız bağlantılar** kendi tarayıcınızda açılır.

SQL alıştırmaları internete değil, kendi bilgisayarınızdaki SQL Server'a
bağlanır.
