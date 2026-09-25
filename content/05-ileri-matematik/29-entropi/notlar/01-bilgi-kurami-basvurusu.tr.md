Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Formül |
|---|---|
| bilgi | $I(x) = -\log_2 p(x)$ |
| entropi | $H(P) = -\sum p(x)\log_2 p(x)$ |
| çapraz entropi | $H(P, Q) = -\sum p(x)\log_2 q(x)$ |
| KL ıraksaması | $D_{\mathrm{KL}}(P \parallel Q) = \sum p(x)\log_2\frac{p(x)}{q(x)}$ |
| ilişki | $H(P, Q) = H(P) + D_{\mathrm{KL}}(P \parallel Q)$ |
| bilgi kazancı | $H(\text{ebeveyn}) - \sum \frac{n_k}{n} H(\text{çocuk}_k)$ |
| şaşkınlık | $2^{H}$ (bit) ya da $e^{H}$ (nat) |

## Özellikler

- $0 \leq H(P) \leq \log_2 K$; en büyük değer düzgün dağılımda.
- $H(P, Q) \geq H(P)$, $D_{\mathrm{KL}} \geq 0$; eşitlik yalnızca $P = Q$
  iken.
- KL simetrik değil.
- $0 \log 0 = 0$; $p > 0$ iken $q = 0$ ise KL ve çapraz entropi sonsuz.

## Kullanışlı değerler

| $p$ | $-\log_2 p$ | $-\ln p$ |
|---|---|---|
| $1/2$ | $1$ | $0{,}693$ |
| $1/4$ | $2$ | $1{,}386$ |
| $0{,}9$ | $0{,}152$ | $0{,}105$ |
| $0{,}1$ | $3{,}322$ | $2{,}303$ |

$1$ bit $= \ln 2 \approx 0{,}693$ nat.

## Pratik ipuçları

- Tek-sıcak etikette çapraz entropi $= -\log q_{\text{doğru}}$.
- Çapraz entropiyi en küçük yapmak = KL'yi en küçük yapmak = MLE.
- Bilgi kazancında çocukların entropisini örnek sayısıyla ağırlıklandır.
