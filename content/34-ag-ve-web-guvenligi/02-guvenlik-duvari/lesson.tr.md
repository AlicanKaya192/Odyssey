# Güvenlik Duvarı

Ağ Saldırıları bölümünün savunma listesinde bir araç sürekli geçti:
paketleri bir kurala göre geçiren ya da durduran bir süzgeç. Buna
**güvenlik duvarı** (firewall) denir. Bu bölüm güvenlik duvarının nasıl
karar verdiğini, kuralların nasıl yazıldığını ve en sık yapılan hataları
anlatıyor. Kuralları yine Python'da küçük bir değerlendiriciyle
deneyeceğiz; gerçek bir güvenlik duvarına dokunmuyoruz.

## Güvenlik duvarı ne yapar?

Güvenlik duvarı iki ağın (ya da bir bilgisayar ile ağın) arasında durur ve
her paket için **geçsin mi, geçmesin mi** diye karar verir. Kararı
başlıklara bakarak verir: protokol (TCP/UDP), kaynak ve hedef adresi,
hedef portu. Ağ Katmanları bölümündeki dilde, sıradan bir güvenlik duvarı
**ağ ve taşıma katmanlarında** (OSI 3–4) çalışır.

İki yerde bulunur:

- **Ağ güvenlik duvarı:** kurumun ya da evin internet bağlantısında,
  bütün ağın önünde. Ev yönlendiricilerinin içinde de basit bir tane
  vardır.
- **Bilgisayar (host) güvenlik duvarı:** her bilgisayarın kendi üstünde
  çalışır; ağın içinden gelen trafiğe de bakar. İkisi birlikte
  derinlemesine savunmadır.

## Kural, sıra ve varsayılan

Bir güvenlik duvarı bir **kural listesi** tutar. Her kural "şu
özellikleri taşıyan paketlere şunu yap" der. Paket gelince kurallar
**yukarıdan aşağıya** denenir ve **ilk tutan kural** kararı verir. Hiçbiri
tutmazsa **varsayılan** karar uygulanır. Güvenlik İlkeleri bölümündeki
"varsayılan olarak reddet" kuralı burada doğrudan uygulanır: izin
verilmeyen her şey yasaktır.

```python
import ipaddress

RULES = [
    {"action": "allow", "proto": "tcp", "port": 443, "src": "0.0.0.0/0"},
    {"action": "allow", "proto": "tcp", "port": 22, "src": "192.168.1.0/24"},
]


def matches(rule, packet):
    return (rule["proto"] in ("any", packet["proto"])
            and rule["port"] in ("any", packet["port"])
            and ipaddress.ip_address(packet["src"]) in ipaddress.ip_network(rule["src"]))


def decide(packet):
    for number, rule in enumerate(RULES, 1):
        if matches(rule, packet):
            return f"{rule['action']} (rule {number})"
    return "deny (default)"


for packet in [{"proto": "tcp", "port": 443, "src": "203.0.113.7"},
               {"proto": "tcp", "port": 22, "src": "192.168.1.20"},
               {"proto": "tcp", "port": 22, "src": "203.0.113.7"},
               {"proto": "udp", "port": 53, "src": "203.0.113.7"}]:
    print(packet["port"], packet["src"], "->", decide(packet))
```

```text
443 203.0.113.7 -> allow (rule 1)
22 192.168.1.20 -> allow (rule 2)
22 203.0.113.7 -> deny (default)
53 203.0.113.7 -> deny (default)
```

Kurallar şunu söylüyor: web sunucusuna (443) herkes gelebilir
(`0.0.0.0/0` "bütün adresler" demektir); SSH'ye (22) yalnızca iç ağdan
gelinebilir. Dışarıdan gelen SSH denemesi hiçbir kurala uymadı ve
varsayılanla reddedildi. UDP 53 için de kural yazılmadığı için aynısı
oldu. **Yazmadığın şeye izin vermemiş olursun**; açılması gereken her
şey bilinçli olarak tek tek açılır.

