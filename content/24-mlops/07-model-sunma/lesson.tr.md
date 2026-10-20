# Modeli Paketlemek ve Sunmak

Model kayıtta, kapıdan geçti, `production` etiketini aldı. Ama bir
dosya olarak diskte durduğu sürece kimseye faydası yok. **Sunmak**
(serving), modelin tahminlerini onları kullanacak kişiye ya da programa
ulaştırmak demek. FastAPI ile REST API Yazmak modülünde bir modeli API
olarak sunmayı gördün; bu bölümde işin MLOps tarafına bakıyoruz: kayıttaki
dosyayı güvenle yüklemek, tahmini toplu mu anlık mı yapacağına karar
vermek, cevaba model sürümünü koymak, hızı doğru ölçmek ve hepsini bir
imaja paketlemek.

## Kaydedilmiş model

Önce sunacağımız modeli hazırlayalım: eğitip dosyaya yazalım, yanına da
kayıttaki bilgisini (ad, sürüm, özet) koyalım:

```python
import hashlib
import json
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from ml_data import make_customers, NUMERIC


def features(row):
    return [row[c] for c in NUMERIC] + [1 if row["plan"] == "pro" else 0]


rows = make_customers(2000)
model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=0)
model.fit([features(r) for r in rows], [r["churned"] for r in rows])
data = pickle.dumps(model)
Path("model.pkl").write_bytes(data)
digest = hashlib.sha256(data).hexdigest()
card = {"name": "churn", "version": 3, "sha256": digest}
Path("model.json").write_text(json.dumps(card), encoding="utf-8")
print("model file:", len(data), "bytes")
```

```text
model file: 1966988 bytes
```

Yaklaşık 2 MB'lık bir dosya. Sunan program bunu açıp 100 ağacı belleğe
yeniden kurmak zorunda.

## Bir kez yükle

En sık yapılan hata, modeli **her istekte** yeniden yüklemek. Kaç kez
yüklendiğini sayan bir sayaçla bakalım:

```python
loads = {"count": 0}


def load_model():
    loads["count"] += 1
    return pickle.loads(Path("model.pkl").read_bytes())


requests = make_customers(100, seed=5)
for row in requests:
    load_model().predict_proba([features(row)])
print("loads for 100 requests, reloading:", loads["count"])

loads["count"] = 0
loaded = load_model()
for row in requests:
    loaded.predict_proba([features(row)])
print("loads for 100 requests, loaded once:", loads["count"])
```

```text
loads for 100 requests, reloading: 100
loads for 100 requests, loaded once: 1
```

İlk yolda her istek diski okuyor ve 100 ağacı baştan kuruyor; ikinci
yolda bu iş bir kez, program açılırken yapılıyor. Model büyüdükçe fark
da büyür: yüz megabaytlık bir model her istekte yüklenirse istek
saniyeler sürer. Kural: model program **açılırken** bir kez yüklenir,
istekler bellekteki aynı nesneyi kullanır.

## Toplu mu, anlık mı?

Tahmin iki biçimde istenir:

- **Toplu tahmin** (batch prediction): belli aralıklarla (her gece gibi)
  bütün müşteriler bir kerede puanlanır, sonuçlar bir tabloya yazılır.
  Müşteri ekibi sabah listeye bakıp kimi arayacağına karar verir.
- **Anlık tahmin** (online prediction): bir istek gelir, cevap hemen
  döner. Müşteri iptal sayfasını açtığı anda ona bir teklif göstermek
  gibi.

İhtiyaç beklemeye izin veriyorsa toplu tahmin hem daha basit hem daha
ucuz. Model, satırları tek tek değil bir arada işlerken çok daha
hızlı:

```python
import time

batch = [features(r) for r in make_customers(1000, seed=6)]
start = time.perf_counter()
loaded.predict_proba(batch)
per_row_batch = (time.perf_counter() - start) / len(batch)
start = time.perf_counter()
for x in batch[:50]:
    loaded.predict_proba([x])
per_row_single = (time.perf_counter() - start) / 50
faster = per_row_batch * 10 < per_row_single
print("batch is at least 10x faster per customer:", faster)
```

