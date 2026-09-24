**Ne soruluyor?** İki veri noktası için kare hatayı en küçük yapan ağırlık ve o hata.

**Fikir:** Her kare $w$'ye göre ikinci dereceden; toplamları da öyle. Yukarı açılan bir parabolün en küçük değeri tepesinde, $w = -\frac{b}{2a}$'da.

**Adım 1 — Kareleri aç.**

$$
\begin{aligned}
(7 - 2w)^2 &= 49 - 28w + 4w^2 \\
(5 - w)^2 &= 25 - 10w + w^2
\end{aligned}
$$

**Adım 2 — Topla.**

$$
E(w) = 5w^2 - 38w + 74
$$

**Adım 3 — Tepe.**

$$
w = -\frac{-38}{2 \cdot 5} = \frac{38}{10} = 3{,}8
$$

**Adım 4 — En küçük hata.** Hataları doğrudan hesaplamak kolay: $7 - 2 \cdot 3{,}8 = -0{,}6$ ve $5 - 3{,}8 = 1{,}2$:

$$
E(3{,}8) = 0{,}36 + 1{,}44 = 1{,}8
$$

**Sonucu yorumla:** Birinci nokta $w = 3{,}5$'i, ikincisi $w = 5$'i istiyor; ikisini birden tam sağlayan $w$ yok. En iyi uzlaşma $3{,}8$ ve kalan hata $1{,}8$ sıfırdan büyük. Doğrusal regresyon tam olarak bu uzlaşmayı buluyor.

**Cevap:** $w = 3{,}8$; en küçük hata $1{,}8$.
