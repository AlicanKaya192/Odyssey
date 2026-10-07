# Konteyner Nedir?

Bir program yazdın, kendi bilgisayarında güzelce çalışıyor. Arkadaşına
gönderiyorsun, açmıyor. Sunucuya koyuyorsun, hata veriyor. Yazılımcıların en
eski şikâyeti bu: **"Ama benim bilgisayarımda çalışıyordu!"**

Docker bu şikâyeti ortadan kaldırmak için var. Programı, çalışması için
gereken her şeyle birlikte **tek bir kutuya** koyuyor; kutu nereye giderse
gitsin içindeki program aynı çalışıyor. O kutunun adı **konteyner**.

Bu bölümde henüz Docker kurmuyoruz. Önce kavramları oturtacağız: sorun ne,
konteyner neyi çözüyor, imaj ile konteyner arasındaki fark ne. Kurulum bir
sonraki bölümde.

## Sorun: program yalnız değil

Bir Python programı tek başına çalışmıyor. Arkasında görünmeyen bir kalabalık
var:

- **Python'un kendisi**, hem de belli bir sürümü (3.11'de çalışan kod 3.8'de
  çalışmayabilir),
- **paketler** (`pandas`, `requests`...), onların da belli sürümleri,
- **işletim sisteminin parçaları** (bazı paketler Linux'ta başka, Windows'ta
  başka davranıyor),
- **ayarlar**: ortam değişkenleri, dosya yolları, açık portlar.

Senin bilgisayarında bunların hepsi tesadüfen doğru duruyor. Başka bir
bilgisayarda biri eksik ya da farklıysa program bozuluyor. Hangisinin farklı
olduğunu bulmak saatler sürebiliyor.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Senin bilgisayarın</h4><p>Python 3.12</p><p>pandas 2.2 kurulu</p><p>APP_ENV ayarlı</p><p><b>Çalışıyor</b></p></div>
    <div class="no"><h4>Sunucu</h4><p>Python 3.8</p><p>pandas yok</p><p>APP_ENV yok</p><p><b>Hata veriyor</b></p></div>
  </div>
  <figcaption>Kod aynı, çevresi farklı. Konteyner kodu çevresiyle birlikte taşıyarak bu farkı ortadan kaldırıyor.</figcaption>
</figure>

## Bir benzetme: yük konteyneri

1950'lere kadar gemiler yükü tek tek taşıyordu: çuvallar, fıçılar, sandıklar,
her biri başka biçimde. Her limanda işçiler her şeyi elle indirip
yüklüyordu. 1956'da **standart bir çelik kutu** kullanılmaya başlandı:
içine ne koyarsan koy, dışı hep aynı ölçüde.

O günden beri vinç, gemi, tır ve tren kutunun içinde ne olduğunu bilmeden onu
taşıyabiliyor. Kutunun **dışı standart**, içi senin.

Docker'ın konteyneri de aynı fikir. İçinde senin programın ve ihtiyaç
duyduğu her şey var; dışı standart. Docker'ın kurulu olduğu **her**
bilgisayar bu kutuyu aynı biçimde açıp çalıştırabiliyor: senin dizüstün,
arkadaşının bilgisayarı, şirketin sunucusu, bulut.

## Konteyner nedir?

**Konteyner**, bilgisayarında çalışan ama **kendi küçük dünyasında yaşayan**
bir programdır. Kendi dosyaları, kendi Python'u, kendi paketleri var;
bilgisayarındaki öbür programları görmüyor, onlar da onu görmüyor.

İçinde neler var:

- programın (`app.py`),
- programın ihtiyaç duyduğu paketler,
- Python gibi çalışma ortamı,
- en küçük hâliyle bir Linux'un dosyaları (komutlar, kütüphaneler).

Neler **yok**: koca bir işletim sistemi, masaüstü, ayrı bir çekirdek.
Konteyner bilgisayarının çekirdeğini ortak kullanıyor; bu yüzden küçük ve
hızlı. Bir konteyner bir saniyeden kısa sürede açılabiliyor.

## Sanal makineden farkı

