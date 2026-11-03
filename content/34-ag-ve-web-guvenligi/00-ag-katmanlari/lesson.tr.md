# Ağ Katmanları ve Adresler

Bu modül bir web sayfasının senin bilgisayarına nasıl geldiğini ve yolun
her adımında neyin ters gidebileceğini anlatıyor. Saldırıları anlamak için
önce yolun kendisini tanımak gerekiyor: bir mesaj hangi parçalara bölünür,
her parçanın üstüne hangi bilgiler yazılır, alıcı nasıl bulunur. Bu
bölümde hiçbir ağa bağlanmıyoruz; adresleri ve paketleri Python'da küçük
veri yapılarıyla taklit ediyoruz.

## Neden katman?

Bir mektup göndermeyi düşün. Sen mektubu yazarsın; zarfa adresi postane
için yazarsın; postane zarfı bir torbaya koyar, torba bir kamyonla gider.
Mektubu yazan kişi kamyonun yolunu bilmez, kamyon şoförü mektubun
içeriğini bilmez. Herkes yalnızca kendi işini yapar.

Ağlar da böyle çalışır. İş **katmanlara** (layer) bölünür; her katman
altındakinin hizmetini kullanır ve üstündekine hizmet verir. Bugün
internette kullanılan model **TCP/IP** modelidir ve dört katmanı vardır:

<figure class="fig anat">
  <div class="anat-row"><span><b>Uygulama</b> (Application)</span><span>Programların konuştuğu dil: web için HTTP, alan adı için DNS, uzak bağlantı için SSH.</span></div>
  <div class="anat-row"><span><b>Taşıma</b> (Transport)</span><span>Veriyi doğru programa götürür: TCP (güvenilir, sıralı) ya da UDP (hızlı, garantisiz). Port numarası burada.</span></div>
  <div class="anat-row"><span><b>Ağ</b> (Internet)</span><span>Veriyi doğru bilgisayara götürür: IP adresi ve yönlendirme burada.</span></div>
  <div class="anat-row"><span><b>Bağlantı</b> (Link)</span><span>Aynı yerel ağdaki bir sonraki cihaza götürür: Ethernet, Wi-Fi, MAC adresi.</span></div>
  <figcaption>TCP/IP modelinin dört katmanı, yukarıdan aşağıya.</figcaption>
</figure>

Ders kitaplarında yedi katmanlı **OSI modeli** de geçer. Aynı fikrin daha
ince bölünmüş hâlidir: TCP/IP'nin uygulama katmanı OSI'de üçe (uygulama,
sunum, oturum), bağlantı katmanı ikiye (veri bağlantısı, fiziksel)
ayrılır. Güvenlik yazılarında "katman 3 saldırısı" ya da "katman 7
güvenlik duvarı" gibi sözler OSI numaralarıdır: **3 ağ (IP), 4 taşıma
(TCP/UDP), 7 uygulama (HTTP).**

## Kapsülleme: zarfın içinde zarf

Bir web isteği yola çıkarken her katman ona kendi **başlığını** (header)
ekler. Taşıma katmanı port numaralarını, ağ katmanı IP adreslerini,
bağlantı katmanı da MAC adreslerini yazar. Buna **kapsülleme**
(encapsulation) denir. Alıcı tarafta her katman kendi başlığını okuyup
söker ve içini üsttekine verir.

<figure class="fig"><div class="flow">
  <span class="node">Veri</span><span class="arrow">→</span>
  <span class="node">Segment</span><span class="arrow">→</span>
  <span class="node">Paket</span><span class="arrow">→</span>
  <span class="node acc">Çerçeve</span>
</div><figcaption>Her katman bir öncekini kendi başlığıyla sarar: TCP segmenti, IP paketi, Ethernet çerçevesi.</figcaption></figure>

Bunu iç içe sözlüklerle taklit edelim:

