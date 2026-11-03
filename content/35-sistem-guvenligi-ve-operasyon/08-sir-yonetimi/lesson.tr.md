# Sır Yönetimi

Her programın gizli tutması gereken birkaç değeri vardır: veritabanı
parolası, bir hizmetin API anahtarı, oturumları imzalayan gizli anahtar.
Bunlara **sır** (secret) denir. Kod İnceleme ve Statik Analiz bölümünde
kaynak koda yazılmış sırları ağaçla aramayı gördük; bu bölüm madalyonun
öteki yüzünü anlatıyor: sırlar **nerede** tutulur, programa **nasıl**
verilir, kayıtlara sızmaları nasıl engellenir ve **ne zaman** değiştirilir.

Örnekler yine oyuncak: gerçek ortam değişkenlerine ya da bir sır kasasına
bağlanmıyoruz; ortamı bir sözlükle taklit ediyoruz.

## Sır kodda durmaz

Koda yazılan bir sır, kodun gittiği her yere gider: depo geçmişine,
yedeklere, geliştiricilerin bilgisayarlarına, belki herkese açık bir depoya.
Depodan silmek de yetmez, çünkü geçmişte durmaya devam eder. Kodda
yalnızca sırrın **adı** durur; değeri çalışma anında dışarıdan gelir:

<figure class="fig"><div class="versus">
  <div><h4>Kodda sır</h4><code>DB_PASSWORD = "hunter2"</code>. Kodu gören sırrı görür; değiştirmek için kodu değiştirmek gerekir; geçmişten silinmez.</div>
  <div><h4>Dışarıdan sır</h4>Kod yalnızca <code>DB_PASSWORD</code> adını bilir. Değer ortam değişkeninden ya da bir <b>sır kasasından</b> gelir; her ortamda farklı olabilir ve kod değişmeden yenilenir.</div>
</div><figcaption>Kod herkese gösterilebilecek kadar temiz olmalı; sırlar ayrı ve erişimi denetimli bir yerde durur.</figcaption></figure>

Sırrı ortamdan okuyan bir program, sır **eksikse** ne yapmalı? Güvenli
Yazılım Geliştirme bölümündeki kural: **kapalı başarısız ol**. Boş bir
parolayla ya da varsayılan bir değerle devam etmek yerine hemen dur:

```python
ENV = {"DB_HOST": "db.internal", "DB_PASSWORD": "s3cr3t-value"}


def get_secret(env, name):
    value = env.get(name, "")
    if not value:
        raise RuntimeError(f"missing secret: {name}")
    return value


print(len(get_secret(ENV, "DB_PASSWORD")))
try:
    get_secret(ENV, "API_TOKEN")
except RuntimeError as error:
    print(error)
```

```text
12
missing secret: API_TOKEN
```

Eksik sır programın **açılışında** fark edildi ve iletide yalnızca sırrın
adı yazıyor, değeri değil. Program sırrın kendisini hiçbir yere yazmadı;
yalnızca uzunluğunu bastı.

## Sırrı kayıtlara sızdırmamak

Sırların en sık sızdığı yer kayıt dosyalarıdır: bir hata ayıklama satırı
bütün isteği ya da bütün yapılandırmayı yazar ve parola da onunla gider.
Kayıt yazılmadan önce sır içeren alanlar **gizlenir** (redaction):

```python
import re

PATTERN = re.compile(r"(password|token|secret)=\S+", re.IGNORECASE)


def redact(line):
    return PATTERN.sub(r"\1=***", line)


print(redact("login user=ada password=hunter2 ok"))
print(redact("call api TOKEN=abc123 status=200"))
```

```text
login user=ada password=*** ok
call api TOKEN=*** status=200
```

Anahtar adı kaldı, değeri `***` oldu; kaydı okuyan kişi neyin gizlendiğini
görür ama sırrı göremez. Bir sırrı insanlara tanıtmak gerektiğinde (hangi
anahtar kullanılıyor?) tamamı yerine yalnızca son birkaç karakteri
gösterilir: `****1a2b`.

## Sırrı bulmak: entropi

