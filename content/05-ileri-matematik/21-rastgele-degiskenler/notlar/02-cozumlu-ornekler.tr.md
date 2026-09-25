Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Eksik olasılık

**Soru:** $p(0) = 0{,}2$, $p(1) = 0{,}5$, $p(2) = c$. $c$ ve $E[X]$ nedir?

Toplam $1$: $c = 0{,}3$. $E[X] = 0 + 0{,}5 + 0{,}6 = 1{,}1$.

## 2. Beklenen değer ve varyans

**Soru:** $X$ $1, 2, 3$ değerlerini $0{,}2$; $0{,}5$; $0{,}3$ olasılıkla
alıyor. $E[X]$, $\operatorname{Var}(X)$ ve $\sigma$?

$E[X] = 0{,}2 + 1 + 0{,}9 = 2{,}1$. $E[X^2] = 0{,}2 + 2 + 2{,}7 = 4{,}9$.
$\operatorname{Var}(X) = 4{,}9 - 4{,}41 = 0{,}49$, $\sigma = 0{,}7$.

## 3. Adil oyun

**Soru:** $5$ lira verip iki kez yazı tura atıyorsun; ikisi de tura gelirse
$20$ lira kazanıyorsun. Oyun adil mi?

$E[\text{kazanç}] = 20 \cdot \frac{1}{4} - 5 = 0$. Beklenen net kazanç $0$:
adil.

## 4. Doğrusallık

**Soru:** İkinci örnekteki $X$ için $E[3X + 2]$ ve
$\operatorname{Var}(3X + 2)$?

$3 \cdot 2{,}1 + 2 = 8{,}3$. $9 \cdot 0{,}49 = 4{,}41$; $+2$ varyansı
değiştirmez.

## 5. İki zarın toplamı

**Soru:** İki zarın toplamının beklenen değeri ve varyansı?

$E = 3{,}5 + 3{,}5 = 7$. Zarlar bağımsız: $\operatorname{Var} =
\frac{35}{12} + \frac{35}{12} = \frac{35}{6} \approx 5{,}83$.

## 6. Ortalamanın yayılımı

**Soru:** Standart sapması $10$ olan bir ölçüm $25$ kez bağımsız
tekrarlanıyor. Ortalamanın standart sapması?

$\frac{10}{\sqrt{25}} = 2$.

## 7. Sürekli değişken

**Soru:** $[0, 1]$'de $f(x) = 3x^2$. $P(X \leq 0{,}5)$, $E[X]$ ve
varyans?

$\int_0^{0{,}5} 3x^2 \, dx = 0{,}5^3 = 0{,}125$. $E[X] = \int_0^1 3x^3 \, dx
= \frac{3}{4}$. $E[X^2] = \frac{3}{5}$; varyans $\frac{3}{5} - \frac{9}{16}
= \frac{3}{80}$.

## 8. Tekdüze dağılım

**Soru:** $X$, $[0, 10]$'da tekdüze. $P(2 \leq X \leq 5)$, $E[X]$ ve
varyans?

Yoğunluk $\frac{1}{10}$: olasılık $\frac{3}{10}$. $E[X] = 5$, varyans
$\frac{100}{12} \approx 8{,}33$.

## 9. Dropout

**Soru:** Açık tutma olasılığı $p = 0{,}5$, nöron çıkışı $6$. Eğitimde
çıkışın beklenen değeri?

Açıksa $\frac{6}{0{,}5} = 12$, kapalıysa $0$: $0{,}5 \cdot 12 = 6$. Ölçek
korunmuş.

## 10. Farkın varyansı

**Soru:** Bağımsız $X$ ve $Y$ için $\operatorname{Var}(X) = 4$,
$\operatorname{Var}(Y) = 9$. $\operatorname{Var}(X - Y)$?

$\operatorname{Var}(X) + (-1)^2 \operatorname{Var}(Y) = 13$. Çıkarmak da
yayılımı artırır.
