Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Tablo hangi türden?

**Soru:** $x = 0, 1, 2, 3$ için A tablosu $3, 6, 12, 24$; B tablosu
$3, 6, 9, 12$. Hangisi üstel?

A'da oranlar sabit: $\frac{6}{3} = \frac{12}{6} = 2$. Üstel, $3 \cdot 2^x$.
B'de farklar sabit: $6 - 3 = 9 - 6 = 3$. Doğrusal, $3 + 3x$.

## 2. Başlangıç değeri ve çarpan

**Soru:** $f(x) = a \cdot b^x$ için $f(0) = 5$ ve $f(1) = 15$. $f(3)$ kaç?

$f(0) = a = 5$. $f(1) = 5b = 15$, yani $b = 3$.
$f(3) = 5 \cdot 27 = 135$.

## 3. İki noktadan

**Soru:** $f(1) = 6$ ve $f(3) = 54$. $a$ ile $b$ nedir?

Oranı al: $\frac{f(3)}{f(1)} = \frac{a b^3}{a b} = b^2 = 9$, yani $b = 3$
($b > 0$). $a \cdot 3 = 6$, $a = 2$.

## 4. Yüzdeyle büyüme

**Soru:** $5000$ TL yıllık yüzde $8$ bileşik faizle iki yılda kaç olur?

$5000 \cdot 1{,}08^2 = 5000 \cdot 1{,}1664 = 5832$ TL. Basit faizle
$5800$ olurdu; fark, faizin faizi.

## 5. Değer kaybı

**Soru:** $400\,000$ TL'lik bir araba her yıl yüzde $15$ değer kaybediyor.
İki yıl sonra değeri ne olur?

Çarpan $1 - 0{,}15 = 0{,}85$. $400\,000 \cdot 0{,}85^2 = 400\,000 \cdot
0{,}7225 = 289\,000$ TL.

## 6. Yarı ömür

**Soru:** Yarı ömrü $3$ gün olan $200$ gram maddeden $12$ gün sonra ne
kalır?

$\frac{12}{3} = 4$ yarı ömür: $200 \cdot \left( \frac{1}{2} \right)^4 =
\frac{200}{16} = 12{,}5$ gram.

## 7. İki katına çıkma

**Soru:** $500$ bakteri her $30$ dakikada ikiye katlanıyor. $3$ saat sonra
kaç bakteri olur?

$3$ saat $= 180$ dakika $= 6$ kez $30$ dakika. $500 \cdot 2^6 = 500 \cdot 64
= 32\,000$.

## 8. Üstel denklem

**Soru:** $8^x = 4^{x + 1}$ denklemini çöz.

Ortak taban $2$: $2^{3x} = 2^{2(x + 1)} = 2^{2x + 2}$. Üsleri eşitle:
$3x = 2x + 2$, $x = 2$. Sınama: $8^2 = 64$, $4^3 = 64$ ✓.

## 9. Sürekli büyüme

**Soru:** $2000$ TL yüzde $5$ sürekli faizle iki yılda kaç olur?

$2000 \cdot e^{0{,}05 \cdot 2} = 2000 \cdot e^{0{,}1} \approx 2000 \cdot
1{,}10517 \approx 2210{,}34$ TL.

## 10. Sigmoid

**Soru:** $\sigma(z) = \frac{1}{1 + e^{-z}}$ için $\sigma(0)$ ve
$\sigma(-2)$ kaç?

$\sigma(0) = \frac{1}{1 + 1} = 0{,}5$. $\sigma(-2) = \frac{1}{1 + e^2}
\approx \frac{1}{8{,}39} \approx 0{,}12$. Negatif puan, düşük olasılık.