"Ayrı bir dünya" deyince akla **sanal makine** (virtual machine, VM)
geliyor: bilgisayarın içinde çalışan koca bir bilgisayar taklidi. Sanal
makine işini görür ama ağırdır, çünkü içinde **bütün bir işletim sistemi**
taşır.

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Sanal makine</h4><p>Program</p><p>Paketler</p><p><b>Bütün bir işletim sistemi</b></p><p>Sanal donanım</p><p>Birkaç GB · dakikalar</p></div>
    <div class="ok"><h4>Konteyner</h4><p>Program</p><p>Paketler</p><p>Birkaç Linux dosyası</p><p><b>Ortak çekirdek</b></p><p>MB'lar · saniyeden kısa</p></div>
  </div>
  <figcaption>Sanal makine her seferinde bir işletim sistemi daha taşıyor; konteyner ana makinenin çekirdeğini ortak kullanıyor.</figcaption>
</figure>

Kısaca: sanal makine **bilgisayarı** taklit ediyor, konteyner yalnızca
**programın çevresini** ayırıyor. Bir sunucuda on sanal makine zor sığarken
yüzlerce konteyner rahatça çalışabiliyor.

## İmaj ve konteyner

Docker'da iki kelime sürekli geçecek ve en çok bunlar karıştırılıyor:

- **İmaj** (image): konteynerin **kalıbı**. İçinde program ve her şeyi var
  ama çalışmıyor; diskte duran, değişmeyen bir paket.
- **Konteyner** (container): imajdan **çalıştırılan** kopya. Canlı, çalışan,
  durdurulabilen şey.

Python bildiğin için tanıdık bir benzetme var: imaj bir **sınıf**, konteyner
o sınıftan oluşturulmuş bir **nesne**. Tek bir `Book` sınıfından istediğin
kadar kitap nesnesi oluşturabildiğin gibi, tek bir imajdan istediğin kadar
konteyner çalıştırabilirsin. Her biri ötekinden bağımsız.

<figure class="fig">
  <div class="flow">
    <span class="node acc">İmaj: myapp<br><small>kalıp · sınıf</small></span><span class="arrow">→ docker run →</span>
    <span class="node ok">Konteyner 1</span><span class="node ok">Konteyner 2</span><span class="node ok">Konteyner 3</span>
  </div>
  <figcaption>Tek bir imajdan istediğin kadar konteyner çalıştırılır; her biri ayrı, birinde olan ötekini etkilemez.</figcaption>
</figure>

## Dockerfile: imajın tarifi

İmajı nasıl elde ediyorsun? Bir tarif yazarak. Tarifin adı **Dockerfile**:
"şu hazır imajdan başla, şu dosyaları kopyala, şu komutu çalıştır" diyen
kısa bir metin dosyası.

```dockerfile
FROM python:3.13-slim
COPY app.py .
CMD ["python", "app.py"]
```

Üç satır, üç talimat:

- `FROM python:3.13-slim` → içinde Python 3.13 kurulu hazır bir imajdan
  başla.
- `COPY app.py .` → senin `app.py` dosyanı imajın içine kopyala.
- `CMD ["python", "app.py"]` → konteyner çalışınca `python app.py` komutunu
  çalıştır.

Bu tarifin her satırını ileride tek tek öğreneceğiz. Şimdilik akış önemli:

<figure class="fig">
  <div class="flow">
    <span class="node">Dockerfile<br><small>tarif</small></span><span class="arrow">→ docker build →</span>
    <span class="node acc">İmaj<br><small>kalıp</small></span><span class="arrow">→ docker run →</span>
    <span class="node ok">Konteyner<br><small>çalışan program</small></span>
  </div>
  <figcaption>Tarif bir kez imaja dönüşüyor; imaj istendiği kadar konteynere.</figcaption>
</figure>

## İlk bakış: komutlar

Docker'ı terminalden komutlarla kullanıyorsun. Hepsi `docker` kelimesiyle
başlıyor; ardından ne yapılacağı geliyor. Bir sonraki bölümlerde
çalıştıracağın üç komut:

