# Kayıt ve İzleme

Önceki bölümlerde önlemleri gördük: izinler, yetki denetimi, güvenli
varsayılanlar. Ama hiçbir önlem kusursuz değildir. Bir şey ters gittiğinde
bunu **fark edebilmek** ve sonradan **ne olduğunu anlayabilmek** için
sistemlerin olayları kaydetmesi gerekir. Buna **kayıt tutma** (logging),
kayıtları sürekli takip edip dikkat gerektiren durumları yakalamaya da
**izleme** (monitoring) denir.

Kayıt yoksa bir saldırı hiç fark edilmeyebilir; fark edilse bile ne kadar
sürdüğü, neye dokunduğu bilinemez. Bu bölümdeki bütün kayıtlar sahte,
elle yazılmış satırlardır.

## İyi bir kayıt satırı

Bir güvenlik olayının kaydı beş soruya cevap verir:

| Soru | Alan | Örnek |
|---|---|---|
| Ne zaman? | `time` | `2026-11-01T10:00:07Z` |
| Kim? | `user` | `bob` |
| Nereden? | `source` | `203.0.113.7` |
| Ne yaptı? | `event` | `login` |
| Sonuç ne? | `result` | `fail` |

Kayda **yazılmayanlar** da en az bu kadar önemlidir: parola, oturum jetonu,
kart numarası ve gereğinden fazla kişisel veri kayda girmez (Sır Yönetimi
ve Gizlilik ve Veri Koruma bölümleri).

## Yapılı kayıt

"bob giriş yapamadı" gibi serbest bir cümleyi okumak insan için kolaydır,
ama bir programın binlerce satır içinde onu araması zordur. Bu yüzden
kayıtlar **yapılı** (structured) yazılır: her satır, alanları adıyla
taşıyan bir JSON nesnesidir.

```python
import json
from collections import Counter

LINES = [
    '{"t": "10:00:01", "level": "INFO", "user": "ada", "event": "login_ok"}',
    '{"t": "10:00:07", "level": "WARNING", "user": "bob", "event": "login_fail"}',
    '{"t": "10:00:09", "level": "WARNING", "user": "bob", "event": "login_fail"}',
    '{"t": "10:01:30", "level": "ERROR", "user": "-", "event": "db_timeout"}',
]
records = [json.loads(line) for line in LINES]
print(Counter(r["level"] for r in records))
print([r["t"] for r in records if r["event"] == "login_fail"])
```

```text
Counter({'WARNING': 2, 'INFO': 1, 'ERROR': 1})
['10:00:07', '10:00:09']
```

Düzeyleri saymak ve başarısız girişleri bulmak birer satır sürdü, çünkü
alanlar adıyla duruyor. **Kayıt düzeyleri** (`DEBUG`, `INFO`, `WARNING`,
`ERROR`, `CRITICAL`) bir olayın ne kadar önemli olduğunu söyler; izleme
araçları önce yüksek düzeylere bakar.

## Saat: her kayıt aynı dili konuşmalı

Bir olayı anlamak, farklı sistemlerin kayıtlarını **zaman sırasıyla**
yan yana koymaktır. Sistemlerin saatleri farklı saat dilimlerindeyse bu
sıra yanıltır:

```python
from datetime import datetime, timezone

STAMPS = ["2026-11-01T10:00:05+03:00", "2026-11-01T07:00:02+00:00"]
for stamp in STAMPS:
    utc = datetime.fromisoformat(stamp).astimezone(timezone.utc)
    print(stamp, "->", utc.strftime("%H:%M:%S"))
```

```text
2026-11-01T10:00:05+03:00 -> 07:00:05
2026-11-01T07:00:02+00:00 -> 07:00:02
```

Yerel saatiyle bakınca birincisi `10:00`'da, ikincisi `07:00`'de gibi
görünüyor; ortak saate (UTC) çevirince ikinci olayın aslında **3 saniye
önce** olduğu ortaya çıkıyor. Bu yüzden kayıtlar saat dilimiyle ya da
doğrudan UTC ile yazılır ve sistemlerin saatleri bir zaman sunucusuyla
eşitlenir.

## İzleme: eşik ve pencere

İzleme, kayıtlardaki **örüntüleri** arar. En basit örüntü bir sayıdır:
"bir dakika içinde beş başarısız giriş". Bunu bulmak için kayan bir
**zaman penceresi** tutulur: yeni olay eklenir, pencerenin dışına düşen
eski olaylar atılır.

```python
from collections import deque

FAILS = [0, 5, 12, 20, 31, 44, 200, 205]
WINDOW, LIMIT = 60, 5
window = deque()
for t in FAILS:
    window.append(t)
    while window[0] <= t - WINDOW:
        window.popleft()
    if len(window) >= LIMIT:
        print("alert at", t, "with", len(window), "failures")
```

```text
alert at 31 with 5 failures
alert at 44 with 6 failures
```

İlk altı başarısızlık bir dakikaya sığdığı için 31. ve 44. saniyelerde
uyarı çıktı. 200. saniyedeki başarısızlıklar tek başına kaldı. Pencere ve
eşik seçimi, Yetki Yükseltme bölümünde gördüğümüz dengeyi kurar: dar
pencere ve yüksek eşik yavaş denemeleri kaçırır, geniş pencere ve düşük
eşik yanlış alarm üretir.

## Kayıtların bütünlüğü

Bir saldırgan izini silmek için kayıtları değiştirmeye çalışabilir. Buna
karşı kayıtlar **ayrı bir sisteme** gönderilir (saldırganın eriştiği
makinede kalmaz) ve değişiklik **fark edilebilir** yapılır. Bir yol özet
zinciridir: her satırın özeti, bir önceki satırın özetini de içerir.

```python
import hashlib


def chain(entries):
    prev = "0" * 64
    hashes = []
    for entry in entries:
        prev = hashlib.sha256((prev + entry).encode()).hexdigest()
        hashes.append(prev)
    return hashes


LOG = ["login ada ok", "delete report-7", "logout ada"]
saved = chain(LOG)
tampered = ["login ada ok", "delete report-8", "logout ada"]
print([a == b for a, b in zip(saved, chain(tampered))])
```

```text
[True, False, False]
```

Yalnızca ikinci satırda tek bir rakam değişti, ama o satırdan sonraki
**bütün** özetler tutmadı. Değişikliğin yeri ve sonrası kendiliğinden
belli oldu. Özet zinciri değişikliği engellemez, fark edilmesini sağlar;
zincirin son özeti ayrı bir yerde saklanmalıdır.

## Ne kadar saklanır?

Kayıtlar sonsuza kadar saklanmaz: hem yer kaplar hem de içlerindeki
kişisel veri bir yüktür. **Saklama süresi** (retention) yasaların ve
kurumun ihtiyacına göre yazılı olarak belirlenir. Kısa tutulursa geç fark
edilen bir saldırının izleri silinmiş olur; uzun tutulursa gereksiz veri
birikir.

## Özet

- **Kayıt** olayları yazar, **izleme** onları takip edip örüntü arar.
- İyi kayıt: ne zaman, kim, nereden, ne yaptı, sonuç; parola ve jeton
  **yazılmaz**.
- **Yapılı (JSON) kayıt** programla aranabilir; düzeyler önemi söyler.
- Saatler **UTC**'ye çevrilir ve eşitlenir; yoksa olayların sırası
  yanıltır.
- İzleme **pencere ve eşikle** çalışır; seçim yanlış alarm ile kaçırma
  arasında bir dengedir.
- Kayıtlar ayrı bir sisteme gönderilir; **özet zinciri** değişikliği fark
  ettirir.
