# ML Sistem Tasarımı

Bu modülde parçaları tek tek kurduk: tekrarlanabilir eğitim, doğrulama,
kayıt, sunma, izleme, yeniden eğitim, kanarya, ölçeklenme. **ML sistem
tasarımı**, kod yazmadan önce bu parçaların hangilerinin, nasıl bir araya
geleceğine karar vermektir. Tasarım bir dizi soruyla başlar; bu bölümde
soruları sıralıyor ve en önemli ikisini ölçerek cevaplıyoruz: başarı neyle
ölçülür ve model çökerse ne olur?

## Tasarım soruları

| Soru | Bu örnekte cevap |
|---|---|
| İş hedefi ne? | İptali azaltmak: riskli müşteriye indirim teklif etmek |
| ML görevi ne? | İkili sınıflandırma; iptal olasılığı |
| Başarı neyle ölçülür? | Bir **iş ölçüsüyle** (kâr); doğruluk yardımcı ölçü |
| Etiket ne zaman gelir? | Bir ay sonra; bu bir **etiket gecikmesi** |
| Tahmin ne zaman yapılır? | Toplu, her gece (Ölçeklenme) |
| Temel çizgi ne? | Basit bir kural ya da hiç teklif etmemek |
| Model çökerse? | Bir **yedek plan** (fallback) |
| Ne izlenir? | Kayma, kalibrasyon ve iş ölçüsü (İzleme) |

Soruların sırası önemli: modeli seçmek listenin ortasında bile değil.
Önce hedef ve ölçü yazılır, çünkü onlar olmadan "iyi model" diye bir şey
yoktur.

Ortak parçalar: model, test müşterileri, olasılıklar ve etiketler.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


train = make_customers(2000)
model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit([features(r) for r in train], [r["churned"] for r in train])
test = make_customers(1000, seed=99)
probs = model.predict_proba([features(r) for r in test])[:, 1]
labels = [r["churned"] for r in test]
print(sum(labels), "of", len(test), "customers churned")
```

```text
297 of 1000 customers churned
```

## İş ölçüsünü yazmak

Modelin işi bir karar vermek: kime teklif gidecek? Kararın değerini
yazmak için birkaç varsayım gerekir. Diyelim ki:

- Bir teklifin maliyeti **5 birim**.
- İptal edecek bir müşteri teklifi **%30** olasılıkla kabul edip kalıyor
  ve kalan müşteri **60 birim** değerinde. Yani iptal edecek birine giden
  teklifin beklenen getirisi 0,3 × 60 = **18 birim**.
- Kalacak müşteriye giden teklif boşa gider: yalnızca maliyeti var.

Bu sayılar örnek; gerçek bir işte pazarlama ve finans ekibinden gelir.
Ama yazılmaları şarttır: karar eşiğini onlar belirler.

```python
COST, SAVED = 5, 18


def profit(threshold):
    offered = [y for p, y in zip(probs, labels) if p >= threshold]
    return len(offered), sum(SAVED * y - COST for y in offered)


def accuracy(threshold):
    hits = sum((p >= threshold) == bool(y) for p, y in zip(probs, labels))
    return round(hits / len(labels), 3)


for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    offers, total = profit(threshold)
    score = accuracy(threshold)
    print(f"{threshold}: {offers:>3} offers, profit {total:>5}, accuracy {score}")
