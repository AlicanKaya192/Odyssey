Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Sigmoid değerleri

**Soru:** $\sigma(0)$, $\sigma(2)$, $\sigma(-2)$?

$0{,}5$; $\frac{1}{1 + e^{-2}} \approx 0{,}881$; $1 - 0{,}881 = 0{,}119$.

## 2. Oran ve log-oran

**Soru:** $p = 0{,}75$. Oran ve log-oran?

Oran $\frac{0{,}75}{0{,}25} = 3$; log-oran $\ln 3 \approx 1{,}099$.

## 3. Log-orandan olasılığa

**Soru:** $z = -1$. $p$?

Oran $e^{-1} \approx 0{,}368$; $p = \frac{0{,}368}{1{,}368} \approx 0{,}269$.

## 4. Katsayıyı yorumlamak

**Soru:** Bir özelliğin katsayısı $0{,}4$. Özellik bir birim artınca oran
ne olur?

$e^{0{,}4} \approx 1{,}49$ ile çarpılır; yaklaşık yüzde $49$ artar.

## 5. Karar sınırı

**Soru:** $z = 2x_1 - x_2 - 4$. $(3, 1)$ noktası hangi sınıfa atanır?

$z = 6 - 1 - 4 = 1 > 0$: sınıf $1$, $p = \sigma(1) \approx 0{,}731$.

## 6. Tek örnekte log-loss

**Soru:** $y = 0$, $p = 0{,}3$. Kayıp?

$-\ln(1 - 0{,}3) = -\ln 0{,}7 \approx 0{,}357$.

## 7. Ortalama log-loss

**Soru:** İki örnek: ($y = 1$, $p = 0{,}8$) ve ($y = 0$, $p = 0{,}4$).
Ortalama kayıp?

$-\ln 0{,}8 \approx 0{,}223$ ve $-\ln 0{,}6 \approx 0{,}511$; ortalama
$\approx 0{,}367$.

## 8. Gradyan

**Soru:** $x = (1, 3)$, $y = 0$, $p = 0{,}7$. Kaybın $w$'ye göre gradyanı?

$(p - y)x = 0{,}7 \cdot (1, 3) = (0{,}7; \ 2{,}1)$.

## 9. Softmax

**Soru:** Skorlar $(1, 1, 0)$. Olasılıklar?

$e, e, 1$; toplam $2e + 1 \approx 6{,}437$. $p \approx (0{,}422; \ 0{,}422;
\ 0{,}155)$.

## 10. Eşik seçimi

**Soru:** Bir hastalık için model $p = 0{,}3$ veriyor. Eşik $0{,}2$ seçildiyse
karar nedir?

$0{,}3 \geq 0{,}2$: "hasta olabilir", ileri teste gönderilir. Eşik $0{,}5$
olsaydı kaçırılırdı.
