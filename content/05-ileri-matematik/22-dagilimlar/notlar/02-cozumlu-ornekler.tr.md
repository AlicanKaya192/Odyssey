Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Bernoulli

**Soru:** Bir kullanıcının reklama tıklama olasılığı $0{,}2$. Tıklama
değişkeninin beklenen değeri ve varyansı?

$E = 0{,}2$, $\operatorname{Var} = 0{,}2 \cdot 0{,}8 = 0{,}16$.

## 2. Binom

**Soru:** $5$ kez yazı tura. Tam $2$ tura ve en az $1$ tura olasılığı?

$\binom{5}{2} \cdot 0{,}5^5 = \frac{10}{32} = 0{,}3125$. En az bir:
$1 - \frac{1}{32} = \frac{31}{32}$.

## 3. Binomun beklenen değeri

**Soru:** Bir üretimde parçaların yüzde $4$'ü hatalı. $100$ parçada
beklenen hatalı sayısı ve varyansı?

$np = 4$, $np(1 - p) = 4 \cdot 0{,}96 = 3{,}84$.

## 4. Poisson

**Soru:** Bir çağrı merkezine dakikada ortalama $2$ çağrı geliyor. Bir
dakikada hiç çağrı gelmemesi ve en fazla $1$ çağrı gelmesi olasılığı?

$P(0) = e^{-2} \approx 0{,}135$. $P(1) = 2e^{-2}$; en fazla bir:
$3e^{-2} \approx 0{,}406$.

## 5. Binomdan Poisson'a

**Soru:** $n = 20$, $p = 0{,}1$ binomunda $P(X = 0)$ ile $\lambda = 2$
Poisson'unda $P(X = 0)$'ı karşılaştır.

Binom $0{,}9^{20} \approx 0{,}122$, Poisson $e^{-2} \approx 0{,}135$.
Yakın; $n$ büyüyüp $p$ küçüldükçe daha da yaklaşır.

## 6. Üstel bekleme

**Soru:** Müşteriler dakikada ortalama $0{,}25$ hızla geliyor. Ortalama
bekleme ve $8$ dakikadan uzun bekleme olasılığı?

$\frac{1}{0{,}25} = 4$ dakika. $e^{-0{,}25 \cdot 8} = e^{-2} \approx 0{,}135$.

## 7. Hafızasızlık

**Soru:** Aynı yerde $5$ dakikadır müşteri gelmedi. En az $3$ dakika daha
gelmeme olasılığı?

Hafızasızlık: $P(X > 3) = e^{-0{,}75} \approx 0{,}472$; beklenen süre
$5$ dakikadan etkilenmez.

## 8. Normal ve 68–95–99,7

**Soru:** Bir testin puanları $\mathcal{N}(100, 15^2)$. $85$ ile $115$
arası ve $130$'dan yüksek puan alanların oranı?

$\mu \pm \sigma$: yaklaşık yüzde $68$. $130 = \mu + 2\sigma$:
$1 - 0{,}977 = 0{,}023$.

## 9. Standart normal

**Soru:** Aynı testte $P(X \leq 115)$ ve $P(X \leq 85)$?

$z = 1$: $0{,}841$. $z = -1$: $1 - 0{,}841 = 0{,}159$.

## 10. Tekdüze

**Soru:** Otobüs her saat başı geliyor ve durağa rastgele bir anda
geliyorsun; bekleme $[0, 60]$ dakikada tekdüze. $15$ dakikadan az bekleme
olasılığı ve ortalama bekleme?

$\frac{15}{60} = 0{,}25$; ortalama $30$ dakika.
