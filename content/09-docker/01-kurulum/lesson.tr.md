# Docker'ı Kurmak

Bu bölüm tek bir şey yapıyor: **Docker'ı bilgisayarına kuruyor ve
çalıştığını gösteriyor.** Sonunda ilk konteynerini çalıştırmış ve
patikanın bütün alıştırmalarında kullanılacak iki imajı indirmiş olacaksın.

Kurulum bir kez yapılıyor ve 15–30 dakika sürüyor (çoğu indirme ve yeniden
başlatma). Adımları sırayla izle; bir yerde takılırsan bu bölümün
"Kurulum Sorunları" notuna bak.

## Ne kuracağız?

Windows'ta Docker'ın adı **Docker Desktop**. Tek bir kurulum programı
şunların hepsini getiriyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Docker Engine</span><span>Konteynerleri çalıştıran motor. Arka planda çalışır.</span></div>
    <div class="anat-row"><span>docker komutu</span><span>Terminalde yazacağın komut (Client).</span></div>
    <div class="anat-row"><span>Docker Desktop</span><span>Motoru açıp kapatan ve durumunu gösteren pencere.</span></div>
    <div class="anat-row"><span>WSL 2</span><span>Motorun içinde çalıştığı küçük Linux. Docker Desktop kendisi ayarlıyor.</span></div>
  </div>
  <figcaption>Hepsi tek kurulumla geliyor; ayrı ayrı kurman gerekmiyor.</figcaption>
</figure>

**WSL 2** (Windows Subsystem for Linux) Windows'un içinde gerçek bir Linux
çekirdeği çalıştıran Microsoft bileşeni. Linux konteynerleri bir Linux
çekirdeği istediği için Docker Desktop onu kullanıyor. Çoğu güncel Windows'ta
zaten var; yoksa kurulum seni yönlendiriyor.

Mac kullanıyorsan Docker Desktop for Mac, Linux kullanıyorsan doğrudan
**Docker Engine** kuruluyor (docs.docker.com/engine/install). Komutların
hepsi aynı.

## Gereksinimler

- **Windows 10 (22H2) ya da Windows 11**, 64 bit.
- **Donanım sanallaştırması açık.** Görev Yöneticisi › Performans › CPU
  sayfasının sağ altında **Sanallaştırma: Etkin** yazmalı. Kapalıysa BIOS
  ayarından açılıyor (notta anlatılıyor).
- **En az 4 GB bellek**, rahat çalışmak için 8 GB.
- Diskte birkaç GB boş yer: Docker Desktop ~2 GB, imajlar ayrıca.

Docker Desktop kişisel kullanım, eğitim ve küçük işletmeler (250 kişiden ve
10 milyon dolar yıllık gelirden az) için ücretsiz. Büyük bir şirkette iş
için kullanacaksan şirketin lisansı olmalı.

## Adım 1 — İndir

1. **docker.com** sitesinde **Docker Desktop**'ı aç ve **Download for
   Windows** düğmesine bas. (Bilgisayarın ARM işlemciliyse "ARM64" sürümünü
   seç; çoğu bilgisayar "AMD64 / x86_64".)
2. İnen dosyanın adı **Docker Desktop Installer.exe**; boyutu yarım
   gigabayt civarında.

## Adım 2 — Kur

1. **Docker Desktop Installer.exe**'ye çift tıkla. Yönetici izni isterse
   **Evet** de.
2. Yapılandırma ekranında **Use WSL 2 instead of Hyper-V (recommended)**
   seçeneği işaretli kalsın. "Add shortcut to desktop" isteğe bağlı.
3. **OK**'a bas; dosyalar kopyalanıyor (birkaç dakika).
4. Bitince **Close and restart** (ya da "Close and log out") düğmesi
   çıkıyor. Bas; bilgisayar yeniden başlıyor.

Kurulum WSL'nin eksik ya da eski olduğunu söylerse yönetici olarak açılmış
bir PowerShell'de şunu çalıştır, sonra bilgisayarı yeniden başlat:

```text
wsl --install
```

## Adım 3 — İlk açılış

1. Başlat menüsünden **Docker Desktop**'ı aç.
2. **Docker Subscription Service Agreement** penceresi çıkıyor; okuyup
   **Accept** de.
3. Oturum açma (sign in) istenirse **Skip** ya da "Continue without signing
   in" ile geçebilirsin. Docker Hub hesabı bu patika için gerekmiyor.
