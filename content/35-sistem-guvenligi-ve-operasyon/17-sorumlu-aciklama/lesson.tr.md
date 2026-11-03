# Sorumlu Açıklama

Bir gün, bir siteyi normal kullanırken bir açık fark edebilirsin: bir hata
sayfası başka kullanıcıların e-postalarını gösteriyordur ya da adresteki
bir sayıyı değiştirince başkasının siparişi açılıyordur. Bu bölüm böyle
bir anda ne yapılacağını anlatıyor: açığı sahibine **sorumlu bir şekilde**
bildirmenin yolunu ve karşı tarafın, yani bildirimi alan ekibin işini.

Bütün adresler, kişiler ve açık kimlikleri uydurmadır. Bölüm, Etik ve Hukuk
bölümündeki izin çizgisinin üzerine kurulu: açığı fark etmek ile onu
**denemek** farklı şeylerdir.

## Bir açık bulunca

Elinde bir açık olan kişinin önünde birkaç yol vardır:

| Yol | Ne olur? |
|---|---|
| Sessiz kalmak | Açık açık kalır; başkası bulup kötüye kullanabilir |
| Hemen herkese duyurmak (tam açıklama) | Düzeltme hazır olmadan herkes açığı öğrenir; kullanıcılar korumasız kalır |
| Satmak ya da kullanmak | Etik dışı ve çoğu ülkede suç |
| **Koordineli (sorumlu) açıklama** | Önce sahibine gizlice bildirilir, düzeltme çıkınca birlikte duyurulur |

Koordineli açıklamanın amacı, açığın kamuya **düzeltme ile birlikte**
çıkmasıdır: kullanıcılar korunur, sahibine düzeltmek için makul bir süre
tanınır ve bulan kişi emeğinin karşılığını (teşekkür, bazen ödül) alır.

Önemli bir sınır: açığı fark ettiğin anda dur. Var olduğunu göstermek için
başka kayıtlara bakmak, veri indirmek ya da "ne kadar derine gidiyor" diye
denemek, izin olmadan yapılan bir test olur.

## Kime bildirilir: security.txt

Birçok kurum güvenlik bildirimlerinin nereye gönderileceğini sitesinde
`/.well-known/security.txt` adresindeki küçük bir metin dosyasında yazar
(RFC 9116). Dosyada `Alan: değer` satırları vardır; `Contact` ve `Expires`
zorunludur. Bu dosyayı okumak basit bir metin işidir:

```python
SECURITY_TXT = """# Security contact for shop.example.org
Contact: mailto:security@example.org
Contact: https://example.org/report
Expires: 2026-12-31T23:59:59Z
Preferred-Languages: en, tr
Policy: https://example.org/disclosure-policy
"""
fields = {}
for line in SECURITY_TXT.splitlines():
    if not line or line.startswith("#"):
        continue
    name, value = line.split(":", 1)
    fields.setdefault(name.strip().lower(), []).append(value.strip())
for name in sorted(fields):
    print(name, fields[name])
```

```text
contact ['mailto:security@example.org', 'https://example.org/report']
expires ['2026-12-31T23:59:59Z']
policy ['https://example.org/disclosure-policy']
preferred-languages ['en, tr']
```

Bir alan birden çok kez yazılabildiği için (`Contact` iki kez) değerler
liste olarak tutuldu. `split(":", 1)` yalnızca ilk iki noktada bölüyor;
yoksa `https://...` adresindeki iki nokta da bölünürdü.

`Expires` alanı dosyanın ne zamana kadar güvenilir olduğunu söyler; süresi
geçmiş bir dosyadaki adres artık okunmuyor olabilir:

```python
from datetime import datetime, timezone

expires = datetime.fromisoformat("2026-12-31T23:59:59Z")
now = datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc)
print("expired" if expires < now else "valid")
print((expires - now).days, "days left")
```

```text
valid
58 days left
```

Dosya yoksa sitenin iletişim sayfası, bir güvenlik ekibi adresi ya da
kurumun açıklama politikası aranır. Bir açık **sosyal medyada** ya da
herkese açık bir hata kaydında bildirilmez.

## İyi bir rapor

Rapor, ekibin açığı **hızla anlayıp doğrulamasını** sağlamalı:

| Bölüm | İçerik |
|---|---|
| Başlık | Tek cümle: ne, nerede |
| Etkilenen yer | Adres, sürüm, sayfa |
| Nasıl fark edildi | Gördüğün şey ve yeniden görmek için gereken en az bilgi |
| Etki | Kimin hangi verisi risk altında; ölçtüğün kadarıyla |
| Öneri | Biliyorsan olası düzeltme |
| İletişim | Sana nasıl ulaşılacağı |

