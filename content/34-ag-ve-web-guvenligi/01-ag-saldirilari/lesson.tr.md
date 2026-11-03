# Ağ Saldırıları

Ağ Katmanları bölümünde paketin yolunu gördük: her katman bir başlık
ekliyor, yolu izleyen biri başlıkları okuyabiliyor. Bu bölüm o yolda
yapılan saldırıları **kavram olarak** ve **neden çalıştıklarıyla**
anlatıyor; amaç her birini tanıyıp savunmasını kurabilmek. Örnekler yine
Python'da oyuncak veri yapıları: hiçbir yere paket gönderilmiyor, gerçek
bir ağ dinlenmiyor. Örnek dış adresler belgeler için ayrılmış
`203.0.113.0/24` ve `198.51.100.0/24` aralıklarından.

Ortak bir fikir bütün bölümü taşıyor: ağ protokollerinin çoğu, internetin
küçük ve güvenilir bir topluluk olduğu yıllarda tasarlandı. **Birçoğu
karşı tarafın kim olduğunu doğrulamaz.** Saldırıların çoğu bu güvenden
yararlanıyor.

## Dinleme (eavesdropping)

Paket hedefe giderken birçok cihazdan geçer: kafedeki Wi-Fi erişim
noktası, ev yönlendiricisi, internet sağlayıcısının cihazları. Bunlardan
birine erişen biri, şifrelenmemiş trafiği olduğu gibi okuyabilir. Buna
**dinleme** (eavesdropping, sniffing) denir.

```python
packets = [
    {"dport": 80, "data": "POST /login user=ada&password=s3cret"},
    {"dport": 443, "data": "<TLS: unreadable bytes>"},
]
for p in packets:
    print(p["dport"], "->", p["data"])
```

```text
80 -> POST /login user=ada&password=s3cret
443 -> <TLS: unreadable bytes>
```

Düz HTTP (port 80) ile giden parola, yolu izleyen herkesin önünde duruyor.
HTTPS (port 443) ile giden içerik ise şifreli: dinleyen yalnızca anlamsız
baytlar görür. **Savunma şifrelemedir** (Kriptografi modülünün TLS El
Sıkışması bölümü). Dikkat: şifreleme içeriği saklar, başlıkları
saklamaz. Dinleyen hâlâ kimin hangi sunucuyla, ne zaman ve ne kadar veri
alışverişi yaptığını görür.

## Ortadaki adam (MitM)

Dinlemenin bir adım ötesi, saldırganın iki tarafın **arasına girmesidir**.
İki taraf birbiriyle konuştuğunu sanır, oysa her mesaj saldırgandan geçer;
saldırgan okuyabilir, değiştirebilir, durdurabilir. Buna **ortadaki adam**
(man-in-the-middle, MitM) saldırısı denir.

<figure class="fig"><div class="flow">
  <span class="node">İstemci</span><span class="arrow">→</span>
  <span class="node acc">Saldırgan</span><span class="arrow">→</span>
  <span class="node">Sunucu</span>
</div><figcaption>İki taraf da öteki ile konuştuğunu sanır. Kimlik doğrulama olmadan bunu fark edemezler.</figcaption></figure>

MitM'e karşı yalnızca şifreleme yetmez; **karşı tarafın kim olduğunu
doğrulamak** gerekir. Şifreli bir bağlantıyı saldırganla kurarsan gizlilik
bir işe yaramaz. TLS'teki sertifika denetimi bu yüzden vardır (Kriptografi
modülünün Sertifikalar ve PKI bölümü): tarayıcının "bu bağlantı güvenli
değil" uyarısı tam olarak "karşındakinin o site olduğunu doğrulayamadım"
demektir. O uyarı geçilmez.

## ARP sahteciliği: yerel ağda araya girmek

