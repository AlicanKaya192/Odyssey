**Ne soruluyor?** Çarpma, max ve dallanma içeren bir grafikte türevler.

**Fikir:** Sondaki toplama gradyanı $1$ olarak iki kola dağıtır. Çarpma kolunda girdiler değiş tokuş edilir, max kolunda gradyan yalnızca kazanana gider. $y$ iki kolda da var: katkılar toplanır.

**Adım 1 — İleri.** $xy = -6$, $\max(-2, 1) = 1$, $f = -5$.

**Adım 2 — Çarpma kolu.** Gelen $1$: $x$'e $y = -2$, $y$'ye $x = 3$.

**Adım 3 — Max kolu.** Gelen $1$: kazanan $z$, ona $1$; $y$'ye $0$.

**Adım 4 — Topla.** $\frac{\partial f}{\partial x} = -2$, $\frac{\partial f}{\partial y} = 3 + 0 = 3$, $\frac{\partial f}{\partial z} = 1$.

**Sağlama:** $y$'yi $0{,}01$ artır: $xy = -5{,}97$, max hâlâ $1$; $f = -4{,}97$, değişim $0{,}03 / 0{,}01 = 3$ ✓.

**Dikkat:** Max düğümünün gradyanı iki girdiye de yollamak $\frac{\partial f}{\partial y} = 4$ verir; $y$ max'ı kazanmadığı için oraya katkısı yok.

**Cevap:** $-2$, $3$ ve $1$.
