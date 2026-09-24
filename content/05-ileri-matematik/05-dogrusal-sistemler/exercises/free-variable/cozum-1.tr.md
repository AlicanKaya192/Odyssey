**Ne soruluyor?** Sonsuz çözümlü bir sistemin **bütün** çözümlerini bir parametreyle yazıp, içinden $z = 1$ olanı seçmek.

**Fikir:** Eleme sonunda pivotu olmayan sütun serbest değişken olur. Ona $t$ deyip ötekileri geri yerine koymayla $t$ cinsinden yazarız.

**Adım 1 — Artırılmış matris.**

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 5 \\ 2 & 3 & 3 & 13 \\ 1 & 2 & 1 & 8 \end{array}\right]
$$

**Adım 2 — 1. sütunu temizle.** $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 5 \\ 0 & 1 & -1 & 3 \\ 0 & 1 & -1 & 3 \end{array}\right]
$$

**Adım 3 — 2. sütunu temizle.** $R_3 \to R_3 - R_2$: son satır tamamen sıfır.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 5 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right]
$$

$0 = 0$: çelişki yok ama bilgi de yok. 3. sütunda pivot yok, $z$ serbest.

**Adım 4 — $z = t$ ile geri yerine koy.**

$$
\begin{aligned}
y &= 3 + z = 3 + t \\
x &= 5 - y - 2z \\
&= 5 - (3 + t) - 2t \\
&= 2 - 3t
\end{aligned}
$$

Bütün çözümler: $(2 - 3t,\ 3 + t,\ t)$.

**Adım 5 — $z = 1$ seç.** $t = 1$: $x = 2 - 3 = -1$, $y = 3 + 1 = 4$.

**Sağlama:** $(-1, 4, 1)$ üç denklemde: $-1 + 4 + 2 = 5$ ✓, $-2 + 12 + 3 = 13$ ✓, $-1 + 8 + 1 = 8$ ✓.

**Sonucu yorumla:** 3. denklem aslında 1. ve 2.'nin bir birleşimi ($R_3 = R_2 - R_1$); üç düzlem bir doğru boyunca kesişiyor ve $(2 - 3t,\ 3 + t,\ t)$ o doğru.

**Cevap:** $x = -1$, $y = 4$.
