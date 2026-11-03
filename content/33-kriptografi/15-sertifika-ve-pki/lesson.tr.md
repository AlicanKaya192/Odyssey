# Sertifikalar ve PKI

Dijital İmza bölümü bir soruyu açık bıraktı: imzayı doğrulamak için
kullandığımız açık anahtarın **gerçekten** o kişiye ya da siteye ait
olduğunu nereden biliyoruz? Diffie-Hellman bölümündeki "arada biri"
sorunu da aynı yere çıkıyor. Cevap **sertifika**: bir açık anahtarı bir
kimliğe bağlayan, güvenilen bir otoritenin imzaladığı belge. Bu
otoritelerin ve kuralların bütününe **açık anahtar altyapısı** (public key
infrastructure, **PKI**) denir.

## Sertifika neyi bağlar

Bir sertifikanın en önemli alanları:

| Alan | Örnek | Anlamı |
|---|---|---|
| `subject` | `shop.example.test` | Anahtarın sahibi |
| `e`, `n` | açık anahtar | Sahibin açık anahtarı |
| `issuer` | `Toy Root CA` | İmzalayan otorite |
| `not_before`, `not_after` | `2026-01-01`, `2026-12-31` | Geçerlilik aralığı |
| `signature` | sayı | Otoritenin, öteki alanların üzerine attığı imza |

Otorite (certificate authority, **CA**) sertifikayı imzalarken "bu açık
anahtar bu ada aittir" der. Oyuncak bir sertifika kuralım; imzalanan şey,
`signature` dışındaki alanların sıralı JSON hâli.

```python
import hashlib
import json


def digest(data, n):
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h, "big") % n


def tbs(cert):
    body = {k: v for k, v in cert.items() if k != "signature"}
    return json.dumps(body, sort_keys=True).encode()


def issue(fields, issuer_name, issuer_d, issuer_n):
    cert = dict(fields, issuer=issuer_name)
    cert["signature"] = pow(digest(tbs(cert), issuer_n), issuer_d, issuer_n)
    return cert


def check_signature(cert, issuer_e, issuer_n):
    return pow(cert["signature"], issuer_e, issuer_n) == digest(tbs(cert), issuer_n)


ca_n = 104723 * 104729
ca_d = pow(65537, -1, (104723 - 1) * (104729 - 1))
site_n = 104717 * 104743
leaf = issue({"subject": "shop.example.test", "e": 65537, "n": site_n,
              "not_before": "2026-01-01", "not_after": "2026-12-31"},
             "Toy Root CA", ca_d, ca_n)
print(leaf["issuer"], "->", leaf["subject"])
print(check_signature(leaf, 65537, ca_n))
```

```text
Toy Root CA -> shop.example.test
True
```

CA'nın açık anahtarını bilen herkes sertifikanın gerçek olduğunu
doğrulayabildi. `tbs` (to be signed) imzalanacak baytları **her seferinde
aynı sırayla** üretir: `sort_keys=True` olmasa aynı sertifika iki farklı
bayt dizisi verebilirdi.

## Değiştirilen sertifika

Sertifikanın içindeki açık anahtarı ya da adı değiştirmek, imzayı
bozar:

```python
fake_key = dict(leaf, n=12345)
fake_name = dict(leaf, subject="bank.example.test")
print(check_signature(fake_key, 65537, ca_n))
print(check_signature(fake_name, 65537, ca_n))
```

```text
False
False
```

Bu yüzden sertifika açıkça gönderilebilir: içindeki bilgiyi değiştiren
biri CA'nın özel anahtarı olmadan geçerli bir imza atamaz.

## Güven zinciri

Tarayıcılar ve işletim sistemleri birkaç yüz **kök sertifikayı** (root)
önceden, bir **güven deposunda** taşır. Kök CA'lar sertifikaları genelde
doğrudan imzalamaz; bir **ara CA**'yı imzalar, ara CA da sitelerin
sertifikalarını. Doğrulama, siteden köke kadar her halkada "bu sertifikayı
bir üstteki imzaladı mı" sorusunu sorar ve sonunda kökün güven deposunda
olup olmadığına bakar.