Yerel ağda paket bir sonraki cihaza **MAC adresiyle** gider. Bir cihaz
"`192.168.1.1` adresinin MAC'i ne?" diye ağa sorar, sahibi cevap verir.
Bu protokolün adı **ARP**'tir ve cevabın gerçekten adresin sahibinden
gelip gelmediğini **hiç denetlemez**: en son gelen cevap tabloya yazılır.

```python
arp_table = {}
replies = [("192.168.1.1", "02:00:00:00:00:fe"),
           ("192.168.1.20", "02:00:00:00:00:14"),
           ("192.168.1.1", "02:00:00:00:00:66")]

for ip, mac in replies:
    old = arp_table.get(ip)
    if old and old != mac:
        print(f"WARNING {ip}: {old} -> {mac}")
    arp_table[ip] = mac
print(arp_table["192.168.1.1"])
```

```text
WARNING 192.168.1.1: 02:00:00:00:00:fe -> 02:00:00:00:00:66
02:00:00:00:00:66
```

Aynı ağdaki biri "`192.168.1.1` (yönlendirici) benim" diye sahte cevap
gönderince tablo sessizce değişti; bundan sonra internete giden bütün
paketler önce ona gider. Buna **ARP sahteciliği** (ARP spoofing) denir ve
yerel ağda MitM'in en bilinen yoludur. Bu yüzden ortak Wi-Fi'de
şifrelenmemiş bir şey göndermek risklidir.

Savunmalar:

- **Şifreleme:** araya giren olsa da TLS içeriği korur, sertifika denetimi
  sahte sunucuyu yakalar.
- **Ağ cihazında denetim:** kurumsal anahtarlar (switch) hangi bağlantı
  noktasında hangi IP–MAC eşleşmesinin geçerli olduğunu bilip sahte ARP
  cevaplarını düşürebilir.
- **Tespit:** yukarıdaki gibi "bir adresin MAC'i birden değişti" uyarısı.
  Yönlendiricinin MAC'i normalde hiç değişmez.

## Sahte kaynak adresi (IP spoofing)

Paketin IP başlığındaki **kaynak adresi** gönderen kendisi yazar ve yol
boyunca kimse doğrulamaz. Saldırgan başka birinin adresini yazabilir. Bu
iki şey için kullanılır:

- **Kimliği gizlemek:** paket nereden geldiği belli olmadan hedefe varır
  (ama cevap sahte adrese gittiği için saldırgan cevabı göremez).
- **Yansıtma** (reflection): kaynak olarak kurbanın adresini yazıp küçük bir
  soruyu birçok sunucuya gönderir; bütün cevaplar kurbana yağar. Cevap
  sorudan büyükse buna **büyütme** (amplification) denir: 60 baytlık bir
  soru 3000 baytlık bir cevap üretiyorsa saldırganın her baytı kurbana 50
  bayt olarak döner.

Savunmanın temeli **giriş süzmesidir** (ingress filtering): dışarıdan gelen
bir paket kaynak olarak kendi iç ağının ya da geri döngünün adresini
taşıyorsa, bu paket sahtedir ve düşürülür. İçeriden çıkan paketin kaynağı
da iç ağdan olmalıdır; olmayanı çıkarmamak, ağının başkalarına saldırı
için kullanılmasını önler.

```python
import ipaddress

INTERNAL = ipaddress.ip_network("192.168.1.0/24")


def ingress_ok(src):
    ip = ipaddress.ip_address(src)
    return not (ip in INTERNAL or ip.is_loopback)


for src in ["203.0.113.7", "192.168.1.20", "127.0.0.1"]:
    print(src, "accept" if ingress_ok(src) else "drop")
```

```text
203.0.113.7 accept
192.168.1.20 drop
127.0.0.1 drop
```

Bu kural dış adres yazan sahteciliği yakalamaz (onu kimse tek başına
yakalayamaz), ama "ben içerdenim" diyen dış paketi yakalar. Adrese dayalı
güvene neden yaslanılmayacağının da cevabı bu: **IP adresi bir kimlik
kanıtı değildir.**

## Hizmet engelleme (DoS ve DDoS)

