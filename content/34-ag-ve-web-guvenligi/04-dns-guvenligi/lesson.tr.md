# DNS Güvenliği

Tarayıcıya bir alan adı yazdığında bilgisayarın önce o adın IP adresini
bulması gerekir; Ağ Katmanları bölümünde gördüğümüz gibi paketler adla
değil adresle yol alır. Bu çeviriyi **DNS** (Domain Name System, alan adı
sistemi) yapar. DNS internetin telefon rehberidir ve rehberdeki bir satırı
değiştirebilen, insanları istediği yere gönderebilir. Bu bölüm DNS'in
nasıl çalıştığını, nerelerden saldırıya açık olduğunu ve nasıl
korunduğunu anlatıyor. Örnek adlar belgeler için ayrılmış `example.com`,
`example.net` ve `.example` adlarıdır; hiçbir sorgu gerçekten
gönderilmiyor.

## DNS nasıl çalışır?

Ad sağdan sola okunan bir **hiyerarşidir**: en üstte kök, sonra `com` gibi
üst düzey alan (TLD), sonra `example.com` alanının kendisi. Her alanın
kayıtlarını o alanın **yetkili sunucusu** (authoritative) tutar.
Bilgisayarın ise genellikle internet sağlayıcısının ya da kurumun
**çözümleyicisine** (resolver) sorar; çözümleyici gerekirse kökten başlayıp
yetkili sunucuya kadar sorar ve cevabı geri getirir.

<figure class="fig"><div class="flow">
  <span class="node">Bilgisayar</span><span class="arrow">→</span>
  <span class="node">Çözümleyici</span><span class="arrow">→</span>
  <span class="node">Kök, TLD</span><span class="arrow">→</span>
  <span class="node acc">Yetkili sunucu</span>
</div><figcaption>Çözümleyici zinciri izleyip cevabı bulur ve bir süre önbellekte tutar.</figcaption></figure>

Sık kullanılan kayıt türleri:

<figure class="fig anat">
  <div class="anat-row"><span><b>A</b> / <b>AAAA</b></span><span>Adın IPv4 / IPv6 adresi.</span></div>
  <div class="anat-row"><span><b>CNAME</b></span><span>"Bu ad aslında şu adın takma adıdır." Çözümleme hedef adla sürer.</span></div>
  <div class="anat-row"><span><b>MX</b></span><span>Alanın e-postasını kabul eden sunucu.</span></div>
  <div class="anat-row"><span><b>NS</b></span><span>Alanın yetkili sunucuları.</span></div>
  <div class="anat-row"><span><b>TXT</b></span><span>Serbest metin; e-posta doğrulama kuralları gibi bilgiler burada.</span></div>
  <figcaption>Bir alanın DNS kayıtları. Hepsi "bu ad için şu bilgi" eşleşmesidir.</figcaption>
</figure>

Bir çözümleyiciyi sözlükle taklit edelim. CNAME görünce hedef adla devam
ediyor, A kaydında duruyor:

```python
RECORDS = {
    "example.com": ("A", "203.0.113.10"),
    "www.example.com": ("CNAME", "example.com"),
    "shop.example.com": ("CNAME", "cdn.example.net"),
    "cdn.example.net": ("A", "198.51.100.20"),
}


def resolve(name):
    steps = [name]
    while True:
        record = RECORDS.get(name)
        if record is None:
            return steps, "NXDOMAIN"
        kind, value = record
        if kind == "A":
            return steps, value
        name = value
        steps.append(name)


for name in ["www.example.com", "shop.example.com", "mail.example.com"]:
    steps, answer = resolve(name)
    print(" -> ".join(steps), "=", answer)
```

```text
www.example.com -> example.com = 203.0.113.10
shop.example.com -> cdn.example.net = 198.51.100.20
mail.example.com = NXDOMAIN
```

`NXDOMAIN` "böyle bir ad yok" demektir. `shop.example.com` başka bir
alana (`example.net`) yönleniyor: dükkânın sayfaları bir içerik dağıtım
ağında duruyor olabilir. Bu tür dış yönlendirmeler aşağıda bir riske
dönüşecek.

