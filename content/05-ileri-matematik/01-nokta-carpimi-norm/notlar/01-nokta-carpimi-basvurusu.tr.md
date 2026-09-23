Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Formül |
|---|---|
| Nokta çarpımı | $\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2 + \cdots + a_n b_n$ |
| Geometrik hâli | $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta$ |
| Uzunluk | $\|\mathbf{a}\| = \sqrt{\mathbf{a} \cdot \mathbf{a}}$ |
| Açı | $\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$ |
| Skaler izdüşüm | $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{b}\|}$ |
| Vektör izdüşüm | $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}$ |
| Kosinüs benzerliği | $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$, $-1$ ile $1$ arası |

## Özellikler

- $\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$
- $\mathbf{a} \cdot (\mathbf{b} + \mathbf{c}) = \mathbf{a} \cdot \mathbf{b} + \mathbf{a} \cdot \mathbf{c}$
- $(k\,\mathbf{a}) \cdot \mathbf{b} = k\,(\mathbf{a} \cdot \mathbf{b})$
- $\mathbf{a} \cdot \mathbf{a} = \|\mathbf{a}\|^2 \ge 0$
- Cauchy–Schwarz: $|\mathbf{a} \cdot \mathbf{b}| \le \|\mathbf{a}\|\,\|\mathbf{b}\|$
- $\|\mathbf{a} + \mathbf{b}\|^2 = \|\mathbf{a}\|^2 + 2\,\mathbf{a} \cdot \mathbf{b} + \|\mathbf{b}\|^2$

Son satır, $\mathbf{a} \cdot \mathbf{b} = 0$ iken Pisagor teoremine dönüşüyor.

## İşaret tablosu

| $\mathbf{a} \cdot \mathbf{b}$ | Açı | Anlamı |
|---|---|---|
| $> 0$ | $0° \le \theta < 90°$ | kabaca aynı yön |
| $= 0$ | $\theta = 90°$ | dik |
| $< 0$ | $90° < \theta \le 180°$ | kabaca zıt yön |

## Kosinüs değerleri

| $\theta$ | $0°$ | $30°$ | $45°$ | $60°$ | $90°$ | $120°$ | $135°$ | $180°$ |
|---|---|---|---|---|---|---|---|---|
| $\cos\theta$ | $1$ | $\approx 0.866$ | $\approx 0.707$ | $0.5$ | $0$ | $-0.5$ | $\approx -0.707$ | $-1$ |

## Normlar

| Norm | Formül | $(3, -4)$ |
|---|---|---|
| $L_1$ (Manhattan) | $\sum \lvert a_i \rvert$ | $7$ |
| $L_2$ (Öklid) | $\sqrt{\sum a_i^2}$ | $5$ |
| $L_\infty$ | $\max \lvert a_i \rvert$ | $4$ |

Her zaman $L_\infty \le L_2 \le L_1$.

## Pratik ipuçları

- Düzlemde $(p, q)$'ya dik bir vektör: $(-q, p)$.
- İki vektör aynı yöndeyse kosinüs benzerliği $1$; biri ötekinin pozitif katıdır.
- Birim vektörler arasında kosinüs benzerliği = düz nokta çarpımı.
- Bir vektörün $x$ bileşeni, $(1, 0)$ üzerindeki izdüşümüdür.
