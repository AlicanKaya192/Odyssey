Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Model

| Ne | Formül |
|---|---|
| skor | $z = w^\mathsf{T}x + b$ |
| sigmoid | $p = \sigma(z) = \frac{1}{1 + e^{-z}}$ |
| oran | $\frac{p}{1 - p} = e^{z}$ |
| log-oran | $\ln\frac{p}{1 - p} = z$ |
| katsayı etkisi | oran $\times\, e^{w_j}$ |
| karar sınırı | $w^\mathsf{T}x + b = 0$ |

## Birkaç sigmoid değeri

| $z$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|---|---|---|
| $\sigma(z)$ | $0{,}047$ | $0{,}119$ | $0{,}269$ | $0{,}5$ | $0{,}731$ | $0{,}881$ | $0{,}953$ |

$\sigma(-z) = 1 - \sigma(z)$, $\ \sigma'(z) = \sigma(z)(1 - \sigma(z))$.

## Kayıp ve gradyan

| Ne | Formül |
|---|---|
| log-loss (tek örnek) | $-[y\ln p + (1 - y)\ln(1 - p)]$ |
| $z$'ye göre türev | $p - y$ |
| $w$'ye göre gradyan | $(p - y)\,x$ |
| gradyan inişi | $w \leftarrow w - \eta\sum_i (p_i - y_i)x_i$ |
| softmax | $p_k = \frac{e^{z_k}}{\sum_j e^{z_j}}$ |
| çapraz entropi | $-\ln p_{\text{doğru}}$; gradyan $p_k - y_k$ |

## Pratik ipuçları

- $y = 1$ için kayıp $-\ln p$, $y = 0$ için $-\ln(1 - p)$.
- Log-loss'u çarpımdan da hesaplayabilirsin: $-\ln\prod(\text{doğru sınıfın olasılığı})$.
- Softmax'ta bütün skorlara aynı sabiti eklemek sonucu değiştirmez.
- Ayrılabilir veride ağırlıklar büyür; düzenlileştirme ekle.