Rapora başkalarının verisi konmaz; gerekirse Etik ve Hukuk bölümündeki gibi
maskelenir. Rapor bir tehdit ya da pazarlık içermez ("ödemezseniz
yayınlarım" şantajdır).

## Süre: açıklama takvimi

Koordineli açıklamada genellikle bir **süre** konur; sık kullanılan değer
bildirimden itibaren **90 gündür**. Düzeltme daha önce çıkarsa, kullanıcılar
güncellesin diye kısa bir bekleme süresinden sonra birlikte duyurulur.
Hangisi önce gelirse:

```python
from datetime import date, timedelta

reported = date(2026, 11, 3)
deadline = reported + timedelta(days=90)
fixed = date(2027, 1, 10)
publish = min(deadline, fixed + timedelta(days=14))
print("deadline", deadline)
print("publish", publish)
```

```text
deadline 2027-02-01
publish 2027-01-24
```

Düzeltme 10 Ocak'ta çıktığı için duyuru, son tarihi beklemeden iki hafta
sonra yapılabiliyor. Süreler bir kural değil, iki tarafın anlaşmasıdır;
karmaşık bir açıkta uzatılabilir.

## CVE ve önem derecesi

Duyurulan açıklara genellikle bir **CVE** kimliği verilir: `CVE-yıl-sayı`
biçiminde, herkesin aynı açıktan söz ettiğinden emin olmasını sağlayan bir
ad. Önemi ise sık olarak **CVSS** puanıyla (0–10) anlatılır ve puan bir
derece adına çevrilir:

```python
import re


def rating(score):
    if score == 0:
        return "none"
    if score < 4:
        return "low"
    if score < 7:
        return "medium"
    if score < 9:
        return "high"
    return "critical"


for cve, score in [("CVE-2099-12345", 9.8), ("CVE-2099-0042", 5.3), ("CVE-99-1", 7.5)]:
    valid = re.fullmatch(r"CVE-[0-9]{4}-[0-9]{4,}", cve) is not None
    print(cve, valid, rating(score))
```

```text
CVE-2099-12345 True critical
CVE-2099-0042 True medium
CVE-99-1 False high
```

Kimlikler uydurma (2099 yılı bu yüzden). Üçüncü kimlik biçime uymuyor:
yıl dört, sıra numarası en az dört haneli olmalı. Derece bir başlangıçtır;
bir açığın senin sistemindeki gerçek riski, o sistemin nasıl kullanıldığına
da bağlıdır.

## Ödül programları ve güvenli liman

Bazı kurumlar **hata ödül programı** (bug bounty) yürütür: hangi
sistemlerin test edilebileceğini, neyin yasak olduğunu ve bulgulara ne
ödeneceğini yazarlar. Programın kuralları bir **izin belgesidir** ve
yalnızca yazdığı kapsamı kapsar. Pek çok politika, kurallara uyan iyi
niyetli araştırmacıya karşı hukuki yola gidilmeyeceğini söyleyen bir
**güvenli liman** (safe harbor) maddesi içerir. Program olmayan bir
sistemde bu güvence yoktur.

## Karşı taraf: bildirimi almak

Bildirim alan ekip için de iyi uygulamalar vardır: bildirimin alındığını
kısa sürede söylemek, açığı doğrulamak, düzeltme takvimini paylaşmak ve
bulan kişiye teşekkür etmek. Alındı bildiriminin gecikip gecikmediği
basitçe izlenebilir:

```python
from datetime import date

REPORTS = [["R-1", "2026-10-20", "2026-10-21"],
           ["R-2", "2026-10-25", None],
           ["R-3", "2026-11-01", None]]
TODAY = date(2026, 11, 3)
for rid, received, acknowledged in REPORTS:
    start = date.fromisoformat(received)
    end = date.fromisoformat(acknowledged) if acknowledged else TODAY
    days = (end - start).days
    print(rid, days, "late" if days > 5 else "ok")
```

```text
R-1 1 ok
R-2 9 late
R-3 2 ok
```

Henüz cevap verilmemiş bildirimin süresi bugüne kadar sayılıyor; `R-2`
dokuz gündür bekliyor. Cevapsız kalan bildirim, bulan kişiyi tam
açıklamaya iter.

## Özet

- Bir açığı fark edince **dur**; daha fazlasını denemek izinsiz bir test
  olur.
- **Koordineli açıklama**: önce sahibine gizlice bildir, düzeltmeyle
  birlikte duyur.
- Nereye bildirileceği çoğu zaman **security.txt** dosyasında yazar;
  `Contact` ve `Expires` zorunludur.
- İyi rapor kısa, doğrulanabilir ve başkalarının verisini içermez;
  şantaj içermez.
- Açıklama için genellikle **90 günlük** bir süre konur; düzeltme önce
  çıkarsa daha erken duyurulur.
- **CVE** açığın ortak adı, **CVSS** önem derecesidir.
- Ödül programının kuralları bir izindir ve yalnızca yazdığı kapsamı
  kapsar.
