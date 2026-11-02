## SRM testi, her bölme için

Beklenen oran 50/50 değilse `f_exp` ile verilir:

```python
from scipy import stats


def srm_p(n_a, n_b, share_b=0.5):
    total = n_a + n_b
    expected = [total * (1 - share_b), total * share_b]
    return stats.chisquare([n_a, n_b], f_exp=expected).pvalue


print(f"{srm_p(24976, 23973):.1e}")
print(f"{srm_p(9030, 970, share_b=0.1):.3f}")
```

```text
5.8e-06
0.317
```

İkinci satırda 90/10 bir test: B'de 970 kişi, beklenen 1000. Bu fark şansla
açıklanabilir.

## SRM görülünce

1. Sonucu okuma, kararı beklet.
2. Kesim kesim bak: platform, tarayıcı, ülke, gün, yeni / eski kullanıcı.
3. Kayıt yolunu karşılaştır: iki grup aynı olay kodundan geçiyor mu?
4. Yönlendirme, önbellek, bot süzgeci, çökme kayıtlarına bak.
5. Neden düzeltilince testi **baştan** başlat; eski veriyle birleştirme.

## A/A testi ne zaman?

- Yeni bir deney sistemi kurulduğunda.
- Atama, kayıt ya da analiz kodu değiştiğinde.
- Sürekli: bazı ekipler trafiğin küçük bir kısmında hep bir A/A testi
  çalıştırır.
