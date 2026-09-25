**Fikir:** $v$, geçmiş gradyanların ağırlıklı toplamı: $v_{k+1} = g_k + \beta g_{k-1} + \beta^2 g_{k-2} + \cdots$. Bunu kullanarak her adımı doğrudan yaz.

**Adım 1 — Birinci.** $g_0 = 2$: $v_1 = 2$, $w_1 = 1 - 0{,}2 = 0{,}8$.

**Adım 2 — İkinci.** $g_1 = 1{,}6$: $v_2 = 1{,}6 + 0{,}9 \cdot 2 = 3{,}4$, $w_2 = 0{,}8 - 0{,}34 = 0{,}46$.

**Adım 3 — Üçüncü.** $g_2 = 0{,}92$: $v_3 = 0{,}92 + 0{,}9 \cdot 1{,}6 + 0{,}81 \cdot 2 = 0{,}92 + 1{,}44 + 1{,}62 = 3{,}98$, $w_3 = 0{,}46 - 0{,}398 = 0{,}062$.

**Adım 4 — Düz iniş.** $1 \cdot 0{,}8^3 = 0{,}512$.

**Neden aynı sonuç?** Açık toplam, özyinelemeli $v \leftarrow \beta v + g$ kuralının adım adım açılmış hâli. Açılım neden hızlandığını da gösteriyor: gradyanlar hep aynı işaretli olduğu sürece katkıları üst üste biniyor; tutarlı bir yönde etkin adım boyu yaklaşık $\frac{\eta}{1 - \beta} = 1$'e, yani on katına çıkabiliyor.

**Cevap:** $0{,}46$, $0{,}062$, $0{,}512$.
