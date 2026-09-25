**Ne soruluyor?** Mini-yığın gradyanının gürültüsü ve dropout ölçeği.

**Fikir:** Bağımsız $n$ gözlemin ortalamasının standart sapması $\frac{\sigma}{\sqrt{n}}$; dropout beklenen çıkışı korur.

**Adım 1 — $64$ örnek.** $\frac{4}{\sqrt{64}} = \frac{4}{8} = 0{,}5$.

**Adım 2 — Yarısı.** $0{,}25 = \frac{4}{\sqrt{n}}$, $\sqrt{n} = 16$, $n = 256$.

**Adım 3 — Dropout.** $\frac{2}{0{,}8} = 2{,}5$. Beklenen değer $0{,}8 \cdot 2{,}5 + 0{,}2 \cdot 0 = 2$ ✓.

**Sağlama:** Standart sapmayı yarıya indirmek için örnek sayısı dört katına çıkıyor ($64 \to 256$) ✓.

**Dikkat:** Standart sapmayı $n$ ile bölmek ($\frac{4}{64}$); $n$ varyansı böler, standart sapmayı $\sqrt{n}$.

**Cevap:** $0{,}5$; $256$; $2{,}5$.
