Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Tek adım

**Soru:** $L(w) = (w - 2)^2$, $w = 5$, $\eta = 0{,}1$. Bir adım sonra $w$?

$L'(5) = 6$; $5 - 0{,}6 = 4{,}4$.

## 2. Çarpan

**Soru:** Aynı kayıpta ($\lambda = 2$) $\eta = 0{,}1$ ile uzaklık her adımda kaç katına iner?

$1 - 0{,}2 = 0{,}8$.

## 3. Üst sınır

**Soru:** $L(w) = 5w^2$ için yakınsamayı sağlayan en büyük öğrenme oranı?

$\lambda = 10$; $\eta < \frac{2}{10} = 0{,}2$.

## 4. İki değişken

**Soru:** $f = x^2 + y^2$, $(3, 4)$, $\eta = 0{,}25$. Bir adım sonra?

$\nabla f = (6, 8)$; $(3 - 1{,}5; \ 4 - 2) = (1{,}5; \ 2)$.

## 5. Koşul sayısı

**Soru:** Hessian'ın özdeğerleri $50$ ve $0{,}5$. Koşul sayısı kaç?

$\frac{50}{0{,}5} = 100$.

## 6. Mini-batch

**Soru:** $10\,000$ örnek, $B = 100$. Bir epoch kaç adım?

$\frac{10\,000}{100} = 100$.

## 7. Momentum

**Soru:** $\beta = 0{,}9$, $\mathbf{v} = 2$, yeni gradyan $1$. Yeni $\mathbf{v}$?

$0{,}9 \cdot 2 + 1 = 2{,}8$.

## 8. Tanı

**Soru:** Kayıp birkaç adımda `nan` oldu. İlk ne değiştirilmeli?

Öğrenme oranı küçültülmeli (ya da gradyan kırpılmalı).
