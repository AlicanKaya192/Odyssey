# Örneklem Büyüklüğü

Güç Analizi bölümünde "kaç kişi gerekir?" sorusunu `solve_power` ile
cevaplamayı gördük. Bu bölüm aynı hesabı bir deney planının içine koyuyor:
hangi metrik, hangi etki, hangi trafik, kaç hafta? Bir testin sonucunu
belirleyen kararların çoğu burada, test başlamadan verilir.

## Aynı göreli etki, çok farklı maliyet

Mağaza her metrikte **%5'lik göreli artışı** görmek istesin. Her metrik için
gereken kişi sayısı (grup başına, %80 güç, α = 0,05):

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower
from ab_data import make_user_log

users = make_user_log()
solver = TTestIndPower()
needed = {}
for col in ["bought", "minutes", "revenue"]:
    mean, sd = users[col].mean(), users[col].std()
    d = 0.05 * mean / sd
    n = solver.solve_power(effect_size=d, power=0.8, alpha=0.05)
    needed[col] = int(np.ceil(n))
    print(col, round(mean, 3), round(sd, 3), needed[col])
```

```text
bought 0.117 0.322 47209
minutes 21.096 23.273 7643
revenue 11.413 49.344 117372
```

Aynı %5 için süre metriğinde grup başına 7 643, satın almada
47 209, gelirde 117 372 kişi gerekiyor. Fark, Deney
Sorusu ve Metrik Seçimi bölümündeki değişim katsayısından geliyor: etki
büyüklüğü $d = 0{,}05 \cdot \bar{x} / s$, n ise $1/d^2$ ile büyüyor. Gelir
işin asıl amacı olabilir ama birincil metrik yapmak çok pahalı olabilir.

## Akılda hesap: 16 kuralı

%80 güç ve α = 0,05 için iki grup karşılaştırmasında kabaca:

$$n \approx \frac{16\, s^2}{\delta^2}$$

$\delta$ yakalamak istediğin mutlak fark, $s$ metriğin sapması. Satın alma
için:

```python
mean, sd = users["bought"].mean(), users["bought"].std()
delta = 0.05 * mean
print(int(np.ceil(16 * sd**2 / delta**2)))
```

```text
48117
```

`solve_power` ile çok yakın. 16 nereden geliyor? $2 \cdot (1{,}96 +
0{,}84)^2 \approx 15{,}7$: iki yönlü %5 için 1,96 ve %80 güç için 0,84
standart sapma. Plan toplantısında bilgisayarsız tahmin için yeterli.

## Elimizdeki trafikle neyi görebiliriz?

Soru çoğu zaman tersinden sorulur: günde 3000 farklı kullanıcı geliyor, test
iki hafta sürecek. Hangi etkiyi %80 güçle görebiliriz? Bu **en küçük
yakalanabilir etkidir** (MDE):

```python
n_group = 3000 * 14 // 2
d_min = solver.solve_power(nobs1=n_group, power=0.8, alpha=0.05)
for col in ["bought", "minutes", "revenue"]:
    mean, sd = users[col].mean(), users[col].std()
    print(col, f"{d_min * sd / mean:.1%}")
```

```text
bought 7.5%
minutes 3.0%
revenue 11.8%
```

İki haftada süre metriğinde küçük bir değişiklik bile görünür, ama gelirde
ancak %11,8 civarı bir artış güvenle yakalanır. Ekip gelirde
%2'lik bir artış umuyorsa bu test başlamadan başarısızdır: ya süre uzar ya
metrik değişir ya da varyans azaltılır (CUPED bölümü).

## Eşit olmayan bölme

Riskli bir değişikliği trafiğin yalnızca küçük bir kısmına göstermek
istenebilir. Ama aynı gücü korumak için toplam kişi artar:

```python
d = 0.05 * mean / sd
for share_b in [0.5, 0.2, 0.1]:
    ratio = share_b / (1 - share_b)
    n_a = solver.solve_power(effect_size=d, power=0.8, alpha=0.05,
                             ratio=ratio)
    n_a = int(np.ceil(n_a))
    n_b = int(np.ceil(n_a * ratio))
    print(share_b, n_a, n_b, n_a + n_b)
```

```text
0.5 47209 47209 94418
0.2 118022 29506 147528
0.1 236041 26227 262268
```

`ratio` B grubunun A'ya oranı. %20'lik bir B için toplam kişi 50/50'ye göre
yaklaşık %56 fazla, %10'luk bir B için yaklaşık
2,8 kat. Hesabı belirleyen küçük grup: onun gürültüsü büyük
kaldığı için öteki grubu büyütmek yalnızca biraz yardım eder.

## Kişiden haftaya

```python
def weeks_needed(n_per_group, daily_users, traffic=1.0):
    days = 2 * n_per_group / (daily_users * traffic)
    return int(np.ceil(days / 7))


print(weeks_needed(needed["bought"], 3000),
      weeks_needed(needed["bought"], 3000, traffic=0.5),
      weeks_needed(needed["revenue"], 3000))
```

```text
5 9 12
```

- Süre **tam haftaya** yuvarlanır: hafta içi ve hafta sonu davranışı
  farklıdır, yarım hafta bir günü fazla temsil eder.
- `traffic` deneye giren trafik payı: başka deneyler de çalışıyorsa ya da
  yalnızca ödeme sayfasına gelenler sayılıyorsa küçülür ve süre uzar.
- "Günde 3000 farklı kullanıcı" iyimser bir varsayım: aynı kişiler tekrar
  geldikçe yeni kullanıcı sayısı günlük ziyaretten yavaş büyür. Sayılan
  birim kullanıcıdır, ziyaret değil.

## Özet

- Aynı göreli etki için gereken kişi, metriğin değişim katsayısının
  karesiyle büyür; gelir pahalı, satın alma oranı daha ucuz.
- $n \approx 16 s^2 / \delta^2$ kabaca doğru bir akılda hesaptır.
- Trafik sabitse MDE hesaplanır; umulan etkiden büyükse plan değişir.
- Eşit olmayan bölme toplam kişiyi artırır.
- Süre tam haftaya yuvarlanır, sayılan birim kullanıcıdır.