Kararı kuralın numarasıyla birlikte yazdırmak boşuna değil: gerçek
güvenlik duvarları da hangi kuralın hangi paketi karşıladığını kaydeder.
Bir paket neden geçti ya da neden durdu sorusunun cevabı oradadır.

## Sıra önemlidir: gölgelenen kural

İlk tutan kural kazandığı için **sıra** kuralın kendisi kadar önemlidir.
Geniş bir kural daha dar bir kuralın üstündeyse, dar olan hiçbir zaman
çalışmaz. Buna **gölgelenen kural** (shadowed rule) denir:

```python
def first_action(rules, port):
    for rule_port, action in rules:
        if rule_port in ("any", port):
            return action
    return "deny"


intended = [(23, "deny"), (80, "allow"), (443, "allow")]
broken = [("any", "allow"), (23, "deny")]
print("intended:", first_action(intended, 23), first_action(intended, 8080))
print("broken:  ", first_action(broken, 23), first_action(broken, 8080))
```

```text
intended: deny deny
broken:   allow allow
```

İkinci listede biri sorun ararken en üste "geçici olarak her şeye izin
ver" kuralı eklemiş ve unutmuş. Altındaki "23'ü (eski, şifresiz uzak
bağlantı) kapat" kuralı hâlâ listede duruyor, okuyan güvende sanıyor, ama
hiçbir paket ona ulaşmıyor. Üstelik varsayılan reddetme de devre dışı
kaldı: 8080 da açıldı. Kural listesi büyüdükçe bu hata çok kolay olur; bu
yüzden kurallar düzenli olarak gözden geçirilir ve **hiç tutmayan
kurallar** ayıklanır.

## Durumsuz ve durumlu

Sorun şu: bilgisayarın dışarıdaki bir web sunucusuna bağlanınca sunucunun
**cevabı** da içeri girmeli. Cevap, senin rastgele seçtiğin büyük bir
porta (`51514` gibi) gelir. Her paketi tek başına değerlendiren bir
**durumsuz** (stateless) süzgeç bunu bilemez; cevapları geçirmek için
yüksek portların hepsini dışarıya açmak zorunda kalır. Bu da kocaman bir
deliktir.

**Durumlu** (stateful) güvenlik duvarı bağlantıları hatırlar. İçeriden
dışarıya bir bağlantı başlayınca onu bir tabloya yazar; dışarıdan gelen bir
paketi ancak tablodaki bir bağlantının **tersiyse** geçirir:

```python
outgoing = set()


def send(src, sport, dst, dport):
    outgoing.add((src, sport, dst, dport))


def reply_ok(src, sport, dst, dport):
    return (dst, dport, src, sport) in outgoing


send("192.168.1.10", 51514, "203.0.113.7", 443)
print(reply_ok("203.0.113.7", 443, "192.168.1.10", 51514))
print(reply_ok("203.0.113.7", 443, "192.168.1.10", 51999))
print(reply_ok("198.51.100.9", 443, "192.168.1.10", 51514))
```

```text
True
False
False
```

Yalnızca gerçekten başlatılmış bağlantının cevabı geçti. Aynı sunucudan
başka bir porta gelen ve başka bir adresten gelen paket durdu. Bugünkü
güvenlik duvarlarının neredeyse hepsi durumludur.

<figure class="fig"><div class="versus">
  <div><h4>Durumsuz</h4>Her paketi tek başına, yalnızca kendi başlıklarına bakarak değerlendirir. Hızlı ve basittir; ama cevapları geçirmek için geniş aralıklar açmak gerekir.</div>
  <div><h4>Durumlu</h4>Bağlantıları bir tabloda izler; dışarıdan gelen paketi ancak içeriden başlamış bir bağlantının cevabıysa geçirir. Dışarıdan başlatılan bağlantı kendiliğinden durur.</div>
</div><figcaption>Durumlu güvenlik duvarı "kim başlattı" sorusunu sorabilir.</figcaption></figure>

## Çıkışı da süz

