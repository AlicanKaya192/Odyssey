# Bitirme: Uçtan Uca MLOps Hattı

Bu modülde her bölüm bir parça kurdu. Bitirme bölümünde parçaları tek bir
hatta birleştiriyoruz: her ay kendiliğinden çalışan, modeli izleyen,
gerekince yeniden eğiten, veriyi ve yeni modeli denetleyen bir hat. Sonra
hattı sekiz ay boyunca çalıştırıp her ay ne karar verdiğini okuyoruz.

## Hattın haritası

<figure class="fig">
  <div class="flow">
    <span class="node">İzle</span>
    <span class="arrow">→</span>
    <span class="node">Tetik</span>
    <span class="arrow">→</span>
    <span class="node">Doğrula</span>
    <span class="arrow">→</span>
    <span class="node">Eğit</span>
    <span class="arrow">→</span>
    <span class="node acc">Kapı</span>
  </div>
  <figcaption>Kapıdan geçen model canlıya alınır ve izlenir; döngü her ay döner.</figcaption>
</figure>

| Adım | Ne yapar | Bölüm |
|---|---|---|
| İzle | Bugünün girdilerinde kayma, geçen ayın etiketleriyle doğruluk | İzleme, Veri Kayması |
| Tetik | Doğruluk düştüyse ya da kayma büyükse yeniden eğitimi başlatır | Kavram Kayması |
| Doğrula | Eğitim penceresindeki hatalı satırların payına bakar | Veri Doğrulama |
| Eğit | Son iki ayla, sabit tohumla eğitir | Tekrarlanabilir Eğitim |
| Kapı | Yeni modeli güncel kümede canlı modelle karşılaştırır | Model Kaydı, ML İçin CI |

## Parçalar

Önceki bölümlerin parçalarını kısaltarak bir araya getirelim: doğrulama
kuralları, eğitim, doğruluk ve PSI. Hattın durumu (canlı model, onun
eğitildiği veri, sürümü ve kapıdaki skoru) bir sözlükte duruyor:

```python
import bisect
import math
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC

LIMITS = {"tenure": (1, 72), "monthly_fee": (5, 100),
          "support_calls": (0, 10), "usage_hours": (0, 100)}


def valid(row):
    if row["plan"] not in ("basic", "pro"):
        return False
    return all(low <= row[c] <= high for c, (low, high) in LIMITS.items())


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


def train(rows):
    model = make_pipeline(StandardScaler(), LogisticRegression())
    return model.fit([features(r) for r in rows], [r["churned"] for r in rows])


def accuracy(model, rows):
    score = model.score([features(r) for r in rows], [r["churned"] for r in rows])
    return round(score, 3)


def psi(reference, current, bins=10):
    ordered = sorted(reference)
    edges = [ordered[len(ordered) * i // bins] for i in range(1, bins)]

    def shares(values):
        counts = [0] * bins
        for v in values:
            counts[bisect.bisect_left(edges, v)] += 1
        return [max(c / len(values), 0.0001) for c in counts]

    ref, cur = shares(reference), shares(current)
    return sum((c - r) * math.log(c / r) for r, c in zip(ref, cur))


def column(rows, name):
    return [r[name] for r in rows]


def drift(reference, current):
    values = [psi(column(reference, n), column(current, n)) for n in NUMERIC]
    return round(max(values), 3)


first = make_customers(2000)
model = train(first)
state = {"model": model, "reference": first, "version": 1,
         "base": accuracy(model, make_customers(1000, seed=99))}
print("v1 accuracy:", state["base"])
```

```text
v1 accuracy: 0.813
```

`drift` bütün sayısal sütunların PSI'sini hesaplayıp en büyüğünü veriyor:
bir sütunun kayması tetik için yeter. `base`, canlı modelin kapıdan
geçerken aldığı skor; izlemede doğruluk buna göre karşılaştırılıyor.

## Aylık adım

Hattın her ay yaptığı iş tek bir fonksiyon. Eşikler en başta, adlarıyla
duruyor; tasarım belgesindeki sayılar bunlar:

```python
MAX_DROP, MAX_DRIFT, MAX_INVALID, MIN_GAIN = 0.05, 0.25, 0.05, 0.003
BROKEN = {5}


def run_month(month, state):
    today = make_customers(1000, seed=5, month=month)
    holdout = make_customers(1000, seed=99, month=month - 1)
    moved = drift(state["reference"], today)
    live = accuracy(state["model"], holdout)
    report = f"month {month}: drift {moved:.3f} acc {live:.3f} ->"
    if live >= state["base"] - MAX_DROP and moved <= MAX_DRIFT:
        return f"{report} keep"
    older = make_customers(500, seed=7, month=max(month - 2, 0))
    window = older + make_customers(500, seed=7, month=month - 1)
    if month in BROKEN:
        for row in window:
            row["monthly_fee"] = round(row["monthly_fee"] * 100)
    invalid = sum(not valid(r) for r in window) / len(window)
    if invalid > MAX_INVALID:
        return f"{report} data rejected ({invalid:.0%} invalid)"
    candidate = train(window)
    score = accuracy(candidate, holdout)
    if score < live + MIN_GAIN:
        return f"{report} candidate kept out ({score:.3f})"
    state.update(model=candidate, reference=window, base=score)
    state["version"] += 1
    return f"{report} v{state['version']} promoted ({score:.3f})"
```

Adımlar haritadaki sırayla:

- **İzle:** `today` bu ayın girdileri (etiketsiz), `holdout` geçen ayın
  etiketi gelmiş müşterileri. Kayma bugüne, doğruluk geçen aya bakıyor;
  etiket gecikmesi bu.
