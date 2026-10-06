<div align="right">
  <b>Türkçe</b> · <a href="./README.md">English</a>
</div>

<p align="center">
  <img src="docs/media/banner_tr.png" alt="Odyssey: uygulamanın morunda, menderes bordürlü zeminde yayını germiş siyah figürlü bir sentor ve Odyssey yazısı" width="100%">
</p>

<p align="center">
  <a href="https://github.com/AlicanKaya192/Odyssey/releases"><img alt="Sürüm 0.9.2" src="https://img.shields.io/badge/S%C3%9CR%C3%9CM-0.9.2-7466EE?style=for-the-badge&labelColor=1E1A3C"></a>
  <img alt="Windows 10 ve 11" src="https://img.shields.io/badge/Windows-10%20%7C%2011-7466EE?style=for-the-badge&labelColor=1E1A3C">
  <img alt="Python 3.10 ile 3.14 arası" src="https://img.shields.io/badge/Python-3.10%E2%80%933.14-7466EE?style=for-the-badge&logo=python&logoColor=white&labelColor=1E1A3C">
  <img alt="Qt 6 ve PySide6 ile yapıldı" src="https://img.shields.io/badge/Qt%206-PySide6-7466EE?style=for-the-badge&logo=qt&logoColor=white&labelColor=1E1A3C">
  <br>
  <a href="LICENSE"><img alt="MIT lisansı" src="https://img.shields.io/github/license/AlicanKaya192/Odyssey?style=for-the-badge&label=L%C4%B0SANS&color=7466EE&labelColor=1E1A3C"></a>
  <img alt="Türkçe ve İngilizce" src="https://img.shields.io/badge/D%C4%B0L-TR%20%7C%20EN-7466EE?style=for-the-badge&labelColor=1E1A3C">
  <img alt="Çevrimdışı çalışır" src="https://img.shields.io/badge/%C3%87ALI%C5%9EIR-%C3%87EVR%C4%B0MDI%C5%9EI-7466EE?style=for-the-badge&labelColor=1E1A3C">
  <a href="https://github.com/AlicanKaya192/Odyssey/stargazers"><img alt="GitHub yıldızları" src="https://img.shields.io/github/stars/AlicanKaya192/Odyssey?style=for-the-badge&logo=github&color=7466EE&labelColor=1E1A3C"></a>
</p>

Python, veri bilimi, makine öğrenmesi, SQL, zaman serileri ve bunların arkasındaki matematiği bölüm bölüm öğreten, çevrimdışı çalışan bir masaüstü uygulaması.

Her bölümde konu anlatımı, ders notları, sınav ve kod alıştırmaları var; matematik bölümlerinde alıştırma yerine çizim kâğıdında çözülen problemler var. Bir bölümü tamamlamak için sınavı geçmek ve alıştırmaları çözmek gerekiyor. Kod uygulamanın içinde yazılıyor; program onu çalıştırıyor, ardından çıktısını, oluşturduğu değişkenleri ve tanımladığı fonksiyonları kontrol ediyor. Yapay zeka kullanılmıyor — her kontrol önceden tanımlıdır ve deterministik olarak değerlendirilir, yani aynı kod her zaman aynı sonucu verir.

## İçeriden bir bakış

**Açılış.** Uygulama yüklenirken Odyssey'in maskotu — antik Yunan vazolarındaki siyah figür üslubunda bir sentor — dörtnala gelip okunu atıyor ve ok hedefi tam ortadan vuruyor. Yaklaşık üç saniye sürüyor; `Esc`'ye basarak ya da tıklayarak geçebilirsiniz.

<p align="center">
  <img src="docs/media/startup_tr.gif" alt="Açılış animasyonu: sentor dörtnala gelip atıyor, ok hedefi vuruyor, ODYSSEY yazısı çıkıyor ve Öğrenme Yolu açılıyor" width="880">
</p>

**Konu anlatımları** formüller, şekiller ve sayfanın başlık listesiyle geliyor; nereye kadar okuduğunuzu hatırlıyor.

<p align="center">
  <img src="docs/media/lesson_tr.gif" alt="Lojistik Regresyon dersini formülleri ve şekilleriyle aşağı kaydırmak" width="880">
</p>

**Alıştırmalar** kodunuzu uygulamanın içinde çalıştırıyor. Sonuç editörün altındaki terminalde görünüyor; kod bir grafik çizdiyse solda açılıyor.

<p align="center">
  <img src="docs/media/exercise_tr.gif" alt="Bir alıştırmada kodu yazıp çalıştırmak: terminalde sonuç, solda kodun çizdiği grafik" width="880">
</p>