Sır tarayıcıları kodda ve geçmişte sızmış sırları arar. Adı bilinmeyen bir
sırrı bulmanın yollarından biri **entropiye** bakmaktır: rastgele üretilmiş
bir anahtar, sıradan bir kelimeden çok daha "dağınıktır". Shannon
entropisi, bir metnin karakter başına kaç bit bilgi taşıdığını ölçer:

```python
import math
from collections import Counter


def entropy(text):
    counts = Counter(text)
    total = len(text)
    return sum(c / total * math.log2(total / c) for c in counts.values())


for text in ["aaaaaaaa", "password", "q8Zr2LxP0vT7mWk9"]:
    print(f"{text:<18} {entropy(text):.2f}")
```

```text
aaaaaaaa           0.00
password           2.75
q8Zr2LxP0vT7mWk9   4.00
```

Tek harfin tekrarı 0,00 bit, sıradan bir kelime 2,75 bit,
rastgele görünen anahtar 4,00 bit taşıyor. Tarayıcılar belirli bir
eşiğin üstündeki uzun metinleri "olası sır" diye işaretler. Bu bir
kestirimdir: rastgele görünen her metin sır değildir (yanlış alarm) ve
kısa ya da kelimelerden oluşan sırlar eşiğin altında kalabilir.

## Güçlü sır üretmek

Sır üretirken `random` değil, Rastgelelik bölümünde gördüğümüz `secrets`
modülü kullanılır:

```python
import secrets

token = secrets.token_urlsafe(32)
print(len(token))
print(all(c.isalnum() or c in "-_" for c in token))
```

```text
43
True
```

32 rastgele bayt, URL'de güvenle taşınabilecek 43 karakterlik
bir metne dönüştü. Değerin kendisini basmadık: her çalıştırmada farklıdır
ve bir sır ekrana da yazılmaz.

## Sırları yenilemek

Bir sır ne kadar uzun yaşarsa, fark edilmeden sızmış olma ihtimali o kadar
artar. Bu yüzden sırlar düzenli olarak **yenilenir** (rotation): yeni değer
üretilir, sistemler ona geçirilir, eskisi iptal edilir. Hangi sırrın
yenileme zamanının geldiğini bulmak bir tarih hesabıdır:

```python
from datetime import date

TODAY = date(2026, 11, 1)
SECRETS = [
    ("db-password", date(2026, 9, 20)),
    ("api-token", date(2026, 6, 1)),
    ("signing-key", date(2025, 12, 15)),
]
MAX_DAYS = 90
for name, created in SECRETS:
    age = (TODAY - created).days
    status = "rotate" if age > MAX_DAYS else "ok"
    print(f"{name:<12} {age:>3} days  {status}")
```

```text
db-password   42 days  ok
api-token    153 days  rotate
signing-key  321 days  rotate
```

Sızdığı bilinen ya da şüphelenilen bir sır ise beklemeden yenilenir:
silmek ya da gizlemek yetmez, çünkü değer zaten başkasının elinde olabilir.
Sır yenilemeyi kolaylaştıran asıl şey, sırrın kodda değil tek bir yerde
durmasıdır.

## Sır kasası

Kurumlarda sırlar bir **sır kasasında** (secrets manager, vault) tutulur.
Kasa sırları şifreli saklar, kimin hangi sırra eriştiğini kaydeder, erişimi
en az yetkiyle sınırlar ve yenilemeyi kendiliğinden yapabilir. Bazı kasalar
**kısa ömürlü** sırlar üretir: her uygulama birkaç saatlik bir parola alır,
süresi dolunca parola kendiliğinden geçersiz olur.

## Özet

- Sır **kodda durmaz**; kodda yalnızca adı olur, değeri ortamdan ya da sır
  kasasından gelir.
- Sır eksikse program **kapalı başarısız olur**: boş değerle devam etmez.
- Kayıtlara yazmadan önce sırlar **gizlenir**; tanıtmak için yalnızca son
  karakterler gösterilir.
- Sır tarayıcıları adlara ve **entropiye** bakar; bu bir kestirimdir.
- Sır `secrets` modülüyle üretilir ve ekrana yazılmaz.
- Sırlar düzenli **yenilenir**; sızan sır hemen yenilenir.
