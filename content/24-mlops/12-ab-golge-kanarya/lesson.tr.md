# A/B Testi, Gölge ve Kanarya

Kavram Kayması bölümünde yeni model güncel kümede kapıdan geçti. Ama kapı
**çevrimdışı** bir sınamadır: kayıtlı veride ölçer. Canlıda başka şeyler
olur: gerçek istekler, gerçek gecikme, sunucudaki bir yapılandırma hatası.
Yeni modeli bütün müşterilere bir anda açmak yerine onu adım adım ve
ölçerek canlıya almanın üç yolu var: **gölge** (shadow), **kanarya**
(canary) ve **A/B testi**.

| | Gölge | Kanarya | A/B testi |
|---|---|---|---|
| Müşteri yeni modelin cevabını görür mü | Hayır | Küçük bir pay görür | Grubun yarısı görür |
| Risk | Yok | Küçük, sınırlı | Var, ama ölçülü |
| Neyi cevaplar | Yeni model canlıda çalışıyor mu, ne kadar farklı? | Bozuk mu? | Gerçekten daha iyi mi? |

Ortak parçalar: eski model, son pencereyle eğitilen yeni model ve bugünün
(6. ay) müşterileri.

```python
import zlib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


def fit(rows):
    model = make_pipeline(StandardScaler(), LogisticRegression())
    return model.fit([features(r) for r in rows], [r["churned"] for r in rows])


def accuracy(model, rows):
    return model.score([features(r) for r in rows], [r["churned"] for r in rows])


old = fit(make_customers(2000))
window = make_customers(500, seed=7, month=4) + make_customers(500, seed=7, month=5)
new = fit(window)
today = make_customers(1000, seed=99, month=6)
X = [features(r) for r in today]
print(len(today), "customers today")
```

```text
1000 customers today
```

## Gölge

Gölgede yeni model eski modelin yanında çalışır: her isteği o da alır,
cevabını verir, cevap **kaydedilir ama kullanılmaz**. Müşteri yalnızca eski
modelin cevabını görür:

```python
served = old.predict(X)
shadow = new.predict(X)
print("different answers:", int((served != shadow).sum()))
print("churn share:", served.mean(), "vs", shadow.mean())
scores = [round(accuracy(model, today), 3) for model in (old, new)]
print("later, with labels:", scores)
```

```text
different answers: 298
churn share: 0.586 vs 0.456
later, with labels: [0.685, 0.821]
```

İlk iki satır etiket **beklemeden** görülür: iki model 298
müşteride farklı karar veriyor ve yeni model çok daha az iptal bekliyor.
Bu kadar büyük bir fark ne iyi ne kötüdür; yalnızca "dikkatle bak" der.
Etiketler gelince üçüncü satır kararı verir: yeni model açık ara iyi.

Gölgenin bedeli iki kat hesaplamadır, riski ise sıfırdır. Yeni modelin
canlı ortamda **çalıştığını** (hata vermediğini, zamanında cevap
verdiğini) da gösterir; çevrimdışı sınama bunu gösteremez.

## Kanarya

Kanaryada trafiğin küçük bir payı yeni modele gider; sorun yoksa pay adım
adım büyür: %1, %5, %25, %50, %100. Adı madencilerin ocağa götürdüğü
kanaryadan gelir: tehlikeyi önce o fark eder.

Kim yeni modele gidecek? Her istekte zar atmak (`random.random()`) aynı
müşteriyi bir eski bir yeni modele gönderir; müşteri tutarsız cevaplar
görür. Bunun yerine müşterinin kimliğinden bir **kova** hesaplanır:

```python
def route(customer_id, percent):
    bucket = zlib.crc32(str(customer_id).encode()) % 100
    return "new" if bucket < percent else "old"


for percent in [1, 5, 25, 50]:
    count = sum(route(r["id"], percent) == "new" for r in today)
    print(f"{percent:>3}% -> {count} customers")
```

```text
  1% -> 8 customers
  5% -> 39 customers
 25% -> 238 customers
 50% -> 491 customers
```

`zlib.crc32` aynı kimliğe her zaman aynı sayıyı verir (Büyük Veri
patikasındaki bölmeyle aynı fikir); müşteri hep aynı modelde kalır. Bir
artısı daha var: kovası 5'ten küçük olan 25'ten de küçüktür, yani %5'te
yeni modeli gören müşteri %25'te de onu görmeye devam eder. Sayılar
yüzdeye tam oturmaz; kovalar 1000 müşteriye tam eşit dağılmaz.

## Kanaryada bozuk bir model

Diyelim ki yeni modelin sunucusunda Eğitim-Sunma Farkı bölümündeki hata
var: sütunlar ters sırayla gidiyor. Kanaryanın her aşamasında sağlam yeni
model ile bozuk olanı aynı müşterilerde ölçelim:

```python
def healthy(rows):
    return new.predict([features(r) for r in rows])


def broken(rows):
    return new.predict([features(r)[::-1] for r in rows])


def canary_score(predict, rows, percent):
    canary = [r for r in rows if route(r["id"], percent) == "new"]
    hits = sum(p == r["churned"] for p, r in zip(predict(canary), canary))
    return len(canary), round(hits / len(canary), 3)


for percent in [1, 5, 25]:
    n, good = canary_score(healthy, today, percent)
    bad = canary_score(broken, today, percent)[1]
    print(f"{percent:>3}% n={n:<4} healthy {good:.3f} broken {bad:.3f}")
```

```text
  1% n=8    healthy 0.875 broken 0.500
  5% n=39   healthy 0.795 broken 0.538
 25% n=238  healthy 0.832 broken 0.529
```