- **Tetik:** doğruluk `base`'ten `MAX_DROP` kadar düşmediyse ve kayma
  `MAX_DRIFT`'i aşmadıysa hiçbir şey yapılmaz.
- **Doğrula:** eğitim penceresi son iki ay (Kavram Kayması). `BROKEN`,
  veri kaynağının 5. ayda ücretleri kuruşa çevirdiğini **taklit ediyor**
  (Veri Doğrulama bölümündeki hata).
- **Eğit** ve **Kapı:** aday, canlı modelle **aynı güncel kümede**
  ölçülüyor ve en az `MIN_GAIN` kadar iyi değilse dışarıda kalıyor.

## Sekiz ay

```python
for month in range(1, 8):
    print(run_month(month, state))
print("live model: v" + str(state["version"]))
```

```text
month 1: drift 0.070 acc 0.813 -> keep
month 2: drift 0.185 acc 0.820 -> keep
month 3: drift 0.578 acc 0.778 -> v2 promoted (0.782)
month 4: drift 0.326 acc 0.787 -> candidate kept out (0.784)
month 5: drift 0.575 acc 0.691 -> data rejected (100% invalid)
month 6: drift 0.922 acc 0.697 -> v3 promoted (0.837)
month 7: drift 0.127 acc 0.821 -> keep
live model: v3
```

Her satır bir kararı anlatıyor:

| Ay | Ne oldu | Neden |
|---|---|---|
| 1–2 | Model yerinde kaldı | Kayma küçük, doğruluk yerinde |
| 3 | v2 geçti | Kayma 0,578; aday canlı modelden biraz iyi |
| 4 | Aday dışarıda kaldı | Kayma yine büyük ama aday canlı modelden iyi değil |
| 5 | Veri reddedildi | Doğruluk 0,691'e düştü, ama pencerenin tamamı geçersiz |
| 6 | v3 geçti | Temiz veriyle eğitilen aday 0,837 |
| 7 | Model yerinde kaldı | Yeni referansa göre kayma küçük |

Dikkat edilecek üç şey var. 4. ayda kayma eşiği yeniden eğitimi
tetikledi ama **kapı** gereksiz bir model değişikliğini durdurdu: kayma
tek başına model değiştirmez. 5. ayda hat en çok ihtiyaç duyduğu anda
model **değiştiremedi**. Doğrulama olmasaydı ne olurdu? Bozuk veriyle
eğitilen aday, aynı bozuk kaynaktan gelen bir kümede 0,784
alır ve kapıdan geçerdi; kaynak düzeltildiği gün temiz veride
0,673 doğruluğa düşerdi. Kapı tek başına yetmez: kapının
kümesi de aynı bozuk kaynaktan gelebilir. Reddin bedeli ise müşterilerin
bir ay daha eski modelle karşılaşması; doğrulama bu yüzden aynı zamanda
bir **uyarı** göndermeli, veri kaynağını düzelten biri olmalı. 6. ayda
temiz veriyle model toparlandı.

## Her ay çalıştırmak

Hat bir betik (`pipeline.py`) olunca onu her ay çalıştırmak bir iş
akışıdır. Testler önce koşar; hattın raporu, sonuç ne olursa olsun
saklanır:

```yaml
name: Monthly model

on:
  schedule:
    - cron: "0 3 1 * *"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q

  retrain:
    needs: test
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python pipeline.py
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: pipeline-report
          path: report.txt
```

`"0 3 1 * *"` her ayın 1'inde 03:00 (UTC) demek. `workflow_dispatch`
hattı elle de başlatmayı sağlar: kalite uyarısı çaldığında takvimi
beklemeden (Kavram Kayması'ndaki "ikisi birden").

## Modülün haritası

| Bölüm | Hattaki yeri |
|---|---|
| Tekrarlanabilir Eğitim | `train`: aynı veri, aynı model |
| Veri Doğrulama | `valid` ve `MAX_INVALID` |
| Veri ve Model Sürümleme, Deney Takibi | Gerçek hatta pencerenin özeti ve adayın ölçümleri kaydedilir (burada kısaltıldı) |
| Model Kaydı | `state`: sürüm, canlı model, kapı skoru |
| ML İçin CI | Testler ve kapı iş akışında |
| Model Sunma, Ölçeklenme | Canlı modelin her gece toplu skorlaması |
| Eğitim-Sunma Farkı | Aynı `features` hem eğitimde hem sunmada |
| İzleme, Veri Kayması | `drift` ve `holdout` doğruluğu |
| Kavram Kayması | Son pencere, güncel kapı kümesi |
| A/B Testi, Gölge ve Kanarya | Geçen modelin canlıya adım adım alınması |
| ML Sistem Tasarımı | Eşikler ve yedek plan |

## Özet

- Hat her ay şu sırayla döner: izle, tetikle, doğrula, eğit, kapıdan geçir.
- Eşikler (`MAX_DROP`, `MAX_DRIFT`, `MAX_INVALID`, `MIN_GAIN`) adlarıyla
  yazılır; tasarım belgesindeki kararlardır.
- Dersteki sekiz ay: 3. ayda v2, 4. ayda aday dışarıda, 5. ayda bozuk veri
  reddedildi, 6. ayda v3.
- Kayma tek başına model değiştirmez; kararı kapı verir.
- Doğrulama bozuk veriyi durdurur ama modeli eski bırakır; ret bir uyarı
  da göndermeli. Kapı tek başına yetmez: kapının kümesi de bozuk olabilir.
- Hat bir iş akışıyla her ay ve elle çalıştırılır; rapor her durumda
  saklanır.
