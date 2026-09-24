**Ne soruluyor?** Üç denklemi aynı anda sağlayan $x, y, z$.

**Fikir:** Artırılmış matrisi basamak biçimine getir (pivotların altını sıfırla), sonra en alttan başlayıp geri yerine koy.

**Adım 1 — Artırılmış matris.**

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 2 & -1 & 1 & 8 \\ 1 & 2 & -1 & -3 \end{array}\right]
$$

**Adım 2 — 1. sütunu temizle.** Pivot $1$. $R_2 \to R_2 - 2R_1$ ve $R_3 \to R_3 - R_1$. Örneğin 2. satır: $(2 - 2,\ -1 - 2,\ 1 - 2 \mid 8 - 8) = (0, -3, -1 \mid 0)$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & -3 & -1 & 0 \\ 0 & 1 & -2 & -7 \end{array}\right]
$$

**Adım 3 — Satırların yerini değiştir.** 2. sütunda pivot olarak $-3$ yerine $1$ kullanmak kesirleri önlüyor: $R_2 \leftrightarrow R_3$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & -2 & -7 \\ 0 & -3 & -1 & 0 \end{array}\right]
$$

**Adım 4 — 2. sütunu temizle.** $R_3 \to R_3 + 3R_2$: $(0,\ -3 + 3,\ -1 - 6 \mid 0 - 21)$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & -2 & -7 \\ 0 & 0 & -7 & -21 \end{array}\right]
$$

**Adım 5 — Geri yerine koy.** Alttan yukarı:

$$
\begin{aligned}
-7z &= -21 \;\Rightarrow\; z = 3 \\
y - 2z &= -7 \;\Rightarrow\; y = -7 + 6 = -1 \\
x + y + z &= 4 \;\Rightarrow\; x = 4 + 1 - 3 = 2
\end{aligned}
$$

**Sağlama:** Orijinal denklemlere koy: $2 - 1 + 3 = 4$ ✓, $4 + 1 + 3 = 8$ ✓, $2 - 2 - 3 = -3$ ✓.

**Cevap:** $x = 2$, $y = -1$, $z = 3$.
