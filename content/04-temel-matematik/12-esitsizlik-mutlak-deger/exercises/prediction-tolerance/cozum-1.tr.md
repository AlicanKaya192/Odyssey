**Ne soruluyor?** Bir modelin tahmininin hedefe yeterince yakın olduğu girdi aralığı.

**Fikir:** Tolerans koşulu bir mutlak değer eşitsizliği. Tahmin ifadesini yerine koyup çift eşitsizliğe çevirir, $x$'i ortada yalnız bırakırız.

**Adım 1 — Yerine koy.**

$$
|2x + 1 - 15| \le 3 \quad\Rightarrow\quad |2x - 14| \le 3
$$

**Adım 2 — Çift eşitsizlik.**

$$
-3 \le 2x - 14 \le 3
$$

**Adım 3 — $14$ ekle, $2$'ye böl.**

$$
\begin{aligned}
11 &\le 2x \le 17 \\
5{,}5 &\le x \le 8{,}5
\end{aligned}
$$

**Sağlama:** $x = 5{,}5$: $\hat{y} = 12$, $|12 - 15| = 3 \le 3$ ✓. $x = 8{,}5$: $\hat{y} = 18$, $|18 - 15| = 3$ ✓. $x = 7$: $\hat{y} = 15$, uzaklık $0$ ✓ (aralığın ortası).

**Sonucu yorumla:** Model hedefi tam $x = 7$'de tutturuyor; tahmin $x$'le $2$ kat hızlı değiştiği için $3$'lük tolerans $x$'te $1{,}5$'lik bir pay bırakıyor.

**Cevap:** $a = 5{,}5$, $b = 8{,}5$.
