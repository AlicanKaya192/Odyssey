**Fikir:** Aynı hesabı genel hâliyle kurup bir adım öteye gidelim: sıkıştırma hangi $k$'ye kadar gerçekten yer kazandırıyor? Cevabı bilmek, $k = 30$'un neden iyi bir seçim olduğunu gösteriyor.

**Adım 1 — Genel formül.** Rankı $k$ olan yaklaşım $k(m + n + 1)$, orijinal $mn$ sayı. Oran:

$$
\frac{k(m + n + 1)}{mn}
$$

**Adım 2 — $k = 30$ için.**

$$
\begin{aligned}
\frac{30 \cdot 1001}{400 \cdot 600} &= \frac{30\,030}{240\,000} \\
&\approx 0.125
\end{aligned}
$$

Yani %12.5; saklanan sayı $30\,030$.

**Adım 3 — Başa baş noktası.** Oran $1$'e ulaşınca kazanç biter:

$$
\begin{aligned}
k(m + n + 1) &= mn \\
k &= \frac{240\,000}{1001} \approx 240
\end{aligned}
$$

$k \approx 240$'tan sonra katmanları saklamak orijinalden daha çok yer tutuyor. Bu matrisin en fazla $400$ tekil değeri var (rank $\le \min(400, 600)$); ilk 30'u, başa baş noktasının sekizde biri.

**Neden işe yarar?** Kazancın kaynağı, her katmanın $m \times n$ sayı yerine $m + n + 1$ sayıyla anlatılması. Katman sayısı az kaldıkça bu çok büyük bir tasarruf.

**Cevap:** $30\,030$ ve $12.5$.
