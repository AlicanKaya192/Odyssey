# Deney Takibi

İyi bir model bulmak için onlarca şey denersin: başka bir algoritma,
başka bir ayar, bir sütun eklemek, bir sütun çıkarmak. Bir hafta sonra
biri soruyor: "0,83'ü hangi ayarla almıştın?" Cevap bir defterin
köşesinde, silinmiş bir hücrede ya da hiçbir yerde. Bu bölümde her
denemeyi kendiliğinden kaydeden küçük bir **deney takip** (experiment
tracking) aracı yazıyoruz ve kayıtlara bakarak doğru modeli seçmeyi
öğreniyoruz.

## Üç küme

Deney yaparken veriyi üçe böleriz. Bunu Makine Öğrenmesi patikasından
hatırlıyorsun, ama burada neden üç olduğu daha da önemli:

- **Eğitim** (train): modeller bununla eğitilir.
- **Doğrulama** (validation): deneyler bununla karşılaştırılır.
- **Test**: yalnızca en sonda, seçilen model için **bir kez** kullanılır.

```python
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(3000))
X_train, X_rest, y_train, y_rest = train_test_split(
    X, y, test_size=0.4, random_state=0)
X_val, X_test, y_val, y_test = train_test_split(
    X_rest, y_rest, test_size=0.5, random_state=0)
print("train:", len(X_train), "validation:", len(X_val), "test:", len(X_test))
```

```text
train: 1800 validation: 600 test: 600
```

Önce yüzde 40'ı ayırdık, sonra onu ikiye böldük: doğrulama ve test
600'er müşteri.

## Kayıt defteri: bir dosya, her satır bir deney

Kaydı bir dosyada tutalım. Her deney dosyaya **bir satır** olarak
eklensin; satır, o deneyin JSON'u. Bu biçime **JSON Lines** (dosya adı
çoğu zaman `.jsonl`) denir. İki iyi yanı var: yeni deney eklemek için
dosyanın sonuna bir satır yazmak yeter, eski satırlara hiç dokunulmaz;
okumak için de her satırı ayrı ayrı `json.loads` ile açarız.

```python
import json
from pathlib import Path

LOG = Path("runs.jsonl")


def log_run(params, metrics):
    run_id = len(load_runs()) + 1
    record = {"run": run_id, "params": params, "metrics": metrics}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return run_id


def load_runs():
    if not LOG.exists():
        return []
    lines = LOG.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines]


stays = 1 - sum(y_val) / len(y_val)
log_run({"model": "baseline"}, {"val_accuracy": round(stays, 3)})
print(LOG.read_text(encoding="utf-8"))
```

```text
{"run": 1, "params": {"model": "baseline"}, "metrics": {"val_accuracy": 0.748}}
```

`open("a")` dosyayı **ekleme** (append) kipinde açıyor: yazılan satır
dosyanın sonuna gidiyor, eskiler silinmiyor. Her deneyin bir numarası
(`run`), ayarları (`params`) ve ölçümleri (`metrics`) var.

İlk kaydımız bir model bile değil: herkese "kalır" demenin doğruluğu.
Bu **temel çizgi** (baseline). Müşterilerin çoğu kaldığı için bu hiçbir
şey bilmeyen tahmin bile 0,748 doğruluk veriyor. Her modelin
önce bu sayıyı geçmesi gerekir; temel çizgi kayıtta durmazsa "0,80 iyi
mi?" sorusunun cevabı yok.

## Deneyleri çalıştırmak

Şimdi iki model ailesini birkaç ayarla deneyelim. Her deney kendiliğinden
kayda geçsin; elle not almak yok:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build(params):
    if params["model"] == "logistic":
        return make_pipeline(StandardScaler(), LogisticRegression(C=params["C"]))
    return RandomForestClassifier(n_estimators=100, max_depth=params["max_depth"],
                                  random_state=0)


experiments = [{"model": "logistic", "C": c} for c in [0.01, 0.1, 1, 10]]
experiments += [{"model": "forest", "max_depth": d} for d in [3, 5, 8, None]]
for params in experiments:
    model = build(params).fit(X_train, y_train)
    log_run(params, {"val_accuracy": round(model.score(X_val, y_val), 3)})
print("runs logged:", len(load_runs()))
```

```text
runs logged: 9
```

`build` ayarlardan modeli kuruyor: deneyin bütün tarifi `params`
sözlüğünde. Lojistik regresyonda `C` düzenlileştirmenin gücünü, ormanda
`max_depth` ağaçların en fazla kaç kat derinleşebileceğini belirliyor
(`None` sınırsız demek).

## Kayıtlara bakmak

Kayıt dosyası artık bir tablo gibi sorgulanabilir. Deneyleri doğrulama
doğruluğuna göre sıralayalım:

```python
def val_accuracy(run):
    return run["metrics"]["val_accuracy"]


runs = sorted(load_runs(), key=val_accuracy, reverse=True)
for r in runs:
    settings = ", ".join(f"{k}={v}" for k, v in r["params"].items())
    print(f'{r["run"]:>3}  {r["metrics"]["val_accuracy"]:.3f}  {settings}')
```

```text
  3  0.832  model=logistic, C=0.1
  5  0.830  model=logistic, C=10
  2  0.828  model=logistic, C=0.01
  4  0.828  model=logistic, C=1
  7  0.813  model=forest, max_depth=5
  8  0.803  model=forest, max_depth=8
  9  0.788  model=forest, max_depth=None
  6  0.785  model=forest, max_depth=3
  1  0.748  model=baseline
