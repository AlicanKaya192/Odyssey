Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## İki geçiş

| Geçiş | Yön | İş |
|---|---|---|
| ileri | girdi → çıktı | değerleri hesapla ve sakla |
| geri | çıktı → girdi | $\frac{\partial L}{\partial L} = 1$'den başla; gelen gradyan × yerel türev |

## Kapılar (gelen gradyan g)

| Düğüm | Girdilere giden |
|---|---|
| $a + b$ | $g$, $g$ |
| $a - b$ | $g$, $-g$ |
| $a \cdot b$ | $g b$, $g a$ |
| $\max(a, b)$ | büyüğe $g$, küçüğe $0$ |
| $\mathrm{ReLU}(z)$ | $z > 0$ ise $g$, değilse $0$ |
| $\sigma(z)$ | $g \, \sigma(1 - \sigma)$ |
| $e^z$ | $g \, e^z$ |
| dallanma | gelenlerin toplamı |

## Bir katman

$\mathbf{z} = W\mathbf{x} + \mathbf{b}$, $\mathbf{a} = \phi(\mathbf{z})$

| Türev | Formül |
|---|---|
| $\frac{\partial L}{\partial \mathbf{z}}$ | $\frac{\partial L}{\partial \mathbf{a}} \odot \phi'(\mathbf{z})$ |
| $\frac{\partial L}{\partial W}$ | $\frac{\partial L}{\partial \mathbf{z}} \, \mathbf{x}^\mathsf{T}$ |
| $\frac{\partial L}{\partial \mathbf{b}}$ | $\frac{\partial L}{\partial \mathbf{z}}$ |
| $\frac{\partial L}{\partial \mathbf{x}}$ | $W^\mathsf{T} \frac{\partial L}{\partial \mathbf{z}}$ |

## Sık kullanılan kayıplar

| Kayıp | $\frac{\partial L}{\partial \hat{y}}$ |
|---|---|
| $\frac{1}{2}(\hat{y} - y)^2$ | $\hat{y} - y$ |
| $(\hat{y} - y)^2$ | $2(\hat{y} - y)$ |

## Maliyet

| Konu | Açıklama |
|---|---|
| zaman | bir geri geçiş ≈ birkaç ileri geçiş |
| bellek | ileri geçişin ara değerleri saklanır |
| sayısal türev | ağırlık sayısı kadar ileri geçiş |

## Derin ağlar

| Sorun | Neden | Çare |
|---|---|---|
| sönen gradyan | çarpanlar $< 1$ (sigmoid $\le 0{,}25$) | ReLU, artık bağlantı, iyi başlangıç |
| patlayan gradyan | çarpanlar $> 1$ | kırpma, iyi başlangıç, normalizasyon |