Her saldırı veri çalmaz; bazıları yalnızca hizmeti **kullanılamaz** yapar.
CIA üçlüsünün erişilebilirlik ayağına yöneliktir. Tek kaynaktan gelirse
**DoS** (denial of service), binlerce cihazdan birden gelirse **DDoS**
(distributed) denir. Çoğu zaman bu cihazlar, sahiplerinin haberi olmadan
ele geçirilmiş bilgisayar ve kameralardan oluşan bir **botnet**'tir.

En bilinen örneklerden biri **SYN seli**dir. Ağ Katmanları bölümündeki el
sıkışmayı hatırla: sunucu SYN alınca SYN-ACK gönderir ve yarım kalmış
bağlantı için yer ayırır. Saldırgan (çoğu zaman sahte kaynak adresleriyle)
çok sayıda SYN gönderip ACK'yı hiç göndermezse bu yer dolar:

```python
BACKLOG = 5
half_open = []


def on_syn(src):
    if len(half_open) >= BACKLOG:
        return "refused"
    half_open.append(src)
    return "syn-ack"


for i in range(5):
    on_syn(f"198.51.100.{i}")
print(len(half_open), "half-open")
print("real client:", on_syn("192.168.1.10"))
```

```text
5 half-open
real client: refused
```

Beş sahte istek tabloyu doldurdu; gerçek müşteri geri çevrildi. Gerçek
sunucularda tablo çok daha büyüktür ama saldırgan da çok daha fazla istek
gönderir.

Savunmalar:

- **SYN çerezleri** (SYN cookies): sunucu ACK gelene kadar yer ayırmaz;
  gereken bilgiyi SYN-ACK'nın sıra numarasına kriptografik olarak
  gömer, ACK gelince geri okur. Tablo dolmaz.
- **Zaman aşımı:** yarım bağlantıyı uzun tutmamak.
- **Hız sınırı** (rate limiting): bir kaynaktan belli sürede gelen istek
  sayısını sınırlamak (aşağıda).
- **Kapasite ve yukarı akış süzmesi:** DDoS'ta tek bir sunucu ne yaparsa
  yapsın bağlantısı dolabilir; trafiği önceden süzen büyük ağlar ve
  dağıtılmış sunucular kullanılır.

## Hız sınırı

Hız sınırı DoS'a, parola deneme saldırısına ve kötüye kullanıma karşı
yaygın bir savunmadır. **Kayan pencere** yöntemi son `window` saniyedeki
istekleri sayar; `limit`'e ulaşıldıysa yenisini reddeder:

```python
from collections import deque


def make_limiter(limit, window):
    times = deque()

    def allow(now):
        while times and now - times[0] >= window:
            times.popleft()
        if len(times) >= limit:
            return False
        times.append(now)
        return True

    return allow


allow = make_limiter(3, 10)
print([allow(t) for t in [0, 1, 2, 3, 9, 10, 11, 12]])
```

```text
[True, True, True, False, False, True, True, True]
```

İlk üç istek geçti, dördüncü ve beşinci (3. ve 9. saniye) reddedildi. 10.
saniyede ilk istek pencereden çıktığı için yer açıldı. Gerçek sistemler
sınırı **her kaynak için ayrı** tutar; yoksa bir saldırgan herkesin
hakkını tüketir. DDoS'ta kaynak çok olduğu için kaynak başına sınır tek
başına yetmez.

## Port tarama ve keşif

Saldırılar çoğu zaman bir **keşif** aşamasıyla başlar: hedefte hangi
portların açık olduğunu, hangi servislerin çalıştığını öğrenmek. Bunun
için birçok porta art arda bağlanmayı denemeye **port tarama** denir. Tek
başına zarar vermez ama saldırının habercisidir; sahibinin izni olmadan
yapılması çoğu kurumun kuralına ve birçok ülkenin yasasına aykırıdır
(Etik ve Hukuk bölümü).

