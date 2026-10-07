"Yapılandırma ortamda durur" kuralı, bulut uygulamaları için yazılmış ve
çok yaygın bir ilke listesinden geliyor: **On İki Faktörlü Uygulama**
(The Twelve-Factor App). Konteynerlerle çalışırken en çok işine yarayacak
maddeleri:

## III. Yapılandırma ortamda

Kod her yerde aynı; ortama göre değişen her şey (veritabanı adresi,
anahtarlar, kip) ortam değişkeninde. Bir test: **kodu bugün herkese açık
yapsan bir sır sızar mıydı?** Sızardıysa o sır koddadır.

## V. Kur, yayınla, çalıştır ayrı

- **Kur** (build): koddan imaj → `docker build`.
- **Yayınla** (release): imaj + o ortamın ayarları.
- **Çalıştır** (run): `docker run -e ...`.

Aynı imaj test sunucusunda denenip **değiştirilmeden** gerçek sunucuya
gidiyor; yalnızca ayarlar farklı. "Testte çalışıyordu, yayında bozuldu"
sorununun ilacı.

## VI. Süreçler durumsuz

Program kalıcı bilgiyi kendi içinde değil, bir veritabanında ya da volume'da
tutar. Konteyner her an silinip yeniden oluşturulabilir (İlk Konteynerler
bölümündeki kural).

## VII. Port yayınlama

Program kendisi bir portu dinler ve dışarıya o portla hizmet verir (Portlar
bölümü).

## IX. Hızlı açılış, düzgün kapanış

Hızlı açılan ve SIGTERM'de düzgün kapanan programlar kolayca taşınır,
çoğaltılır, yeniden başlatılır (CMD ve ENTRYPOINT bölümü).

## XI. Günlükler bir akış

Program günlüğünü bir dosyaya değil **standart çıktıya** (`print`) yazar;
toplamak Docker'ın işi (`docker logs`).

## Ne kazandırıyor?

Bu kurallara uyan bir imajı herhangi bir sunucuda, bulutta ya da
arkadaşının bilgisayarında **hiç değiştirmeden** çalıştırabiliyorsun:
Docker'ın vaat ettiği şey tam olarak bu.
