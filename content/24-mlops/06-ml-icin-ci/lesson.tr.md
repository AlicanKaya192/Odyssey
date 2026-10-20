# ML İçin CI: Kalite Kapısı

CI/CD ve DevOps modülünde her değişiklikte testleri çalıştıran bir hat
kurduk. Bir ML projesinde o hat yetmez: bütün testler geçerken model
kötüleşmiş olabilir. Birinin bir ayarı yanlışlıkla değiştirmesi kodu
bozmaz ama modeli bozar. Bu bölümde hatta **modeli de** sınayan bir adım
ekliyoruz: **kalite kapısı** (quality gate). Model belirlenen çıtayı
geçmezse hat kırmızıya döner ve değişiklik birleştirilmez.

## ML hattında ne sınanır?

| Ne | Örnek sınama | Hangi bölüm |
|---|---|---|
| Kod | Özellik fonksiyonu doğru sütunları doğru sırayla veriyor mu? | Bu bölüm |
| Veri | Şemaya uyuyor mu, profil kaymış mı? | Veri Doğrulama |
| Tekrarlanabilirlik | Aynı ayarla iki eğitim aynı tahminleri veriyor mu? | Tekrarlanabilir Eğitim |
| Model | Doğruluk çıtayı geçiyor mu, her müşteri grubunda? | Bu bölüm |
| Davranış | Model beklenen yönde tepki veriyor mu? | Bu bölüm |

Önce ortak parçaları kuralım: özellik fonksiyonu, eğitim verisi,
değerlendirme kümesi ve temel çizgi.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(row):
    return [row[c] for c in NUMERIC] + [1 if row["plan"] == "pro" else 0]


TRAIN = make_customers(2000)
HOLD = make_customers(1000, seed=99)
BASELINE = 1 - sum(r["churned"] for r in HOLD) / len(HOLD)


def train(model):
    return model.fit([features(r) for r in TRAIN], [r["churned"] for r in TRAIN])


print("baseline:", round(BASELINE, 3))
```

```text
baseline: 0.703
```

## Kodun testi

Modelin girdisini hazırlayan kod sıradan bir fonksiyon; sıradan birim
testleriyle sınanır. Sütunların sırası değişirse model hata vermez ama
yanlış sütunları yanlış yerde görür, bu yüzden sırayı da sınarız:

```python
def test_feature_order():
    row = {"tenure": 5, "monthly_fee": 20.0, "support_calls": 1,
           "usage_hours": 30.0, "plan": "pro"}
    assert features(row) == [5, 20.0, 1, 30.0, 1]


def test_basic_plan_is_zero():
    row = {"tenure": 5, "monthly_fee": 20.0, "support_calls": 1,
           "usage_hours": 30.0, "plan": "basic"}
    assert features(row)[-1] == 0


for test in [test_feature_order, test_basic_plan_is_zero]:
    test()
    print(test.__name__, "passed")
```

```text
test_feature_order passed
test_basic_plan_is_zero passed
```

Gerçek projede bu fonksiyonlar `test_features.py` dosyasında durur ve
`pytest` onları kendisi bulup çalıştırır (CI/CD ve DevOps modülünün
Otomatik Testler bölümü). `test.__name__` fonksiyonun adını veriyor.

## Kalite kapısı

Şimdi modelin kendisi. Kapının kuralları üç soru soruyor:

- **Yeterince iyi mi?** Doğruluk bir alt sınırın üstünde mi?
- **Temel çizgiyi açıkça geçiyor mu?** Herkese "kalır" demekten en az
  belli bir pay kadar iyi mi?
- **Her grupta iyi mi?** Ortalama iyi görünürken bir müşteri grubunda
  model çok kötü olabilir. Paketlere (`basic`, `pro`) ayrı ayrı bakalım.
  Bir verinin belli bir kesimine **dilim** (slice) denir.

```python
RULES = {"min_accuracy": 0.78, "min_lift": 0.05, "min_slice": 0.75}


def accuracy_on(model, rows):
    X = [features(r) for r in rows]
    return model.score(X, [r["churned"] for r in rows])


def quality_gate(model):
    failures = []
    accuracy = accuracy_on(model, HOLD)
    if accuracy < RULES["min_accuracy"]:
        failures.append(f"accuracy {accuracy:.3f} is below the floor")
    if accuracy < BASELINE + RULES["min_lift"]:
        failures.append(f"accuracy {accuracy:.3f} is too close to the baseline")
    for plan in ["basic", "pro"]:
        part = accuracy_on(model, [r for r in HOLD if r["plan"] == plan])
        if part < RULES["min_slice"]:
            failures.append(f"{plan} slice: {part:.3f} is too low")
    return failures


good = train(make_pipeline(StandardScaler(), LogisticRegression()))
print("good model:", quality_gate(good))
weak = train(make_pipeline(StandardScaler(), LogisticRegression(C=0.0001)))
print("weak model:")
for failure in quality_gate(weak):
    print(" ", failure)
```

```text
good model: []
weak model:
  accuracy 0.703 is below the floor
  accuracy 0.703 is too close to the baseline
  basic slice: 0.735 is too low
  pro slice: 0.654 is too low
