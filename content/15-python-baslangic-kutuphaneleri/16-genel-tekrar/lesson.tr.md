# Genel Tekrar

Python Kütüphaneleri: Başlangıç modülünün sonuna geldin. Artık bir betikte
sayı, tarih, dosya, klasör, CSV, metin ve kalıp gerektiren işlerin çoğunu
hiçbir paket kurmadan, standart kütüphaneyle yapabiliyorsun. Bu bölüm yolu
bir kez daha yürüyor; sonunda modülün araçlarının birlikte çalıştığı bir
örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">Sayılar<br><small>01–02</small></span><span class="arrow">→</span>
    <span class="node">Zaman<br><small>03–04</small></span><span class="arrow">→</span>
    <span class="node">Dosyalar<br><small>05–08, 14</small></span><span class="arrow">→</span>
    <span class="node">Metin<br><small>09–10, 13</small></span><span class="arrow">→</span>
    <span class="node acc">Yapılar<br><small>11–12, 15</small></span>
  </div>
  <figcaption>Modülün yolu: sayılar ve zaman, sonra dosyalar ve metin, en sonda veri yapıları.</figcaption>
</figure>

## 1. Standart kütüphane (Bölüm 0)

Python'la birlikte gelen yaklaşık 300 modül (`sys.stdlib_module_names`);
kurulum gerekmez, her bilgisayarda aynı. Bir modülün ne sunduğunu `dir(modül)` ve `help(...)` söyler. Bir iş için
paket aramadan önce standart kütüphaneye bak.

## 2. Sayılar: math, statistics, random (Bölüm 1–2)

| İş | Araç |
|---|---|
| Ondalık karşılaştırmak | `math.isclose(a, b)` |
| Yukarı / aşağı yuvarlamak | `math.ceil`, `math.floor` |
| Kombinasyon, permütasyon | `math.comb`, `math.perm` |
| Ortalama, medyan, standart sapma | `statistics.mean`, `median`, `stdev` |
| Normal dağılımda olasılık | `statistics.NormalDist(...).cdf(x)` |
| Tekrarlanabilir rastgelelik | `random.Random(tohum)` |
| Seçmek | `choice`, `choices(..., weights=)`, `sample` |

`0.1 + 0.2 == 0.3` yanlıştır; `round(2.5)` 2'dir (bankacı yuvarlaması);
aynı tohum aynı diziyi verir.

## 3. Zaman: datetime, time (Bölüm 3–4)

| İş | Araç |
|---|---|
| Tarih kurmak | `date(2026, 3, 15)`, `datetime(...)` |
| Fark, ekleme | `timedelta`; toplam süre `total_seconds()` |
| Metin ↔ tarih | `strftime` / `strptime`; ISO için `isoformat` |
| Saat dilimi | `ZoneInfo("Europe/Istanbul")`, `astimezone` |
| Süre ölçmek | `time.perf_counter()` farkı |
| Beklemek | `time.sleep(saniye)` |

`%m` ay, `%M` dakika; `timedelta`'da ay yok; süre ölçmek için `time.time()`
değil `perf_counter`.

## 4. Dosya sistemi (Bölüm 5–7)

| İş | Araç |
|---|---|
| Yol kurmak, parçalar | `Path("a") / "b"`, `.name`, `.stem`, `.suffix`, `.parent` |
| Okumak, yazmak | `read_text` / `write_text` (`encoding="utf-8"`) |
| Klasör açmak | `mkdir(parents=True, exist_ok=True)` |
| Aramak | `glob("*.csv")`, `rglob("*.csv")` |
| Ağacı dolaşmak | `os.walk` |
| Kopyalamak, taşımak | `shutil.copy2`, `copytree`, `move` |
| Dolu klasör silmek | `shutil.rmtree` (kalıcı!) |
| Ortam değişkeni | `os.environ.get(ad, varsayılan)` |
| Sürüm, argümanlar | `sys.version_info`, `sys.argv` |

## 5. Veri dosyaları (Bölüm 8 ve 14)

- CSV: `open(..., newline="", encoding="utf-8")`, `DictReader` /
  `DictWriter`; değerler metin; Excel için `utf-8-sig` ve `;`.
