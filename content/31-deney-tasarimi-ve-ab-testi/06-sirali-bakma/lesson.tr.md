# Sıralı Bakma Tuzağı ve Ardışık Test

Test iki hafta sürecek ama sonuç panosu her gün güncelleniyor. Üçüncü gün p
0,04'e iniyor; "anlamlı oldu, durduralım" demek çok çekici. Bu bölüm bu
alışkanlığın neden yanlış alarm oranını patlattığını ölçüyor ve testi
erken durdurmanın doğru yolunu gösteriyor: **ardışık test** (sequential
testing).

## Her gün p değeri

İki haftalık bir testte her günün sonunda, o güne kadar biriken
kullanıcılarla iki oran z-testi yapan bir fonksiyon:

```python
import numpy as np
from scipy import stats
from ab_data import make_experiment


def daily_p(test, days=14):
    is_b = (test["group"] == "B").to_numpy()
    day = test["day"].to_numpy()
    bought = test["bought"].to_numpy().astype(float)
    size = days + 1
    n_a = np.cumsum(np.bincount(day[~is_b], minlength=size))[1:]
    n_b = np.cumsum(np.bincount(day[is_b], minlength=size))[1:]
    k_a = np.cumsum(np.bincount(day[~is_b], bought[~is_b], size))[1:]
    k_b = np.cumsum(np.bincount(day[is_b], bought[is_b], size))[1:]
    pooled = (k_a + k_b) / (n_a + n_b)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (k_b / n_b - k_a / n_a) / se
    return 2 * stats.norm.sf(np.abs(z))


def simulate(reps, lift, first_seed):
    seeds = range(first_seed, first_seed + reps)
    return np.array([daily_p(make_experiment(n=14000, seed=s, lift=lift))
                     for s in seeds])
```

`np.bincount` her günün kullanıcı ve satın alma sayısını, `np.cumsum` o
güne kadarki toplamı veriyor; z, Oranları Karşılaştırmak bölümündeki
birleşik oranlı z-testi. `simulate` aynı deneyi farklı tohumlarla
tekrarlayıp her deneyin 14 günlük p değerlerini bir satıra koyuyor.

## Fark yokken her gün bakmak

500 A/A deneyi (B'nin hiçbir etkisi yok). Kaç kez bakılırsa, en az bir
bakışta p < 0,05 görme olasılığı ne olur?

```python
aa = simulate(500, 0.0, 1000)
for looks in [[14], [7, 14], list(range(2, 15, 2)), list(range(1, 15))]:
    hit = (aa[:, np.array(looks) - 1] < 0.05).any(axis=1)
    print(len(looks), round(float(hit.mean()), 3))
```

```text
1 0.046
2 0.08
7 0.172
14 0.228
```

- Yalnızca son gün bakılınca yanlış alarm %4,6: söz verilen %5.
- İki kez bakmak bunu %8,0, her gün bakmak %22,8
  yapıyor. Etkisiz bir değişiklik, her gün bakan bir ekipte yaklaşık dört
  testten birinde "kazandı" ilan ediliyor.

Neden? p değeri veri geldikçe rastgele dolaşır. Her bakış ona eşiğin
altına düşmek için yeni bir şans verir; "anlamlı olunca dur" kuralı da o
şansları toplar. Bu, Çoklu Karşılaştırma bölümündeki sorunun zaman
içindeki hâlidir: aynı testi tekrar tekrar yapmak.

## Çözüm: bakışları önceden planlamak

Erken durmak istiyorsak her bakışta daha **sıkı** bir eşik kullanırız,
öyle ki bütün bakışlar boyunca toplam yanlış alarm %5'te kalsın. İki yol:

- **Bonferroni:** α'yı bakış sayısına böl: 0,05 / 14. Basit ama fazla
  temkinli.
- **Ayarlanmış eşik:** A/A benzetimlerinde "14 bakışın en küçük p'si"nin
  dağılımına bakıp %5'lik dilimini eşik yap. Böylece toplam yanlış alarm
  tam %5'e oturur. (Bu, **Pocock** sınırı denen yöntemin benzetimle
  bulunmuş hâli.)

Eşiği bir benzetimle bulup **başka tohumlu yeni** 500 A/A deneyinde
sınayalım:

```python
bonferroni = 0.05 / 14
calibrated = np.quantile(aa.min(axis=1), 0.05)
print(round(bonferroni, 4), round(float(calibrated), 4))
fresh = simulate(500, 0.0, 5000)
for limit in [0.05, bonferroni, calibrated]:
    print(round(float((fresh.min(axis=1) < limit).mean()), 3))
```

```text
0.0036 0.0074
0.212
0.016
0.04
```

- Her gün 0,05'le bakmak yeni deneylerde de %21,2 yanlış
  alarm veriyor.
- Bonferroni %1,6: güvenli ama gereğinden sıkı; bakışlar
  birbirinden bağımsız değil (aynı veriler birikiyor), bu yüzden Bonferroni
  fazla öder.
- Ayarlanmış eşik (0,0074) yanlış alarmı %4,0
  düzeyinde tutuyor: %5'e yakın.

## Bedeli: güç

Erken durma hakkı bedava değildir. Gerçek bir etki varken (B satın almayı
%12 artırıyor) üç yolu karşılaştıralım:

```python
real = simulate(500, 0.12, 9000)
print(round(float((real[:, -1] < 0.05).mean()), 3))
for limit in [bonferroni, calibrated]:
    hit = real < limit
    stopped = hit.any(axis=1)
    first_day = hit.argmax(axis=1)[stopped] + 1
    print(round(float(stopped.mean()), 3), round(float(first_day.mean()), 1))
```

```text
0.736
0.5 8.4
0.584 7.7
```

- Yalnızca 14. günde bakan sabit test etkiyi %73,6 oranında
  yakalıyor.
- Her gün sıkı eşikle bakan testler etkiyi daha az yakalıyor
  (%50,0 ve %58,4), ama yakaladıklarında ayarlanmış
  eşikle ortalama 7,7 gün sonra duruyor.

Yani ardışık test bir değiş tokuştur: daha erken karar karşılığında aynı
süre için biraz güç. Gerçek ardışık tasarımlar (ör. **O'Brien–Fleming**
sınırları) başta çok sıkı, sonda 0,05'e yakın eşikler kullanarak bu kaybı
küçültür; günlük panolar için "her an geçerli" (always-valid) p değerleri
de kullanılır. Hepsinin ortak noktası: **kurallar test başlamadan
yazılır.**

## Pratikte

- Sabit süreli test: süre planda yazılı, p yalnızca sonda okunur.
- Panoda koruma metriklerini izlemek serbest: bir şey **bozuluyorsa**
  durmak (zararı kesmek) yanlış alarm sorunu yaratmaz, çünkü kazanç ilan
  edilmiyor.
- Erken "kazandı" demek isteniyorsa ardışık tasarım baştan seçilir ve
  eşikleri plana yazılır.
- Bayesçi Bakışa Giriş bölümünde gördüğümüz gibi Bayesçi yöntemde de durma
  kuralı önceden yazılmazsa yanlış kararların sıklığı artar.

## Özet

- Her bakış, p'ye eşiğin altına düşmek için yeni bir şans verir; her gün
  bakmak yanlış alarmı %5'ten %22,8 düzeyine çıkardı.
- Erken durmak için her bakışta daha sıkı eşik gerekir: Bonferroni fazla
  temkinli, benzetimle ayarlanmış eşik %5'i tutturur.
- Erken durma hakkının bedeli aynı süre için güç kaybıdır.
- Kurallar test başlamadan yazılır; koruma metrikleri için durmak serbest.