```python
data = "GET /index.html"
segment = {"sport": 51514, "dport": 80, "data": data}
packet = {"src": "192.168.1.10", "dst": "203.0.113.7", "segment": segment}
frame = {"src_mac": "02:00:00:00:00:01", "dst_mac": "02:00:00:00:00:fe",
         "packet": packet}

for name, header in [("frame", frame), ("packet", packet), ("segment", segment)]:
    fields = [k for k, v in header.items() if not isinstance(v, dict)]
    print(f"{name:<8} {fields}")
print("data    ", repr(segment["data"]))
```

```text
frame    ['src_mac', 'dst_mac']
packet   ['src', 'dst']
segment  ['sport', 'dport', 'data']
data     'GET /index.html'
```

Güvenlik açısından önemli bir sonuç var: **yolu izleyen biri bütün
başlıkları okuyabilir.** Kim kiminle, hangi portta konuşuyor, başlıklardan
bellidir. İçerik (`data`) de şifrelenmemişse o da okunur. Bir sonraki
bölümdeki dinleme saldırısı tam buna dayanıyor.

## IP adresi

Ağ katmanında her cihazın bir **IP adresi** vardır. Bugün en çok
kullanılan sürüm **IPv4**'tür: adres 32 bitlik bir sayıdır ve okunması
kolay olsun diye noktalarla ayrılmış dört bayt olarak yazılır
(`192.168.1.10`). Her bayt 0 ile 255 arasındadır. Python'ın standart
kütüphanesindeki `ipaddress` modülü adreslerle çalışmayı kolaylaştırır:

```python
import ipaddress

ip = ipaddress.ip_address("192.168.1.10")
print(ip.version)
print(list(ip.packed))
print(int(ip))

value = 0
for part in [192, 168, 1, 10]:
    value = value * 256 + part
print(value)
```

```text
4
[192, 168, 1, 10]
3232235786
3232235786
```

Adres gerçekte tek bir sayıdır; noktalı yazım yalnızca okumak içindir. Her
bayt bir önceki değeri 256 ile çarpıp eklenerek sayıya katılır, bu yüzden
elle hesap da `int(ip)` ile aynı sonucu verdi. IPv4'te yaklaşık 4,3 milyar
adres var ve bu yetmiyor; daha uzun (128 bit) **IPv6** adresleri
(`2001:db8::1`) bu yüzden geldi. Fikirler aynı, biz örneklerde IPv4
kullanıyoruz.

## Ağ ve alt ağ: CIDR

Adresler tek tek değil, **ağlar** hâlinde dağıtılır. `192.168.1.0/24`
yazımı (CIDR) şunu söyler: ilk 24 bit ağı, kalan 8 bit o ağdaki cihazı
gösterir. Ağ kısmı aynı olan adresler aynı yerel ağdadır.

```python
import ipaddress

net = ipaddress.ip_network("192.168.1.0/24")
print(net.netmask)
print(net.num_addresses)
print(net.network_address, net.broadcast_address)
print(ipaddress.ip_address("192.168.1.77") in net)
print(ipaddress.ip_address("192.168.2.5") in net)
```

```text
255.255.255.0
256
192.168.1.0 192.168.1.255
True
False
```

`/24` ağında 256 adres var. İlki (`.0`) ağın kendisini, sonuncusu (`.255`)
**yayın** (broadcast) adresini gösterir; cihazlara kalan 254 adres
verilir. **Ağ maskesi** (netmask) `255.255.255.0` aynı bilginin eski
yazımıdır: 1 olan bitler ağ kısmıdır. Önek büyüdükçe ağ küçülür:

```python
import ipaddress

for prefix in [8, 16, 24, 28, 32]:
    net = ipaddress.ip_network(f"10.0.0.0/{prefix}")
    print(f"/{prefix:<3}{net.num_addresses:>10}  {net.netmask}")
```

```text
/8    16777216  255.0.0.0
/16      65536  255.255.0.0
/24        256  255.255.255.0
/28         16  255.255.255.240
/32          1  255.255.255.255
```

Her bit önek, adres sayısını yarıya indirir. `/32` tek bir cihazdır;
güvenlik duvarı kurallarında "yalnızca bu bilgisayar" demek için sık
kullanılır.