```python
mid_n = 104701 * 104707
mid_d = pow(65537, -1, (104701 - 1) * (104707 - 1))
root = issue({"subject": "Toy Root CA", "e": 65537, "n": ca_n},
             "Toy Root CA", ca_d, ca_n)
mid = issue({"subject": "Toy Issuing CA", "e": 65537, "n": mid_n},
            "Toy Root CA", ca_d, ca_n)
site = issue({"subject": "shop.example.test", "e": 65537, "n": site_n},
             "Toy Issuing CA", mid_d, mid_n)


def verify_chain(chain, trusted):
    for cert, parent in zip(chain, chain[1:]):
        if cert["issuer"] != parent["subject"]:
            return "issuer mismatch"
        if not check_signature(cert, parent["e"], parent["n"]):
            return "bad signature"
    top = chain[-1]
    if trusted.get(top["subject"]) != [top["e"], top["n"]]:
        return "untrusted root"
    return "ok"


trusted = {"Toy Root CA": [65537, ca_n]}
print(verify_chain([site, mid, root], trusted))
print(verify_chain([site, mid, root], {}))
print(verify_chain([site, root], trusted))
```

```text
ok
untrusted root
issuer mismatch
```

Zincir tamken doğrulama geçti. Güven deposu boşsa zincir kendi içinde
tutarlı olsa bile **güvenilmez**: herkes kendi kökünü kurup kendine
sertifika verebilir; önemli olan kökün önceden güvenilen listede olması.
Ara sertifika eksikse site sertifikasının imzalayanı bulunamadı.

## İmza yetmez: tarih ve ad

İmzası doğru bir sertifika yine de reddedilebilir. Doğrulayan iki şeye
daha bakar: **bugün geçerlilik aralığında mı** ve **sertifikadaki ad,
bağlanılan adla eşleşiyor mu**. Ad bir **joker** (`*.example.test`)
olabilir; joker yalnızca **tek bir** etiketin yerini tutar.

```python
def in_date(cert, today):
    return cert["not_before"] <= today <= cert["not_after"]


def host_matches(pattern, host):
    if pattern.startswith("*."):
        suffix = pattern[1:]
        rest = host[: -len(suffix)]
        return host.endswith(suffix) and rest != "" and "." not in rest
    return pattern == host


print(in_date(leaf, "2026-11-03"), in_date(leaf, "2027-01-15"))
print(host_matches("shop.example.test", "shop.example.test"))
print(host_matches("*.example.test", "shop.example.test"))
print(host_matches("*.example.test", "a.b.example.test"))
print(host_matches("shop.example.test", "shop.example.test.evil.test"))
```

```text
True False
True
True
False
False
```

Tarihler `YYYY-AA-GG` biçiminde olduğu için metin olarak karşılaştırmak
doğru sıralamayı verir. Joker `a.b.example.test`'i kapsamadı ve ad bir
başka alan adının içine gömülünce eşleşmedi. Gerçek doğrulayıcılar adı
`subject` yerine sertifikanın **Subject Alternative Name** (SAN)
listesinden alır.

## Sertifika iptali ve şeffaflık

- **İptal:** özel anahtar çalınırsa sertifika süresi dolmadan iptal edilir.
  İptal listeleri (CRL) ya da çevrim içi sorgu (OCSP) bunu duyurur. İptal
  bilgisine her zaman ulaşılamadığı için bugün sertifikaların ömrü kısa
  tutulur (aylarla ölçülür).
- **Sertifika şeffaflığı** (Certificate Transparency): CA'lar verdikleri
  her sertifikayı herkese açık, yalnızca eklenebilen kayıtlara yazar. Bir
  alan adının sahibi, haberi olmadan kendi adına verilmiş bir sertifikayı
  oradan görebilir.
- **Otomatik yenileme:** ACME protokolü sertifika almayı ve yenilemeyi
  otomatikleştirir; kısa ömürlü sertifikalar böylece sorun olmaz.

## Özet

- **Sertifika**, bir açık anahtarı bir ada bağlar; bir **CA** imzalar.
- Sertifikanın herhangi bir alanı değişirse imza tutmaz.
- **Güven zinciri:** site → ara CA → kök; kök önceden **güven deposunda**
  olmalı.
- İmza yetmez: **geçerlilik tarihi** ve **ad eşleşmesi** de denetlenir;
  joker tek etiketi kapsar.
- **İptal** (CRL, OCSP), **şeffaflık kayıtları** ve kısa ömürlü,
  otomatik yenilenen sertifikalar sistemi ayakta tutar.