Savunma tarafı için iki ders var. Birincisi: kullanılmayan port
kapatılırsa tarama bir şey bulamaz. İkincisi: tarama kayıtlarda **iz
bırakır**; kısa sürede çok sayıda farklı porta dokunan bir kaynak
dikkat çeker:

```python
from collections import defaultdict

log = [("198.51.100.9", port) for port in range(20, 32)] + [
    ("192.168.1.10", 443), ("192.168.1.10", 443), ("192.168.1.11", 22)]

ports_by_src = defaultdict(set)
for src, port in log:
    ports_by_src[src].add(port)
for src, ports in sorted(ports_by_src.items()):
    flag = "SUSPECT" if len(ports) >= 10 else "ok"
    print(f"{src:<14} {len(ports):>2} ports  {flag}")
```

```text
192.168.1.10    1 ports  ok
192.168.1.11    1 ports  ok
198.51.100.9   12 ports  SUSPECT
```

Saldırı tespit sistemleri (Sistem Güvenliği modülünün Saldırı Tespiti
bölümü) bunun çok daha gelişmiş hâlini yapar.

## Yeniden oynatma (replay)

Saldırgan içeriği okuyamasa bile yakaladığı geçerli bir mesajı **olduğu
gibi yeniden gönderebilir**: "100 lira gönder" isteği iki kez işlenir.
Şifreleme ve HMAC bunu tek başına önlemez, çünkü mesaj gerçekten
geçerlidir. Savunma mesaja **bir kez kullanılan bir değer** (nonce) ya da
zaman damgası koymak ve sunucunun görülmüş olanı reddetmesidir. HMAC
bölümündeki API imzasında zaman damgası bu yüzden vardı.

## Saldırı ve savunma haritası

<figure class="fig anat">
  <div class="anat-row"><span>Dinleme</span><span>Şifreleme (TLS). Başlıklar yine görünür.</span></div>
  <div class="anat-row"><span>Ortadaki adam</span><span>Şifreleme + karşı tarafı doğrulama (sertifika).</span></div>
  <div class="anat-row"><span>ARP sahteciliği</span><span>Anahtarda denetim, tespit, ve her durumda TLS.</span></div>
  <div class="anat-row"><span>Sahte kaynak adresi</span><span>Giriş ve çıkış süzmesi; IP adresini kimlik saymamak.</span></div>
  <div class="anat-row"><span>SYN seli, DoS</span><span>SYN çerezleri, zaman aşımı, hız sınırı, yukarı akış süzmesi.</span></div>
  <div class="anat-row"><span>Port tarama</span><span>Kullanılmayan portu kapatmak, kayıtlardan tespit.</span></div>
  <div class="anat-row"><span>Yeniden oynatma</span><span>Nonce ya da zaman damgası, görüleni reddetmek.</span></div>
  <figcaption>Her satır ayrı bir katman. Tek bir savunma bütün listeyi kapatmaz.</figcaption>
</figure>

## Özet

- Ağ protokollerinin çoğu **karşı tarafı doğrulamaz**; saldırılar bu
  güvenden yararlanır.
- **Dinleme** şifresiz içeriği okur; şifreleme içeriği saklar, başlıkları
  saklamaz.
- **Ortadaki adam**'a karşı şifreleme + kimlik doğrulama gerekir;
  sertifika uyarısı geçilmez.
- **ARP** cevapları denetlenmez; yerel ağda araya girmenin yolu budur.
- **Kaynak IP adresi** sahte olabilir; giriş süzmesi "ben içerdenim" diyen
  dış paketi düşürür. IP adresi kimlik kanıtı değildir.
- **SYN seli** yarım bağlantı tablosunu doldurur; SYN çerezleri, zaman
  aşımı ve **hız sınırı** savunmadır.
- **Port tarama** keşiftir; kapalı port bulunamaz, tarama kayıtta iz
  bırakır.
- **Yeniden oynatma**ya karşı nonce ya da zaman damgası.