## Özel, açık ve geri döngü adresleri

Bazı adres aralıkları internette yönlendirilmez, yalnızca ev ve kurum
ağlarının içinde kullanılır. Bunlara **özel adres** (private) denir:
`10.0.0.0/8`, `172.16.0.0/12` ve `192.168.0.0/16`. Evindeki bütün
cihazların `192.168...` ile başlaması bundandır; dışarıya çıkarken
yönlendirici (router) hepsini tek bir **açık** (public) adresin arkasına
saklar. `127.0.0.1` ise **geri döngü** (loopback) adresidir: "bu
bilgisayarın kendisi" demektir, paket kablolara hiç çıkmaz.

```python
import ipaddress

for text in ["127.0.0.1", "10.1.2.3", "172.31.0.9", "172.32.0.9",
             "192.168.0.1", "203.0.113.7", "100.20.30.40"]:
    ip = ipaddress.ip_address(text)
    print(f"{text:<14} private={ip.is_private!s:<5} loopback={ip.is_loopback}")
```

```text
127.0.0.1      private=True  loopback=True
10.1.2.3       private=True  loopback=False
172.31.0.9     private=True  loopback=False
172.32.0.9     private=False loopback=False
192.168.0.1    private=True  loopback=False
203.0.113.7    private=True  loopback=False
100.20.30.40   private=False loopback=False
```

Üç ayrıntıya dikkat:

- `172.16.0.0/12` aralığı `172.31.255.255`'te biter. `172.31.0.9` özel,
  `172.32.0.9` açık. Göz kararı "172 ile başlıyorsa özel" demek yanlıştır.
- `127.0.0.1` için `is_private` de `True`. Bir adresi sınıflandırırken
  geri döngüyü **önce** ayırman gerekir.
- `203.0.113.0/24` belgelerde **örnek** olarak kullanılmak üzere ayrılmış
  bir aralıktır; gerçek bir cihaza ait değildir ve internette
  yönlendirilmediği için Python onu da `is_private` sayıyor. Bu modülde
  dışarıdaki bir sunucuyu anlatırken bu aralığı kullanıyoruz.

Bu ayrım güvenlikte sık geçer: içerden gelmesi gereken bir istek dışarıdaki
bir adresten geliyorsa, ya da dışarıdan gelen bir paket "ben içerdenim"
diye özel adres taşıyorsa bir sorun vardır.

## Port: aynı bilgisayardaki doğru program

IP adresi paketi doğru bilgisayara götürür; ama o bilgisayarda web
sunucusu, e-posta sunucusu, veritabanı aynı anda çalışıyor olabilir. Doğru
programı **port numarası** seçer. Port 16 bitlik bir sayıdır (0–65535).
Sık kullanılan servislerin bilinen portları vardır:

```python
WELL_KNOWN = {22: "ssh", 25: "smtp", 53: "dns", 80: "http",
              443: "https", 3306: "mysql"}

for host, port in [("203.0.113.7", 443), ("203.0.113.7", 22),
                   ("192.168.1.20", 3306), ("192.168.1.20", 8081)]:
    print(f"{host}:{port} -> {WELL_KNOWN.get(port, 'unknown')}")
```

```text
203.0.113.7:443 -> https
203.0.113.7:22 -> ssh
192.168.1.20:3306 -> mysql
192.168.1.20:8081 -> unknown
```

Adres ile portun ikilisi (`203.0.113.7:443`) bir bağlantının bir ucunu
tanımlar. Bağlantıyı başlatan taraf da kendi tarafında genellikle rastgele
seçilmiş büyük bir port kullanır (kapsülleme örneğindeki `51514` gibi).

Güvenlik için anlamı şu: **açık her port, dinleyen bir program ve
dolayısıyla saldırı yüzeyinin bir parçasıdır.** Saldırı Yüzeyi bölümündeki
kural burada da geçerli: kullanılmayan servis kapatılır. Veritabanı portu
(`3306`) gibi yalnızca içeriden erişilmesi gereken portlar internete hiç
açılmaz.