```

Tablodan okunanlar:

- Bütün modeller temel çizgiyi geçmiş; en kötü orman bile.
- Lojistik regresyon dört ayarda da birbirine çok yakın. `C`'yi
  değiştirmek burada pek bir şey katmıyor.
- Ormanda derinlik önemli: sınırsız derinlik (`None`) orta derinlikten
  kötü. Ağaçlar eğitim verisini ezberliyor.

`key=val_accuracy` sıralamaya her deneyin hangi sayısına bakacağını
söylüyor. `f'{r["run"]:>3}'` sayıyı üç karakterlik alanda sağa
yaslıyor; sütunlar bu yüzden hizalı.

## Seçim, sonra bir kez test

En iyi deneyi **doğrulamaya göre** seçelim, modeli yeniden eğitelim ve
test kümesinde bir kez ölçelim. Bu son ölçüm de kayda girsin:

```python
best = max(load_runs(), key=val_accuracy)
model = build(best["params"]).fit(X_train, y_train)
test_accuracy = round(model.score(X_test, y_test), 3)
log_run({**best["params"], "final": True},
        {"val_accuracy": best["metrics"]["val_accuracy"], "test_accuracy": test_accuracy})
print("chosen run:", best["run"], best["params"])
print("validation:", best["metrics"]["val_accuracy"], "test:", test_accuracy)
```

```text
chosen run: 3 {'model': 'logistic', 'C': 0.1}
validation: 0.832 test: 0.793
```

Raporlanacak sayı **test** sonucu: 0,793. Doğrulamadaki
0,832 daha yüksek, ve bu bir rastlantı değil. Farkın bir
kısmı bölmenin şansı (bu bölmede doğrulama kümesi biraz kolay çıkmış),
bir kısmı **seçimin kendisi**. Sekiz deneyin içinden doğrulamada en
yüksek olanı seçtik; şansı yaver gidenin seçilme olasılığı daha yüksek.

## Kazananın laneti

Seçimin etkisini ayrı ölçelim. Aynı modeli, aynı ayarlarla, yalnızca
tohumunu değiştirerek 20 kez eğitelim. Bu 20 model gerçekte eşit derecede
iyi; aralarındaki her fark şanstan geliyor:

```python
scores = []
for seed in range(20):
    model = RandomForestClassifier(n_estimators=20, random_state=seed)
    model.fit(X_train, y_train)
    scores.append((model.score(X_val, y_val), model.score(X_test, y_test)))
val_mean = sum(v for v, _ in scores) / len(scores)
test_mean = sum(t for _, t in scores) / len(scores)
best_val, its_test = max(scores)
val_lead, test_lead = best_val - val_mean, its_test - test_mean
print(f"validation: best {best_val:.3f}, lead {val_lead:+.3f}")
print(f"test: same run {its_test:.3f}, lead {test_lead:+.3f}")
```

```text
validation: best 0.818, lead +0.028
test: same run 0.757, lead +0.009
```

Doğrulamada en iyi model ortalamanın +0,028 önünde. Ama aynı
model testte ortalamanın yalnızca +0,009 önünde: seçtiğimiz
üstünlüğün çoğu, yeni veride kayboldu. Buna **kazananın laneti**
(winner's curse) denir: çok sayıda adayın en iyisi, ölçüldüğü veride
gerçekte olduğundan iyi görünür.

Deney takibinin önemli bir yararı da burada: kaç deney yaptığını
gösteriyor. Üç deneyin en iyisiyle iki yüz deneyin en iyisi aynı şey
değil; ne kadar çok deneme, doğrulama sonucu o kadar iyimser. Bu yüzden:

- Seçim **doğrulamayla**, rapor **testle** yapılır.
- Test kümesi seçim için kullanılmaz. Her deneyi teste de bakarak
  seçersen test de doğrulamaya dönüşür ve iyimser olur.
- Kayıt yalnızca kazananları değil **bütün** denemeleri tutar; kötü
  sonuçlar da bilgidir.

`max(scores)` demetleri ilk elemanlarına göre karşılaştırıyor: en
yüksek doğrulama skorlu demeti, testteki skoruyla birlikte veriyor.
`lead` (önde olma) seçilen modelin ortalamadan farkı; `:+.3f` farkı
işaretiyle yazıyor.

## Kayda başka ne girer?

Bu bölümdeki kayıt yalnızca ayarları ve ölçümleri tutuyor. Gerçek bir
projede her deneyin yanında önceki bölümlerdeki bilgiler de durur:

- Verinin parmak izi (Tekrarlanabilir Eğitim): hangi veriyle?
- Kodun sürümü: Git commit kimliği.
- Model dosyasının özeti (Veri ve Model Sürümleme): hangi model?
- Kısa bir not: "ücret sütununu çıkardım" gibi, neden denediğin.

**MLflow** gibi araçlar tam bunu yapıyor: `mlflow.log_param` ayarı,
`mlflow.log_metric` ölçümü kaydediyor, bir web arayüzü de deneyleri
tablo ve grafikle karşılaştırıyor. Fikir bu bölümde yazdığımızın aynısı.

## Özet

- Her deney **kendiliğinden** kayda geçmeli: ayarlar, ölçümler,
  numarası.
- **JSON Lines**: her satır bir deney; ekleme kipinde yazılır, eski
  satırlara dokunulmaz.
- Kayıtta bir **temel çizgi** olmalı; her model önce onu geçmeli.
- Deneyler **doğrulama** kümesiyle karşılaştırılır; seçilen model
  **test** kümesinde bir kez ölçülür ve raporlanan sayı odur.
- **Kazananın laneti**: çok adayın en iyisi, seçildiği veride olduğundan
  iyi görünür. Deney sayısı arttıkça doğrulama sonucu daha iyimserdir.
- Kötü sonuçlar da kaydedilir.
