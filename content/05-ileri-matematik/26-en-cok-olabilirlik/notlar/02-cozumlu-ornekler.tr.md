Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Oranın MLE'si

**Soru:** $20$ atışta $6$ yazı. $\hat{p}$?

$\hat{p} = \frac{6}{20} = 0{,}3$.

## 2. İki olabilirliği karşılaştırmak

**Soru:** $10$ atışta $7$ yazı. $L(0{,}7)$, $L(0{,}5)$'in kaç katı?

$L(0{,}7) = 0{,}7^7 \cdot 0{,}3^3 \approx 0{,}00222$,
$L(0{,}5) = 0{,}5^{10} \approx 0{,}000977$. Oran $\approx 2{,}28$.

## 3. Log-olabilirlik değeri

**Soru:** Aynı veride $\ell(0{,}7)$?

$7\ln 0{,}7 + 3\ln 0{,}3 \approx 7(-0{,}357) + 3(-1{,}204) \approx -6{,}11$.

## 4. Normal dağılım

**Soru:** Veri $2, 4, 9$. $\hat{\mu}$ ve $\hat{\sigma}^2$?

$\hat{\mu} = 5$. Sapmaların kareleri $9, 1, 16$; $\hat{\sigma}^2 =
\frac{26}{3} \approx 8{,}67$. (Yansız tahmin $\frac{26}{2} = 13$.)

## 5. Poisson

**Soru:** Günlük hata sayıları $2, 0, 3, 1, 4$. $\hat{\lambda}$?

$\hat{\lambda} = \bar{x} = \frac{10}{5} = 2$.

## 6. Üstel dağılım

**Soru:** Bekleme süreleri $2, 3, 5$ dakika. $\hat{\lambda}$?

$\bar{x} = \frac{10}{3}$, $\hat{\lambda} = \frac{3}{10} = 0{,}3$ (dakikada).

## 7. Neden logaritma?

**Soru:** Olasılığı $0{,}1$ olan $1000$ bağımsız olayın ortak olasılığı ve
logaritması?

$0{,}1^{1000} = 10^{-1000}$: bilgisayar bunu $0$ yapar. Logaritması
$1000 \ln 0{,}1 \approx -2302{,}6$: sorunsuz bir sayı.

## 8. Kare hata ve NLL

**Soru:** $y_i = \hat{y}_i + \varepsilon_i$, $\varepsilon_i \sim
\mathcal{N}(0, \sigma^2)$. NLL neye orantılı?

$-\ell = \frac{n}{2}\ln(2\pi\sigma^2) + \frac{1}{2\sigma^2}\sum (y_i -
\hat{y}_i)^2$; $\sigma$ sabitse kare hataların toplamıyla aynı yerde en
küçük.

## 9. Laplace düzeltmesi

**Soru:** $3$ atışta $3$ yazı. MLE ve Laplace tahmini?

MLE $\frac{3}{3} = 1$. Laplace $\frac{3 + 1}{3 + 2} = 0{,}8$.

## 10. Kategorik dağılım

**Soru:** Bir zar $10$ kez atıldı: $1$ iki kez, $2$ üç kez, $3$ bir kez,
$4$ hiç, $5$ iki kez, $6$ iki kez. $\hat{p}_4$ ve $\hat{p}_2$?

$\hat{p}_k = \frac{n_k}{n}$: $\hat{p}_4 = 0$, $\hat{p}_2 = 0{,}3$. Az
veride $0$ tahmini güvenilmez.