## TCP ve UDP

Taşıma katmanında iki ana protokol var:

<figure class="fig"><div class="versus">
  <div><h4>TCP</h4>Önce bağlantı kurar. Her parçanın ulaştığını doğrular, kaybolanı yeniden gönderir, sırayı korur. Web (HTTP/HTTPS), e-posta ve SSH bunu kullanır.</div>
  <div><h4>UDP</h4>Bağlantı kurmaz, paketi gönderir ve unutur. Kayıp ya da sıra garantisi yoktur ama hızlıdır. DNS sorguları, görüntülü görüşme ve oyunlar bunu kullanır.</div>
</div><figcaption>Güvenilirlik ile hız arasında bir seçim.</figcaption></figure>

TCP bağlantısı **üç adımlı el sıkışmayla** (three-way handshake) başlar:
istemci "bağlanmak istiyorum" (SYN) der, sunucu "tamam, ben de" (SYN-ACK)
diye cevap verir, istemci "aldım" (ACK) der. Bundan sonra veri akar.

<figure class="fig"><div class="flow">
  <span class="node">SYN</span><span class="arrow">→</span>
  <span class="node">SYN-ACK</span><span class="arrow">→</span>
  <span class="node">ACK</span><span class="arrow">→</span>
  <span class="node acc">Veri</span>
</div><figcaption>TCP üç adımlı el sıkışma. Sunucu ikinci adımdan sonra bağlantı için yer ayırır.</figcaption></figure>

Son cümle önemli: sunucu SYN-ACK gönderdiğinde yarım kalmış bağlantı için
bellekte yer ayırır. Ağ Saldırıları bölümünde göreceğimiz **SYN seli** bu
yeri doldurmaya dayanıyor.

## Her katmanın kendi saldırısı

Katmanlar yalnızca işi bölmez, güvenlik sorunlarını da sınıflandırmaya
yarar. Önümüzdeki bölümlerin haritası kabaca şöyle:

<figure class="fig anat">
  <div class="anat-row"><span>Bağlantı</span><span>ARP sahteciliği: yerel ağda başkasının yerine geçmek (Ağ Saldırıları).</span></div>
  <div class="anat-row"><span>Ağ</span><span>Sahte kaynak adresi, adres bazlı süzme (Ağ Saldırıları, Güvenlik Duvarı).</span></div>
  <div class="anat-row"><span>Taşıma</span><span>SYN seli, açık portlar (Ağ Saldırıları, Güvenlik Duvarı).</span></div>
  <div class="anat-row"><span>Uygulama</span><span>DNS, HTTP, çerez, SQL enjeksiyonu, XSS (modülün geri kalanı).</span></div>
  <figcaption>Savunma da katmanlıdır: bir katmanın korunması ötekileri korumaz (derinlemesine savunma).</figcaption>
</figure>

## Özet

- Ağ işi **katmanlara** bölünür: uygulama, taşıma, ağ, bağlantı (TCP/IP).
  OSI numaraları: 3 ağ, 4 taşıma, 7 uygulama.
- Her katman veriyi kendi başlığıyla sarar (**kapsülleme**); yolu izleyen
  biri başlıkları okuyabilir.
- **IPv4 adresi** 32 bitlik bir sayıdır; `ipaddress` modülü adres ve ağlarla
  çalışır.
- **CIDR** (`/24`) adresin ne kadarının ağı gösterdiğini söyler; her bit
  önek adres sayısını yarıya indirir.
- **Özel** aralıklar `10/8`, `172.16/12`, `192.168/16`; `127.0.0.1` **geri
  döngü**. Sınıflandırırken geri döngüyü önce ayır.
- **Port** aynı bilgisayardaki programı seçer; açık her port saldırı
  yüzeyidir.
- **TCP** güvenilir ve bağlantılı (üç adımlı el sıkışma), **UDP** hızlı ve
  garantisiz.
