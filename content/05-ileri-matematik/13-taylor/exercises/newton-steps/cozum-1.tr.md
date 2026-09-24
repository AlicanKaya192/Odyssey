**Ne soruluyor?** İki Newton adımı ve gerçek en küçük nokta.

**Fikir:** Newton her adımda $w - \frac{L'}{L''}$'ye gidiyor. Türevler kolay: $L' = e^w - 2$, $L'' = e^w$.

**Adım 1 — Birinci adım.** $w = 0$: $L' = -1$, $L'' = 1$; $w = 0 - \frac{-1}{1} = 1$.

**Adım 2 — İkinci adım.** $w = 1$: $L' = e - 2 \approx 0{,}71828$, $L'' = e$;

$$
w = 1 - \frac{0{,}71828}{2{,}71828} \approx 1 - 0{,}26424 = 0{,}73576
$$

**Adım 3 — Gerçek en küçük.** $e^w = 2 \Rightarrow w = \ln 2 \approx 0{,}693$. $L'' = e^w > 0$: gerçekten en küçük.

**Sağlama:** Hata birinci adımdan sonra $1 - 0{,}693 = 0{,}307$, ikinciden sonra $0{,}736 - 0{,}693 = 0{,}043$. Newton'da hata yaklaşık karesine iner: $0{,}307^2 \cdot \frac{1}{2} \approx 0{,}047$ ✓.

**Dikkat:** Gradyan inişindeki gibi $w - \eta L'$ yazmak Newton değil; Newton'da öğrenme oranı yok, adım boyunu $L''$ belirliyor.

**Cevap:** $1$, $0{,}736$ ve $0{,}693$.