```text
batch is at least 10x faster per customer: True
```

Süreler her bilgisayarda farklıdır; bu yüzden süreyi değil karşılaştırmayı
yazdırdık. Bir tahmin çağrısının sabit bir hazırlık maliyeti var; toplu
çağrıda bu maliyet 1000 müşteriye bölünüyor.

## Toplu puanlama işi

Toplu tahmin çoğu zaman küçük bir betiktir: dosyayı oku, puanla, sonucu
yaz. CSV'den okunan değerler metin olduğu için `from_csv` onları sayıya
çeviriyor. Sonuç dosyasına **model sürümünü** de yazmak önemli: üç ay sonra
"bu müşteriyi neden aramışız?" diye sorulduğunda hangi modelin karar
verdiği bilinmeli.

```python
import csv
from ml_data import write_customers_csv

write_customers_csv("customers.csv", 1000, seed=6)
with open("customers.csv", encoding="utf-8") as f:
    customers = list(csv.DictReader(f))


def from_csv(r):
    return [float(r[c]) for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


X = [from_csv(r) for r in customers]
probabilities = loaded.predict_proba(X)[:, 1]
with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["id", "churn_probability", "model_version"])
    for row, p in zip(customers, probabilities):
        writer.writerow([row["id"], round(float(p), 3), card["version"]])
for line in Path("scores.csv").read_text(encoding="utf-8").splitlines()[:4]:
    print(line)
print("customers to call:", int((probabilities >= 0.5).sum()))
```

```text
id,churn_probability,model_version
C00-00001,0.035,3
C00-00002,0.091,3
C00-00003,0.009,3
customers to call: 226
```

## Anlık tahmin: API

Anlık tahmin için bir API kuralım. FastAPI ile REST API Yazmak
modülündeki yapının aynısı; MLOps açısından üç şey ekleniyor:

1. Model **açılışta** yükleniyor (`lifespan`) ve dosyanın özeti
   kayıttakiyle karşılaştırılıyor: tutmazsa program hiç başlamıyor.
2. Girdi, Veri Doğrulama bölümündeki kurallarla denetleniyor; kurala
   uymayan istek sessizce yanlış bir tahmin değil, açık bir `422` alıyor.
3. Her cevapta ve sağlık uç noktasında **model sürümü** var.

```python
from contextlib import asynccontextmanager
from typing import Literal
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

state = {}


@asynccontextmanager
async def lifespan(app):
    info = json.loads(Path("model.json").read_text(encoding="utf-8"))
    data = Path("model.pkl").read_bytes()
    if hashlib.sha256(data).hexdigest() != info["sha256"]:
        raise RuntimeError("model.pkl does not match model.json")
    state["model"], state["version"] = pickle.loads(data), info["version"]
    yield
    state.clear()


app = FastAPI(lifespan=lifespan)


class Customer(BaseModel):
    tenure: int = Field(ge=1, le=72)
    monthly_fee: float = Field(ge=5, le=100)
    support_calls: int = Field(ge=0, le=10)
    usage_hours: float = Field(ge=0, le=100)
    plan: Literal["basic", "pro"]


@app.get("/health")
def health():
    return {"status": "ok", "model_version": state["version"]}


@app.post("/predict")
def predict(customer: Customer):
    row = customer.model_dump()
    probability = float(state["model"].predict_proba([features(row)])[0, 1])
    return {"churn_probability": round(probability, 3),
            "model_version": state["version"]}


good = {"tenure": 2, "monthly_fee": 45.0, "support_calls": 6,
        "usage_hours": 5.0, "plan": "pro"}
with TestClient(app) as client:
    print(client.get("/health").json())
    print(client.post("/predict", json=good).json())
    print(client.post("/predict", json={**good, "plan": "PRO"}).status_code)
```

```text
{'status': 'ok', 'model_version': 3}
{'churn_probability': 0.901, 'model_version': 3}
422
```

