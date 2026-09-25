**Ne soruluyor?** Koşulsuz, tam bir koşullu ve "en az" koşullu ekip sayıları.

**Fikir:** Gruplara ayrılan seçimde her grup ayrı seçilip çarpılır. "En az bir" için tersini saymak daha kolay.

**Adım 1 — Bütün ekipler.** $12$ kişiden $4$: $\binom{12}{4} = 495$.

**Adım 2 — Tam $2$ kadın.** $\binom{5}{2} \cdot \binom{7}{2} = 10 \cdot 21 = 210$.

**Adım 3 — En az $1$ kadın.** Hiç kadın olmayan ekipler, yalnızca erkeklerden: $\binom{7}{4} = 35$. $495 - 35 = 460$.

**Sağlama:** $0$, $1$, $2$, $3$, $4$ kadınlı ekipler $35 + 175 + 210 + 70 + 5 = 495$ ✓.

**Dikkat:** "En az bir kadın" için önce bir kadın seçip ($5$) sonra kalan $11$ kişiden $3$ seçmek ($5 \cdot 165 = 825$) aynı ekipleri defalarca sayar: iki kadınlı bir ekip, hangi kadın "önce" seçildiyse ona göre iki kez sayılır.

**Cevap:** $495$, $210$, $460$.
