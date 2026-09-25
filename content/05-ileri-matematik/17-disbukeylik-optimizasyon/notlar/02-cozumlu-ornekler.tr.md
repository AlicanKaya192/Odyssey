Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. İkinci türev testi

**Soru:** $f(x) = x^4 + x^2$ dışbükey mi?

$f''(x) = 12x^2 + 2 > 0$ her yerde: evet, hatta kesin dışbükey.

## 2. Dışbükey olmayan bir fonksiyon

**Soru:** $f(x) = x^3$ dışbükey mi?

$f''(x) = 6x$, $x < 0$'da negatif: hayır.

## 3. Kiriş testi

**Soru:** $f(x) = x^2$ için $a = 0$, $b = 4$, $t = \frac{1}{2}$ ile kiriş eşitsizliğini kontrol et.

$f(2) = 4$; kiriş $\frac{0 + 16}{2} = 8$. $4 \le 8$ ✓.

## 4. Hessian testi

**Soru:** $f(x, y) = x^2 + xy + y^2$ dışbükey mi?

$H = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, özdeğerler $3$ ve $1$: evet.

## 5. Kurallarla

**Soru:** $L(\mathbf{w}) = \sum_i (y_i - \mathbf{w} \cdot \mathbf{x}_i)^2 + \lVert \mathbf{w} \rVert^2$ dışbükey mi?

Her terim dışbükey bir fonksiyona ($u^2$) doğrusal bir ifade konmuş hâli; $\lVert \mathbf{w} \rVert^2$ de dışbükey. Toplam dışbükey.

## 6. Lagrange

**Soru:** $x + 2y = 4$ kısıtıyla $f = x^2 + y^2$'yi en küçük yap.

$(2x, 2y) = \lambda(1, 2)$: $x = \frac{\lambda}{2}$, $y = \lambda$. $\frac{\lambda}{2} + 2\lambda = 4$, $\lambda = \frac{8}{5}$: $\left(\frac{4}{5}, \frac{8}{5}\right)$, $f = \frac{16}{5}$.

## 7. Çarpanın anlamı

**Soru:** $x + y = c$ kısıtıyla $xy$'nin en büyük değeri $\frac{c^2}{4}$. $c = 10$'da $c$'ye göre türevi kaç, $\lambda$ ile karşılaştır.

$\frac{c}{2} = 5 = \lambda$ ✓.

## 8. Yerel en küçük

**Soru:** Dışbükey bir kaybın gradyanı $\mathbf{w}_0$'da sıfır. $\mathbf{w}_0$ hakkında ne söylenir?

Genel en küçük; daha iyi bir nokta yok.
