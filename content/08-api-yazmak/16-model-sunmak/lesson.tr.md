# Bir ML Modelini Sunmak

Makine Öğrenmesi patikasında modeller eğittin ve `predict` ile tahmin
aldın; ama o model yalnızca senin not defterinde çalışıyordu. Bir uygulama
ya da web sitesi onu kullanmak istese ne yapacak? Cevap bu patikanın
tamamı: modeli bir **API'nin arkasına** koymak. İstemci ölçümleri gönderir,
API tahmini döndürür.

Bu bölümde scikit-learn'ün içinde gelen **iris** verisiyle (çiçeklerin
çanak ve taç yaprak ölçüleri → üç tür) bir modeli sunuyorsun.

## İki ayrı iş: eğitmek ve sunmak

| | Eğitim | Sunum |
|---|---|---|
| Ne zaman? | Bir kez, ara sıra | Sürekli, her istekte |
| Ne yapar? | Veriden model çıkarır | Hazır modelle tahmin eder |
| Süre | Saniyeler, saatler | Milisaniyeler |

Eğitim ayrı bir betikte yapılır ve model **dosyaya** kaydedilir:

```python
# train.py
import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

iris = load_iris()
model = LogisticRegression(max_iter=1000).fit(iris.data, iris.target)
joblib.dump(model, "model.joblib")
```

`joblib.dump` modeli olduğu gibi diske yazıyor (bu model 991 bayt); 
`joblib.load` geri okuyor (ölçtük: 0,001 sn). API eğitmez, yalnızca yükler.

## Modeli bir kez yüklemek

Async bölümündeki `lifespan` tam bunun için:

```python
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI

ml = {}


@asynccontextmanager
async def lifespan(app):
    ml["model"] = joblib.load("model.joblib")
    yield
    ml.clear()


app = FastAPI(lifespan=lifespan)
```

Model her istekte değil, sunucu açılırken bir kez yükleniyor. Büyük
modellerde (yüzlerce MB) fark çok büyük.

## Girdiyi doğrulamak

Model yanlış girdiyle hata vermez, **saçma** bir tahmin verir. Bu yüzden
kapıdaki denetim modelin değil API'nin işi:

```python
from pydantic import BaseModel, Field


class Flower(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)
```

Eksik ölçü ya da eksi uzunluk modele hiç ulaşmıyor (`422`).

## Tahmin uç noktası

```python
SPECIES = ["setosa", "versicolor", "virginica"]


@app.post("/predict")
def predict(flower: Flower):
    row = [[flower.sepal_length, flower.sepal_width,
            flower.petal_length, flower.petal_width]]
    label = int(ml["model"].predict(row)[0])
    proba = ml["model"].predict_proba(row)[0]
    return {"species": SPECIES[label],
            "probability": round(float(proba[label]), 3)}
```

- `row` iki boyutlu: **bir satırlık** tablo. scikit-learn tek örneği de
  tablo olarak ister (ML patikasından hatırla: `Expected 2D array`).
- Sütun sırası eğitimdekiyle **aynı** olmalı; model sütun adlarını değil
  sırasını bilir.
- `int(...)` ve `float(...)`: aşağıda neden.

Ölçtük:

```text
POST /predict  5.1, 3.5, 1.4, 0.2   200 {"species": "setosa", "probability": 0.982}
POST /predict  6.7, 3.0, 5.2, 2.3   200 {"species": "virginica", "probability": 0.92}
POST /predict  5.9, 3.0, 4.2, 1.5   200 {"species": "versicolor", "probability": 0.899}
POST /predict  sepal_length: -1     422 greater_than
POST /predict  petal_width yok      422 missing
```

<figure class="fig">
  <div class="flow">
    <span class="node">POST /predict<br><small>4 ölçü</small></span><span class="arrow">→</span>
    <span class="node acc">Flower<br><small>doğrulama</small></span><span class="arrow">→</span>
    <span class="node">model.predict([[...]])<br><small>lifespan'da yüklendi</small></span><span class="arrow">→</span>
    <span class="node ok">{"species": "setosa"}<br><small>int(), float()</small></span>
  </div>
  <figcaption>Kapıda doğrulama, ortada bir kez yüklenmiş model, çıkışta NumPy değerlerinin Python'a çevrilmesi.</figcaption>
</figure>

## NumPy tuzağı

`predict` NumPy dizisi döndürüyor; içindeki değer Python'un `int`'i değil
NumPy'nin `int64`'ü. Onu doğrudan cevaba koyduk:

```python
return {"label": ml["model"].predict(row)[0]}
```

```text
POST /predict   500 Internal Server Error
```

FastAPI NumPy sayısını JSON'a çeviremedi (ölçtük). Çözüm: cevaba
koymadan önce `int(...)`, `float(...)`, listeler için `.tolist()`.
Modelden gelen **her** değeri böyle çevir.

## Birden fazla tahmin

```python
@app.post("/predict/batch")
def predict_batch(flowers: list[Flower]):
    rows = [[f.sepal_length, f.sepal_width, f.petal_length, f.petal_width]
            for f in flowers]
    labels = ml["model"].predict(rows)
    return [SPECIES[int(i)] for i in labels]
```

Gövde bir liste; model hepsini tek seferde tahmin ediyor (her biri için ayrı
istekten çok daha hızlı). Ölçtük: iki çiçek → `["setosa", "virginica"]`.

## Modelin kimliği

İstemci hangi modelle konuştuğunu bilmeli; yeni model yüklenince
cevaplar değişebilir:

```python
@app.get("/model")
def model_info():
    model = ml["model"]
    return {"type": type(model).__name__, "classes": SPECIES,
            "features": int(model.n_features_in_)}
```

```text
GET /model  200 {"type": "LogisticRegression", "classes": [...], "features": 4}
```

Gerçek projelerde buraya modelin sürümü, eğitildiği tarih ve doğrulama
puanı da yazılır.

## Docker'a giden yol

Bu API'yi başka bir bilgisayarda çalıştırmak için Docker patikasında
gördüğün yol: `main.py` + `model.joblib` + `requirements.txt` bir imaja
konur, `uvicorn main:app --host 0.0.0.0` ile başlatılır. API Yazmak modülünün sonu,
modelini dünyaya açmanın başı.

## Özet

- Eğitim ayrı (`joblib.dump`), sunum ayrı (`joblib.load`, `lifespan`'da
  bir kez).
- Girdi Pydantic ile doğrulanır; model saçma girdiye hata vermez.
- `predict` iki boyutlu girdi ister; sütun sırası eğitimdekiyle aynı.
- NumPy değerleri `int()` / `float()` / `.tolist()` ile çevrilir; yoksa
  `500`.
- Toplu tahmin tek çağrıda; `/model` hangi modelin çalıştığını söyler.
