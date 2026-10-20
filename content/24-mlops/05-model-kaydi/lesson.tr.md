# Model Kaydı

Klasörde `model.pkl`, `model_yeni.pkl`, `model_final.pkl` ve
`model_final_gercek.pkl` var. Hangisi şu anda müşterilere tahmin veriyor?
Hangisi daha iyiydi? Yenisi kötü çıkarsa eskisine nasıl dönülür? Bu
soruların cevabı dosya adlarında değil, bir **model kaydında** (model
registry) durur. Bu bölümde küçük bir model kaydı kuruyoruz: her modelin
numaralı sürümleri, hangi sürümün canlıda olduğunu söyleyen etiketler ve
yeni bir sürümü canlıya almadan önce geçmesi gereken bir kapı.

## Değerlendirme kümesi

Sürümleri karşılaştırabilmek için hepsini **aynı** veride ölçmeliyiz.
Değişmeyen bir değerlendirme kümesi ayıralım ve modelleri eğitip bu
kümede ölçen bir fonksiyon yazalım:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X_hold, y_hold = to_xy(make_customers(1000, seed=99))


def train(kind, rows):
    if kind == "logistic":
        model = make_pipeline(StandardScaler(), LogisticRegression())
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=0)
    model.fit(*to_xy(rows))
    return model, round(model.score(X_hold, y_hold), 3)


model_1, accuracy_1 = train("logistic", make_customers(2000))
print("first model:", accuracy_1)
```

```text
first model: 0.813
```

## Kayıt: sürüm numaraları

Kayıt bir JSON dosyası olsun. Her model adının altında sürümlerin bir
listesi duruyor; her sürüm kendi numarasını, dosyasını, dosyasının
özetini, ölçümlerini ve kısa bir notu taşıyor:

```python
import hashlib
import json
import pickle
from pathlib import Path

REGISTRY = Path("registry.json")
MODELS = Path("models")


def read_registry():
    if not REGISTRY.exists():
        return {}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def write_registry(registry):
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def register(name, model, metrics, note):
    registry = read_registry()
    empty = {"versions": [], "aliases": {}, "history": []}
    entry = registry.setdefault(name, empty)
    version = len(entry["versions"]) + 1
    data = pickle.dumps(model)
    MODELS.mkdir(exist_ok=True)
    path = MODELS / f"{name}-v{version}.pkl"
    path.write_bytes(data)
    entry["versions"].append({"version": version, "file": path.as_posix(),
                              "sha256": hashlib.sha256(data).hexdigest(),
                              "metrics": metrics, "note": note})
    write_registry(registry)
    return version


v1 = register("churn", model_1, {"accuracy": accuracy_1}, "logistic")
print("registered version:", v1)
for key, value in read_registry()["churn"]["versions"][0].items():
    print(f"{key:>8}: {value}")
```

```text
registered version: 1
 version: 1
    file: models/churn-v1.pkl
  sha256: 5d94979f5608ab49cfc694e7530a88737ea8c2acbe5c070ef20e499578ba1b16
 metrics: {'accuracy': 0.813}
    note: logistic
```

Birkaç ayrıntı:

- `setdefault` model adı kayıtta yoksa boş bir girdi açıyor, varsa
  olanı veriyor. İlk sürüm böylece kendiliğinden doğuyor.
- Sürüm numarası artıyor ve **hiç tekrar kullanılmıyor**. "Sürüm 3"
  dendiğinde herkes aynı dosyayı anlar.
- Dosyanın özeti kayıtta: Veri ve Model Sürümleme bölümündeki gibi,
  dosya sonradan değişirse anlaşılır.
- `as_posix()` yolu `/` ile yazıyor; kayıt her işletim sisteminde aynı
  görünsün diye.

## Etiketler: hangi sürüm canlıda?

Sürüm numaraları değişmez; ama "canlıdaki model" değişir. Bunu bir
**etiketle** (alias) söyleriz: `production` etiketi hangi sürümü
gösteriyorsa canlıdaki model odur. Tahmin yapan kod sürüm numarası
bilmez, yalnızca etiketi sorar:

```python
def set_alias(name, alias, version):
    registry = read_registry()
    entry = registry[name]
    entry["aliases"][alias] = version
    entry["history"].append([alias, version])
    write_registry(registry)


def load_model(name, alias):
    entry = read_registry()[name]
    version = entry["aliases"][alias]
    info = entry["versions"][version - 1]
    data = Path(info["file"]).read_bytes()
    if hashlib.sha256(data).hexdigest() != info["sha256"]:
        raise ValueError(f"{info['file']} does not match the registry")
    return version, pickle.loads(data)


set_alias("churn", "production", 1)
version, model = load_model("churn", "production")
print("production is version", version)
print("first predictions:", model.predict(X_hold[:5]).tolist())
```

```text
production is version 1
first predictions: [0, 0, 0, 0, 0]
```

Bunun güzelliği şu: canlıdaki modeli değiştirmek için tahmin kodunu
değiştirmeye, yeniden yayınlamaya gerek yok. Etiketi başka sürüme
çevirmek yetiyor. Her etiket değişikliği de `history` listesine
yazılıyor: hangi sürüm ne zaman canlıya alındı, sırasıyla belli.

`load_model` dosyayı açmadan önce özetini kayıttakiyle karşılaştırıyor:
kayıtta olmayan bir dosya canlıya giremez.

## Kapı: kim canlıya geçer?

Yeni bir sürüm kaydedildi diye canlıya geçmemeli. Önce canlıdakinden
**daha iyi** olduğunu aynı değerlendirme kümesinde göstermeli. Bunu bir
kural olarak yazalım: aday, canlıdakini en az `min_gain` kadar geçerse
etiket ona taşınsın.

```python
def should_promote(candidate, current, min_gain=0.003):
    gain = candidate["accuracy"] - current["accuracy"]
    return gain >= min_gain, round(gain, 3)


