**Ne soruluyor?** Pozitif sonucun toplam olasılığı, pozitiften sonra hasta olma olasılığı ve ikinci pozitiften sonraki güncelleme.

**Fikir:** $P(+)$ toplam olasılıkla, sonsal Bayes kuralıyla; ikinci test için sonsal yeni önsel.

**Adım 1 — $P(+)$.** $0{,}98 \cdot 0{,}005 = 0{,}0049$ ve $0{,}03 \cdot 0{,}995 = 0{,}02985$. Toplam $0{,}03475$.

**Adım 2 — Sonsal.** $\frac{0{,}0049}{0{,}03475} \approx 0{,}141$.

**Adım 3 — İkinci test.** Önsel $p = 0{,}141$:

$$
\begin{aligned}
&\frac{0{,}98 \cdot 0{,}141}{0{,}98 \cdot 0{,}141 + 0{,}03 \cdot 0{,}859} \\
&= \frac{0{,}1382}{0{,}1382 + 0{,}0258} \approx 0{,}843
\end{aligned}
$$

**Sağlama:** Sonsal önselden ($0{,}005$) büyük ✓, ama tek testte yüzde $14$'te kalıyor: hastalık nadir.

**Dikkat:** İkinci testte önseli yine $0{,}005$ almak, birinci testin bilgisini atmak olur.

**Cevap:** $0{,}03475$; $\approx 0{,}141$; $\approx 0{,}843$.