- Arşiv: `zipfile.ZipFile(..., compression=ZIP_DEFLATED)`,
  `shutil.make_archive`, `gzip.open(..., "rt")`.
- Geçici: `tempfile.TemporaryDirectory()`; güvenli yazma geçici dosya +
  `os.replace`.

## 6. Metin (Bölüm 9–10 ve 13)

| İş | Araç |
|---|---|
| Kalıp aramak | `re.search`, `re.findall`; doğrulamak `re.fullmatch` |
| Parça çekmek | gruplar `(...)`, adlı `(?P<ad>...)` |
| Değiştirmek, bölmek | `re.sub` (`\1` ya da fonksiyon), `re.split` |
| Satırlara sarmak | `textwrap.wrap`, `shorten`, `dedent` |
| Benzerlik, fark | `difflib.get_close_matches`, `unified_diff` |
| Aksan atmak | `unicodedata.normalize("NFD", ...)` + `Mn` |

Kalıplar `r"..."`; regex biçimi denetler, anlamı Python'da denetle;
Türkçe `I`/`İ` için `lower()`'a güvenme.

## 7. Veri yapıları (Bölüm 11–12 ve 15)

| İş | Araç |
|---|---|
| Saymak | `Counter(...).most_common(n)` |
| Gruplamak | `defaultdict(list)` |
| Adlı kayıt | `namedtuple` |
| Kuyruk, son N | `deque`, `deque(maxlen=N)` |
| Ardışık, parça, birikim | `pairwise`, `batched`, `accumulate` |
| Kombinasyon | `product`, `permutations`, `combinations` |
| Bağımsız kopya | `copy.deepcopy` |
| Okunur yazdırmak | `pprint(..., depth=)` |
| Sabit seçenekler | `Enum`, `IntEnum`, `Flag` |

## Hepsi bir arada

Bir kayıt dosyasından hataları çekip günlere göre sayan ve en sık hataları
CSV raporuna yazan küçük bir araç: `pathlib`, `re`, `datetime`,
`collections` ve `csv` birlikte.

```python
import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

log = Path("app.log")
log.write_text(
    "2026-03-15 10:02:11 ERROR [db] connection lost\n"
    "2026-03-15 10:02:15 INFO [web] request ok\n"
    "2026-03-15 11:40:03 ERROR [web] timeout\n"
    "2026-03-16 09:05:44 ERROR [db] connection lost\n",
    encoding="utf-8",
)
LINE = re.compile(r"(\S+ \S+) (\w+) \[(\w+)\] (.+)")
errors = Counter()
by_day = Counter()
for line in log.read_text(encoding="utf-8").splitlines():
    m = LINE.fullmatch(line)
    if m and m[2] == "ERROR":
        when = datetime.strptime(m[1], "%Y-%m-%d %H:%M:%S")
        errors[m[4]] += 1
        by_day[when.date().isoformat()] += 1
with open("report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["message", "count"])
    writer.writerows(errors.most_common())
print(dict(by_day))
print(Path("report.csv").read_text(encoding="utf-8"))
```

```text
{'2026-03-15': 2, '2026-03-16': 1}
message,count
connection lost,2
timeout,1
```

Her satır bir bölümden geliyor: dosya `pathlib` ile yazılıp okunuyor, satır
`re` ile parçalanıyor, zaman `datetime` ile çözülüyor, sayım `Counter` ile
yapılıyor, rapor `csv` ile yazılıyor. Hiçbir paket kurulmadı.

## Sık hatalar

| Hata | Doğrusu |
|---|---|
| `0.1 + 0.2 == 0.3` | `math.isclose` |
| `random.seed` her yerde | `random.Random(tohum)` |
| `strptime(..., "%H:%m")` | `%M` dakika |
| Süreyi `time.time()` ile ölçmek | `perf_counter` |
| Yolu `+` ile yapıştırmak | `Path / "ad"` |
| `encoding` vermemek | `encoding="utf-8"` |
| CSV'yi `split(",")` ile okumak | `csv` modülü |
| `newline=""` unutmak | Windows'ta boş satırlar |
| Kalıbı `r` olmadan yazmak | `r"\b..."` |
| `groupby`'dan önce sıralamamak | `sorted(..., key=)` |
| `[[0] * 3] * 3` | kavrama |
| `"İ".lower()` | önce `I`/`İ` çevir |
