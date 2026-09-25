**Fikir:** $f = g(x) + y^2$, $g(x) = x^3 - 3x$: iki değişken birbirinden bağımsız. Her birini tek değişkenli olarak incele.

**Adım 1 — $g$.** $g' = 3x^2 - 3$, $g'' = 6x$. $x = 1$: $g'' > 0$, yerel en küçük, $g(1) = -2$. $x = -1$: $g'' < 0$, yerel en büyük.

**Adım 2 — $y^2$.** $y = 0$'da en küçük, değeri $0$.

**Adım 3 — Birleştir.** $(1, 0)$: iki yönde de dip, en küçük $-2$. $(-1, 0)$: $x$ yönünde tepe, $y$ yönünde dip: eyer. $\det H = g''(-1) \cdot 2 = -12$.

**Neden aynı sonuç?** Değişkenler ayrıksa Hessian köşegendir ve özdeğerler tam olarak tek değişkenli ikinci türevler. Genel Hessian testi, değişkenler iç içe geçtiğinde (köşegen dışı $f_{xy} \neq 0$) bu ayırmayı özdeğer yönlerinde yapıyor.

**Cevap:** $1$, $-2$ ve $-12$.
