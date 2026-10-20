# Eğitim-Sunma Farkı ve Özellik Deposu

Model testte 0,81 doğruluk verdi, kapıdan geçti, canlıya çıktı. Bir hafta
sonra müşteri ekibi soruyor: "Aradığımız müşterilerin çoğu zaten
kalacakmış, neden?" Model aynı model; değişen, ona verilen girdi. Eğitimde
özellikler bir yolla, canlıda başka bir yolla hesaplanıyorsa model
canlıda başka bir dünya görür. Buna **eğitim-sunma farkı**
(training-serving skew) denir. Bu bölümde iki biçimini ölçüyoruz ve
çözümü olan **özellik deposuna** (feature store) bakıyoruz.

## Eğitimdeki özellikler

Model, özellikleri bu sırayla görerek eğitiliyor: abonelik süresi,
ücret, destek araması, kullanım, paket.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers

NAMES = ["tenure", "monthly_fee", "support_calls", "usage_hours", "is_pro"]


def features(r):
    return [r["tenure"], r["monthly_fee"], r["support_calls"], r["usage_hours"],
            1 if r["plan"] == "pro" else 0]


TRAIN = make_customers(2000)
HOLD = make_customers(1000, seed=99)
y_train = [r["churned"] for r in TRAIN]
y_hold = [r["churned"] for r in HOLD]


def accuracy(model, make, rows):
    return round(model.score([make(r) for r in rows], y_hold), 3)


X_train = [features(r) for r in TRAIN]
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
print("offline accuracy:", accuracy(model, features, HOLD))
```

```text
offline accuracy: 0.813
```

## Aynı özellik, iki kod

Modeli sunan servisi başka bir ekip yazıyor. Özellik kodunu kopyalamak
yerine yeniden yazıyorlar ve iki sütunun yerini karıştırıyorlar: ücret
ile destek araması yer değiştiriyor.

```python
def serve_features(r):
    return [r["tenure"], r["support_calls"], r["monthly_fee"], r["usage_hours"],
            1 if r["plan"] == "pro" else 0]


print("served accuracy:", accuracy(model, serve_features, HOLD))
```

```text
served accuracy: 0.297
```

Doğruluk 0,813'ten 0,297'ye düştü: herkese
"kalır" demekten (0,703) bile kötü. Hiçbir hata çıkmadı: iki
sütun da sayı, model sayıları aldı ve hesapladı. Model artık 30'luk
ücreti "30 kez destek aramış" diye okuyor; neredeyse herkesi gidecek
sanıyor.

## Farkı yakalamak

Bu hatayı yakalamanın yolu, **sunma anında modele giren özellikleri
kaydetmek** ve onları eğitimdekilerle karşılaştırmak. Veri Doğrulama
bölümündeki profil fikrinin aynısı, ama bu kez kaynak veri değil modele
giren vektör:

```python
def column_means(rows):
    return [sum(column) / len(column) for column in zip(*rows)]


served = [serve_features(r) for r in HOLD]
pairs = zip(NAMES, column_means(X_train), column_means(served))
for name, trained, live in pairs:
    flag = "CHECK" if abs(live - trained) > 0.5 * abs(trained) else "ok"
    print(f"{name:14} {trained:7.2f} {live:7.2f}  {flag}")
```

```text
tenure           36.68   37.67  ok
monthly_fee      30.23    0.73  CHECK
support_calls     0.74   29.80  CHECK
usage_hours      32.18   32.00  ok
is_pro            0.41    0.40  ok
```

İki sütun hemen göze batıyor: ücretin ortalaması 30'dan 0,7'ye, destek
aramasınınki 0,7'den 30'a çıkmış. `zip(*rows)` satır listesini sütunlara
çeviriyor: ilk eleman bütün satırların ilk değerleri, ikincisi ikinci
değerleri. Sunma anındaki girdiler kaydedilmezse bu karşılaştırma
yapılamaz; o yüzden kayıt şart.

Asıl çözüm ise farkın hiç doğmaması: özellik kodu **tek bir yerde**
yazılır, eğitim de sunma da aynı fonksiyonu içe aktarır (`from features
import features`). Kopyalanan ya da yeniden yazılan özellik kodu er geç
ayrışır.

## Geleceği gören özellik

İkinci fark daha sinsi. Eğitim verisinde müşterinin **toplam** destek
araması duruyor; ama iptal eden müşteriler iptal ederken de birkaç kez
arıyor. Bu aramalar tahmin anında **henüz yok**: model "bu müşteri gidecek
mi?" sorusunu iptalden önce soruyor. Eğitim verisine sızan bu bilgiyi
ölçelim:

```python
import random


def with_exit_calls(rows, seed):
    rng = random.Random(seed)
    result = []
    for r in rows:
        exit_calls = rng.randint(1, 3) if r["churned"] else 0
        result.append({**r, "calls_total": r["support_calls"] + exit_calls})
    return result


def leaky_features(r):
    return [r["tenure"], r["monthly_fee"], r["calls_total"], r["usage_hours"],
            1 if r["plan"] == "pro" else 0]


