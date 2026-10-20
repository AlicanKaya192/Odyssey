# Kavram Kayması ve Yeniden Eğitim

Veri Kayması bölümünde girdiler kaydığı hâlde modelin üç ay boyunca iyi
kaldığını gördük. Sonra 4. ayda doğruluk birden düştü. O ay değişen
müşteriler değil, müşterilerin **karar verme biçimiydi**: fiyat artık çok
daha önemli, destek aramaları ise eskisi kadar değil. Girdi ile sonuç
arasındaki ilişkinin değişmesine **kavram kayması** (concept drift)
denir. Bu bölümde onu nasıl fark edeceğimizi ve modeli **nasıl yeniden
eğiteceğimizi** ölçerek görüyoruz.

## İki kayma

| | Veri kayması | Kavram kayması |
|---|---|---|
| Ne değişir | Girdilerin dağılımı | Girdi ile sonuç arasındaki ilişki |
| Örnek | Müşteriler daha çok ödüyor | Aynı ücret artık daha çok iptale götürüyor |
| Etiketsiz görülür mü | Evet | Hayır, etiket gerekir |
| Modele etkisi | Bazen zararsız | Model artık yanlış kuralı biliyor |

Ortak parçalar: özellikler, eğitim ve aylık doğruluk.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC

NAMES = NUMERIC + ["is_pro"]


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


def fit(rows):
    model = make_pipeline(StandardScaler(), LogisticRegression())
    return model.fit([features(r) for r in rows], [r["churned"] for r in rows])


def accuracy(model, month):
    rows = make_customers(1000, seed=99, month=month)
    X = [features(r) for r in rows]
    return round(model.score(X, [r["churned"] for r in rows]), 3)


first = fit(make_customers(2000))
print("month 0:", accuracy(first, 0), " month 4:", accuracy(first, 4))
```

```text
month 0: 0.813  month 4: 0.673
```

## Kavram kaymasını görmek

Etiketler gelince yapılabilecek en basit sınama: modelin **verdiği**
ortalama iptal olasılığı ile **gerçekleşen** iptal oranını karşılaştırmak.
Model dünyayı doğru tanıyorsa ikisi yakın olur:

```python
print("month  predicted  actual")
for month in range(8):
    rows = make_customers(1000, seed=99, month=month)
    predicted = first.predict_proba([features(r) for r in rows])[:, 1].mean()
    actual = sum(r["churned"] for r in rows) / len(rows)
    print(f"{month:>5} {predicted:>10.3f} {actual:>7.3f}")
```

```text
month  predicted  actual
    0      0.277   0.297
    1      0.346   0.347
    2      0.385   0.358
    3      0.425   0.410
    4      0.504   0.413
    5      0.526   0.469
    6      0.576   0.471
    7      0.573   0.488
```

İlk dört ay iki sütun birbirine yakın: girdiler kaysa da model
olasılıkları doğru veriyor. 4. aydan itibaren model sürekli **fazla**
iptal bekliyor (0,504 beklenen, 0,413 gerçekleşen).
Modelin olasılıklarının gerçekle tutarlı olmasına **kalibrasyon**
(calibration) denir; kalibrasyonun birden bozulması kavram kaymasının
işaretidir.

`predict_proba(...)[:, 1].mean()` müşteri başına iptal olasılıklarının
ortalaması; `predict(...).mean()` gibi 0/1 tahminlerin değil.

## Ne değişti?

Lojistik regresyon her özelliğe bir ağırlık veriyor; ağırlıkların
karşılaştırılması ilişkinin nasıl değiştiğini gösterir. İlk modeli, 4. ve
5. ayın müşterileriyle eğitilen bir modelle karşılaştıralım:

```python
window = make_customers(500, seed=7, month=4) + make_customers(500, seed=7, month=5)
recent = fit(window)
old_w = first.named_steps["logisticregression"].coef_[0]
new_w = recent.named_steps["logisticregression"].coef_[0]
for name, a, b in zip(NAMES, old_w, new_w):
    print(f"{name:14} {a:6.2f} {b:6.2f}")