`Literal["basic", "pro"]` alanın yalnızca bu iki değerden birini
alabileceğini söylüyor; `"PRO"` bu yüzden `422` aldı. `model_dump()`
Pydantic nesnesini sözlüğe çeviriyor, böylece eğitimdeki `features`
fonksiyonunun **aynısı** kullanılıyor. Eğitimle sunmanın aynı kodu
kullanması çok önemli; bir sonraki bölümün konusu tam olarak bu.

`with TestClient(app) as client:` bloğu `lifespan`'ı da çalıştırıyor:
model blok başlarken yükleniyor.

## Hızı doğru ölçmek

Bir API'nin hızı **gecikmeyle** (latency) ölçülür: bir isteğin cevabı ne
kadar sürede geliyor. Gecikmenin ortalaması yanıltıcıdır. Yirmi isteğin
süresine bakalım; ikisi yavaş:

```python
import math


def percentile(values, p):
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


latencies_ms = [12, 15, 11, 14, 13, 90, 12, 16, 13, 14,
                12, 15, 13, 11, 14, 12, 13, 15, 14, 250]
print("average:", sum(latencies_ms) / len(latencies_ms))
print("p50:", percentile(latencies_ms, 50))
print("p95:", percentile(latencies_ms, 95))
```

```text
average: 28.95
p50: 13
p95: 90
```

Ortalama 28,95 ms: hiçbir isteğin gerçekten yaşamadığı bir sayı.
Bunun yerine **yüzdelik** (percentile) kullanılır:

- **p50** (ortanca): isteklerin yarısı bundan hızlı. Tipik kullanıcının
  gördüğü.
- **p95**: isteklerin yüzde 95'i bundan hızlı. Yavaş günü yaşayan
  kullanıcının gördüğü.

Hız sözü çoğu zaman p95 ya da p99 üzerinden verilir: "isteklerin yüzde
95'i 100 ms'nin altında". `math.ceil` sayıyı yukarı yuvarlıyor;
`rank` sıralanmış listede kaçıncı elemana bakılacağı.

## Bir imaja paketlemek

Docker patikasında bir Python uygulamasını imaja koymayı gördün. Model
sunan bir uygulama için birkaç ek kural var:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py model.pkl model.json ./
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

- `requirements.txt`'teki sürümler **eğitimdekiyle aynı** ve `==` ile
  sabit. Bir sürümde kaydedilen model başka bir sürümde açılınca uyarı
  verebilir ya da farklı davranabilir (Makine Öğrenmesi Kütüphaneleri
  modülü).
- Model dosyası imajın içinde. İmajın etiketi model sürümünü taşır
  (`churn-api:3` gibi): hangi imajın hangi modeli sunduğu bellidir. Diğer
  yol, imajın açılışta modeli kayıttan `production` etiketiyle
  indirmesi; o zaman imaj değişmeden model değişebilir, ama açılış
  internete ve kayda bağımlı olur.
- Program açılırken modeli yüklediği için ilk istek gelmeden hazırdır.
  Sağlık uç noktası (`/health`) model sürümünü de söyler; dağıtımdan
  sonra doğru modelin canlıda olduğu tek bir istekle doğrulanır.

## Özet

- **Sunmak**, modelin tahminlerini kullanacak yere ulaştırmaktır.
- Model program açılırken **bir kez** yüklenir; her istekte yüklemek
  boşa iş ve yavaşlıktır.
- **Toplu tahmin** bekleyebilen işler için daha basit ve ucuzdur;
  **anlık tahmin** cevabın hemen gerektiği yerler içindir.
- Tahminin yanına her zaman **model sürümü** yazılır.
- API, girdiyi eğitimdeki kurallarla denetler ve eğitimdeki **aynı**
  özellik kodunu kullanır.
- Hız **yüzdeliklerle** (p50, p95) ölçülür; ortalama yavaş istekleri
  gizler.
- İmajda kütüphane sürümleri eğitimdekiyle aynıdır; imajın etiketi
  model sürümünü taşır.