## Önbellek ve TTL

Her sorguda kökten başlamak çok yavaş olurdu. Çözümleyici cevabı
**önbellekte** tutar; ne kadar tutacağını kaydın **TTL**'i (time to live,
saniye) söyler:

```python
cache = {}


def lookup(name, now, ttl=300):
    entry = cache.get(name)
    if entry and now < entry[1]:
        return entry[0], "cache"
    answer = resolve(name)[1]
    cache[name] = (answer, now + ttl)
    return answer, "asked"


for now in [0, 100, 299, 300, 450]:
    print(now, *lookup("www.example.com", now))
```

```text
0 203.0.113.10 asked
100 203.0.113.10 cache
299 203.0.113.10 cache
300 203.0.113.10 asked
450 203.0.113.10 cache
```

İlk sorgu yetkili zincire gitti, sonrakiler 300. saniyeye kadar önbellekten
geldi. Önbellek DNS'i hızlı yapar ama bir güvenlik sonucu da var: **yanlış
bir cevap önbelleğe girerse, TTL bitene kadar o çözümleyiciyi kullanan
herkese aynı yanlış cevap verilir.**

## Önbellek zehirleme

DNS sorguları çoğunlukla UDP ile gider (Ağ Katmanları bölümü): bağlantı
yoktur, çözümleyici soruyu gönderir ve gelen ilk uygun görünen cevabı
kabul eder. Saldırgan, gerçek cevaptan **önce** sahte bir cevap
yetiştirmeyi başarırsa çözümleyici onu önbelleğe yazar. Buna **önbellek
zehirleme** (cache poisoning) denir; sonrasında `bank.example`'ı soran
herkes saldırganın adresine gider.

Çözümleyici "bu cevap benim soruma mı?" diye iki şeye bakar: sorudaki
16 bitlik **sorgu numarası** ve sorunun gönderildiği **kaynak port**.
Eski çözümleyiciler hep aynı portu kullanıyordu; saldırganın tahmin etmesi
gereken tek şey sorgu numarasıydı:

```python
ids = 2 ** 16
ports = 65535 - 1024 + 1
print(ids)
print(ids * ports)
```

```text
65536
4227858432
```

Yalnızca sorgu numarası rastgele olduğunda 65536 olasılık var; bu, hızlı
bir saldırganın kısa sürede tutturabileceği bir sayı. Kaynak port da
1024–65535 arasında rastgele seçilince olasılık dört milyarı geçiyor.
Bugünkü çözümleyiciler ikisini de rastgele seçer. Bu tahmini zorlaştırır
ama cevabı **doğrulamaz**; asıl çözüm cevapları imzalamaktır.

## DNSSEC: imzalı cevaplar

**DNSSEC**, DNS kayıtlarını dijital imzayla imzalar (Kriptografi
modülünün Dijital İmza bölümü). Çözümleyici imzayı alanın açık
anahtarıyla doğrular; sahte cevabın imzası tutmaz. Peki alanın açık
anahtarının gerçek olduğu nasıl bilinir? Üst alan (`com`), alt alanın
anahtarının **özetini** kendi imzalı kaydında yayımlar (DS kaydı). Böylece
kökten aşağıya bir **güven zinciri** kurulur. Zincirin bir halkası özet
karşılaştırmasıdır:

```python
import hashlib
import hmac

child_key = "example.com zone key 2026"
published = hashlib.sha256(child_key.encode()).hexdigest()


def key_ok(presented):
    digest = hashlib.sha256(presented.encode()).hexdigest()
    return hmac.compare_digest(digest, published)


print(key_ok(child_key))
print(key_ok("example.com forged key"))
```

```text
True
False
```

Üst alanın yayımladığı özetle tutmayan anahtar reddedildi. Gerçek DNSSEC'te
anahtarlar açık anahtar, imzalar dijital imzadır; buradaki yalnızca
zincirin "üstteki, alttakini özetle tanır" fikrini gösteren oyuncak.
DNSSEC bütünlük ve kimlik doğruluğu sağlar, **gizlilik sağlamaz**:
sorgular yine okunabilir.

