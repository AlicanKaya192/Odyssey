<div align="right">
  <b>Türkçe</b> · <a href="./README.md">English</a>
</div>

# Odyssey

Data Science ve Machine Learning konularını bölüm bölüm öğreten, çevrimdışı çalışan bir masaüstü uygulaması.

Her bölümde konu anlatımı, ders notları, sınav ve kod alıştırmaları var. Bir bölümü tamamlamak için sınavı geçmek ve alıştırmaları çözmek gerekiyor. Kod uygulamanın içinde yazılıyor; program onu çalıştırıyor, ardından çıktısını, oluşturduğu değişkenleri ve tanımladığı fonksiyonları kontrol ediyor. Yapay zeka kullanılmıyor — her kontrol önceden tanımlıdır ve deterministik olarak değerlendirilir, yani aynı kod her zaman aynı sonucu verir.

## Başlarken

**1. Paketi indirin.** [Releases](https://github.com/AlicanKaya192/Odyssey/releases) sayfasından `Odyssey-<sürüm>-windows-x64.zip` dosyasını alın. Windows 10 veya 11, 64-bit. Kurulum sihirbazı yok, yönetici yetkisi gerekmiyor.

**2. Klasörün tamamını çıkarın — uygulamayı zip'in içinden çalıştırmayın.** Windows zip dosyasını sıradan bir klasör gibi açıyor ve `Odyssey.exe` orada çalıştırılabilir görünüyor. Değil: uygulamanın yanındaki `_internal` klasörüne ihtiyacı var, Windows ise yalnızca çift tıkladığınız tek dosyayı çıkarıyor. Zip'e sağ tıklayıp **Tümünü Ayıkla** deyin ve `Odyssey` klasörünü bütün hâlde tutun.

Yazma izniniz olan bir yere koyun: masaüstü, belgeler ya da kendi açtığınız bir klasör. `C:\Program Files` içine koymayın — uygulama güncellenirken kendi dosyalarını değiştiriyor ve orası yönetici yetkisi istiyor.

**3. `Odyssey.exe` dosyasını çalıştırın.** İlk açılış sonrakilerden birkaç saniye uzun sürüyor.

**4. Windows ilk seferde uyarı verecek.** "Windows kişisel bilgisayarınızı korudu" yazan mavi bir kutu çıkıyor. Bu SmartScreen ve sebebi uygulamanın **imzalı olmaması**: Windows yayıncının kim olduğunu göremiyor, o yüzden daha önce görmediği her programa aynı uyarıyı veriyor. **Ek bilgi**'ye, ardından **Yine de çalıştır**'a tıklayın. Windows seçiminizi hatırlıyor, bir daha sormuyor.

### İlerlemeniz uygulamanın dışında duruyor

Yaptığınız her şey — ilerlemeniz, sınav notlarınız, yazdığınız kodlar, profiliniz ve seçtiğiniz fotoğraf — çıkardığınız klasörde değil, `%APPDATA%\Odyssey\` içinde saklanıyor.

Bu ayrım bilinçli: uygulama klasörünü değiştirebilir, silebilir ya da başka bir sürücüye taşıyabilirsiniz, hiçbiri ilerlemenize dokunmuyor. Güncellediğinizde kaldığınız yerden devam ediyorsunuz.

### Güncelleme

Odyssey her açılışta yeni bir sürüm çıkıp çıkmadığına bakıyor; açık bırakırsanız üç saatte bir yeniden bakıyor. Yeni sürüm varsa haber veriyor ve kurmayı öneriyor.

**Güncelle**'ye bastığınızda uygulama yeni sürümü indiriyor, dosyanın sağlam geldiğini denetliyor, kendini kapatıyor, dosyalarını değiştiriyor ve tekrar açılıyor — toplam bir dakika kadar, ilerleme baştan sona ekranda. İlerlemenize dokunulmuyor.

Güncelleme yapılamıyorsa — klasöre yazılamıyor ya da diskte yer yok — uygulama sebebini söylüyor ve sürüm sayfasını veriyor, elle yapabilirsiniz. Elle yapmak her zaman aynı şey: yeni klasörü eskisinin yerine çıkarmak.

Denetimi **Ayarlar › Güncelleme** bölümünden kapatabilirsiniz. Kapalıyken uygulama ağa hiç çıkmıyor.

## Durum

Erken geliştirme aşaması (`0.7.3.1`), açık beta olarak yayınlandı. Uygulama uçtan uca çalışıyor. Motor — öğrenme yolları, konu anlatımı, sınavlar, alıştırma çalıştırıcısı, ilerleme kaydı, güncelleme — yerinde; müfredat büyümeye devam ediyor.

**Bugünkü içerik:** iki modül **tamamlandı**. Python Temelleri on beş bölüm, ilk programdan veritabanına kadar; Veri Bilimi on bölüm, NumPy'dan keşifçi analize kadar. 560 sınav sorusu, 115 kod alıştırması ve 54 ders notu; tamamı Türkçe ve İngilizce.

**Altı öğrenme patikası** tanımlı: Python ve Veri Bilimi açık; Makine Öğrenmesi, SQL, API ve Docker içerikleri hazırlanana kadar kilitli görünüyor.

**Çalışanlar:** öğrenme patikaları, bölüm içi başlık listesi ve okuma takibiyle konu anlatımı, ders notları, süreli sınavlar, otomatik kontrollü kod alıştırmaları, kademeli ipuçları, hata açıklamaları, sırayla açılan bölümler, kalıcı ilerleme kaydı, 19 rozet ve etkinlik takvimi, kendi fotoğrafınızı seçebildiğiniz profil, Türkçe/İngilizce arayüz ve içerik, açık/koyu tema, uygulama içinden güncelleme, kilidi ve sınav süresini kaldırma seçenekleri.

**Henüz yok:** diğer dört patikanın içeriği, kendi notlarınızı tutabileceğiniz alan ve bir veri setini baştan sona işleyen proje tipi alıştırmalar için daha geniş bir alıştırma motoru.

Yol haritası [CHANGELOG.md](CHANGELOG.md) dosyasında ilerliyor.

## Kaynak koddan çalıştırma

- Windows 10 / 11
- Python 3.10 – 3.14 (temiz bir CPython kurulumu)

Anaconda'nın Python'unu kullanmayın. Anaconda kendi MSVC çalışma zamanı kütüphanelerini taşıyor; Qt'nin DLL'leri onları yüklediğinde uygulama açılmıyor.

```bash
py -3.14 tools/setup_env.py
```

Bu komut hem uygulamanın çalıştığı ortamı hem de alıştırmaların çalıştığı ayrı ortamı kuruyor. Ardından:

```bash
.venv\Scripts\python app\main.py
```

## Diller

Arayüz ve içerik Türkçe ve İngilizce. Ayarlardan istediğiniz an değiştirebilirsiniz, uygulamayı yeniden başlatmaya gerek yok. Kendiniz seçene kadar uygulama, Türkçe bir bilgisayarda Türkçe, diğerlerinde İngilizce açılıyor. Bir bölümün İngilizce çevirisi henüz yoksa Türkçesi gösterilir ve üstte bunu belirten bir uyarı çıkar.

## Alıştırmalar nasıl kontrol ediliyor?

Kodunuz ayrı bir işlemde, izole bir çalışma klasöründe çalıştırılır. Ardından çıktısı, oluşturduğu değişkenler ve tanımladığı fonksiyonlar beklenen değerlerle karşılaştırılır. Kontrollerin tamamı önceden tanımlıdır; kod değerlendirmesinde herhangi bir dış servis kullanılmaz.

**Not:** Bu bir güvenlik sandbox'ı değildir. Kendi yazdığınız kodu kendi bilgisayarınızda çalıştırıyorsunuz. Sistemin sağladığı şey izole bir çalışma klasörü, zaman aşımı sınırı, çıktı sınırı ve kodun hata vermesi durumunda uygulamanın çökmemesidir.

## İnternet

Öğrenmeyle ilgili her şey çevrimdışı çalışır: dersler, ders notları, sınavlar, alıştırmalar ve ilerlemeniz. Hiçbiri bir sunucuya uğramaz; ilerlemeniz bilgisayarınızdan çıkmaz.

Uygulamanın yaptığı tek ağ çağrısı var, o da açık bırakırsanız: yukarıda anlatılan sürüm denetimi. Bu istekte hiçbir bilgi gönderilmez — kimlik, ilerleme, kullanım verisi yok — ve dosya yalnızca siz Güncelle'ye bastığınızda iniyor.

"Bağlantılarım" ve "Ekstra İçerikler" sekmelerindeki adresler uygulamanın içinde açılmaz; tıklandığında sistemin tarayıcısına devredilir.

## Katkıda bulunma

Sorun bildirimleri ve pull request'ler açığa açık. Önce [CONTRIBUTING.md](CONTRIBUTING.md) ve [Davranış Kuralları](CODE_OF_CONDUCT.md) dosyalarını okuyun. Güvenlik bildirimlerinin ayrı bir yolu var: [SECURITY.md](SECURITY.md).

## Lisans

MIT Lisansı — Telif hakkı (c) 2026 Alican Kaya. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.

Ders içeriği [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) projesinden geliyor ve aynı lisansa tabi.