```

```text
tenure          -1.25  -1.31
monthly_fee      0.87   1.89
support_calls    1.02   0.24
usage_hours     -0.70  -0.62
is_pro          -0.38  -0.07
```

Ücretin ağırlığı iki katından fazlasına çıkmış, destek aramasınınki
dörtte birinin altına inmiş. Eski model "çok arayan gidiyor" diye biliyor;
yeni dünyada ise asıl neden fiyat. Özellikler ölçeklendiği için
(`StandardScaler`) ağırlıklar birbiriyle karşılaştırılabilir.
`named_steps` hattın (pipeline) içindeki adımlara adıyla ulaşıyor.

## Hangi veriyle yeniden eğitmeli?

5. ayın sonundayız; 4. ve 5. ayın etiketleri geldi. Üç seçenek var:

- **Hiç eğitme:** ilk modelle devam.
- **Bütün geçmiş:** 0–5. ayların hepsiyle eğit.
- **Son pencere:** yalnızca son iki ayla (4–5) eğit.

Hangisinin iyi olduğunu **geleceğe** bakarak ölçelim: 6. ve 7. aylar,
hiçbir modelin görmediği müşteriler.

```python
history = []
for month in range(6):
    history += make_customers(500, seed=7, month=month)
choices = {"never": first, "all history": fit(history), "last window": recent}
for name, model in choices.items():
    print(f"{name:12} month 6: {accuracy(model, 6)}  month 7: {accuracy(model, 7)}")
```

```text
never        month 6: 0.685  month 7: 0.658
all history  month 6: 0.759  month 7: 0.742
last window  month 6: 0.821  month 7: 0.798
```

Son pencere açık ara kazandı. Bütün geçmişle eğitmek, eski ilişkiyi
(arama önemli) yeni ilişkiyle (fiyat önemli) **karıştırıyor**: veri
çok olsa da yarısı artık yanlış bir dünyayı anlatıyor. Kavram kaydıysa
eski veri yardım etmez, zarar verir.

Ama bu her zaman böyle değil: kavram kaymadıysa daha çok veri daha iyi
model demektir, ve son pencere küçük olduğu için şansa açıktır. Pencerenin
boyu bir **seçimdir**; doğrusu birkaç boyu, Deney Takibi bölümündeki gibi
gelecekteki bir dönemde ölçerek karar vermektir.

## Kapı tuzağı

Yeni model kapıdan geçmeli (Model Kaydı). Ama **hangi** değerlendirme
kümesinde? Kayıttaki eski değerlendirme kümesi 0. aydan:

```python
for name, model in [("first", first), ("last window", recent)]:
    old_set, new_set = accuracy(model, 0), accuracy(model, 5)
    print(f"{name:12} on month 0: {old_set}  on month 5: {new_set}")
```

```text
first        on month 0: 0.813  on month 5: 0.681
last window  on month 0: 0.718  on month 5: 0.837
```

Eski kümede (0. ay) eski model daha iyi görünüyor: kapı yeni modeli
**geri çevirirdi**. Güncel kümede (5. ay) yeni model açık ara iyi. Kavram
kaydığında değerlendirme kümesi de eskir; kapı **güncel, etiketli** bir
kümeyle çalışmalıdır. Aksi hâlde hat, dünyaya uyum sağlamış modeli
reddedip eskisini korur.

## Ne zaman yeniden eğitmeli?

| Yol | Nasıl | Artısı | Eksisi |
|---|---|---|---|
| Takvimle | Her ay, her hafta | Basit, öngörülebilir | Gerekmediğinde de çalışır; ani değişimde geç kalır |
| Tetikleyiciyle | Kalite uyarısı çalınca | Gerektiğinde çalışır | Etiket gecikmesi kadar geç kalır |
| İkisi birden | Takvim + acil tetikleyici | Yaygın seçim | Daha çok parça |

Yeniden eğitim yeni bir model üretmekten ibaret değildir; hattın
tamamından geçer: veriyi tarih itibarıyla çek (Eğitim-Sunma Farkı),
doğrula (Veri Doğrulama), eğit ve kaydet (Tekrarlanabilir Eğitim, Deney
Takibi), **güncel** kümede kapıdan geçir, kayda koy (Model Kaydı), canlıya
al ve izle. Bu modüldeki her bölüm bu döngünün bir halkası.

## Özet

- **Kavram kayması**: girdi ile sonuç arasındaki ilişkinin değişmesi.
  Etiketsiz görülemez.
- İşareti: modelin verdiği ortalama olasılık ile gerçekleşen oranın
  ayrışması (**kalibrasyon** bozulur).
- Dersteki ölçüm: ücretin ağırlığı iki katından fazlasına çıktı, destek
  aramasınınki dörtte birinin altına indi.
- Kavram kaydıysa **son pencereyle** eğitmek bütün geçmişten iyi
  çıkabilir: eski veri yanlış ilişkiyi öğretir.
- Pencere boyu bir seçimdir; gelecekteki bir dönemde ölçülerek seçilir.
- Kapı **güncel** etiketli bir kümeyle çalışmalı; eski küme yeni modeli
  haksızca reddeder.
- Yeniden eğitim takvimle, tetikleyiciyle ya da ikisiyle yapılır ve
  hattın tamamından geçer.
