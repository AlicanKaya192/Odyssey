# VPN ve Ağ Bölümleme

Güvenlik Duvarı bölümü iki soruyu açık bıraktı: evden ya da kafeden
çalışan biri kurumun iç ağına **güvenle** nasıl ulaşır, ve içeride bir
bilgisayar ele geçirilirse saldırganın **her yere yayılması** nasıl
önlenir? Birincinin cevabı VPN, ikincininki ağ bölümleme. Bölümün sonunda
ikisinin de ötesine geçen bir fikre bakacağız: ağın içinde olmak güven
sebebi değildir. Örnekler yine Python'da oyuncak veri yapıları.

## VPN: şifreli tünel

**VPN** (virtual private network, sanal özel ağ) iki nokta arasında
internetin üstünden **şifreli bir tünel** kurar. Tünelin içinden giden
paketler, sanki iki taraf aynı özel ağdaymış gibi akar. Ağ Katmanları
bölümündeki kapsülleme burada bir kat daha derinleşir: **asıl paket**
(iç paket) bütünüyle şifrelenip **başka bir paketin** (dış paket) içine
konur.

<figure class="fig"><div class="flow">
  <span class="node">İç paket</span><span class="arrow">→</span>
  <span class="node">Şifrele</span><span class="arrow">→</span>
  <span class="node">Dış paket</span><span class="arrow">→</span>
  <span class="node acc">VPN geçidi</span>
</div><figcaption>Dış paket yalnızca VPN geçidine gider; geçit onu açar, iç paketi iç ağa bırakır.</figcaption></figure>

Yolu izleyen biri yalnızca dış paketi görür:

```python
import json

inner = {"src": "10.8.0.2", "dst": "10.20.0.15", "dport": 80,
         "data": "GET /payroll"}
payload = json.dumps(inner)
outer = {"src": "203.0.113.50", "dst": "198.51.100.1", "dport": 443,
         "payload": f"<encrypted {len(payload)} bytes>"}

print("inner:", inner["src"], "->", inner["dst"], inner["dport"])
print("outer:", outer["src"], "->", outer["dst"], outer["dport"])
print("observer sees:", outer["payload"])
```

```text
inner: 10.8.0.2 -> 10.20.0.15 80
outer: 203.0.113.50 -> 198.51.100.1 443
observer sees: <encrypted 77 bytes>
```

İç pakette kurumun iç adresleri (`10.20.0.15`) ve istenen sayfa var;
dışarıdan bakan bunları göremez. Gördüğü tek şey çalışanın kafedeki
adresinden (`203.0.113.50`) kurumun VPN geçidine (`198.51.100.1`) giden,
belli boyutta şifreli bir trafik. İç ağa da yalnızca geçitten girilir;
yani kurumun iç sunucuları internete hiç açılmaz, yalnızca geçit açılır.

İki kullanım biçimi var:

- **Uzaktan erişim** (remote access): bir çalışanın bilgisayarı kurumun
  ağına bağlanır. Bilgisayarda bir VPN istemcisi çalışır.
- **Siteden siteye** (site-to-site): iki şubenin ağları birbirine bağlanır;
  bilgisayarların haberi bile olmaz, tüneli iki yönlendirici kurar.

## VPN neyi korur, neyi korumaz?

VPN çok sık yanlış anlaşılan bir araçtır. Koruduğu şey **yolun bir
parçasıdır**: senin bilgisayarınla VPN geçidi arasındaki yol.

<figure class="fig"><div class="versus">
  <div class="ok"><h4>Korur</h4>Kafedeki Wi-Fi'yi dinleyen ya da ARP sahteciliğiyle araya giren biri trafiğini okuyamaz. İç ağın sunucuları internete açılmadan uzaktan kullanılabilir.</div>
  <div class="no"><h4>Korumaz</h4>Bilgisayarındaki zararlı yazılımı, oltalama sayfasına girdiğin parolayı, VPN geçidinden sonraki yolu ya da ziyaret ettiğin sitenin kendi açıklarını. VPN anonimlik de değildir: VPN sağlayıcısı trafiğini görür.</div>
</div><figcaption>VPN bir tüneldir; tünelin iki ucundaki sorunları çözmez.</figcaption></figure>

Bir tuzak daha: VPN'e bağlanan bilgisayar **iç ağın bir parçası** olur.
O bilgisayar ele geçirilmişse, saldırgan da tünelden içeri girer. Bu
yüzden VPN'e kimlerin hangi cihazla bağlanabildiği sıkı denetlenir (çok
aşamalı doğrulama, Kimlik Doğrulama ve MFA bölümü) ve VPN'den gelen
herkese iç ağın tamamı açılmaz. Bu da bizi bölümlemeye getiriyor.

