**Fikir:** $2 \times 2$'de iki özdeğerin toplamı izi, çarpımı determinantı verir. Toplamı ve çarpımı bilinen iki sayıyı bulmak çoğu zaman denklemi açmaktan hızlı.

**Adım 1 — İz.** Köşegen toplamı:

$$
\operatorname{tr} B = 4 + 3 = 7
$$

**Adım 2 — Determinant.**

$$
\det B = 4 \cdot 3 - 1 \cdot 2 = 10
$$

**Adım 3 — İki sayıyı bul.** $\lambda_1 + \lambda_2 = 7$ ve $\lambda_1 \lambda_2 = 10$. $10$'u çarpanlarına ayır: $1 \cdot 10$ (toplam 11), $2 \cdot 5$ (toplam 7) ✓.

$$
\lambda_1 = 2, \qquad \lambda_2 = 5
$$

**Adım 4 — Bir özvektörle sına.** $\lambda = 5$ için $B - 5I = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}$; $y = x$, yani $(1, 1)$. $B(1, 1) = (5, 5) = 5 \cdot (1, 1)$ ✓.

**Neden aynı sonuç?** Karakteristik denklem $\lambda^2 - (\operatorname{tr} B)\lambda + \det B = 0$; ikinci dereceden bir denklemde köklerin toplamı $-b/a$, çarpımı $c/a$. Kısayol bu kuralın ta kendisi.

**Cevap:** $2$ ve $5$.
