**Fikir:** $f$'de $x$ ile $y$ ayrık; her koordinat kendi eğriliğiyle bağımsız küçülür. $x$ için $\lambda = 2$, $y$ için $\lambda = 8$.

**Adım 1 — Çarpanlar.** $x$: $1 - 0{,}1 \cdot 2 = 0{,}8$. $y$: $1 - 0{,}1 \cdot 8 = 0{,}2$.

**Adım 2 — Kapalı formül.** $x_k = 2 \cdot 0{,}8^k$, $y_k = 0{,}2^k$. $k = 1$: $(1{,}6; 0{,}2)$. $k = 2$: $(1{,}28; 0{,}04)$.

**Adım 3 — Değer.** $1{,}6384 + 0{,}0064 = 1{,}6448$.

**Neden aynı sonuç?** Hessian köşegen olduğu için gradyan inişi her özdeğer yönünde ayrı ayrı çalışıyor. Koşul sayısı $\frac{8}{2} = 4$: dik $y$ yönü hızla sönerken yatık $x$ yönü $0{,}8$ çarpanıyla ağır ilerliyor. Bu, zikzak ve basık vadi sorununun en basit hâli.

**Cevap:** $1{,}6$, $0{,}2$ ve $1{,}6448$.