```text
docker run hello-world      # hello-world imajından bir konteyner çalıştır
docker build -t myapp .     # buradaki Dockerfile'dan "myapp" adında imaj kur
docker run myapp            # o imajdan bir konteyner çalıştır
```

- `run` → "bir konteyner çalıştır". Ardından imajın adı geliyor.
- `build` → "bir imaj kur". `-t myapp` imaja ad veriyor (t: tag, etiket);
  sondaki `.` "Dockerfile burada, bu klasörde" demek.

## Docker'ın parçaları

"Docker" kelimesi aslında birkaç parçanın ortak adı:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Docker Engine</span><span>Konteynerleri gerçekten çalıştıran, arka planda bekleyen servis. Penceresi yok.</span></div>
    <div class="anat-row"><span>docker komutu</span><span>Terminalde yazdığın <code>docker run</code>, <code>docker build</code>... Engine'e ne yapacağını söylüyor.</span></div>
    <div class="anat-row"><span>Docker Desktop</span><span>Windows ve Mac'te Engine'i kuran, açan ve gösteren masaüstü programı.</span></div>
    <div class="anat-row"><span>Docker Hub</span><span>Hazır imajların paylaşıldığı internet sitesi; <code>python</code>, <code>alpine</code> gibi imajlar oradan iniyor.</span></div>
  </div>
  <figcaption>Sen komutu yazıyorsun, Engine işi yapıyor, gereken imajı da Docker Hub'dan indiriyor.</figcaption>
</figure>

Windows'ta konteynerler aslında küçük, gizli bir Linux'un içinde çalışıyor.
Docker Desktop bunu senin yerine kuruyor ve yönetiyor; sen yalnızca
`docker` komutlarını yazıyorsun.

## Docker nerede kullanılıyor?

- **Programı yayınlamak:** sunucuya program değil imaj gönderiliyor. Sunucuda
  Python kurmak, paket yüklemek gerekmiyor.
- **Takımda aynı ortam:** herkes aynı imajla çalıştığı için "bende çalışıyor,
  sende neden çalışmıyor" tartışması bitiyor.
- **Hazır yazılımları denemek:** bir veritabanını kurmadan, tek komutla
  çalıştırıp işin bitince silebiliyorsun.
- **Makine öğrenmesi modellerini sunmak:** model, kütüphaneleri ve onu sunan
  API tek bir imajda; her yerde aynı sonucu veriyor.

## Bu patikada nasıl çalışacağız?

Alıştırmalarda **Dockerfile**, **compose.yaml** ya da **komut** yazacaksın.
Odyssey yazdığını iki aşamada denetliyor:

1. **Önce dosyayı okuyor:** talimatlar doğru mu, sıra doğru mu, eksik var mı.
   Bunun için Docker gerekmiyor; bu bölümün alıştırmaları yalnızca bu
   aşamadan oluşuyor.
2. **Sonra Docker açıksa gerçekten kuruyor:** imajı kurup konteyneri
   çalıştırıyor, çıktısına bakıyor. Bu aşama kurulumdan sonraki bölümlerde
   başlıyor.

Odyssey'nin kurduğu her şey `odyssey` diye işaretli; senin kendi imajlarına
ve konteynerlerine dokunmuyor. Kurduğu imajları Ayarlar › Docker'dan
silebilirsin.

## Özet

- Program yalnız değil: Python sürümü, paketler, işletim sistemi ve ayarlar
  da gerekiyor. "Benim bilgisayarımda çalışıyordu" sorunu buradan çıkıyor.
- **Konteyner**, programı ihtiyaç duyduğu her şeyle birlikte ayrı bir küçük
  dünyada çalıştırıyor. Sanal makineden küçük ve hızlı, çünkü işletim
  sistemini değil yalnızca programın çevresini taşıyor.
- **İmaj** kalıp (sınıf), **konteyner** ondan çalıştırılan kopya (nesne).
- **Dockerfile** imajın tarifi: `docker build` tariften imaj, `docker run`
  imajdan konteyner yapıyor.