Bozuk model her aşamada kötü görünüyor; %1'de bile. Ama %1'de kanaryada
yalnızca 8 müşteri var. Aynı %1'i on gün boyunca, her gün yeni
müşterilerle tekrarlayalım:

```python
for day in range(1, 11):
    rows = make_customers(1000, seed=99 + day, month=6)
    good = canary_score(healthy, rows, 1)[1]
    bad = canary_score(broken, rows, 1)[1]
    print(f"day {day:>2}: healthy {good:.3f} broken {bad:.3f}")
```

```text
day  1: healthy 0.750 broken 0.375
day  2: healthy 0.750 broken 0.125
day  3: healthy 0.875 broken 0.000
day  4: healthy 0.750 broken 0.500
day  5: healthy 0.750 broken 0.250
day  6: healthy 0.500 broken 0.375
day  7: healthy 0.750 broken 0.750
day  8: healthy 1.000 broken 0.750
day  9: healthy 1.000 broken 0.250
day 10: healthy 0.625 broken 0.375
```

Sekiz müşteride bozuk modelin skoru 0,000 ile 0,750
arasında oynuyor; 7. gün sağlam modelle **aynı** skoru alıyor ve o gün
bakan biri onu bir sonraki aşamaya geçirirdi. Ters yön de var: sağlam
model 6. gün 0,500 alıyor, eski modelin altında; o gün bakan
biri iyi modeli geri çekerdi. Bugünkü %1'lik sonuca da bu yüzden
güvenilemez. %5'te 39, %25'te 238 müşteriyle fark açıkça
görünür.

Buradan iki kural çıkar: her aşamada karar vermeden önce **en az kaç
müşteri** gerektiği önceden yazılır; aşama ancak o kadar müşteri
görülünce geçilir. Ve kanarya yalnızca doğruluğa bakmaz: etiketler geç
gelir, o yüzden hata oranı, gecikme ve tahmin dağılımı (İzleme bölümü)
etiketsiz de izlenir. Bozukluk %5'te yakalanırsa etkilenen 39
müşteri olur; model doğrudan yayınlansaydı 1000 müşterinin hepsi olurdu.

## A/B testi

A/B testinde müşteriler rastgele iki gruba bölünür: A eski modeli, B yeni
modeli görür ve bir ölçü karşılaştırılır. Asıl soru şu: aradaki fark
**gerçek mi, şans mı**?

Bunu ölçmenin dürüst yolu bir **A/A testi**dir: iki gruba **aynı** modeli
koyup aradaki farka bakmak. Model aynı olduğu için her fark şanstır.
Grup boyunu değiştirerek 200 kez tekrarlayalım:

```python
for n in [100, 400, 1600]:
    gaps = []
    for s in range(200):
        a = make_customers(n, seed=1000 + s, month=6)
        b = make_customers(n, seed=5000 + s, month=6)
        gaps.append(abs(accuracy(old, a) - accuracy(old, b)))
    gaps.sort()
    print(f"n={n:<5} 95% of gaps below {gaps[int(0.95 * len(gaps))]:.3f}")
```

```text
n=100   95% of gaps below 0.130
n=400   95% of gaps below 0.062
n=1600  95% of gaps below 0.034
```

Aynı model, yalnızca şansla, grup başına 100 müşteride 0,13
kadar fark gösterebiliyor. Grup **dört kat** büyüyünce gürültü yaklaşık
**yarıya** iniyor. Bizim iki modelimiz arasındaki fark (0,685 → 0,821)
bu gürültünün çok üstünde. Ama gürültü bu hızla inerse 0,01'e ancak grup
başına on binden fazla müşteride iner: küçük bir iyileşmeyi görmek uzun
bir test ister. Önce gürültü ölçülür, sonra test ne kadar
süreceğine karar verilir: farkı gördüğün anda durmak, şansın en büyük
olduğu anda durmaktır.

Gerçek A/B testlerinde karşılaştırılan ölçü çoğu zaman doğruluk değil, bir
**iş ölçüsüdür** (iptal oranı, gelir): model iptal edeceğini düşündüğü
müşteriye indirim teklif ediyorsa, modelin kararı sonucu da değiştirir.
Bunu yalnızca canlıdaki bir deney ölçebilir.

## Hangisi ne zaman?

| Yöntem | Ne zaman | Dikkat |
|---|---|---|
| Gölge | Her yeni modelde, önce | İki kat hesaplama; sonucu değiştiren kararları ölçemez |
| Kanarya | Gölgeden sonra, yayının kendisi | Aşama başına en az müşteri sayısı; etiketsiz ölçüler |
| A/B testi | "Gerçekten daha iyi mi?" sorusu için | Önce A/A ile gürültü; süre önceden belirlenir |

Çoğu ekip üçünü sırayla kullanır: gölgede çalıştığını görür, kanaryada
bozuk olmadığını görür, A/B testinde gerçekten iyi olduğunu ölçer.

## Özet

- Kapı çevrimdışıdır; canlıya alma ayrıca ölçülerek yapılır.
- **Gölge:** yeni model her isteği görür, cevabı kullanılmaz. Risk yok,
  ayrışma etiketsiz görülür.
- **Kanarya:** trafiğin küçük payı yeni modele, pay adım adım büyür.
  Müşteri kimliğinden kova (`crc32 % 100`): aynı müşteri hep aynı modelde.
- Dersteki ölçüm: %1'de 8 müşteri var; bozuk modelin skoru günden güne
  0,000 ile 0,750 arasında oynadı. Aşama başına en az müşteri sayısı
  önceden yazılır.
- **A/B testi:** fark gerçek mi? Önce **A/A testiyle** gürültü ölçülür;
  grup dört kat büyüyünce gürültü yarıya iner.
- Gerçek A/B testleri çoğu zaman bir iş ölçüsünü karşılaştırır.
