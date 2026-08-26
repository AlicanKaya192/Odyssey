# Güvenlik Politikası

## Desteklenen Sürümler

Proje erken geliştirme aşamasında. Güvenlik bildirimleri her zaman **`main`
dalının en güncel hâli** ve **en son yayınlanan sürüm** için değerlendirilir.

| Sürüm | Destekleniyor mu? |
|---|:-:|
| `main` (geliştirme) | ✅ |
| En son yayınlanan sürüm | ✅ |
| Daha eski sürümler | ❌ |

## Uygulamanın güvenlik yüzeyi

Bu bir masaüstü uygulaması, bir servis değil. Bilinmesi gerekenler:

**Sunucu yok, hesap yok, telemetri yok.** İlerlemen, profilin ve yazdığın
kodlar yalnızca kendi bilgisayarında, `%APPDATA%\Odyssey\progress.db`
dosyasında durur. Hiçbir veri dışarı gönderilmez.

**Uygulama şu an hiçbir ağ çağrısı yapmıyor.** İleride eklenecek güncelleme
kontrolü ayarlardan kapatılabilir olacak.

"Bağlantılarım" ve "Ekstra İçerikler" bölümlerindeki adresler uygulamanın
içinde açılmaz; tıklandığında sistem tarayıcısına devredilir.

**Uygulama kullanıcının yazdığı Python kodunu çalıştırır.** Bu, tasarımın
kendisi — alıştırmalar böyle kontrol ediliyor. Ancak açıkça söylemek gerekir:

> **Bu bir güvenlik sandbox'ı değildir.** Kullanıcı kendi kodunu kendi
> bilgisayarında çalıştırıyor. Sistemin sağladığı şey izole bir çalışma
> klasörü, zaman aşımı, çıktı sınırı ve kodun hata vermesi durumunda
> uygulamanın çökmemesidir. Kötü niyetli bir kodu durdurmaz.

Bu yüzden **başkasından gelen alıştırma içeriğini incelemeden eklemeyin.**
`content/` klasörüne konan bir `solution.py` veya veri dosyası, alıştırma
çalıştırıldığında sizin haklarınızla çalışır.

## Güvenlik açığı bildirme

Aşağıdaki türde bulgular güvenlik açığı sayılır ve bildirilmesi rica olunur:

- Kod içinde yanlışlıkla bırakılmış bir API anahtarı, token veya kimlik bilgisi
- Kullanıcı verisinin beklenmedik biçimde uygulama dışına çıkması
- Uygulamanın, kullanıcı istemeden bir ağ adresine bağlanması
- Alıştırma çalıştırıcısının, olması gerekenden fazla yetkiyle çalışması ya da
  izole çalışma klasörünün dışına yazması
- Bağımlılıklardan gelen ve bu projeyi doğrudan etkileyen bilinen bir açık
- Güncelleme mekanizmasının doğrulanmamış içerik yüklemesi

**Şunlar güvenlik açığı sayılmaz:** kullanıcının kendi yazdığı kodun kendi
dosyalarına erişebilmesi (tasarım gereği), sonsuz döngü yazan kodun CPU
kullanması (zaman aşımıyla durdurulur).

### Nasıl bildirilir

Açığı **herkese açık bir issue'da paylaşmayın.** Bunun yerine:

1. GitHub'ın [Security Advisories](https://github.com/AlicanKaya192/Odyssey/security/advisories/new)
   bölümünden özel bir bildirim açın, ya da
2. [GitHub profilimdeki](https://github.com/AlicanKaya192) iletişim
   adreslerinden birinden yazın.

Bildirimde şunlar olursa değerlendirme hızlanır: etkilenen sürüm, adım adım
nasıl tekrarlanacağı, olası etkisi ve varsa bir düzeltme fikri.

### Süreç

- **48 saat içinde** bildirimin alındığını teyit ederim.
- **7 gün içinde** açığın geçerli olup olmadığını ve etkisini bildiririm.
- Geçerliyse düzeltme yayınlanana kadar bilgilendirmeye devam ederim.
- Düzeltme yayınlandığında, isterseniz sürüm notlarında adınızı anarım.

Proje tek kişilik ve gönüllü yürüyor; süreler iyi niyetli hedeflerdir, taahhüt
değildir.
