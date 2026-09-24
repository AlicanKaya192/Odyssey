**Ne soruluyor?** Çok uzun bir süre sonra hava olasılıklarının oturduğu değerler ve oraya ne kadar hızlı varıldığı.

**Fikir:** Bugünün olasılıkları $\mathbf{p}$ ise yarınınki $M\mathbf{p}$. Uzun vadede olasılıklar bir günden ötekine **değişmez**: $M\mathbf{p} = \mathbf{p}$. Bu, $M$'nin özdeğeri $1$ olan özvektörü.

**Adım 1 — $(M - I)\mathbf{p} = \mathbf{0}$.**

$$
M - I = \begin{bmatrix} -0.1 & 0.5 \\ 0.1 & -0.5 \end{bmatrix}
$$

İlk satır: $-0.1x + 0.5y = 0$, yani $x = 5y$. (İkinci satır aynı bilgiyi veriyor.)

**Adım 2 — Özvektör.** $y = 1$ seçersek $(5, 1)$.

**Adım 3 — Olasılığa çevir.** Bileşenlerin toplamı $1$ olmalı; $(5, 1)$'i toplamına ($6$) böl:

$$
\mathbf{p} = \left( \frac{5}{6},\ \frac{1}{6} \right) \approx (0.833,\ 0.167)
$$

**Sağlama:** $M\mathbf{p}$'nin ilk bileşeni $0.9 \cdot \tfrac{5}{6} + 0.5 \cdot \tfrac{1}{6} = \tfrac{4.5 + 0.5}{6} = \tfrac{5}{6}$ ✓.

**Adım 4 — Öteki özdeğer.** Özdeğerlerin toplamı iz: $1 + \lambda_2 = 0.9 + 0.5 = 1.4$, yani $\lambda_2 = 0.4$. Çarpımla sına: $1 \cdot 0.4 = 0.4$ ve $\det M = 0.45 - 0.05 = 0.4$ ✓.

**Sonucu yorumla:** Başlangıç ne olursa olsun, $0.4^k$ hızla sıfıra gittiği için birkaç hafta sonra günlerin yaklaşık %83'ü güneşli. Başlangıçtaki farkın bir günde kalan payı $0.4$; bir haftada $0.4^7 \approx 0.002$.

**Cevap:** $\tfrac{5}{6}$ (yaklaşık $0.83$) ve $0.4$.