4. Kısa bir anket çıkarsa onu da geçebilirsin.

Docker Desktop açıldığında sol altta motorun durumunu gösteren bir satır
var. **Engine running** yazısını ve yanındaki yeşil noktayı görene kadar
bekle; ilk açılışta bir dakikayı bulabiliyor.

<figure class="fig">
<svg viewBox="0 0 640 300" width="640" xmlns="http://www.w3.org/2000/svg">
  <rect class="box" x="1" y="1" width="638" height="298" rx="10"/>
  <text class="ink" x="16" y="23" font-size="13" font-weight="600">Docker Desktop</text>
  <line class="line" x1="1" y1="34" x2="639" y2="34"/>
  <line class="line" x1="150" y1="34" x2="150" y2="268"/>
  <rect class="box" x="10" y="48" width="130" height="24" rx="6"/>
  <text class="ink" x="22" y="64" font-size="12" font-weight="600">Containers</text>
  <text class="dim" x="22" y="94" font-size="12">Images</text>
  <text class="dim" x="22" y="122" font-size="12">Volumes</text>
  <text class="dim" x="22" y="150" font-size="12">Builds</text>
  <text class="ink" x="170" y="66" font-size="16" font-weight="600">Containers</text>
  <text class="dim" x="170" y="100" font-size="11">Name</text>
  <text class="dim" x="290" y="100" font-size="11">Image</text>
  <text class="dim" x="430" y="100" font-size="11">Status</text>
  <text class="dim" x="540" y="100" font-size="11">Port(s)</text>
  <line class="grid" x1="170" y1="108" x2="625" y2="108"/>
  <text class="ink" x="170" y="132" font-size="12">web</text>
  <text class="ink" x="290" y="132" font-size="12">python:3.13-slim</text>
  <circle class="dot3" cx="434" cy="128" r="4"/>
  <text class="ink" x="444" y="132" font-size="12">Running</text>
  <text class="ink" x="540" y="132" font-size="12">8080:8000</text>
  <line class="grid" x1="170" y1="144" x2="625" y2="144"/>
  <text class="ink" x="170" y="168" font-size="12">happy_turing</text>
  <text class="ink" x="290" y="168" font-size="12">hello-world</text>
  <text class="dim" x="430" y="168" font-size="12">Exited</text>
  <line class="line" x1="1" y1="268" x2="639" y2="268"/>
  <circle class="dot3" cx="20" cy="284" r="5"/>
  <text class="ink" x="32" y="288" font-size="12" font-weight="600">Engine running</text>
  <text class="dim" x="150" y="288" font-size="12">← motor çalışıyor</text>
  <text class="dim" x="625" y="288" font-size="11" text-anchor="end">RAM 1.1 GB · CPU 0.4%</text>
</svg>
  <figcaption>Docker Desktop'ın şeması. Sol altta yeşil nokta ve <b>Engine running</b> görünmeden komutlar çalışmaz. Containers listesinde çalışan (Running) ve bitmiş (Exited) konteynerler duruyor.</figcaption>
</figure>

Docker Desktop kapalıyken `docker` komutları çalışmıyor. Patikada çalışırken
Docker Desktop açık olsun; Ayarlar › General › **Start Docker Desktop when
you sign in to your computer** seçeneğiyle bilgisayar açılınca kendiliğinden
başlamasını sağlayabilirsin.

## Adım 4 — Terminalden doğrula

Komutları bir terminalde yazacaksın. Başlat'a **PowerShell** yaz ve aç
(yönetici olması gerekmiyor). Önce sürümü sor:

```text
docker version
```

Çıktı iki parçalı:

```text
Client:
 Version:           29.8.0
 API version:       1.56
 OS/Arch:           windows/amd64
 ...
Server: Docker Desktop 4.92.0 (240144)
 Engine:
  Version:          29.8.0
  OS/Arch:          linux/amd64
  ...
```

- **Client**: senin yazdığın `docker` komutu. `windows/amd64`: Windows'ta
  çalışıyor.
- **Server**: arka planda çalışan Docker Engine. `linux/amd64`: Linux'ta,
  yani WSL 2'nin içinde çalışıyor.

Senin sürüm numaraların farklı olabilir; önemli olan iki bölümün de
görünmesi.

İkisi de görünüyorsa kurulum tamam. Yalnızca Client görünüyor ve bir hata
yazıyorsa Docker Desktop açık değil ya da motor henüz başlamadı.