**Adım adım** kodunuzu satır satır oynatıyor: editörde sıradaki satır işaretleniyor, altta bütün değişkenler — yeni gelen yeşil, değişen sarı — ve o ana kadarki çıktı görünüyor. Kodunuz boşsa ya da nereden başlayacağınızı bilmiyorsanız **örnek çözüme** geçip doğrusunun nasıl ilerlediğini izleyebiliyorsunuz; kendi kodunuz yerinde kalıyor.

<p align="center">
  <img src="docs/media/trace_tr.gif" alt="Bir döngü yazıp Adım adım'a basmak ve değişkenler ile çıktı değişirken satır satır ilerlemek, sonra örnek çözüme geçmek" width="880">
</p>

**Terimler** derste ilk geçtikleri yerde noktalı altı çizgiyle işaretli; üzerine gelince sayfadan çıkmadan kısa açıklaması görünüyor. Bütün terimler **Hakkında › Sözlük**'te; `Ctrl+K` ile de bulunuyor.

<p align="center">
  <img src="docs/media/glossary_tr.gif" alt="Fonksiyonlar dersinde altı çizili terimlerin üzerine gelip açıklamalarını görmek, sonra Ctrl+K ile parametre arayıp Sözlük'te ona gitmek" width="880">
</p>

**Sınavlar** her bölümü kapatıyor. Fareyle ya da klavyeyle (`1–4` veya `A–D`, sonra `Enter`) cevaplıyorsunuz; her cevaptan sonra doğrusu ve açıklaması çıkıyor. Başlangıç kartında önceki denemelerinizin özeti, sonuçta kaç doğru, yanlış ve boş bıraktığınız var. Bir alıştırmada üç kez üst üste takılırsanız **Takıldın mı?** kartı sizi dersin ilgili kısmına yönlendiriyor.

<p align="center">
  <img src="docs/media/quiz_tr.gif" alt="En iyi ve son puanı gösteren sınav başlangıç kartı, klavyeyle cevaplanan dört soru, sonra doğru, yanlış, boş ve süreyi gösteren sonuç kartı" width="880">
</p>

**Bir kısmını zaten biliyor musunuz?** Patikanın başındaki isteğe bağlı seviye tespit sınavı her bölümden dört soru soruyor ve bildiğiniz bölümleri açıyor; gerçekten olduğunuz yerden başlıyorsunuz. Açılan bölümler tamamlanmış sayılmıyor.

<p align="center">
  <img src="docs/media/placement_tr.gif" alt="Python yolundan seviye tespit sınavını açmak, soruları cevaplamak, bilinen bölümleri listeleyen sonuç ve açılan bölümleriyle yol" width="880">
</p>

**Matematik problemleri** çizim kâğıdında elle çözülüyor. Yalnızca cevap denetleniyor; çözünce ya da iki yanlıştan sonra çözüm yolları solda açılıyor, kendi adımlarınızla karşılaştırabiliyorsunuz.

<p align="center">
  <img src="docs/media/problem_tr.gif" alt="Bir logaritma denklemini çizim kâğıdında çözmek, cevabı denetlemek ve çözüm yollarını açmak" width="880">
</p>

**Notlar** dersin yanında alınıyor: sayfadan bir cümle alıntılayın, kendi sözlerinizi ekleyin; yazdıkça kaydediliyor. **Notlarım** hepsini patikalara göre ve kendi klasörlerinizde topluyor; genel arama (`Ctrl+K`) onları da buluyor, notlarınızı indirip yükleyebiliyorsunuz.

<p align="center">
  <img src="docs/media/notes_tr.gif" alt="Paketler ve Ortamlar dersinde not panelini açmak, bir cümle alıntılamak, not yazmak ve notu Notlarım'da açmak" width="880">
</p>

**Rotalar** hedefinize göre bir sıra öneriyor — sıfırdan başlamak, veri bilimine geçmek ya da ML mühendisi olmak. Her adım neleri kapsadığını, sonunda neler yapabileceğinizi ve yaklaşık süresini söylüyor; odaklanılacak bölümler tek tıkla açılıyor.

<p align="center">
  <img src="docs/media/roadmap_tr.gif" alt="Sıfırdan başlıyorum rotasını kaydırmak, ardından Veri Bilimci rotasına ve odaklanılacak bölümlerine geçmek" width="880">
</p>

**Bir bölümü bitirmek ya da rozet kazanmak** sağ alt köşede bir kartla kutlanıyor.

<p align="center">
  <img src="docs/media/celebration_tr.gif" alt="Sağ alt köşede art arda beliren bir bölüm kartı ve iki rozet kartı" width="410">
</p>

**Güncellemeler** siz çalışmaya devam ederken kendi penceresinde iniyor: sentor koşarken boyut, hız ve kalan süre görünüyor; bitince okunu atıyor ve yeni sürüm kuruluyor.