def try_promote(name, version):
    entry = read_registry()[name]
    current = entry["versions"][entry["aliases"]["production"] - 1]
    candidate = entry["versions"][version - 1]
    ok, gain = should_promote(candidate["metrics"], current["metrics"])
    if ok:
        set_alias(name, "production", version)
    result = "promoted" if ok else "kept out"
    print(f"version {version}: gain {gain:+.3f} -> {result}")


model_2, accuracy_2 = train("forest", make_customers(2000))
v2 = register("churn", model_2, {"accuracy": accuracy_2}, "forest")
try_promote("churn", v2)
model_3, accuracy_3 = train("logistic", make_customers(5000))
v3 = register("churn", model_3, {"accuracy": accuracy_3}, "more data")
try_promote("churn", v3)
print("production is version", read_registry()["churn"]["aliases"]["production"])
```

```text
version 2: gain -0.027 -> kept out
version 3: gain +0.005 -> promoted
production is version 3
```

Sürüm 2 (sınırları olmayan bir rastgele orman) canlıdakinden kötü
çıktı ve dışarıda kaldı. Kayıtta yine de duruyor: neyin denendiği ve
neden geçmediği bilgisi kaybolmuyor. Sürüm 3 (aynı model, daha çok
veriyle) canlıdakini geçti ve etiket ona taşındı.

`min_gain` neden var? Deney Takibi bölümünde gördüğün gibi, tek bir
kümede ölçülen küçük farkların bir kısmı şanstır. Çok küçük bir
üstünlük için canlıdaki modeli değiştirmek, hiçbir şey kazanmadan risk
almak olabilir. Eşiğin ne olacağı alana göre seçilir; burada 0,003, yani
1000 müşteride 3 doğru tahmin.

## Geri dönüş

Sürüm 3 canlıya çıktı. Ertesi gün veriyi hazırlayan ekip haber veriyor:
5000 müşterilik verinin bir kısmı hatalı işlenmiş. Ne yapacağız? Yeni
model eğitmek saatler sürebilir. Ama eski sürüm kayıtta duruyor:

```python
set_alias("churn", "production", 1)
entry = read_registry()["churn"]
print("production is version", entry["aliases"]["production"])
for alias, version in entry["history"]:
    print(f"{alias} -> version {version}")
```

```text
production is version 1
production -> version 1
production -> version 3
production -> version 1
```

**Geri dönüş** (rollback) bir etiketi eski sürüme çevirmek kadar kısa
sürdü. Bu, CI/CD ve DevOps modülündeki dağıtım stratejileriyle aynı fikir:
eski sürüm hazırda bekliyorsa hata ucuz olur. Bunun tek şartı, eski
sürümlerin dosyalarının **silinmemesi**.

## Model kartı

Kayıt makinenin okuduğu bilgiyi tutuyor: sürüm, dosya, ölçüm. Bir de
insanın okuyacağı bir açıklama gerekir: **model kartı** (model card).
Kısa bir belge; modelin ne işe yaradığını, neyle eğitildiğini, nasıl
ölçüldüğünü ve **nerede kullanılmaması** gerektiğini söyler:

- **Ne yapar:** aboneliğini iptal edecek müşterileri tahmin eder.
- **Kim kullanır:** müşteri ekibi, kimi arayacağına karar verirken.
- **Veri:** hangi sürüm, kaç müşteri, hangi aylar.
- **Ölçüm:** değerlendirme kümesinde doğruluk, temel çizgiyle birlikte.
- **Sınırlar:** yalnızca bu hizmetin müşterileri için; fiyatlar büyük
  ölçüde değişirse güvenilmez.

Sınırlar bölümü en çok atlanan ve en önemli bölüm. Model, eğitildiği
dünyanın dışında sessizce yanlış çalışır; kart bunu baştan söyler.

## Gerçek araçlar

**MLflow**'un model kaydı bu bölümde yazdığımızın aynısını yapıyor:
bir modeli adıyla kaydedince sürüm numarası veriyor, sürümlere
`production` gibi etiketler (alias) takılabiliyor ve tahmin kodu modeli
`models:/churn@production` adresiyle yüklüyor. Etiketi başka sürüme
çevirmek canlıdaki modeli değiştiriyor.

## Özet

- **Model kaydı**, her modelin numaralı sürümlerini, dosyalarının
  özetini, ölçümlerini ve notlarını tek yerde tutar.
- Sürüm numaraları **değişmez** ve tekrar kullanılmaz.
- **Etiket** (alias) hangi sürümün canlıda olduğunu söyler; tahmin kodu
  sürüm numarasını değil etiketi sorar.
- Yeni sürüm canlıya bir **kapıdan** geçerek gelir: aynı değerlendirme
  kümesinde canlıdakini en az bir eşik kadar geçmeli.
- Geçemeyen sürüm de kayıtta kalır.
- **Geri dönüş**, etiketi eski sürüme çevirmektir; eski dosyalar
  silinmez.
- **Model kartı** modelin ne yaptığını, verisini, ölçümünü ve
  sınırlarını insanın okuyacağı biçimde yazar.
