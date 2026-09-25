**Fikir:** Kaybı $w$'nin ikinci dereceden polinomu olarak aç; tepe noktası formülü en iyi $w$'yi, baş katsayı eğriliği verir.

**Adım 1 — Aç.**

$$
\begin{aligned}
L(w) &= (2 - w)^2 + (3 - 2w)^2 + \lambda w^2 \\
&= (5 + \lambda) w^2 - 16 w + 13
\end{aligned}
$$

**Adım 2 — Tepe.** $w = \frac{16}{2(5 + \lambda)} = \frac{8}{5 + \lambda}$: $\lambda = 0$'da $\frac{8}{5}$, $\lambda = 1$'de $\frac{4}{3}$.

**Adım 3 — Eğrilik.** $L'' = 2(5 + \lambda) = 12$.

**Neden aynı sonuç?** $w^2$'nin katsayısı $\sum x_i^2 + \lambda$: ceza parabolü dikleştiriyor (Hessian'a $2\lambda$ ekliyor) ve tepeyi sıfıra yaklaştırıyor. Çok değişkende aynı şey $X^\mathsf{T}X + \lambda I$ matrisiyle oluyor; $\lambda > 0$ olunca bu matris her zaman ters çevrilebilir.

**Cevap:** $\frac{8}{5}$, $\frac{4}{3}$, $12$.
