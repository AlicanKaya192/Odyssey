| Yöntem | Ne zaman | NumPy ile | Dikkat |
|---|---|---|---|
| **Kategorik** | Sonlu sayıda seçenek (kelime, token, sınıf) | `np.searchsorted(np.cumsum(p), u, side="right")` ya da `rng.choice(k, p=p)` | Olasılıkların toplamı 1 olmalı |
| **Ters dönüşüm** | Birikimli fonksiyonu tersine çevrilebilen dağılım | Üstel: `-np.log(1 - u) / rate` | Formül her dağılımda yok |
| **Reddetme** | Yoğunluğu hesaplanabilen her şekil | `x[height < f(x)]` | Kabul oranı düşükse yavaş |
| **Histogram** | Elde yalnızca veri varsa | `np.histogram` + `rng.choice` + `rng.uniform` | Gözlenen aralığın dışına çıkmaz |
| **Monte Carlo** | Olasılığı ya da ortalamayı tahmin etmek | `(samples > limit).mean()` | Model kadar doğru |

**Tohum ve üreteç:**

```python
rng = np.random.default_rng(42)   # tek üreteç, sabit tohum
u = rng.random(5)                 # 0-1 arası düzgün sayılar
```

- Aynı üreteçten yapılan çağrıların **sırası** sonucu değiştirir: önce `x`,
  sonra `height` çekmek ile tersi farklı sayılar verir.
- Eski `np.random.seed(...)` + `np.random.rand(...)` yazımı programın her
  yerini etkileyen tek bir genel üreteç kullanır. Yeni kodda
  `default_rng` tercih edilir.

**Büyük sayılar yasası:** örnek sayısı arttıkça oranlar gerçek olasılığa
yaklaşır. Bu bölümde 20 çekilişte `this` (0,10) hiç gelmedi; 100 000
çekilişte oranlar tam oturdu.
