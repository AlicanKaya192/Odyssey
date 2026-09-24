**Ne soruluyor?** Her ev üç sayıyla anlatılmış bir nokta. İki nokta arasındaki düz uzaklığı iki kez hesaplayacağız: bir kez metrekareyle, bir kez yüz metrekareyle. Amaç birimin uzaklığı nasıl değiştirdiğini görmek.

**Fikir:** Öklid uzaklığı üç boyutta da iki boyuttaki gibi: fark vektörünü bul, bileşenlerin karelerini topla, karekökünü al. Bileşen sayısı arttı diye formül değişmiyor, yalnızca toplamaya bir terim daha ekleniyor.

**Adım 1 — Fark vektörü (metrekareyle).** Karşılıklı bileşenleri çıkar:

$$
\begin{aligned}
\mathbf{a} - \mathbf{b} &= (120 - 100,\ 3 - 4,\ 10 - 12) \\
&= (20,\ -1,\ -2)
\end{aligned}
$$

Okunuşu: 20 m² fark, 1 oda fark, 2 yıl fark.

**Adım 2 — Uzunluk.**

$$
\begin{aligned}
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{20^2 + (-1)^2 + (-2)^2} \\
&= \sqrt{400 + 1 + 4} \\
&= \sqrt{405} \approx 20.12
\end{aligned}
$$

**Adım 3 — Birimi değiştir.** Metrekareyi 100'e bölünce evler $\mathbf{a}' = (1.20,\ 3,\ 10)$ ve $\mathbf{b}' = (1.00,\ 4,\ 12)$ oluyor. Oda ve yaş değişmiyor:

$$
\mathbf{a}' - \mathbf{b}' = (0.20,\ -1,\ -2)
$$

**Adım 4 — Yeni uzunluk.**

$$
\begin{aligned}
\|\mathbf{a}' - \mathbf{b}'\| &= \sqrt{0.20^2 + (-1)^2 + (-2)^2} \\
&= \sqrt{0.04 + 1 + 4} \\
&= \sqrt{5.04} \approx 2.24
\end{aligned}
$$

**Sonucu yorumla:** İlk hesapta karekökün içindeki $405$'in $400$'ü metrekareden geldi; oda ve yaş farkı neredeyse hiç sayılmadı. Birimi değiştirince aynı iki ev yaklaşık 9 kat "yakınlaştı" ve bu kez oda ile yaş belirleyici oldu. **Evler değişmedi, yalnızca birim değişti.** Büyük sayılarla ölçülen özellik uzaklığa hâkim oluyor.

**Nerede karşına çıkar?** Uzaklık kullanan yöntemlerde (en yakın komşu, kümeleme) özellikler bu yüzden önce aynı ölçeğe getiriliyor.

**Cevap:** $20.12$ ve $2.24$.