```

İyi model kapıdan geçti: sorun listesi boş. İkinci modelde biri `C`
değerini çok küçük yapmış: düzenlileştirme o kadar güçlü ki model
neredeyse hiçbir şey öğrenemiyor. Kod hiç hata vermedi, bütün birim
testleri hâlâ geçiyor; ama kapı dört sorunu birden yakaladı. Doğruluğu
temel çizgiyle aynı (0,703): model, herkese "kalır" demekten
daha iyi bir şey yapmıyor. İki paket de dilim çıtasının altında;
`pro` müşterilerdeki düşüş ortalamadakinden de büyük.

Hatta bu kapı ayrı bir betik olarak çalışır (`check_quality.py`) ve en
sonda `sys.exit(1 if failures else 0)` der: sorun varsa betik hata
koduyla biter ve adım kırmızıya döner.

## Davranış testleri

Doğruluk, modelin **ne kadar** doğru olduğunu söyler; **nasıl**
düşündüğünü söylemez. **Davranış testleri** (behavioral tests) modelin
mantıklı tepki verip vermediğine bakar. Bu modülün verisinde destek
araması arttıkça iptal olasılığı artıyor. Öyleyse bir müşterinin destek
araması iki artınca modelin verdiği iptal olasılığı **düşmemeli**. Buna
**yön testi** (directional test) denir:

```python
def directional_share(model, rows):
    before = model.predict_proba([features(r) for r in rows])[:, 1]
    more_calls = [{**r, "support_calls": r["support_calls"] + 2} for r in rows]
    after = model.predict_proba([features(r) for r in more_calls])[:, 1]
    return float((after >= before).mean())


forest = train(RandomForestClassifier(n_estimators=100, random_state=0))
print("logistic:", round(directional_share(good, HOLD), 3))
print("forest:", round(directional_share(forest, HOLD), 3))
obvious = {"tenure": 2, "monthly_fee": 45.0, "support_calls": 6,
           "usage_hours": 5.0, "plan": "pro"}
probability = good.predict_proba([features(obvious)])[0, 1]
print("obvious churner:", round(float(probability), 3))
```

```text
logistic: 1.0
forest: 0.957
obvious churner: 1.0
```

`predict_proba(...)[:, 1]` her müşterinin iptal (sınıf 1) olasılığını
veriyor. `(after >= before).mean()` koşulun tuttuğu müşterilerin payı:
`True` 1, `False` 0 sayılıyor.

Lojistik regresyonda yön testi bütün müşterilerde tuttu: model her
sütuna tek bir ağırlık veriyor, ağırlık artıysa yön hep aynı. Ormanda
müşterilerin %95,7'sinde tuttu: ağaçlar sayıları
basamaklara bölüyor, bazı müşterilerde iki fazla arama hiçbir basamağı
aşmıyor ya da başka bir dalda biraz ters etki yapıyor. Bu yüzden yön
testinin eşiği modele göre seçilir; ormanda "yüzde 95'inde tutsun"
gibi.

Son satır başka bir davranış testi: **açık örnek** testi. İki aydır
abone, altı kez destek aramış, hizmeti neredeyse hiç kullanmayan bir
müşteri için model yüksek bir iptal olasılığı vermeli. Böyle birkaç açık
örnek, modelin büyük bir yanlışını hızla yakalar.

## Hattaki yeri

Hepsini GitHub Actions'ta birleştirelim. Önce kod testleri çalışır;
geçerse model eğitilir ve kapıdan geçirilir:

```yaml
name: ML CI

on:
  pull_request:
    branches: [main]

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

  model-gate:
    needs: test
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
      - run: python -m pip install -r requirements.txt
      - run: python train.py
      - run: python check_quality.py
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: metrics
          path: metrics.json
```

Bu iş akışında yeni olan şeyler:

- `model-gate` işi `test`'e bağlı (`needs`): kod testleri düşerse model
  hiç eğitilmez, makine boşuna çalışmaz.
- Eğitim CI'da **küçük ve sabit** bir veriyle yapılır: tohumlar sabit,
  süre birkaç dakika (`timeout-minutes` bunun sınırı). Asıl büyük eğitim
  ayrı bir yerde koşar; CI'daki eğitimin amacı "bu değişiklik modeli
  bozdu mu?" sorusuna hızlı cevap vermek.
- Ölçümler (`metrics.json`) `if: always()` ile her durumda saklanıyor:
  kapı düştüğünde **neden** düştüğünü görmek için en çok o zaman
  gerekir.

## Çıtayı nereden alırız?

Bu bölümde eşikleri elle yazdık (0,78). Daha iyisi, çıtayı **canlıdaki
modelden** almak: Model Kaydı bölümündeki kayıtta `production`
etiketinin ölçümü duruyor. Kapı "yeni model canlıdakinden kötü mü?"
diye sorarsa, eşik model geliştikçe kendiliğinden yükselir. İkisi
birlikte de kullanılır: sabit bir alt sınır (kimse bunun altına
düşmesin) ve canlıdakine göre karşılaştırma.

## Özet

- ML hattında kodla birlikte **veri**, **model** ve **davranış** da
  sınanır.
- Özellik fonksiyonu birim testleriyle sınanır; sütunların sırası da.
- **Kalite kapısı**: alt sınır, temel çizgiye göre pay ve her **dilimde**
  (müşteri grubunda) ayrı çıta. Kod hatasız çalışırken bozulan modeli
  yakalar.
- **Davranış testleri**: yön testi (bir değer artınca tahmin beklenen
  yöne gidiyor mu) ve açık örnek testi. Eşik modele göre seçilir.
- CI'daki eğitim küçük, sabit ve hızlıdır; ölçümler her durumda
  saklanır.
- Çıta en iyi canlıdaki modelden alınır.
