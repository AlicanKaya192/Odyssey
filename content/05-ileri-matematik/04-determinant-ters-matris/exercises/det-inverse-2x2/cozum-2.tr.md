**Fikir:** Formülü ezberlemesen de ters bulunabilir. $AA^{-1} = I$ demek, $A^{-1}$'in 1. sütunu $\mathbf{x}$ için $A\mathbf{x} = (1, 0)$, 2. sütunu $\mathbf{y}$ için $A\mathbf{y} = (0, 1)$ demek. İki küçük denklem sistemi çözüyoruz. Bu yol formülün **neden** doğru olduğunu da gösteriyor.

**Adım 1 — Determinant.** $\det A = 4 \cdot 6 - 7 \cdot 2 = 10$; sıfır değil, sistemlerin tek çözümü var.

**Adım 2 — 1. sütun: $A\mathbf{x} = (1, 0)$.** $\mathbf{x} = (p, r)$ için satır satır:

$$
\begin{aligned}
4p + 7r &= 1 \\
2p + 6r &= 0
\end{aligned}
$$

İkinci denklemden $p = -3r$. Birinciye koy:

$$
\begin{aligned}
4(-3r) + 7r &= 1 \\
-5r &= 1 \\
r &= -0.2
\end{aligned}
$$

ve $p = -3 \cdot (-0.2) = 0.6$.

**Adım 3 — 2. sütun: $A\mathbf{y} = (0, 1)$.** $\mathbf{y} = (q, s)$ için:

$$
\begin{aligned}
4q + 7s &= 0 \\
2q + 6s &= 1
\end{aligned}
$$

İkinci denklemi 2 ile çarpıp birinciden çıkar: $(4q + 7s) - (4q + 12s) = 0 - 2$, yani $-5s = -2$ ve $s = 0.4$. Birinci denklemden $4q = -7 \cdot 0.4 = -2.8$, $q = -0.7$.

**Adım 4 — Sütunları yan yana koy.**

$$
A^{-1} = \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}
$$

**Neden aynı sonuç?** Bu iki sistemi harflerle ($a, b, c, d$) çözseydin, paydada hep $ad - bc$ çıkacaktı; formül tam olarak bu hesabın kısaltması. Determinant sıfır olunca bu sistemlerin çözümü olmuyor, ters de o yüzden yok.

**Cevap:** $10$; $0.6$, $-0.7$, $-0.2$, $0.4$.
