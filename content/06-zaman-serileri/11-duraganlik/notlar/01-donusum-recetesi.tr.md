## Belirtiden dönüşüme

| Seride ne görüyorsun | Bozulan | Dönüşüm | Kod |
|---|---|---|---|
| Yükselen ya da alçalan düzey | Ortalama | Fark | `s.diff()` |
| Takvime bağlı desen | Ortalama | Mevsimsel fark | `s.diff(7)`, `s.diff(12)` |
| Düzeyle büyüyen dalga | Varyans | Logaritma | `np.log(s)` |
| Hem mevsim hem yavaş kayma | Ortalama | Mevsimsel fark + fark | `s.diff(12).diff()` |
| Hepsi birden | İkisi de | Logaritma → mevsimsel fark → fark | `np.log(s).diff(12).diff()` |

Her fark başta satır kaybettirir: `diff()` 1, `diff(12)` 12, ikisi birden 13.
Testten ve modelden önce `dropna()`.

## Geri dönüş

Model dönüştürülmüş seriyi tahmin eder; sonucu okumak için dönüşümleri **ters
sırayla** geri alırsın.

| Dönüşüm | Tersi |
|---|---|
| `d = s.diff()` | `s = d.cumsum() + s.iloc[0]` |
| `d = s.diff(7)` | `s[t] = d[t] + s[t - 7]` (son bilinen haftadan ileri doğru) |
| `y = np.log(s)` | `s = np.exp(y)` |
| `y = np.log(s).diff()` | `s = np.exp(y.cumsum()) * s.iloc[0]` |

Bir adımlık tahminde ters dönüşüm çok basit:

```python
# fark tahmini -> duzey
next_level = s.iloc[-1] + predicted_change

# mevsimsel fark tahmini -> duzey
next_level = s.iloc[-7] + predicted_change

# log fark tahmini -> duzey
next_level = s.iloc[-1] * np.exp(predicted_log_change)
```

Bölüm 17'de ARIMA bu geri dönüşü senin yerine yapıyor; farkın sayısını ona
`d` (düz fark) ve `D` (mevsimsel fark) diye söylüyorsun. Bu bölümde bulduğun
"kaç fark gerekiyor" cevabı doğrudan o iki sayı olacak.

## Logaritmanın farkı ve yüzde değişim

| Gerçek değişim | `pct_change()` | `np.log(s).diff()` |
|---|---|---|
| %1 artış | 0.0100 | 0.00995 |
| %5 artış | 0.0500 | 0.0488 |
| %10 artış | 0.1000 | 0.0953 |
| %50 artış | 0.5000 | 0.4055 |
| %50 düşüş | −0.5000 | −0.6931 |

Küçük değişimlerde ikisi neredeyse aynı. Log farkın iki üstünlüğü var:

- **Toplanabilir.** Günlük log farkların toplamı, dönemin toplam log
  değişimi. Yüzde değişimler toplanmaz (çarpılır).
- **Simetrik.** İki katına çıkmak +0.693, yarıya inmek −0.693. Yüzdeyle +%100
  ve −%50.

Sıfır ya da eksi değer içeren seride logaritma alınamaz. Sıfırlar varsa
`np.log1p(s)` (yani `log(1 + s)`) yaygın bir çözüm; tersi `np.expm1`.

## Kaç fark?

1. Seriyi çiz. Trend, mevsim, büyüyen dalga var mı?
2. Gerekiyorsa logaritma.
3. Mevsim varsa mevsimsel fark. Çiz, standart sapmaya bak.
4. Hâlâ kayma varsa düz fark. Çiz, standart sapmaya bak.
5. Standart sapma **yükseldiyse** son adımı geri al.
6. ADF ve KPSS ile doğrula.

Pratikte düz fark sayısı 0, 1, nadiren 2; mevsimsel fark 0 ya da 1. Daha
fazlası neredeyse her zaman hata.

Fazla farkın belirtileri: standart sapma artıyor; 1. gecikme korelasyonu −0.5
civarına iniyor; seri sıfırın etrafında testere gibi bir yukarı bir aşağı.

## Durağanlık gerekmeyen yerler

- **Ayrıştırma** (Bölüm 10): zaten trendi ve mevsimi ayırmak için var.
- **Üstel düzleştirme** (Bölüm 16): trendi ve mevsimi kendi içinde modelliyor.
- **Ağaç tabanlı makine öğrenmesi** (Bölüm 19): durağanlık şart değil, ama
  ağaçlar eğitimde görmediği düzeyi tahmin edemediği için fark almak yine de
  çoğu zaman yardımcı.

Durağanlığın **şart** olduğu yerler: ARIMA ailesi, otokorelasyon yorumu
(Bölüm 12), iki seri arasında korelasyon ve regresyon.