<p align="center">
  <img src="docs/media/update_tr.gif" alt="Yeni sürüm bildirimi, ardından koşan sentor ve yüzde, megabayt ve hızla ilerleyen indirme penceresi" width="880">
</p>

**Kapatırken** onay istiyor; ilerlemenizin kaydedildiğini ve serinizin bugün güvende olup olmadığını söylüyor.

<p align="center">
  <img src="docs/media/exit_tr.gif" alt="Hilalin altında el sallayan sentorlu çıkış penceresi, Vazgeç ve Çık düğmeleri" width="880">
</p>

## Başlarken

**1. Kurulum dosyasını indirin.** [Releases](https://github.com/AlicanKaya192/Odyssey/releases) sayfasından `Odyssey-<sürüm>-setup.exe` dosyasını alın. Windows 10 veya 11, 64-bit. Yönetici yetkisi gerekmiyor.

**2. Çalıştırın.** Odyssey kendi kullanıcı hesabınıza, `%LOCALAPPDATA%\Programs\Odyssey` altına kuruluyor; Başlat menüsüne ve — kutuyu kaldırmazsanız — masaüstüne kısayol koyuyor. Bundan sonra kısayoldan açıyorsunuz.

**3. Windows ilk seferde uyarı verebilir.** "Windows kişisel bilgisayarınızı korudu" yazan mavi bir kutu çıkıyor. Bu SmartScreen ve sebebi kurulum dosyasının **imzalı olmaması**: Windows yayıncının kim olduğunu göremiyor, o yüzden daha önce görmediği her programa aynı uyarıyı veriyor. **Ek bilgi**'ye, ardından **Yine de çalıştır**'a tıklayın. Akıllı Uygulama Denetimi açıksa Windows kurulum dosyasını tamamen engelleyebilir; imzalı sürümler yolda, ayrıntı için [kod imzalama politikasına](CODE_SIGNING.tr.md) bakın.

**Çıkardığınız bir klasörden mi geliyorsunuz?** 0.8.2.1'e kadarki sürümler sizin çıkardığınız bir zip'ti. Üstüne elle kurmayın, uygulamanın içinden güncelleyin: yeni sürümü kuruyor, eski klasördeki program dosyalarını kaldırıyor ve ilerlemenizi koruyor. 0.8.2.1'den eski bir sürüm önce 0.8.2.1'i, ardından kurulumu öneriyor.

### İlerlemeniz uygulamanın dışında duruyor

Yaptığınız her şey — ilerlemeniz, sınav notlarınız, yazdığınız kodlar, notlarınız, profiliniz ve seçtiğiniz fotoğraf — uygulama klasöründe değil, `%APPDATA%\Odyssey\` içinde saklanıyor.

Bu ayrım bilinçli: yeni sürüm kurmak, kaldırmak ya da yeniden kurmak ilerlemenize dokunmuyor. Güncellediğinizde kaldığınız yerden devam ediyorsunuz.

### Güncelleme

Odyssey her açılışta yeni bir sürüm çıkıp çıkmadığına bakıyor; açık bırakırsanız üç saatte bir yeniden bakıyor. Yeni sürüm varsa haber veriyor ve kurmayı öneriyor.

**Güncelle**'ye bastığınızda uygulama yeni kurulum dosyasını indiriyor, sağlam geldiğini denetliyor ve kapanıyor; kurulum kendiliğinden tamamlanıyor ve Odyssey yeniden açılıyor. İlerlemenize dokunulmuyor. 0.9.1'den itibaren güncelleme kurulum dosyasının tamamını değil, yalnızca değişen dosyaları indiriyor.

Güncelleme başlatılamıyorsa — örneğin diskte yer yoksa — uygulama sebebini söylüyor ve sürüm sayfasını veriyor. Elle yapmak her zaman aynı şey: yeni kurulum dosyasını indirip çalıştırmak.

Denetimi **Ayarlar › Güncelleme** bölümünden kapatabilirsiniz. Kapalıyken uygulama ağa hiç çıkmıyor.

### Kaldırma

**Ayarlar › Uygulamalar › Yüklü uygulamalar › Odyssey › Kaldır** uygulamayı kaldırıyor. `%APPDATA%\Odyssey\` içindeki ilerlemeniz yerinde kalıyor, sonradan kurarsanız kaldığınız yerden devam ediyorsunuz; her şeyi silmek istiyorsanız o klasörü de silin.

## Durum

Erken geliştirme aşaması (`0.9.2`), açık beta olarak yayınlandı. Uygulama uçtan uca çalışıyor. Motor — öğrenme yolları, konu anlatımı, sınavlar, alıştırma çalıştırıcısı, ilerleme kaydı, güncelleme — yerinde; müfredat büyümeye devam ediyor.

**Bugünkü içerik:** altı patika **tamamlandı** — Python Temelleri (on sekiz bölüm, paketler ve ortamlarla başlıyor), Veri Bilimi (on), Makine Öğrenmesi (on üç), SQL (on altı; SQL Server'ı kurmaktan pencere fonksiyonlarına, dizinlere, görünümlere ve saklı yordamlara), Zaman Serileri (yirmi üç; tarihlerle çalışmaktan tahmine, tahmin aralıklarına ve anomali tespitine) ve iki modüllü Matematik: Temel Matematik (yirmi sekiz bölüm, sayılardan olasılık ve istatistiğe) ve Yapay Zekanın Matematiği (otuz iki; doğrusal cebir, kalkülüs, olasılık ve istatistik). 4026 sınav sorusu, 442 kod alıştırması, 300 matematik problemi, 285 ders notu ve 92 terimlik bir sözlük; tamamı Türkçe ve İngilizce.

**On üç öğrenme patikası** tanımlı: Python, Veri Bilimi, Makine Öğrenmesi, SQL, Matematik ve Zaman Serileri açık; API, Docker, Doğal Dil İşleme ve diğerleri içerikleri hazırlanana kadar kilitli görünüyor.

**Çalışanlar:** sentor maskotlu açılış animasyonu, öğrenme patikaları, bölüm içi başlık listesi ve okuma takibiyle konu anlatımı, ders notları, süreli sınavlar, Python ve SQL için otomatik kontrollü kod alıştırmaları (SQL kendi SQL Server'ınızda çalışıyor, her deneme geri alınıyor), kademeli ipuçları, hatalı satırı editörde işaretleyen hata açıklamaları, kodunuzu ve örnek çözümü adım adım izleme, derslerin içinde açıklaması görünen terimler sözlüğü, takılınca dersin ilgili kısmına yönlendirme, bildiğiniz bölümleri açan seviye tespit sınavı, çizim kâğıdında çözülen ve adım adım çözüm yolları olan matematik problemleri, önerilen çalışma rotaları, Windows bildirimi olarak gelen seri hatırlatmaları, sırayla açılan bölümler, kalıcı ilerleme kaydı, kendi notlarınız ve genel arama (`Ctrl+K`), kazanınca bir kartla kutlanan 32 rozet, XP, seviyeler ve profilde gösterilebilen unvanlar, Pomodoro ve başka düzenlerle çalışma zamanlayıcısı, alıştırma ve sınavlarda geçmiş denemeler, klavyeyle cevaplanabilen sınavlar, tam ekran okuma odağı, seviyeniz, rozetleriniz ve çalışma takviminizle paylaşım kartı, ilerlemeyi başka bir bilgisayara taşıma ve günlük yedek, yeni gelenler için tanıtım turu, etkinlik takvimi, kendi fotoğrafınızı seçebildiğiniz profil, Türkçe/İngilizce arayüz ve içerik, açık/koyu tema, uygulama içinden güncelleme, kilidi ve sınav süresini kaldırma seçenekleri.

**Henüz yok:** diğer patikaların içeriği ve bir veri setini baştan sona işleyen proje tipi alıştırmalar için daha geniş bir alıştırma motoru.

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

Uygulama yalnızca güncelleme denetimini açık bırakırsanız ağa çıkar: yukarıda anlatılan sürüm denetimi için ve onunla birlikte, alt şeritte görünen, Odyssey'in GitHub'daki yıldız sayısını okumak için. İki istekte de hiçbir bilgi gönderilmez — kimlik, ilerleme, kullanım verisi yok — ve dosya yalnızca siz Güncelle'ye bastığınızda iniyor. Denetim kapalıyken uygulama ağa hiç çıkmaz.

"Bağlantılarım" ve "Ekstra İçerikler" sekmelerindeki adresler uygulamanın içinde açılmaz; tıklandığında sistemin tarayıcısına devredilir.

## Katkıda bulunma

Sorun bildirimleri ve pull request'ler açığa açık. Önce [CONTRIBUTING.md](CONTRIBUTING.md) ve [Davranış Kuralları](CODE_OF_CONDUCT.md) dosyalarını okuyun. Güvenlik bildirimlerinin ayrı bir yolu var: [SECURITY.md](SECURITY.md). Sürümlerin nasıl derlenip imzalandığı: [CODE_SIGNING.tr.md](CODE_SIGNING.tr.md).

## Lisans

MIT Lisansı — Telif hakkı (c) 2026 Alican Kaya. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.

Ders içeriği [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) projesinden geliyor ve aynı lisansa tabi.
