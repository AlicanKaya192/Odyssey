# scipy.stats

`scipy.stats` istatistiğin araç kutusu: olasılık dağılımları, özet ölçüler ve
hipotez testleri tek modülde. Matematik patikasında bu kavramların
**anlamını** öğrendin; bu bölüm onları **kodda** nasıl kullanacağını ve
çıktıyı nasıl okuyacağını anlatıyor. Bölümün en önemli dersi de bir kod
satırı değil: "p < 0,05" bir sonucu ne kanıtlar ne de çürütür. Bunu ölçerek
göreceğiz.

## Dağılım nesneleri

```python
from scipy import stats

height = stats.norm(loc=170, scale=8)
print(round(float(height.pdf(170)), 4), round(float(height.cdf(186)), 4))
print(round(float(height.sf(186)), 4), round(float(height.ppf(0.975)), 1))
print(height.rvs(size=3, random_state=1).round(1).tolist())
coin = stats.binom(n=10, p=0.5)
print(round(float(coin.pmf(5)), 4), round(float(coin.cdf(2)), 4))
```

```text
0.0499 0.9772
0.0228 185.7
[183.0, 165.1, 165.8]
0.2461 0.0547
```

`stats.norm(loc=ortalama, scale=sapma)` bir dağılım **nesnesi** kurar; bütün
dağılımlarda aynı metotlar var:

| Metot | Soru | Burada |
|---|---|---|
| `pdf(x)` / `pmf(k)` | bu değerin yoğunluğu / olasılığı | 10 atışta tam 5 tura: 0,2461 |
| `cdf(x)` | x **ya da daha azı** | 186 cm ve altı: %97,7 |
| `sf(x)` | x'ten **fazlası** (1 − cdf) | 186'nın üstü: %2,3 |
| `ppf(q)` | hangi değerin altında q kadar var (cdf'nin tersi) | %97,5'in sınırı: 185,7 |
| `rvs(size=, random_state=)` | rastgele örnek | tohumla tekrarlanabilir |

- `sf` küçük olasılıklarda `1 - cdf`'den daha kesindir.
- Sürekli dağılımda `pdf` bir olasılık **değildir**, yoğunluktur: 0,0499
  "170 cm olma olasılığı" demek değil. Olasılık bir **aralığın** alanıdır
  (`cdf(b) - cdf(a)`).

## Özet ölçüler

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(8)
times = rng.exponential(scale=10, size=500)
d = stats.describe(times)
print(d.nobs, round(float(d.mean), 2), round(float(d.variance), 1))
print(round(float(d.skewness), 2), round(float(np.median(times)), 2))
print(round(float(stats.sem(times)), 3), round(float(stats.iqr(times)), 2))
```

```text
500 9.67 90.8
1.88 6.87
0.426 10.36
```

- `describe` tek çağrıda sayı, ortalama, varyans, çarpıklık ve basıklık verir.
- Bekleme süreleri gibi sağa çarpık veride (çarpıklık 1,88) ortalama (9,67)
  medyandan (6,87) belirgin büyük: birkaç uzun bekleme ortalamayı çeker.
  "Tipik" değer için medyan daha dürüst.
- `sem` ortalamanın standart hatası: ortalamanın kendisinin ne kadar
  oynayabileceği. `iqr` ortadaki yarının genişliği; aykırılara dayanıklı.

## İki grubu karşılaştırmak: t-testi

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(9)
old = rng.normal(52, 10, 40)
new = rng.normal(58, 10, 40)
result = stats.ttest_ind(new, old)
welch = stats.ttest_ind(new, old, equal_var=False)
print(round(float(new.mean() - old.mean()), 2))
print(round(float(result.statistic), 3), round(float(result.pvalue), 4))
print(round(float(welch.pvalue), 4), result.pvalue < 0.05)
```

```text
4.33
1.988 0.0503
0.0505 False
```

- Veriyi biz ürettik, yani gerçeği biliyoruz: yeni tasarımın ortalaması
  **gerçekten** 6 puan yüksek. Örneklemde fark 4,33 çıktı.
- `ttest_ind` "iki grubun ortalaması aynı olsaydı bu kadar farkı görmek ne
  kadar olası?" sorusunu cevaplar: p = 0,0503. Eşik 0,05 ise "anlamlı değil".
- Yani gerçek bir fark varken test onu **kaçırdı**. 40 kişilik gruplar,
  10'luk sapma karşısında 6'lık farkı güvenle göstermeye yetmiyor.
  "Anlamlı değil" ≠ "fark yok".
- `equal_var=False` (Welch testi) iki grubun sapmasının eşit olduğunu
  varsaymaz; emin değilsen güvenli seçim budur. Burada sonuç neredeyse aynı.

## Güven aralığı: p'den daha çok şey söyler

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(9)
old = rng.normal(52, 10, 40)
new = rng.normal(58, 10, 40)
res = stats.ttest_ind(new, old)
low, high = res.confidence_interval(confidence_level=0.95)
print(round(float(low), 2), round(float(high), 2))
mean_ci = stats.t.interval(0.95, df=len(new) - 1,
                           loc=new.mean(), scale=stats.sem(new))
print([round(float(v), 2) for v in mean_ci])
```

```text
-0.01 8.66
[53.39, 58.96]
```

- Farkın %95 güven aralığı −0,01 ile 8,66 arası. Bu tek satır p değerinden
  daha fazlasını anlatıyor: fark **sıfır da olabilir, 8,7 puan da**. Veri
  ikisini ayırmaya yetmiyor; daha çok kişi gerekiyor.
- Aralık sıfırı içerdiği için p > 0,05 çıktı; ikisi aynı hesabın iki yüzü.
- `stats.t.interval` tek bir ortalamanın aralığını verir: yeni tasarımın
  ortalaması büyük olasılıkla 53,4–59,0 arasında.

## Kategorik veri: ki-kare

```python
import numpy as np
from scipy import stats

table = np.array([[90, 60],
                  [45, 105]])
res = stats.chi2_contingency(table)
print(round(float(res.statistic), 2), res.dof, f"{res.pvalue:.2e}")
print(res.expected_freq.round(1).tolist())
print((table[:, 0] / table.sum(axis=1)).round(2).tolist())
```

```text
26.07 1 3.29e-07
[[67.5, 82.5], [67.5, 82.5]]
[0.6, 0.3]
```

- Satırlar iki reklam, sütunlar "tıkladı / tıklamadı". Soru: tıklama oranı
  reklama bağlı mı?
- `expected_freq` bağımsızlık olsaydı beklenecek sayılar (her hücrede 67,5 ve
  82,5). Gözlenen ile beklenen arasındaki fark büyük: p = 3,29e-07.
- Oranlar %60 ve %30: fark hem anlamlı **hem büyük**. Her zaman ikisine de
  bak.

## İlişki: pearsonr ve spearmanr

```python
import numpy as np
from scipy import stats

x = np.arange(1, 21)
y = x ** 3
r, p = stats.pearsonr(x, y)
rho, p2 = stats.spearmanr(x, y)
print(round(float(r), 3), round(float(rho), 3))
rng = np.random.default_rng(10)
a = rng.normal(size=30)
b = rng.normal(size=30)
print(round(float(stats.pearsonr(a, b).pvalue), 3))
```

```text
0.922 1.0
0.026
```

- `pearsonr` **doğrusal** ilişkiyi ölçer: y = x³ kusursuz bir ilişki ama
  doğru değil, r = 0,922. `spearmanr` **sıralamaya** bakar: x büyüdükçe y hep
  büyüyor, ρ = 1,0.
- Sonra iki **ilgisiz** rastgele dizi: p = 0,026. Hiçbir ilişki yokken "anlamlı"
  çıktı. 0,05 eşiği, ilişki yokken her yirmi denemeden birinde yanlış alarm
  vermeyi zaten kabul ediyor.

## Çok test, çok yanlış alarm

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(11)
false_alarms = 0
for test in range(100):
    a = rng.normal(0, 1, 30)
    b = rng.normal(0, 1, 30)
    if stats.ttest_ind(a, b).pvalue < 0.05:
        false_alarms += 1
print(false_alarms)
print(round(0.05 / 100, 4))
```

```text
9
0.0005
```

- 100 kez **aynı** dağılımdan iki grup çekildi; gerçekte hiçbir fark yok. Yine
  de 9 test "anlamlı" dedi.
- Yirmi ölçüye bakıp tutanı raporlamak bu yüzden yanıltıcıdır. En basit
  düzeltme (Bonferroni): eşiği test sayısına böl, 100 test için 0,0005.
- Daha iyisi: neye bakacağını veriyi görmeden önce yaz.

## Özet

- Dağılım nesnesi: `pdf`/`pmf`, `cdf`, `sf`, `ppf`, `rvs(random_state=)`.
- Çarpık veride medyan; `describe`, `sem`, `iqr`.
- `ttest_ind(..., equal_var=False)`; "anlamlı değil" fark yok demek değil.
- Güven aralığı farkın büyüklüğünü ve belirsizliğini birlikte gösterir.
- `chi2_contingency` kategorik tablo; `pearsonr` doğrusal, `spearmanr`
  sıralı ilişki.
- Çok test yanlış alarm üretir; eşiği düzelt, hipotezi önceden yaz.
