# Saldırı Tespiti (IDS)

Kayıt ve İzleme bölümünde kayıtları toplamayı ve basit eşiklerle uyarı
üretmeyi gördük. **Saldırı tespit sistemi** (Intrusion Detection System,
IDS) bu fikrin uzmanlaşmış hâlidir: ağ trafiğini ya da sistem olaylarını
sürekli inceler ve saldırıya benzeyen her şey için uyarı üretir.

Bu bölüm iki ana tespit yöntemini, bir tespit sisteminin nasıl
**ölçüldüğünü** ve tek tek zararsız görünen olayların birlikte nasıl bir
anlam taşıyabileceğini anlatıyor. Bütün veri sahte: elle yazılmış istek
satırları, olay listeleri ve belgeler için ayrılmış örnek IP adresleri
(`203.0.113.0/24`, `198.51.100.0/24`).

## Nerede durur, ne yapar?

| Tür | Neye bakar? | Örnek |
|---|---|---|
| **Ağ tabanlı IDS** (NIDS) | Ağdan geçen trafiğe | Bir ağ geçidindeki tespit sistemi |
| **Sunucu tabanlı IDS** (HIDS) | Bir bilgisayarın kendi olaylarına | Dosya değişiklikleri, girişler, süreçler |
| **IDS** | Uyarır, durdurmaz | Güvenlik ekibine bildirim |
| **IPS** (önleme sistemi) | Tespit ettiğini durdurur | Bağlantıyı keser |

IPS daha güçlü görünür ama bir yanlış alarm, gerçek kullanıcıların
isteğini de keser. Bu yüzden yeni bir kural genellikle önce yalnızca
**uyarı** kipinde denenir.

## Yöntem 1: imza

**İmza tabanlı tespit** (signature-based), bilinen saldırıların belirgin
izlerini arar. Her imza bir kalıptır; bir satır kalıba uyarsa uyarı çıkar:

```python
import re

RULES = {
    "path traversal": re.compile(r"\.\./"),
    "script tag": re.compile(r"<script", re.IGNORECASE),
    "sql injection": re.compile(r"'\s*or\s+1=1", re.IGNORECASE),
}
LINES = [
    "GET /index.html",
    "GET /files?name=../../etc/passwd",
    "GET /search?q=' OR 1=1 --",
    "POST /comment body=<SCRIPT>hi</SCRIPT>",
    "GET /search?q=shoes",
]
for number, line in enumerate(LINES, 1):
    for name, pattern in RULES.items():
        if pattern.search(line):
            print(number, name)
```

```text
2 path traversal
3 sql injection
4 script tag
```

Bilinen üç saldırı kalıbı yakalandı, sıradan iki istek sessiz kaldı.
İmzanın gücü **kesinliğidir**: tanıdığını güvenilir biçimde ve az yanlış
alarmla bulur. Zayıflığı da aynı yerdedir: yalnızca **tanıdığını** bulur.
Daha önce görülmemiş bir saldırı için imza yoktur; imzalar bu yüzden
düzenli güncellenir.

## Yöntem 2: anomali

**Anomali tabanlı tespit** (anomaly-based) saldırıyı tanımaya çalışmaz;
önce **olağanı** öğrenir, sonra olağandan çok sapan her şeyi işaretler.
En basit ölçü **z skorudur**: bir değerin ortalamadan kaç standart sapma
uzakta olduğu.

```python
import statistics

BASELINE = [120, 130, 125, 118, 122, 127, 131, 124]
mean = statistics.mean(BASELINE)
stdev = statistics.stdev(BASELINE)
print(f"mean {mean:.1f}, stdev {stdev:.1f}")
for value in [126, 410]:
    z = (value - mean) / stdev
    print(value, f"z={z:.1f}", "ANOMALY" if abs(z) > 3 else "normal")
```

```text
mean 124.6, stdev 4.6
126 z=0.3 normal
410 z=62.1 ANOMALY
```

