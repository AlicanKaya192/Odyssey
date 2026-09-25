Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Güven aralıkları

| Ne | Formül |
|---|---|
| ortalama ($\sigma$ biliniyor) | $\bar{x} \pm z^{*} \frac{\sigma}{\sqrt{n}}$ |
| ortalama (küçük $n$, $\sigma$ bilinmiyor) | $\bar{x} \pm t^{*} \frac{s}{\sqrt{n}}$ |
| oran | $\hat{p} \pm z^{*} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$ |
| gereken örneklem | $n \geq \left(\frac{z^{*}\sigma}{E}\right)^2$, yukarı yuvarla |

## Kritik değerler

| Güven düzeyi | $z^{*}$ | iki yönlü $\alpha$ |
|---|---|---|
| yüzde $90$ | $1{,}645$ | $0{,}10$ |
| yüzde $95$ | $1{,}96$ | $0{,}05$ |
| yüzde $99$ | $2{,}576$ | $0{,}01$ |

## Hipotez testi adımları

1. $H_0$ ve $H_1$'i yaz; tek mi iki yönlü mü, $\alpha$ kaç, önceden seç.
2. Test istatistiği: $z = \frac{\text{gözlenen} - H_0\text{'daki değer}}{\text{SE}}$.
3. p değeri: iki yönlüde $2 \cdot P(Z \geq |z|)$, tek yönlüde tek kuyruk.
4. $p < \alpha$ ise $H_0$ reddedilir; değilse reddedilemez.

## Hatalar

| | $H_0$ doğru | $H_0$ yanlış |
|---|---|---|
| reddet | I. tür ($\alpha$) | doğru |
| reddetme | doğru | II. tür ($\beta$) |

Güç $= 1 - \beta$.

## Pratik ipuçları

- İki bağımsız grup: $\text{SE}_{\text{fark}} = \sqrt{\text{SE}_1^2 + \text{SE}_2^2}$.
- Güven aralığı $\mu_0$'ı dışarıda bırakıyorsa test reddeder.
- $m$ test yapılıyorsa Bonferroni eşiği $\frac{\alpha}{m}$.
- "Reddedilemedi" ≠ "$H_0$ doğru".