X_leaky = [leaky_features(r) for r in with_exit_calls(TRAIN, 1)]
leaky = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_leaky, y_train)
test_rows = with_exit_calls(HOLD, 2)
print("leaky, offline:", accuracy(leaky, leaky_features, test_rows))
live_rows = [{**r, "calls_total": r["support_calls"]} for r in HOLD]
print("leaky, live:", accuracy(leaky, leaky_features, live_rows))
```

```text
leaky, offline: 0.939
leaky, live: 0.787
```

Testte 0,939: harika görünüyor. Ama test kümesi de aynı
yanlışla hazırlandı; o da iptal aramalarını içeriyor. Canlıda bu aramalar
henüz olmadığı için doğruluk 0,787'ye iniyor: sızıntısız
modelden (0,813) **kötü**. Model "çok arayan gidiyor"
kuralını abartmış; canlıda o aramalar gelmeyince yanılıyor.

Buna **zaman sızıntısı** (point-in-time leakage) denir: eğitimde, tahmin
anında bilinemeyecek bir bilgi kullanılmış. Testin de aynı yanlışla
kurulması onu görünmez yapıyor; yalnızca canlıda ortaya çıkıyor.

## Zamanında ne biliniyordu?

Çözüm, her özelliği **tahmin anına göre** hesaplamak: o tarihte
bilinen son değeri almak. Bunun için özellik değerleri tarihleriyle
birlikte saklanır ve sorgu "şu tarih itibarıyla" (as of) yapılır:

```python
calls_history = [["2026-01-01", 0], ["2026-02-01", 1], ["2026-03-01", 4]]


def as_of(history, day):
    value = None
    for when, known in history:
        if when <= day:
            value = known
        else:
            break
    return value


print("as of 2026-02-15:", as_of(calls_history, "2026-02-15"))
print("as of 2026-03-10:", as_of(calls_history, "2026-03-10"))
print("as of 2025-12-31:", as_of(calls_history, "2025-12-31"))
```

```text
as of 2026-02-15: 1
as of 2026-03-10: 4
as of 2025-12-31: None
```

Müşteri 15 Şubat'ta iptal ettiyse eğitimde onun için "1 arama" kullanılır,
mart ayındaki 4 değil. `"2026-02-15" <= "2026-03-01"` gibi
karşılaştırmalar metin karşılaştırması ama doğru çalışıyor: tarih
`YYYY-AA-GG` biçiminde yazılınca abece sırası zaman sırasıyla aynı.
Liste tarihe göre sıralı olduğu için ilk büyük tarihte duruyoruz
(`break`).

## Özellik deposu

İki sorunun ortak çözümü bir **özellik deposu** (feature store):

- Özellikler **bir kez** tanımlanır; eğitim de sunma da aynı tanımı
  kullanır. Sütun sırası karışamaz.
- **Çevrim dışı depo** (offline store) her özelliğin tarihli geçmişini
  tutar. Eğitim verisi "etiket tarihi itibarıyla" çekilir; zaman sızıntısı
  olmaz.
- **Çevrim içi depo** (online store) her müşterinin **son** değerlerini
  tutar; sunma anında müşteri kimliğiyle milisaniyeler içinde okunur.

Küçük bir örnek:

```python
class FeatureStore:
    def __init__(self):
        self.history = {}

    def write(self, customer, day, values):
        self.history.setdefault(customer, []).append([day, values])

    def offline(self, customer, day):
        return as_of(self.history[customer], day)

    def online(self, customer):
        return self.history[customer][-1][1]


store = FeatureStore()
store.write("C7", "2026-01-01", {"support_calls": 0, "usage_hours": 35.0})
store.write("C7", "2026-02-01", {"support_calls": 1, "usage_hours": 28.0})
store.write("C7", "2026-03-01", {"support_calls": 4, "usage_hours": 9.0})
print("for training, as of 2026-02-15:", store.offline("C7", "2026-02-15"))
print("for serving, now:", store.online("C7"))
```

```text
for training, as of 2026-02-15: {'support_calls': 1, 'usage_hours': 28.0}
for serving, now: {'support_calls': 4, 'usage_hours': 9.0}
```

Eğitim için soru "15 Şubat'ta ne biliniyordu?", sunma için "şu an ne
biliniyor?". İkisi de aynı yazılardan okunuyor; tanım tek.

Gerçek projelerde **Feast** gibi açık kaynak özellik depoları bu iki
deposu, tanım dosyalarını ve "as of" birleştirmesini hazır veriyor.

## Özet

- **Eğitim-sunma farkı**: model canlıda eğitimdekinden farklı
  hesaplanmış girdiler görür. Hata çıkmaz, yalnızca tahminler bozulur.
- Dersteki ölçüm: iki sütunun yer değiştirmesi doğruluğu
  0,813'ten 0,297'ye indirdi.
- Sunma anında modele giren özellikler **kaydedilir** ve eğitimdekilerle
  karşılaştırılır.
- Özellik kodu **tek yerde** yazılır; eğitim ve sunma onu içe aktarır.
- **Zaman sızıntısı**: eğitimde tahmin anında bilinemeyecek bir bilgi
  kullanılması. Test de aynı yanlışla kurulursa yalnızca canlıda görünür.
- Her özellik tahmin anı **itibarıyla** (as of) hesaplanır.
- **Özellik deposu**: tek tanım, tarihli çevrim dışı depo (eğitim) ve son
  değerleri tutan çevrim içi depo (sunma).
