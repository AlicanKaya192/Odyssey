Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Güncelleme kuralları

| Yöntem | Kural |
|---|---|
| gradyan inişi | $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$ |
| momentum | $\mathbf{v} \leftarrow \beta\mathbf{v} + \nabla L$, $\mathbf{w} \leftarrow \mathbf{w} - \eta \mathbf{v}$ |
| RMSProp | $\mathbf{s} \leftarrow \beta\mathbf{s} + (1 - \beta)\mathbf{g}^2$, $\mathbf{w} \leftarrow \mathbf{w} - \eta \dfrac{\mathbf{g}}{\sqrt{\mathbf{s}} + \epsilon}$ |
| Adam | momentum ($\mathbf{m}$) + RMSProp ($\mathbf{s}$) |

## Öğrenme oranı (eğriliği λ olan parabol)

| Durum | Çarpan $1 - \eta\lambda$ | Davranış |
|---|---|---|
| $0 < \eta < \frac{1}{\lambda}$ | $0$ ile $1$ arası | düzgün iniş |
| $\eta = \frac{1}{\lambda}$ | $0$ | tek adımda dip |
| $\frac{1}{\lambda} < \eta < \frac{2}{\lambda}$ | $-1$ ile $0$ arası | salınarak iniş |
| $\eta > \frac{2}{\lambda}$ | $< -1$ | ıraksama |

Çok değişkende $\lambda \to \lambda_{\max}$; yatık yönde ilerleme $1 - \eta\lambda_{\min}$ ile.

## Veri kullanımı

| Yöntem | Adım başına örnek |
|---|---|
| tam | hepsi |
| SGD | $1$ |
| mini-batch | $B$ |

Epoch: verinin bir kez tamamen geçilmesi. Adım sayısı $= \frac{n}{B}$ epoch başına.

## Belirtiler

| Kayıp eğrisi | Olası neden |
|---|---|
| çok yavaş iniyor | öğrenme oranı küçük; ölçekleme yok |
| zıplıyor, `nan` | öğrenme oranı büyük |
| dipte titriyor | mini-batch gürültüsü; oranı azalt |
| zikzak | koşul sayısı büyük; momentum ya da ölçekleme |

## Pratik ayarlar

- Momentum $\beta = 0{,}9$; Adam $\beta_1 = 0{,}9$, $\beta_2 = 0{,}999$.
- Öğrenme oranı takvimi ve ısınma; gradyan kırpma.