Saatte 124,6 istek olağan; 126 istek bu aralıkta, 410 ise ortalamadan
62,1 standart sapma uzakta ve işaretlendi. Anomali tespiti hiç
görülmemiş saldırıları da yakalayabilir, ama bedeli **yanlış alarmdır**:
bir kampanya günü ya da yeni bir özellik de "olağandışı"dır. Olağanın
kendisi de zamanla değişir; bu yüzden temel çizgi düzenli yeniden
hesaplanır.

## Tespiti ölçmek

Bir tespit sistemi ne kadar iyi? Bunu cevaplamak için uyarılar, gerçekte
ne olduğuyla karşılaştırılır:

```python
ALERTS = {"e1", "e2", "e5", "e7"}
ATTACKS = {"e2", "e5", "e6"}
tp = len(ALERTS & ATTACKS)
fp = len(ALERTS - ATTACKS)
fn = len(ATTACKS - ALERTS)
print("true positives:", tp, "false positives:", fp, "missed:", fn)
print(f"precision {tp / (tp + fp):.2f}, recall {tp / (tp + fn):.2f}")
```

```text
true positives: 2 false positives: 2 missed: 1
precision 0.50, recall 0.67
```

- **Kesinlik** (precision): uyarıların ne kadarı gerçek saldırı? Burada
  0,50: her iki uyarıdan biri boşa.
- **Duyarlılık** (recall): gerçek saldırıların ne kadarı yakalandı? Burada
  0,67: üç saldırıdan biri (`e6`) kaçtı.

İkisi birbirine karşı çalışır: eşiği düşürmek duyarlılığı artırır ama
kesinliği düşürür; Kayıt ve İzleme bölümündeki uyarı yorgunluğu düşük
kesinliğin sonucudur. Gerçek saldırılar olaylar arasında çok **seyrek**
olduğundan, küçük görünen bir yanlış alarm oranı bile günde yüzlerce boş
uyarı demektir.

## Olayları birleştirmek

Tek başına zararsız görünen olaylar birlikte bir anlam taşıyabilir. Aynı
yerden art arda başarısız girişler olağandır (biri parolasını unutmuştur);
ama ardından **başarılı** bir giriş gelirse, parola tahmin edilmiş olabilir:

```python
from collections import Counter

EVENTS = [
    ("10:00", "203.0.113.9", "bob", "fail"),
    ("10:01", "203.0.113.9", "bob", "fail"),
    ("10:01", "198.51.100.4", "ada", "fail"),
    ("10:02", "203.0.113.9", "bob", "fail"),
    ("10:02", "198.51.100.4", "ada", "ok"),
    ("10:03", "203.0.113.9", "bob", "fail"),
    ("10:04", "203.0.113.9", "bob", "ok"),
]
fails = Counter()
for time, ip, user, result in EVENTS:
    key = (ip, user)
    if result == "fail":
        fails[key] += 1
    elif fails[key] >= 3:
        print(time, "possible compromise:", user, "from", ip)
        print("  failures before:", fails[key])
```

```text
10:04 possible compromise: bob from 203.0.113.9
  failures before: 4
```

`ada` bir kez yanlış yazıp girdi: olağan. `bob`'un hesabına aynı adresten
dört başarısız denemenin ardından giriş yapıldı: hesabın ele geçirilmiş
olabileceğine dair güçlü bir işaret. Bu tür birleştirmeye **olay
ilişkilendirme** (correlation) denir ve iyi bir uyarı sistemi tek tek
olaylardan çok bu tür örüntülere bakar. Uyarı geldiğinde ne yapılacağı bir
sonraki bölümün, Olay Müdahalesi'nin konusudur.

## Özet

- **IDS** saldırıya benzeyeni tespit edip uyarır; **IPS** durdurur.
  Ağ tabanlı (NIDS) ya da sunucu tabanlı (HIDS) olur.
- **İmza tabanlı tespit** bilineni kesin bulur, yeniyi kaçırır.
- **Anomali tabanlı tespit** olağandan sapmayı bulur; yeniyi de yakalar
  ama yanlış alarm üretir.
- **Kesinlik:** uyarıların ne kadarı gerçek; **duyarlılık:** gerçeklerin
  ne kadarı yakalandı. İkisi birbirine karşı çalışır.
- **İlişkilendirme:** art arda başarısızlık + başarı gibi örüntüler tek
  olaydan daha anlamlıdır.