**Bölünmüş tünel** (split tunneling) adı verilen ayarda yalnızca kurumun
ağına giden trafik tünelden geçer, gerisi doğrudan internete çıkar.
Kurumun bağlantısını rahatlatır ama o trafik kurumun güvenlik
denetimlerinden geçmez; seçim bilinçli yapılır.

## Düz ağın sorunu

Birçok küçük ağ **düzdür** (flat): bütün cihazlar aynı ağdadır ve
birbirine serbestçe ulaşabilir. Saldırgan ağa tek bir zayıf noktadan
girdiğinde (oltalama e-postası açılmış bir dizüstü, güncellenmemiş bir
kamera) oradan diğer cihazlara geçer. Buna **yanal hareket** (lateral
movement) denir. Düz ağda yanal hareketin önünde hiçbir engel yoktur:

```python
from collections import deque


def reachable(links, start):
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in links.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen - {start})


hosts = ["laptop", "printer", "camera", "hr-db", "web", "backup"]
flat = {h: [o for o in hosts if o != h] for h in hosts}
segmented = {"laptop": ["web"], "web": ["hr-db"], "backup": ["hr-db"]}

print("flat:     ", reachable(flat, "laptop"))
print("segmented:", reachable(segmented, "laptop"))
```

```text
flat:      ['backup', 'camera', 'hr-db', 'printer', 'web']
segmented: ['hr-db', 'web']
```

Düz ağda ele geçirilen dizüstünden diğer beş cihazın hepsine ulaşılıyor.
Bölünmüş ağda yalnızca web sunucusuna, onun üstünden de insan kaynakları
veritabanına. Yazıcı, kamera ve yedek sunucusu artık erişilemez.

Sonuçtaki ikinci satır da bir ders veriyor: veritabanına hâlâ **bir yol**
var, web sunucusunun üstünden. Bölümleme saldırganı durdurmaz, **yolunu
uzatır ve daraltır**; o dar yol (web sunucusu) özellikle iyi korunur ve
izlenir. Yedek sunucusuna dizüstünden yol olmaması da önemli: Yedek ve
Felaket Kurtarma bölümünde göreceğimiz gibi saldırganın yedeklere
ulaşamaması bir saldırıdan sonra geri dönebilmenin şartıdır.

## Bölgeler ve DMZ

Bölümlemenin olağan yolu ağı **bölgelere** (zone) ayırmak ve bölgeler
arasına güvenlik duvarı koymaktır. Her bölge bir alt ağdır (Ağ Katmanları
bölümünün alt ağ hesabı):

<figure class="fig anat">
  <div class="anat-row"><span><b>DMZ</b></span><span>İnternete hizmet veren sunucular (web, e-posta). Dışarıdan erişilir, içeriye erişimi dardır.</span></div>
  <div class="anat-row"><span><b>Sunucular</b></span><span>Veritabanları, iç uygulamalar. İnternetten hiç erişilmez.</span></div>
  <div class="anat-row"><span><b>Çalışanlar</b></span><span>Dizüstüler ve masaüstüler. Gereken birkaç servise erişir.</span></div>
  <div class="anat-row"><span><b>Misafir</b></span><span>Ziyaretçi Wi-Fi'si. Yalnızca internete çıkar, iç ağa hiç erişmez.</span></div>
  <div class="anat-row"><span><b>Yönetim</b></span><span>Ağ cihazlarının ve sunucuların yönetim arayüzleri. Yalnızca yöneticiler.</span></div>
  <figcaption>Tipik bir kurum ağının bölgeleri. Gerçek ağlarda IoT cihazları ve üretim sistemleri gibi başka bölgeler de olur.</figcaption>
</figure>

**DMZ** (demilitarized zone, arındırılmış bölge) adını iki ülke arasındaki
tampon bölgeden alır: internetle iç ağın arasında, ikisinden de ayrılmış
bir alandır. Web sunucusu ele geçirilse bile saldırgan DMZ'de kalır;
oradan iç ağa yalnızca dar, tanımlı yollar (web sunucusundan
veritabanına tek bir port gibi) açıktır.

Bir adresin hangi bölgede olduğunu bulmak alt ağ denetimidir:

```python
import ipaddress

ZONES = [("dmz", "10.10.0.0/24"), ("servers", "10.20.0.0/24"),
         ("staff", "10.30.0.0/24"), ("guest", "10.99.0.0/24")]


def zone_of(text):
    ip = ipaddress.ip_address(text)
    for name, cidr in ZONES:
        if ip in ipaddress.ip_network(cidr):
            return name
    return "internet"


for text in ["10.10.0.5", "10.20.0.15", "10.99.0.42", "203.0.113.7"]:
    print(text, zone_of(text))
```

