Kurulumda en sık karşılaşılan sorunlar ve çözümleri. Hata mesajının bir
parçasını bu sayfada ara.

## "Virtualization support not detected" / sanallaştırma kapalı

Docker Desktop donanım sanallaştırması istiyor.

1. Görev Yöneticisi'ni aç (Ctrl+Shift+Esc) › **Performans** › **CPU**.
2. Sağ altta **Sanallaştırma: Devre dışı** yazıyorsa BIOS'tan açman
   gerekiyor.
3. Bilgisayarı yeniden başlatırken BIOS tuşuna bas (çoğu bilgisayarda F2,
   F10, Del ya da Esc; açılış ekranında yazar).
4. Ayarın adı üreticiye göre değişiyor: **Intel Virtualization Technology
   (VT-x)**, **SVM Mode** (AMD) ya da **Virtualization**. **Enabled** yap,
   kaydedip çık.

## "WSL 2 installation is incomplete" / WSL eski

Yönetici olarak açılmış PowerShell'de:

```text
wsl --update
```

WSL hiç yoksa `wsl --install`. Ardından bilgisayarı yeniden başlat.

## "'docker' is not recognized as the name of a cmdlet"

Terminal, Docker kurulmadan **önce** açılmış. Kurulumdan sonra açık olan
terminal pencerelerini kapatıp yenisini aç; yeni pencere `docker` komutunu
buluyor.

## "failed to connect to the docker API" / "Cannot connect to the Docker daemon"

`docker` komutu var ama motor çalışmıyor. Bu, kurulumdan sonra en sık
görülen mesaj:

```text
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine;
check if the path is correct and if the daemon is running
```

Docker Desktop'ı aç ve sol altta **Engine running** yazısını bekle. Odyssey
de bu durumda "Docker çalışmıyor" diyor.

## Docker Desktop "Starting the Docker Engine..." ekranında kalıyor

1. Docker Desktop'ı kapat (balina simgesi › Quit Docker Desktop).
2. PowerShell'de `wsl --shutdown` çalıştır (WSL'yi tamamen durdurur).
3. Docker Desktop'ı yeniden aç.

Düzelmezse Docker Desktop › Troubleshoot (böcek simgesi) › **Restart**
ya da en son çare olarak **Reset to factory defaults** (bütün imajları ve
konteynerleri siler).

## `docker pull` takılıyor ya da "TLS handshake timeout"

İmajlar internetten iniyor. Bağlantını kontrol et. Şirket ya da okul
ağındaysan bir vekil sunucu (proxy) indirmeyi engelliyor olabilir; Docker
Desktop › Settings › Resources › Proxies'e ağ yöneticinin verdiği adres
yazılıyor.

## "pull access denied" / "repository does not exist"

İmajın adı yanlış yazılmış. `python:3.13-slim` ile `python:3.13-slm` farklı
şeyler; Docker olmayan bir imajı arıyor.

## Disk doluyor

İmajlar, konteynerler ve derleme önbelleği yer kaplıyor. Ne kadar
kapladıklarını gör:

```text
docker system df
```

Odyssey'nin kurduğu imajları Ayarlar › Docker'dan silebilirsin. Kendi
denemelerinden kalan durmuş konteynerleri ve kullanılmayan imajları
temizlemek için `docker system prune` var; ne sildiğini sorup onay
istiyor. Ayrıntısı İmajlar bölümünde.
