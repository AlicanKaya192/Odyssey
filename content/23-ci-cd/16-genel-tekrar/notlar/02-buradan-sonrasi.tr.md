**Gerçek bir depoda ilk hat**

1. Depoda `.github/workflows/ci.yml` aç; yalnızca kodu çek ve testleri
   çalıştır. Bir PR açıp çalıştığını gör.
2. Hızlı kapıları ekle: biçim ve lint. Önce yerelde çalıştır, sonra hatta.
3. `permissions: contents: read` ve `timeout-minutes` ekle.
4. Testler yavaşsa önbellek; birden çok sürüm destekleniyorsa matris.
5. `main` için kural: PR zorunlu, zorunlu kontrol.
6. Yayın gerekiyorsa: etiketle başlayan iş, sürüm denetimi, bir kez derle.

Her adımdan sonra hattın gerçekten düştüğünü görmek için bir testi bilerek
boz: düşmeyen kapı kapı değildir.

**Bu modülde çalıştırmadıklarımız**

- İş akışlarını GitHub'ın makinesinde çalıştırmadık; durağan denetledik.
  Gerçek çalışmada eylemlerin sürümleri, makinenin kurulu araçları ve
  süreler sayfasında görünür.
- Eylem sürümleri (`@v4`, `@v5`) zamanla değişir; yeni bir dosya
  yazarken eylemin kendi sayfasına bakılır.
- Ücret ve sınırlar: açık depolarda GitHub'ın makineleri ücretsiz; özel
  depolarda aylık dakika sınırı var. Matris ve uzun işler dakikayı
  hızla tüketir.

**Odyssey'de buradan nereye?**

- **MLOps ve ML Sistem Tasarımı:** aynı hat bir modeli eğitmek, ölçmek,
  kaydetmek ve sunmak için.
- **Docker:** on ikinci bölümdeki imajları derinlemesine kurmak.
- **Git ile Sürüm Kontrolü:** dallar, birleştirme ve etiketler hattın dayandığı temel.
- **FastAPI ile REST API Yazmak:** testleri ve dağıtımı olan bir servis.

**Pratik öneriler**

1. Kendi küçük projene bu modüldeki bitirme hattını kur.
2. Hattın süresini ve en yavaş işini not et; kritik yoldan başla.
3. Kararsız bir test gördüğünde not al: hangi commit, hangi sonuç.
4. Her yeni eylemi eklemeden önce kimin yazdığına ve hangi izni istediğine
   bak.
5. Hattın dosyasını da kod gibi incele: PR'la değiştir, gerekçesini yaz.
