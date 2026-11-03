# Çok Kollu Haydut

Klasik bir A/B testi trafiği baştan sona eşit böler: kötü olduğu ortaya
çıkan seçenek de test bitene kadar kullanıcıların üçte birini (ya da
yarısını) alır. Bu bölüm, trafiği test sürerken **iyi görünen seçeneğe
kaydıran** yöntemleri anlatıyor. Adı kumarhane makinelerinden gelir: her
seçenek ayrı bir kolu olan bir makine, amaç toplamda en çok kazanmak.
Kazanç gerçek ama bir bedeli var: ölçmek zorlaşır.

## Keşfetmek mi, kullanmak mı?

Üç başlık seçeneğimiz var; satın alma oranları gerçekte %5, %5,5 ve %6,5
(biz biliyoruz, algoritma bilmiyor). 30 000 ziyaretçi gelecek. İki yol:

- **Sabit bölme:** herkesi rastgele, eşit olarak üç kola dağıt (klasik
  A/B/C testi).
- **Thompson örneklemesi:** her kolun oranı için Bayesçi Bakışa Giriş
  bölümündeki Beta dağılımını tut; her ziyaretçi için her koldan bir değer
  çek ve en büyüğünü göster. Belirsiz kollar ara sıra kazanır (keşif), iyi
  görünen kol çoğu zaman kazanır (kullanım).

Gerçekte algoritma her ziyaretçiden sonra değil, toplu güncellenir; burada
her 500 ziyaretçide bir:

```python
import numpy as np

RATES = np.array([0.050, 0.055, 0.065])
VISITORS, BATCH = 30000, 500


def fixed_split(seed):
    rng = np.random.default_rng(seed)
    arm = rng.integers(0, 3, VISITORS)
    bought = rng.random(VISITORS) < RATES[arm]
    return np.bincount(arm, minlength=3), np.bincount(arm, bought, 3)


def thompson(seed):
    rng = np.random.default_rng(seed)
    n = np.zeros(3)
    k = np.zeros(3)
    for _ in range(VISITORS // BATCH):
        draws = rng.beta(1 + k, 1 + n - k, (BATCH, 3))
        arm = draws.argmax(axis=1)
        bought = rng.random(BATCH) < RATES[arm]
        n += np.bincount(arm, minlength=3)
        k += np.bincount(arm, bought, 3)
    return n, k


for name, method in [("fixed", fixed_split), ("thompson", thompson)]:
    n, k = method(1)
    print(name, n.astype(int).tolist(), int(k.sum()))
```

```text
fixed [10042, 9990, 9968] 1714
thompson [402, 1566, 28032] 1909
```

Sabit bölme her kola yaklaşık 10 000 kişi gönderiyor. Thompson
örneklemesi kısa sürede üçüncü kolun iyi olduğunu görüp ziyaretçilerin
çoğunu ona yönlendiriyor; en kötü kola yalnızca 402 kişi gidiyor.
Satışlar 1 714 yerine 1 909.

## Pişmanlık: kaybedilen satış

Tek bir koşu yanıltabilir. İki yöntemi 200 kez çalıştıralım. **Pişmanlık**
(regret), herkes baştan en iyi kola gönderilseydi beklenecek satışla
gerçekleşen satış arasındaki farktır:

```python
best = RATES.max() * VISITORS
for name, method in [("fixed", fixed_split), ("thompson", thompson)]:
    sales, right = [], 0
    for s in range(200):
        n, k = method(100 + s)
        sales.append(k.sum())
        right += (k / np.maximum(n, 1)).argmax() == 2
    print(name, round(float(np.mean(sales))), round(best - np.mean(sales)),
          right / 200)
```

```text
fixed 1698 252 1.0
thompson 1892 58 1.0
```

Sabit bölme ortalamada 252 satış kaybediyor, Thompson
örneklemesi 58. İkisi de sonunda en iyi kolu doğru buluyor
(%100). Haydut, testin **bedelini** küçültür.

## Bedel: ölçüm bozulur

Haydut kötü görünen kola az kullanıcı gönderdiği için o kolun tahmini hem
gürültülü hem de **yanlıdır**: şanssız bir başlangıç yapan kol bir daha pek
seçilmez ve düşük tahmini düzeltilemez. 200 koşunun ortalama tahminleri:

```python
est_fixed, est_ts = [], []
for s in range(200):
    n, k = fixed_split(100 + s)
    est_fixed.append(k / n)
    n, k = thompson(100 + s)
    est_ts.append(k / np.maximum(n, 1))
print(np.round(np.mean(est_fixed, axis=0), 4))
print(np.round(np.mean(est_ts, axis=0), 4))
```

```text
[0.05   0.0551 0.0647]
[0.0457 0.0526 0.0648]
```

Sabit bölmenin tahminleri gerçek oranlara (0,05, 0,055 ve 0,065) oturuyor.
Thompson örneklemesi en kötü kolun oranını ortalamada %4,57
olarak tahmin ediyor: gerçeğin altında. Haydutun verisiyle sıradan bir
z-testi ya da güven aralığı hesaplamak bu yüzden yanıltır; Rastgele Atama
bölümündeki "her kullanıcının her gruba düşme şansı aynı" şartı artık yok.

## Ne zaman haydut, ne zaman A/B testi?

| Durum | Uygun |
|---|---|
| Kısa ömürlü karar (bir kampanya başlığı, haftalık öneri) | haydut |
| Kaybedilen her dönüşüm pahalı, öğrenmek ikincil | haydut |
| Kalıcı ürün kararı, etkinin büyüklüğü raporlanacak | A/B testi |
| Koruma metrikleri ve uzun vadeli etki önemli | A/B testi |
| Seçenek sayısı çok ve sürekli değişiyor | haydut |

Haydut "hangisi en iyi?" sorusuna hızlı cevap verir; "ne kadar iyi?" sorusuna
güvenilir cevap vermez.

## Özet

- Çok kollu haydut trafiği test sürerken iyi görünen seçeneğe kaydırır.
- Thompson örneklemesi her kolun Beta dağılımından değer çekip en büyüğünü
  seçer: keşif ile kullanım dengelenir.
- Pişmanlık, en iyi kola göre kaybedilen satıştır; haydut onu büyük ölçüde
  küçültür.
- Bedeli: az seçilen kolların tahmini gürültülü ve yanlı olur; klasik
  testler doğrudan uygulanamaz.
