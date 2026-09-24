**Fikir:** Aynı çarpımı sütun gözüyle yapalım. $A\mathbf{x}$, $A$'nın sütunlarının $\mathbf{x}$'in bileşenleriyle ağırlıklı toplamı: 1. sütun $x_1$ kadar, 2. sütun $x_2$ kadar, 3. sütun $x_3$ kadar alınıp toplanıyor.

**Adım 1 — Sütunları ve ağırlıkları eşleştir.** $A$'nın sütunları $(1, 3)$, $(-2, 1)$, $(0, 2)$; $\mathbf{x}$'in bileşenleri $4$, $1$, $-1$:

$$
A\mathbf{x} = 4 \begin{bmatrix} 1 \\ 3 \end{bmatrix} + 1 \begin{bmatrix} -2 \\ 1 \end{bmatrix} + (-1) \begin{bmatrix} 0 \\ 2 \end{bmatrix}
$$

**Adım 2 — Her sütunu ağırlığıyla çarp.**

$$
\begin{aligned}
4 \cdot (1,\ 3) &= (4,\ 12) \\
1 \cdot (-2,\ 1) &= (-2,\ 1) \\
-1 \cdot (0,\ 2) &= (0,\ -2)
\end{aligned}
$$

**Adım 3 — Topla.** Üst bileşenler kendi arasında, alt bileşenler kendi arasında:

$$
\begin{aligned}
\text{üst} &= 4 - 2 + 0 = 2 \\
\text{alt} &= 12 + 1 - 2 = 11
\end{aligned}
$$

**Neden aynı sonuç?** Birinci yoldaki sayıların tamamı burada da var, yalnızca başka sırayla toplanıyor. Satır bakışı her bileşeni ayrı hesaplıyor; sütun bakışı ise sonucun $A$'nın sütunlarından **kurulduğunu** gösteriyor. İkinci bakış, ileride "bu denklemin çözümü var mı?" sorusunu anlamanın anahtarı.

**Cevap:** $(2, 11)$.
