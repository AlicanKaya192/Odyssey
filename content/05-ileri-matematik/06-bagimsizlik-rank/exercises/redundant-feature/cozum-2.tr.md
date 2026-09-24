**Fikir:** Önce çekirdeği bulalım; rank–sıfırlık teoremi ($\operatorname{rank} + \dim(\text{çekirdek}) = 3$) rankı verir.

**Adım 1 — Çekirdek denklemi.** $X(1, 0, c) = \mathbf{0}$, satır satır:

$$
\begin{aligned}
120 + 1.2c &= 0 \\
80 + 0.8c &= 0 \\
150 + 1.5c &= 0 \\
100 + 1.0c &= 0
\end{aligned}
$$

Dördü de aynı cevabı veriyor: $c = -100$. Çekirdekte sıfır olmayan bir vektör var, yani çekirdeğin boyutu en az 1.

**Adım 2 — Çekirdek daha büyük olabilir mi?** Boyutu 2 olsaydı rank $3 - 2 = 1$ olurdu, yani bütün sütunlar tek bir vektörün katı olurdu. Ama 1. ve 2. sütun orantılı değil ($120/3 = 40$, $150/4 = 37.5$). Öyleyse rank en az 2, çekirdeğin boyutu en fazla 1.

**Adım 3 — Rank.** Çekirdeğin boyutu tam 1:

$$
\operatorname{rank} X = 3 - 1 = 2
$$

**Makine öğrenmesiyle bağı:** Doğrusal regresyon $X^\mathsf{T}X$'i tersine çevirmeye çalışır. $X$ tam ranklı olmadığı için ($2 < 3$) $X^\mathsf{T}X$ tekil; kapalı formül çalışmaz. Kütüphaneler bu durumda ya hata verir ya da sonsuz çözümden birini (genellikle en küçük ağırlıklıyı) seçer.

**Cevap:** $2$ ve $-100$.
