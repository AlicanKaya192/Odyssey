# SSRF: Sunucu Taraflı İstek Sahteciliği

CSRF'te saldırgan **kullanıcının tarayıcısına** bir istek
gönderttiriyordu. SSRF'te (server-side request forgery, sunucu taraflı
istek sahteciliği) aynı şeyi **sunucuya** yaptırır. Birçok uygulamanın
"şu adresteki resmi getir", "bağlantının önizlemesini göster", "bu adrese
bildirim gönder" gibi özellikleri vardır: kullanıcı bir adres verir,
sunucu o adrese **kendi adına** istek atar. Sunucu iç ağın içinde durduğu
için, dışarıdan erişilemeyen adreslere ulaşabilir. Bu bölüm açığı oyuncak
bir "internet" sözlüğüyle gösteriyor ve savunmalarını kuruyor: izin
listesi, adresi ayrıştırarak denetlemek, iç adresleri reddetmek ve ağ
katmanında sınırlamak. Hiçbir gerçek istek atılmıyor; "getirmek" bir
sözlükte arama yapmaktır.

## Açık: sunucu her adrese gidiyor

```python
FAKE_WEB = {
    "https://images.example.com/cat.png": "<cat image bytes>",
    "http://127.0.0.1/admin": "internal admin panel",
    "http://10.20.0.15/config": "internal settings page",
}


def fetch(url):
    return FAKE_WEB.get(url, "404")


def preview_bad(url):
    return fetch(url)


print(preview_bad("https://images.example.com/cat.png"))
print(preview_bad("http://127.0.0.1/admin"))
print(preview_bad("http://10.20.0.15/config"))
```

```text
<cat image bytes>
internal admin panel
internal settings page
```

Önizleme özelliği resim için yazılmıştı, ama kullanıcı ona sunucunun
**kendisini** (`127.0.0.1`) ve iç ağdaki bir sunucuyu (`10.20.0.15`)
istetti. Bu adresler internetten erişilemez; güvenlik duvarı onları
dışarıya kapatmıştı (Güvenlik Duvarı bölümü). Ama istek dışarıdan değil,
**içerideki güvenilen sunucudan** geldiği için duvar araya girmedi. VPN ve
Ağ Bölümleme bölümündeki çevre modelinin zayıflığı burada tekrar
görünüyor: içeride olmak güven sebebi sayılırsa, içeriye istek
atabilen her özellik bir kapıya dönüşür.

Bulutta çalışan sunucularda risk daha da büyüktür: bulut ortamları,
sunucunun kendi kimlik bilgilerini veren bir **meta veri hizmetini**
bağlantı yerel aralıktaki (`169.254.0.0/16`) bir adreste sunar. SSRF ile o
adrese ulaşan bir saldırgan sunucunun bulut yetkilerini ele geçirebilir.

## Birinci savunma: izin listesi ve ayrıştırıcı

Özellik yalnızca belirli sitelerden resim getirecekse, en sağlam savunma
**izin listesidir**: adres ayrıştırılır, şeması ve ana bilgisayarı
listeyle **birebir** karşılaştırılır. HTTP ve HTTPS bölümünde gördüğümüz
gibi bu karşılaştırma metin aramasıyla yapılmaz:

```python
from urllib.parse import urlsplit

ALLOWED_HOSTS = {"images.example.com"}


def text_check(url):
    return url.startswith("https://images.example.com")


def allowed(url):
    parts = urlsplit(url)
    return parts.scheme in ("http", "https") and parts.hostname in ALLOWED_HOSTS


for url in ["https://images.example.com/cat.png",
            "http://127.0.0.1/admin",
            "https://images.example.com@127.0.0.1/admin",
            "file:///app/settings.ini"]:
    print(f"{text_check(url)!s:<5} {allowed(url)!s:<5} {url}")
```

```text
True  True  https://images.example.com/cat.png
False False http://127.0.0.1/admin
True  False https://images.example.com@127.0.0.1/admin
False False file:///app/settings.ini
```

Metin denetimi üçüncü adresi geçirdi: adres göze `images.example.com`
gibi görünüyor ama gerçek ana bilgisayarı `127.0.0.1` (`@` işaretinin
solu kullanıcı adıdır). Ayrıştırıcıyla yapılan denetim onu reddetti.
Dördüncü satırdaki `file://` şeması da reddedildi: sunucunun kendi
diskindeki dosyaları okumaya yarayan şemalar getirme özelliğinde hiç
kabul edilmez. **Yalnızca `http` ve `https`.**

## İkinci savunma: iç adresleri reddetmek

Bazen izin listesi kurulamaz (kullanıcı herhangi bir sitenin önizlemesini
istiyor). O zaman tersinden gidilir: **iç ağa giden** adresler reddedilir.
Ağ Katmanları bölümündeki `ipaddress` modülü hangi adreslerin iç adres
olduğunu bilir:

```python
import ipaddress


def is_internal(ip):
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_unspecified or ip.is_reserved)


for text in ["100.20.30.40", "127.0.0.1", "10.20.0.15",
             "169.254.169.254", "0.0.0.0"]:
    print(f"{text:<16} {is_internal(ipaddress.ip_address(text))}")
```

```text
100.20.30.40     False
127.0.0.1        True
10.20.0.15       True
169.254.169.254  True
0.0.0.0          True
```