```text
10.10.0.5 dmz
10.20.0.15 servers
10.99.0.42 guest
203.0.113.7 internet
```

Bölgeler arası kurallar da Güvenlik Duvarı bölümündeki gibi bir izin
listesidir; listede olmayan akış reddedilir:

```python
POLICY = {("internet", "dmz", 443), ("dmz", "servers", 5432),
          ("staff", "dmz", 443), ("staff", "servers", 443)}


def allowed(src_zone, dst_zone, port):
    return (src_zone, dst_zone, port) in POLICY


for flow in [("internet", "dmz", 443), ("internet", "servers", 5432),
             ("guest", "staff", 445), ("dmz", "servers", 5432)]:
    print(*flow, "allow" if allowed(*flow) else "deny")
```

```text
internet dmz 443 allow
internet servers 5432 deny
guest staff 445 deny
dmz servers 5432 allow
```

İnternetten veritabanına doğrudan erişim yok; misafir ağından çalışanların
bilgisayarlarına dosya paylaşımı (445) yok. Web sunucusunun veritabanına
tek bir portu var. Bölgeler ayrı kablolarla kurulmak zorunda değildir:
**VLAN** (sanal yerel ağ) aynı anahtar (switch) ve kablolar üstünde
birbirinden ayrı ağlar kurar. Bölgeleri tek tek sunuculara ve
uygulamalara kadar küçültmeye **mikro bölümleme** (microsegmentation)
denir.

## Sıfır güven

Klasik model **çevre** (perimeter) modelidir: dış duvar sağlamsa içerisi
güvenilirdir. Bu model iki gerçekle çatışıyor: saldırganlar zaten içeride
olabilir (ele geçirilmiş bir dizüstü), ve çalışanlar artık hep içeride
değildir (evden, telefondan, buluttan çalışma). **Sıfır güven** (zero
trust) modeli şunu söyler: **ağdaki konum güven sebebi değildir.** Her
istek kim olduğuna, hangi cihazdan geldiğine ve neye erişmek istediğine
göre **her seferinde** değerlendirilir.

```python
def perimeter(request):
    return request["inside"]


def zero_trust(request):
    return (request["mfa"] and request["device_ok"]
            and request["resource"] in request["grants"])


attempts = [
    {"who": "infected laptop", "inside": True, "mfa": False,
     "device_ok": False, "resource": "hr-db", "grants": []},
    {"who": "remote engineer", "inside": False, "mfa": True,
     "device_ok": True, "resource": "wiki", "grants": ["wiki"]},
]
for r in attempts:
    print(f"{r['who']:<16} perimeter={perimeter(r)!s:<5} zero_trust={zero_trust(r)}")
```

```text
infected laptop  perimeter=True  zero_trust=False
remote engineer  perimeter=False zero_trust=True
```

Çevre modeli içerideki enfekte dizüstüne güvendi, uzaktaki yetkili
mühendisi reddetti; sıfır güven ikisinde de doğru karar verdi. Sıfır güven
bir ürün değil, bir tasarım ilkesidir: Güvenlik İlkeleri bölümündeki **tam
aracılık** (her erişimi her seferinde denetle) ve **en az yetki**
ilkelerinin ağa uygulanmış hâli. Bölümleme ortadan kalkmaz; sıfır güven
onun üstüne gelir.

## Özet

- **VPN** iki nokta arasında şifreli bir tünel kurar; iç paket şifrelenip
  dış pakete konur. Uzaktan erişim ve siteden siteye kullanılır.
- VPN **yolun bir parçasını** korur (sen ile geçit arası); zararlı yazılımı,
  oltalamayı, sitenin açıklarını korumaz ve anonimlik değildir.
- VPN'e bağlanan cihaz iç ağın parçası olur; bağlanan cihaz ve kişi sıkı
  denetlenir.
- **Düz ağda** ele geçirilen tek cihazdan her yere **yanal hareket**
  yapılır; **bölümleme** yolu uzatır ve daraltır.
- Ağ **bölgelere** ayrılır (DMZ, sunucular, çalışanlar, misafir, yönetim);
  bölgeler arasında izin listesi vardır.
- **DMZ** internete hizmet veren sunucuları iç ağdan ayırır.
- **Sıfır güven:** ağdaki konum güven sebebi değildir; her istek kimlik,
  cihaz ve yetkiyle her seferinde değerlendirilir.
