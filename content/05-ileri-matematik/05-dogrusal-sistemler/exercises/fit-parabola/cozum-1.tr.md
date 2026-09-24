**Ne soruluyor?** Bir modelin parametrelerini veriden bulmak. Makine öğrenmesinin temel işi bu; burada veri tam uyduğu için bir doğrusal sistem çözmek yetiyor.

**Fikir:** Her noktada $x$ bilinen bir sayı, dolayısıyla $x^2$ de bilinen bir katsayı. Bilinmeyenler $a, b, c$ ve her biri birinci kuvvetle geçiyor: **doğrusal** bir sistem.

**Adım 1 — Denklemleri yaz.** $x = 1, 2, 3$ için $a + bx + cx^2 = y$:

$$
\begin{aligned}
a + b + c &= 6 \\
a + 2b + 4c &= 11 \\
a + 3b + 9c &= 18
\end{aligned}
$$

**Adım 2 — Artırılmış matris ve 1. sütun.** $R_2 \to R_2 - R_1$, $R_3 \to R_3 - R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & 3 & 5 \\ 0 & 2 & 8 & 12 \end{array}\right]
$$

**Adım 3 — 2. sütun.** $R_3 \to R_3 - 2R_2$: $(0,\ 2 - 2,\ 8 - 6 \mid 12 - 10)$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & 3 & 5 \\ 0 & 0 & 2 & 2 \end{array}\right]
$$

**Adım 4 — Geri yerine koy.**

$$
\begin{aligned}
2c &= 2 \;\Rightarrow\; c = 1 \\
b + 3c &= 5 \;\Rightarrow\; b = 2 \\
a + b + c &= 6 \;\Rightarrow\; a = 3
\end{aligned}
$$

Model: $\hat{y} = 3 + 2x + x^2$.

**Adım 5 — Tahmin.**

$$
\hat{y}(4) = 3 + 2 \cdot 4 + 4^2 = 3 + 8 + 16 = 27
$$

**Sağlama:** Üç noktada: $3 + 2 + 1 = 6$ ✓, $3 + 4 + 4 = 11$ ✓, $3 + 6 + 9 = 18$ ✓.

**Cevap:** $a = 3$, $b = 2$, $c = 1$; tahmin $27$.
