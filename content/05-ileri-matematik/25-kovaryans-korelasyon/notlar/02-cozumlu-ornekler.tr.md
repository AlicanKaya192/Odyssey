Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Örneklem kovaryansı

**Soru:** $x = 2, 4, 6$ ve $y = 1, 3, 8$. $s_{xy}$?

$\bar{x} = 4$, $\bar{y} = 4$. Sapmalar $-2, 0, 2$ ve $-3, -1, 4$;
çarpımlar $6, 0, 8$, toplam $14$. $s_{xy} = \frac{14}{2} = 7$.

## 2. Korelasyon

**Soru:** Aynı veride $r$?

$s_x^2 = \frac{4 + 0 + 4}{2} = 4$, $s_x = 2$.
$s_y^2 = \frac{9 + 1 + 16}{2} = 13$, $s_y \approx 3{,}606$.
$r = \frac{7}{2 \cdot 3{,}606} \approx 0{,}97$.

## 3. Kısa formül

**Soru:** $E[X] = 2$, $E[Y] = 3$, $E[XY] = 7{,}5$. Kovaryans?

$7{,}5 - 2 \cdot 3 = 1{,}5$.

## 4. Birim değişikliği

**Soru:** Boy (cm) ile kilo (kg) arasında kovaryans $60$. Boy metreyle
ölçülürse kovaryans ve korelasyon ne olur?

Boy $0{,}01$ ile çarpılıyor: kovaryans $0{,}6$. Korelasyon değişmez.

## 5. Toplamın varyansı

**Soru:** $\operatorname{Var}X = 9$, $\operatorname{Var}Y = 16$,
$\operatorname{Cov}(X, Y) = 6$. $\operatorname{Var}(X + Y)$ ve
$\operatorname{Var}(X - Y)$?

$9 + 16 + 12 = 37$ ve $9 + 16 - 12 = 13$.

## 6. Korelasyondan kovaryans

**Soru:** $r = -0{,}4$, $\sigma_X = 5$, $\sigma_Y = 10$. Kovaryans?

$-0{,}4 \cdot 5 \cdot 10 = -20$.

## 7. Doğrusal dönüşüm

**Soru:** $\operatorname{Cov}(X, Y) = 2$. $\operatorname{Cov}(3X + 1,
-2Y)$? Korelasyon ne olur?

$3 \cdot (-2) \cdot 2 = -12$. Katsayılar zıt işaretli: korelasyonun
büyüklüğü aynı, işareti değişir.

## 8. Sıfır kovaryans, bağımlı değişkenler

**Soru:** $X$, $-2, -1, 1, 2$ değerlerini eşit olasılıkla alıyor;
$Y = |X|$. Kovaryans?

$E[X] = 0$. $E[XY] = \frac{-4 - 1 + 1 + 4}{4} = 0$. Kovaryans $0$; ama
$X$ bilinince $Y$ kesin biliniyor.

## 9. Kovaryans matrisi

**Soru:** $\operatorname{Var}X_1 = 1$, $\operatorname{Var}X_2 = 4$,
$\operatorname{Cov}(X_1, X_2) = 1{,}2$. Kovaryans matrisi ve $r$?

$\Sigma = \begin{pmatrix} 1 & 1{,}2 \\ 1{,}2 & 4 \end{pmatrix}$,
$r = \frac{1{,}2}{1 \cdot 2} = 0{,}6$.

## 10. İki modelin ortalaması

**Soru:** İki modelin hata varyansı $4$, hataların korelasyonu $0{,}5$.
Ortalamalarının hata varyansı?

$\frac{4 \cdot (1 + 0{,}5)}{2} = 3$. Tek modelden iyi, ama bağımsız
hatalardaki $2$'den kötü.
