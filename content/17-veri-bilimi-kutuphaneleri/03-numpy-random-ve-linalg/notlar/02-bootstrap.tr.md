40 günlük satış ortalaması 117,5. Bu sayı ne kadar güvenilir; başka 40 gün
olsaydı ortalama ne kadar oynardı? **Bootstrap** bu soruyu formülsüz,
yalnızca rastgele örneklemeyle cevaplar: elimizdeki 40 günden **yerine
koyarak** binlerce kez 40 gün çekip her birinin ortalamasını alırız.

```python
import numpy as np

rng = np.random.default_rng(11)
sales = rng.normal(120, 30, size=40).round(1)
samples = rng.choice(sales, size=(5_000, sales.size), replace=True)
means = samples.mean(axis=1)
low, high = np.percentile(means, [2.5, 97.5])
print(round(float(sales.mean()), 1), samples.shape)
print(round(float(low), 1), round(float(high), 1))
print(bool(low < sales.mean() < high))
```

```text
117.5 (5000, 40)
109.8 125.1
True
```

## Adımlar

1. **Tek çağrıda 5000 örneklem:** `rng.choice(sales, size=(5000, 40),
   replace=True)` 5000 × 40'lık bir matris: her satır bir "başka 40 gün".
   Döngü yok.
2. **Her satırın ortalaması:** `mean(axis=1)` → 5000 ortalama.
3. **Ortadaki %95:** bu ortalamaların 2,5 ve 97,5 yüzdelikleri. Ortalama için
   %95 güven aralığı yaklaşık **109,8 – 125,1**.

## Neden yerine koyarak?

Yerine koymadan 40 günden 40 gün çekmek hep aynı günleri verir (sıra
değişir, ortalama aynı). Yerine koyunca bazı günler iki kez, bazıları hiç
gelmez; bu, "başka bir 40 gün olsaydı" belirsizliğini taklit eder.

## Tohumun rolü

`default_rng(11)` sayesinde aralık her çalıştırmada aynı çıkıyor; rapora
yazılan sayı yeniden üretilebilir. Tohumu değiştirince sınırlar biraz oynar
(5000 örneklemde birkaç ondalık); oynamanın büyüklüğü örneklem sayısını
artırmak gerekip gerekmediğini söyler.
