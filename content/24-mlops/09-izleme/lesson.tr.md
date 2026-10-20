# İzleme

Model canlıda. Sunucu çalışıyor, istekler `200` dönüyor, hata yok. Model
iyi mi? Bu soruların ilk ikisinin cevabı sunucu kayıtlarında; sonuncusunun
cevabı orada **yok**. Bir ML sistemi, sunucusu kusursuz çalışırken
sessizce kötüleşebilir. **İzleme** (monitoring), canlıdaki modelin
sağlığını sürekli ölçmek ve kötüleşmeyi kullanıcılardan önce fark etmek
demek. Bu bölümde bir modeli sekiz ay boyunca izliyoruz.

## Üç katman

| Katman | Ne ölçülür | Ne zaman bilinir |
|---|---|---|
| Sistem | Gecikme, hata oranı, istek sayısı | Hemen |
| Veri ve tahmin | Girdilerin dağılımı, tahminlerin dağılımı | Hemen |
| Model kalitesi | Doğruluk, doğru tahmin oranı | **Etiket gelince** (haftalar sonra) |

Üçüncü katman en önemlisi ama en geç geleni: bir müşterinin gerçekten
iptal edip etmediği ancak bir ay sonra belli olur. Bu yüzden ilk iki
katman **erken uyarı** işi görür.

## Sekiz ay

Modeli 0. ayın verisiyle eğitelim ve sonraki her ayın müşterilerine
bakalım. Bu modülün verisi aylar geçtikçe değişiyor: müşteriler hizmeti
daha az kullanıyor, daha çok ödüyor.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


TRAIN = make_customers(2000)
model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit([features(r) for r in TRAIN], [r["churned"] for r in TRAIN])

rates, usages, accuracies = [], [], []
print("month  predicted  usage  accuracy")
for month in range(8):
    batch = make_customers(1000, seed=99, month=month)
    X = [features(r) for r in batch]
    rates.append(model.predict(X).mean())
    usages.append(sum(r["usage_hours"] for r in batch) / len(batch))
    accuracies.append(model.score(X, [r["churned"] for r in batch]))
    print(f"{month:>5} {rates[-1]:>10.3f} {usages[-1]:>6.1f} {accuracies[-1]:>9.3f}")
```

```text
month  predicted  usage  accuracy
    0      0.204   32.0     0.813
    1      0.289   30.6     0.820
    2      0.344   29.1     0.778
    3      0.390   27.5     0.784
    4      0.498   25.0     0.673
    5      0.514   23.5     0.681
    6      0.586   22.1     0.685
    7      0.590   21.5     0.658
```

Sütunlar:

- **predicted**: modelin "gidecek" dediği müşterilerin payı. Hemen
  bilinir: her tahmin kaydedilir.
- **usage**: girdilerden birinin, kullanım süresinin ortalaması. Hemen
  bilinir.
- **accuracy**: doğruluk. Gerçek sonuçlar ancak bir ay sonra geldiği için
  bu sütunu ay bittiğinde **göremeyiz**; burada karşılaştırma için
  yanına koyduk.

Tahmin oranı ilk aydan başlayarak düzenli tırmanıyor (0,204 →
0,590), kullanım düşüyor. Doğruluk ise üç ay boyunca iyi kalıyor
ve 4. ayda birden düşüyor (0,784 → 0,673). Hemen bilinen
sinyaller değişimi aylar önce gösterdi; doğruluk ancak bozulduktan
sonra, o da gecikmeyle.

`model.predict(X).mean()` 1'lerin payını veriyor: tahminler 0 ve 1, ortalamaları
"gidecek" denenlerin oranı. `f"{month:>5}"` sağa yaslıyor, `:>10.3f`
on karakterlik alanda üç basamak.

## Tahmin kaydı ve gecikmeli etiketler

Kaliteyi ölçebilmek için her tahmin bir **tahmin kaydına** (prediction
log) yazılır: hangi müşteri, hangi ay, hangi model sürümü, ne tahmin
edildi. Gerçek sonuç gelince kayıtla birleştirilir:

```python
import json

log = []
for r in make_customers(5, seed=99, month=4):
    probability = float(model.predict_proba([features(r)])[0, 1])
    log.append({"id": r["id"], "month": 4, "model_version": 3,
                "churn_probability": round(probability, 3)})
print(json.dumps(log[0]))