Kurallar çoğu zaman yalnızca **içeri** gelen trafik için yazılır. Oysa
içerideki bir bilgisayar zararlı yazılım bulaştığında dışarıdaki bir
sunucuya bağlanıp komut almaya ya da veri göndermeye çalışır. **Çıkış
süzmesi** (egress filtering) bunu zorlaştırır: içeriden dışarıya yalnızca
gereken portlara izin verilir, gerisi durdurulur ve **kaydedilir**:

```python
ALLOWED_OUT = {53, 80, 443}
attempts = [("192.168.1.10", 443), ("192.168.1.10", 8888),
            ("192.168.1.30", 53), ("192.168.1.30", 2525)]

for host, port in attempts:
    print(host, port, "allow" if port in ALLOWED_OUT else "block + log")
```

```text
192.168.1.10 443 allow
192.168.1.10 8888 block + log
192.168.1.30 53 allow
192.168.1.30 2525 block + log
```

Engellenen deneme tek başına bir şey kanıtlamaz, ama "bu bilgisayar neden
`8888`'e çıkmaya çalışıyor?" sorusu bir olayın ilk ipucu olabilir. Ağ
Saldırıları bölümündeki çıkış süzmesi kuralı da buydu: kendi ağının
başkasına saldırıda kullanılmasını önlemek.

## Uygulama katmanında: WAF

Sıradan güvenlik duvarı başlıklara bakar, içeriğe bakmaz. 443 portuna
izin verdiysen, o porttan gelen her HTTP isteği geçer; isteğin içinde SQL
enjeksiyonu olsa bile. **Web uygulama güvenlik duvarı** (WAF) uygulama
katmanında (OSI 7) çalışır: HTTP isteğinin yolunu, parametrelerini,
başlıklarını inceleyip bilinen saldırı kalıplarına benzeyenleri durdurur.

WAF yararlı bir **ek katmandır**, ama bir kalıp listesi olduğu için
atlatılabilir; uygulamadaki açığı kapatmaz. SQL Enjeksiyonu ve XSS
bölümlerinde göreceğimiz gibi asıl savunma uygulamanın kendi kodundadır
(parametreli sorgu, çıktı kodlama). WAF onun yerini tutmaz.

## Güvenlik duvarı neyi yapamaz?

- **İzin verdiğin trafiğin içindekini göremez.** 443'ten gelen saldırı 443
  açıksa geçer.
- **Şifreli içeriği okuyamaz** (ayrıca çözmek için kurulmadıysa).
- **İçeride başlayan saldırıyı** (ağın içindeki ele geçirilmiş bir
  bilgisayar) ağ güvenlik duvarı görmez; bunun için ağ bölümleme ve
  bilgisayar güvenlik duvarı gerekir (VPN ve Ağ Bölümleme bölümü).
- **Kimlik doğrulamanın yerini tutmaz:** adrese dayalı kural, Ağ
  Saldırıları bölümünde gördüğümüz gibi sahte adresle aldatılabilir.

## Özet

- Güvenlik duvarı her paket için **geçir ya da durdur** kararı verir;
  sıradan olanı başlıklara (adres, port, protokol) bakar.
- Kurallar **yukarıdan aşağıya** denenir, **ilk tutan** kazanır; hiçbiri
  tutmazsa **varsayılan reddet**.
- Geniş kural dar kuralın üstündeyse dar olan **gölgelenir**; kurallar
  düzenli gözden geçirilir.
- **Durumlu** güvenlik duvarı bağlantıları hatırlar, yalnızca içeriden
  başlamış bağlantının cevabını geçirir.
- **Çıkış süzmesi** ele geçirilmiş bilgisayarın dışarıya bağlanmasını
  zorlaştırır; engellenen deneme kaydedilir.
- **WAF** HTTP içeriğine bakan ek bir katmandır; uygulamadaki açığı
  kapatmaz.
- Güvenlik duvarı izin verilen trafiğin içini, içeriden başlayan saldırıyı
  ve kimliği denetleyemez.