## Adım 5 — İlk konteyner

Şimdi gerçek bir konteyner çalıştır:

```text
docker run hello-world
```

İlk seferde şunlar oluyor:

<figure class="fig">
  <div class="flow">
    <span class="node">1. İmaj yok<br><small>Unable to find</small></span><span class="arrow">→</span>
    <span class="node">2. İniyor<br><small>Pulling…</small></span><span class="arrow">→</span>
    <span class="node acc">3. Çalışıyor<br><small>program yazıyor</small></span><span class="arrow">→</span>
    <span class="node ok">4. Bitti<br><small>konteyner durdu</small></span>
  </div>
  <figcaption><code>docker run</code> imajı bulamazsa önce kendisi indiriyor. Program bitince konteyner de bitiyor (Exited).</figcaption>
</figure>

Ekranda `Hello from Docker!` ile başlayan birkaç paragraf görüyorsan Docker
çalışıyor. Komutu bir daha çalıştır: bu sefer "Unable to find image" satırı
çıkmıyor, çünkü imaj artık bilgisayarında.

## Adım 6 — Patikanın iki imajını indir

Bu patikanın bütün alıştırmaları yalnızca iki **taban imaj** kullanıyor.
İkisini şimdi bir kez indir; sonraki bölümlerde internet olmasa da
alıştırmalar çalışır:

```text
docker pull python:3.13-slim
docker pull alpine:3.22
```

- `pull` → bir imajı Docker Hub'dan indir (çek).
- `python:3.13-slim` → Python 3.13 kurulu, gereksiz parçaları atılmış
  ("slim") bir Linux. ~45 MB indiriliyor, açılınca ~180 MB.
- `alpine:3.22` → çok küçük bir Linux, ~4 MB.

İndirdiklerini listele:

```text
docker images
```

```text
IMAGE              ID             DISK USAGE   CONTENT SIZE   EXTRA
alpine:3.22        5291449c3df7       12.8MB         3.88MB
python:3.13-slim   bf44cdfcb76c        178MB         45.3MB
```

- **ID**: imajın kimliğinin ilk 12 karakteri.
- **DISK USAGE**: diskte açılmış hâlinin kapladığı yer.
- **CONTENT SIZE**: indirilen (sıkıştırılmış) boyut.

Listede birkaç KB'lık `hello-world` da var. Sütunların adı Docker'ın
sürümüne göre biraz farklı olabilir (eski sürümlerde `REPOSITORY`, `TAG`,
`SIZE`); önemli olan imajların listede olması.

## Odyssey Docker'ı nasıl buluyor?

Bir şey ayarlaman gerekmiyor. Odyssey `docker` komutunu kendisi buluyor ve
"Çalıştır"a bastığında motorun açık olup olmadığına bakıyor. Durumu
Ayarlar › **Docker** sayfasında görebilirsin: "Docker 29.8.0 çalışıyor"
gibi bir satır ve Odyssey'nin kurduğu imajların toplamı.

Docker kapalıyken bir alıştırmayı çalıştırırsan Odyssey yine Dockerfile'ını
okuyup denetliyor ama imajı kuramıyor; terminalde "Docker çalışmıyor"
uyarısı çıkıyor. Docker Desktop'ı açıp yeniden çalıştırman yeterli.

## Kapatmak ve kaldırmak

- **Kapatmak:** görev çubuğunun sağındaki balina simgesine sağ tıkla ›
  **Quit Docker Desktop**. Pencereyi kapatmak motoru durdurmuyor; arka
  planda çalışmaya devam ediyor.
- **Kaldırmak:** Windows Ayarlar › Uygulamalar › Docker Desktop ›
  Kaldır. İmajlar ve konteynerler de gidiyor.

## Özet

- Windows'ta Docker = **Docker Desktop**; arkasında WSL 2 ile çalışan bir
  Linux çekirdeği var.
- Gereken: 64 bit Windows 10/11, açık sanallaştırma, 4–8 GB bellek.
- Sol altta **Engine running** görünmeden `docker` komutları çalışmaz.
- `docker version` Client ve Server'ı, `docker run hello-world` ilk
  konteyneri, `docker pull` imaj indirmeyi, `docker images` indirilenleri
  gösteriyor.
- Patikanın iki imajı: `python:3.13-slim` ve `alpine:3.22`.