Geri döngü, özel aralıklar, bağlantı yerel aralıktaki meta veri adresi ve
"hiçbir adres" anlamına gelen `0.0.0.0` iç adres sayıldı; yalnızca açık
adres geçti.

Ama adresler çoğu zaman **adla** gelir. Adın kendisine bakmak yetmez:
kulağa dışarıdaki bir site gibi gelen bir ad, DNS'te bir iç adrese
çözülebilir. Denetim **çözümlemeden sonra**, adın gerçekten gittiği IP
adresi üzerinde yapılır (DNS'i yine bir sözlükle taklit ediyoruz):

```python
from urllib.parse import urlsplit

DNS = {"images.example.com": "100.20.30.40",
       "intranet.example.net": "10.20.0.15"}


def safe_target(url):
    host = urlsplit(url).hostname
    try:
        ip = ipaddress.ip_address(DNS.get(host, host))
    except ValueError:
        return "unknown host"
    return "blocked" if is_internal(ip) else f"ok {ip}"


for url in ["https://images.example.com/a.png",
            "https://intranet.example.net/",
            "http://127.0.0.1/admin",
            "https://nowhere.example/"]:
    print(safe_target(url))
```

```text
ok 100.20.30.40
blocked
blocked
unknown host
```

`intranet.example.net` adı zararsız görünüyor ama `10.20.0.15`'e
çözüldüğü için reddedildi. Çözülemeyen ad da reddedildi: emin olunamayan
durumda kapalı kalmak (Güvenlik İlkeleri bölümündeki güvenli
başarısızlık).

İki ayrıntı daha:

- **Denetlenen adrese bağlan.** Ad denetimden sonra yeniden çözülürse, bu
  arada farklı bir adrese dönmüş olabilir (DNS kaydının TTL'i çok
  kısaysa). Doğru yol, adı bir kez çözüp denetlemek ve bağlantıyı
  **denetlenen IP adresine** kurmaktır.
- **Yönlendirmelere dikkat.** İzinli bir sunucu `301` ile bir iç adrese
  yönlendirebilir. Getirme özelliği yönlendirmeyi ya hiç izlemez ya da her
  adımda aynı denetimi yeniden yapar.

## Üçüncü savunma: ağ katmanında sınırlamak

Kodda bir şey gözden kaçarsa ağ son katmandır:

- Getirme işini yapan bileşen ayrı bir bölgede çalışır ve **çıkış
  süzmesiyle** (Güvenlik Duvarı bölümü) yalnızca internete çıkabilir; iç
  ağa ve meta veri adresine yolu yoktur.
- İç hizmetler "istek içeriden geliyor" diye kimlik doğrulamayı atlamaz
  (VPN ve Ağ Bölümleme bölümündeki sıfır güven).
- Bulut meta veri hizmetinin, isteğe özel bir başlık ya da jeton isteyen
  korumalı sürümü açılır.

## Cevabı da sınırla

Getirilen içeriğin olduğu gibi kullanıcıya gösterilmesi, iç sistemlerin
cevaplarını dışarı taşır. Önizleme özelliği yalnızca beklediği türü
(örneğin resim) ve belli bir boyuta kadar kabul eder; hata durumunda
kullanıcıya iç ayrıntı değil, genel bir mesaj döner. Zaman aşımı kısa
tutulur: yanıt vermeyen bir adres, sunucunun kaynaklarını tüketmesin.

<figure class="fig anat">
  <div class="anat-row"><span>İzin listesi</span><span>Şema ve ana bilgisayar listeyle birebir; en sağlamı.</span></div>
  <div class="anat-row"><span>Ayrıştırıcı</span><span><code>urlsplit(url).hostname</code>; metin araması değil.</span></div>
  <div class="anat-row"><span>İç adres reddi</span><span>Çözümlemeden sonra IP üzerinde; özel, geri döngü, bağlantı yerel, ayrılmış.</span></div>
  <div class="anat-row"><span>Bağlantı ve yönlendirme</span><span>Denetlenen IP'ye bağlan; yönlendirmeyi izleme ya da her adımı yeniden denetle.</span></div>
  <div class="anat-row"><span>Ağ</span><span>Getirme bileşenine çıkış süzmesi; iç hizmetlerde kimlik doğrulama.</span></div>
  <figcaption>SSRF'e karşı katmanlar. Biri gözden kaçarsa ötekiler tutar.</figcaption>
</figure>

## Özet

- **SSRF:** sunucu, kullanıcının verdiği adrese kendi adına istek atar;
  içeride durduğu için dışarıdan erişilemeyen adreslere ulaşır.
- Bulutta bağlantı yerel aralıktaki **meta veri hizmeti** özel bir
  risktir.
- En sağlam savunma **izin listesi**: adres **ayrıştırılır**, şema
  (`http`, `https`) ve ana bilgisayar birebir karşılaştırılır.
- İzin listesi kurulamıyorsa **iç adresler reddedilir**; denetim ad
  çözüldükten sonra **IP üzerinde** yapılır, bağlantı denetlenen IP'ye
  kurulur.
- Yönlendirmeler izlenmez ya da her adımda yeniden denetlenir.
- Ağ katmanında getirme bileşenine **çıkış süzmesi**; iç hizmetler
  kimlik doğrulamayı atlamaz.
- Cevap türü, boyutu ve zaman aşımı sınırlanır; hata ayrıntısı
  gösterilmez.
