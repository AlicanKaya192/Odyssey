**Fikir:** Önce kabul edilen tahmin aralığını bul, sonra o tahminleri veren girdileri. İki adımlı düşünmek, modelden bağımsız kısmı (tolerans) modele bağlı kısımdan (tahmin formülü) ayırıyor.

**Adım 1 — Kabul edilen tahminler.** Merkez $15$, yarıçap $3$:

$$
12 \le \hat{y} \le 18
$$

**Adım 2 — Sınır tahminleri veren girdiler.**

$$
\begin{aligned}
2x + 1 = 12 &\;\Rightarrow\; x = 5{,}5 \\
2x + 1 = 18 &\;\Rightarrow\; x = 8{,}5
\end{aligned}
$$

**Adım 3 — Aralık.** $\hat{y} = 2x + 1$, $x$ artınca artıyor; bu yüzden $12 \le \hat{y} \le 18$ tam olarak $5{,}5 \le x \le 8{,}5$ demek.

**Neden aynı sonuç?** Birinci yol tahmin formülünü koşulun içine koyup tek seferde çözdü; bu yol önce tahmin aralığını, sonra her sınırı ayrı çözdü. Tahmin artan bir fonksiyon olduğu için sınırlar sınırlara gidiyor.

**Cevap:** $5{,}5$ ve $8{,}5$.