## Gizlilik: şifreli DNS

Düz DNS sorguları şifresizdir. Ağı dinleyen biri hangi sitelere
gittiğini, sayfaların içeriği HTTPS ile şifreli olsa bile, sorulan
adlardan görebilir. **Şifreli DNS** sorguları TLS içinde taşır: **DoT**
(DNS over TLS) ayrı bir portta, **DoH** (DNS over HTTPS) sıradan HTTPS
trafiğinin içinde. Bu dinlemeyi ve yolda değiştirmeyi önler; ama
çözümleyicinin kendisi sorguları görmeye devam eder, yani kime
güvendiğini seçmiş olursun.

## Başka DNS riskleri

- **Ayar ele geçirme** (hijacking): saldırgan ev yönlendiricisinin ya da
  bilgisayarın DNS ayarını kendi çözümleyicisine çevirirse bütün sorgular
  ona gider. Yönlendiricinin varsayılan yönetim parolası değiştirilir,
  yazılımı güncel tutulur.
- **Alan adı hesabının ele geçirilmesi:** alan adını kaydettiğin hesaba
  giren biri NS kayıtlarını değiştirip alanın tamamını alır. Bu hesapta
  MFA şarttır.
- **Sahipsiz CNAME** (dangling CNAME): `shop.example.com` artık
  kullanılmayan bir dış hizmete yönlenmeye devam ediyorsa, o hizmette aynı
  adı ilk kaydeden kişi `shop.example.com`'da istediğini yayımlar. Buna
  **alt alan devralma** (subdomain takeover) denir. Savunma: bir hizmeti
  kapatırken ona işaret eden DNS kaydını da silmek ve kayıtları düzenli
  gözden geçirmek.
- **Benzer adlar** (typosquatting): `example.com` yerine bir harfi
  değişmiş bir ad kaydedip oltalama için kullanmak.

Benzer adları yakalamanın bir yolu **düzenleme uzaklığıdır**: bir adı
ötekine çevirmek için kaç harf eklemek, silmek ya da değiştirmek gerekir?

```python
def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


for name in ["example.com", "examp1e.com", "exmaple.com", "example.co", "sample.org"]:
    d = distance(name, "example.com")
    flag = "LOOKALIKE" if 0 < d <= 2 else ""
    print(f"{name:<12} {d:>2}  {flag}".rstrip())
```

```text
example.com   0
examp1e.com   1  LOOKALIKE
exmaple.com   2  LOOKALIKE
example.co    1  LOOKALIKE
sample.org    5
```

`l` yerine `1` yazılmış ve iki harfi yer değiştirmiş adlar uzaklığı 1–2
olduğu için işaretlendi. Kurumlar kendi adlarına benzeyen yeni kayıtları
böyle izler; kullanıcı tarafındaki savunma da adresi yazmak yerine yer
imini kullanmak ve adres çubuğunu okumaktır.

## Özet

- **DNS** adları adrese çevirir; ad bir hiyerarşidir (kök, TLD, alan),
  çözümleyici zinciri izler.
- Kayıt türleri: **A/AAAA** adres, **CNAME** takma ad, **MX** e-posta,
  **NS** yetkili sunucu, **TXT** metin.
- Cevaplar **TTL** boyunca önbellekte durur; yanlış cevap da öyle.
- **Önbellek zehirleme** sahte cevabı önbelleğe sokar; rastgele sorgu
  numarası ve kaynak port tahmini zorlaştırır.
- **DNSSEC** kayıtları imzalar; üst alan alttakinin anahtar özetini
  yayımlar (güven zinciri). Gizlilik sağlamaz.
- **Şifreli DNS** (DoT, DoH) sorguları dinlemeye ve değiştirmeye karşı
  korur; çözümleyici yine görür.
- Sahipsiz CNAME, ayar ele geçirme ve benzer adlar da DNS riskidir;
  kayıtlar düzenli gözden geçirilir.
