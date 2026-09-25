**Ne soruluyor?** Eksik bir olasılık, beklenen değer ve varyans.

**Fikir:** Dağılımın toplamı $1$; beklenen değer ağırlıklı ortalama; varyans karelerin ortalaması eksi ortalamanın karesi.

**Adım 1 — $c$.** $0{,}1 + 0{,}3 + c + 0{,}2 = 1$, $c = 0{,}4$.

**Adım 2 — $E[X]$.** $0 \cdot 0{,}1 + 1 \cdot 0{,}3 + 2 \cdot 0{,}4 + 3 \cdot 0{,}2 = 0{,}3 + 0{,}8 + 0{,}6 = 1{,}7$.

**Adım 3 — Varyans.** $E[X^2] = 0{,}3 + 4 \cdot 0{,}4 + 9 \cdot 0{,}2 = 0{,}3 + 1{,}6 + 1{,}8 = 3{,}7$. $\operatorname{Var}(X) = 3{,}7 - 1{,}7^2 = 3{,}7 - 2{,}89 = 0{,}81$.

**Sağlama:** Sapmalarla: $(0 - 1{,}7)^2 \cdot 0{,}1 + (1 - 1{,}7)^2 \cdot 0{,}3 + (2 - 1{,}7)^2 \cdot 0{,}4 + (3 - 1{,}7)^2 \cdot 0{,}2 = 0{,}289 + 0{,}147 + 0{,}036 + 0{,}338 = 0{,}81$ ✓.

**Dikkat:** $E[X^2]$ yerine $(E[X])^2$ yazmak varyansı $0$ yapar; $E[X^2]$ her değerin karesinin ağırlıklı ortalaması.

**Cevap:** $c = 0{,}4$, $E[X] = 1{,}7$, $\operatorname{Var}(X) = 0{,}81$.