```

```text
0.1: 651 offers, profit  1803, accuracy 0.614
0.2: 474 offers, profit  2166, accuracy 0.733
0.3: 363 offers, profit  2235, accuracy 0.79
0.4: 272 offers, profit  2150, accuracy 0.821
0.5: 204 offers, profit  1806, accuracy 0.813
0.6: 152 offers, profit  1580, accuracy 0.811
0.7: 100 offers, profit  1192, accuracy 0.791
```

Doğruluğun en iyi olduğu eşik ile kârın en iyi olduğu eşik **aynı
değil**. Doğruluk, yanlış teklif ile kaçırılan müşteriyi eşit sayar;
ama burada kaçırılan bir müşteri (18 birim) boşa giden bir tekliften
(5 birim) çok daha pahalı. Bu yüzden kâr, daha çok teklif veren düşük bir
eşikte büyüyor.

## En iyi eşik

Eşikleri tek tek deneyip kârı en büyük olanı seçelim:

```python
candidates = [t / 100 for t in range(5, 96)]
best = max(candidates, key=lambda t: profit(t)[1])
print("best threshold:", best, profit(best), "accuracy", accuracy(best))
print("default 0.5:", profit(0.5), "accuracy", accuracy(0.5))
print("offer everyone:", profit(0.0))
```

```text
best threshold: 0.31 (352, 2254) accuracy 0.797
default 0.5: (204, 1806) accuracy 0.813
offer everyone: (1000, 346)
```

Kârı en büyük eşik 0,31: varsayılan 0,5'e göre 448
birim fazla kâr, doğruluğu ise biraz daha düşük. Herkese teklif etmek de
bir seçenek değil: maliyet getiriyi neredeyse yiyor. Model aynı model;
değişen yalnızca **ölçü**. Eşik, Model Kaydı bölümündeki gibi kayda
modelle birlikte yazılır ve iş varsayımları değişince yeniden seçilir.

Eşik bu test kümesinde seçildi; dürüst olmak için başka bir dönemde
doğrulanması gerekir (Deney Takibi'ndeki kazananın laneti).

## Yedek plan

Model sunucusu çökerse, gecikme sınırı aşılırsa ya da kayıt bozuk bir
model verirse ne olacak? İyi tasarımda bunun cevabı önceden yazılıdır:
**yedek plan** (fallback). En basiti, modelden önce de bilinen bir
kuraldır: "destek hattını en az iki kez arayana teklif et."

```python
rule = [y for r, y in zip(test, labels) if r["support_calls"] >= 2]
print("model:", profit(best))
print("rule: ", (len(rule), sum(SAVED * y - COST for y in rule)))
print("nothing:", (0, 0))
```

```text
model: (352, 2254)
rule:  (172, 1066)
nothing: (0, 0)
```

Kural modelin kârının yaklaşık yarısını getiriyor. Model çöktüğünde
müşteriye hiç teklif gitmemesi yerine kural çalışır; kârın hepsi değil,
yaklaşık yarısı kaybedilir. Kural aynı zamanda **temel çizgidir**: model
kuraldan iyi değilse, karmaşıklığına değmez.

Yedek planın da sınanması gerekir: hiç çalışmamış bir yedek, ihtiyaç
anında çalışmayabilir. Onu kanaryadaki gibi küçük bir trafik payında ara
ara gerçekten çalıştırmak bunu gösterir.

## Tasarımı yazmak

Tasarım bir belgeye yazılır; kod ondan sonra gelir. Kısa bir tasarım
belgesinin bölümleri:

| Bölüm | İçinde ne var |
|---|---|
| Hedef | İş hedefi ve iş ölçüsü, varsayımlarıyla |
| Veri | Kaynaklar, etiket ve etiket gecikmesi, doğrulama |
| Model | Temel çizgi, aday modeller, eşik ve nasıl seçildiği |
| Sunma | Toplu ya da anlık, gecikme sınırı, yedek plan |
| İzleme | Kayma, kalibrasyon, iş ölçüsü; uyarılar |
| Yeniden eğitim | Takvim ya da tetikleyici, kapı kümesi |

Bu modülün her bölümü bu tablonun bir satırını dolduruyor.

## Özet

- ML sistem tasarımı, kod yazmadan önce sorulan sorularla başlar; model
  seçimi listenin başında değildir.
- Başarı bir **iş ölçüsüyle** yazılır; varsayımları açıkça yazılır.
- Dersteki ölçüm: doğruluğu en iyi eşik ile kârı en iyi eşik farklı
  (0,31, varsayılan 0,5'ten 448 birim fazla).
- Eşik modelle birlikte kayda yazılır, başka bir dönemde doğrulanır.
- **Yedek plan** önceden yazılır ve sınanır; basit kural hem yedek hem
  temel çizgidir.
- Tasarım belgesi: hedef, veri, model, sunma, izleme, yeniden eğitim.
