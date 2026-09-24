**Ne soruluyor?** Hangi $\mathbf{x}$ vektörünü bu matrisle çarparsak $(7, 2)$ çıkar? Bilinmeyenler vektörün iki bileşeni.

**Fikir:** Matris-vektör çarpımında sonucun her bileşeni, matrisin bir satırıyla $\mathbf{x}$'in nokta çarpımı (satır bakışı). Her satırı sağdaki sayıya eşitlersek iki bilinmeyenli iki denklem çıkar.

**Adım 1 — Satırları denkleme çevir.**

- 1. satır $(2, 1)$: $\ 2x_1 + 1 \cdot x_2$, bu $7$ olmalı.
- 2. satır $(1, -1)$: $\ 1 \cdot x_1 - x_2$, bu $2$ olmalı.

$$
\begin{aligned}
2x_1 + x_2 &= 7 \\
x_1 - x_2 &= 2
\end{aligned}
$$

**Adım 2 — Denklemleri topla.** Birinde $+x_2$, ötekinde $-x_2$ var; toplayınca birbirini götürür ve tek bilinmeyen kalır:

$$
\begin{aligned}
(2x_1 + x_2) + (x_1 - x_2) &= 7 + 2 \\
3x_1 &= 9 \\
x_1 &= 3
\end{aligned}
$$

**Adım 3 — $x_2$'yi bul.** $x_1 = 3$'ü ikinci denkleme koy:

$$
\begin{aligned}
3 - x_2 &= 2 \\
x_2 &= 1
\end{aligned}
$$

**Sağlama:** Matrisle çarpıp gerçekten $(7, 2)$ çıkıyor mu bak:

$$
\begin{aligned}
2 \cdot 3 + 1 \cdot 1 &= 7 \\
1 \cdot 3 - 1 \cdot 1 &= 2
\end{aligned}
$$

İkisi de tutuyor. ✓

**Cevap:** $x_1 = 3$, $x_2 = 1$.