outcomes = {r["id"]: r["churned"] for r in make_customers(5, seed=99, month=4)}
hits = [(e["churn_probability"] >= 0.5) == bool(outcomes[e["id"]]) for e in log]
print("correct:", sum(hits), "of", len(hits))
```

```text
{"id": "C04-00001", "month": 4, "model_version": 3, "churn_probability": 0.994}
correct: 5 of 5
```

Birleştirmenin anahtarı müşteri kimliği. Kayıtta model sürümü olduğu
için doğruluk sürüm sürüm de hesaplanabilir: yeni sürüm canlıya çıktıktan
sonra gerçekten daha mı iyi? Model Kaydı bölümündeki kapı bunu tahmin
ediyordu; tahmin kaydı ölçüyor.

Gerçek bir sistemde `outcomes` bir ay sonra başka bir tablodan gelir;
burada aynı tohumdan yeniden ürettik. `bool(...)` 0 ve 1'i `False` ve
`True`'ya çeviriyor; karşılaştırma iki tarafta da aynı türle yapılsın.

## Uyarılar

Bir panoya her gün bakan olmayabilir. İzlemenin işe yaraması için
eşikler ve **uyarılar** (alerts) gerekir. Ama her küçük dalgalanmada
çalan bir uyarı bir süre sonra görmezden gelinir; buna **uyarı
yorgunluğu** (alert fatigue) denir. Basit bir çare: eşik **üst üste
birkaç kez** aşılınca uyar.

```python
def alert_months(values, reference, limit, patience=2):
    alerts, streak = [], 0
    for month, value in enumerate(values):
        streak = streak + 1 if abs(value - reference) > limit else 0
        if streak >= patience:
            alerts.append(month)
    return alerts


print("prediction rate alerts:", alert_months(rates, rates[0], 0.1))
print("accuracy alerts:", [m for m, a in enumerate(accuracies) if a < 0.75])
```

```text
prediction rate alerts: [3, 4, 5, 6, 7]
accuracy alerts: [4, 5, 6, 7]
```

Tahmin oranı uyarısı 3. ayda çaldı: oran iki ay üst üste
başlangıçtan 0,1'den fazla uzaktaydı. Doğruluk uyarısı 4. aydan itibaren
çalıyor, ama 4. ayın doğruluğu ancak 5. ayda bilinebiliyor. Erken sinyal
bir aydan fazla önce haber verdi.

`streak` üst üste kaç ay eşiğin aşıldığını sayıyor; eşik aşılmayınca
sıfırlanıyor. `patience` (sabır) uyarı için gereken ardışık ay sayısı.

Uyarı tek başına bir hüküm değil, **bakılması gereken** bir şey: tahmin
oranı müşteriler gerçekten değiştiği için de artabilir (bu veride iptal
oranı da artıyor). Ne yapılacağına bir insan karar verir: veriyi
incelemek, yeniden eğitmek, ya da hiçbir şey. Sonraki iki bölüm bu
kararın aracı: Veri Kayması ve Kavram Kayması.

## Neyi izlemeli?

Her şeyi izlemek mümkün değil; bir başlangıç listesi:

- **Sistem:** p95 gecikme, hata oranı (`5xx` yüzdesi), istek sayısı.
- **Girdiler:** her sayısal sütunun ortalaması, eksik değer oranı,
  şemaya uymayan isteklerin oranı (`422` yüzdesi).
- **Tahminler:** "gidecek" oranı, olasılıkların dağılımı.
- **Kalite:** etiket gelince doğruluk ve dilimlerde doğruluk (ML İçin CI
  bölümündeki dilimler).
- **Sürüm:** hangi model sürümünün kaç istek karşıladığı.

Gerçek sistemlerde bu ölçümler **Prometheus** gibi bir zaman serisi
veritabanına yazılır, **Grafana** gibi bir panoda çizilir ve eşik
aşılınca uyarı gönderilir.

## Özet

- Sunucunun sağlıklı olması modelin iyi olduğu anlamına gelmez; ML
  sistemi sessizce kötüleşir.
- Üç katman: **sistem**, **veri ve tahmin** (hemen bilinir), **model
  kalitesi** (etiket gelince, gecikmeyle).
- Dersteki ölçüm: tahmin oranı aylardır tırmanırken doğruluk 4. ayda
  düştü; erken sinyaller önceden haber verdi.
- Her tahmin **kaydedilir** (kimlik, sürüm, tahmin) ve gerçek sonuç
  gelince birleştirilir.
- **Uyarılar** eşikle kurulur; uyarı yorgunluğunu önlemek için üst üste
  birkaç kez aşılma beklenir.
- Uyarı bir hüküm değil, bakılacak bir şeydir.
