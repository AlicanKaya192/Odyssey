**Fikir:** Birinci yoldaki "önce 1000'e böl" adımı bir kısayol. Bölmeden, doğrudan iki tarafın logaritmasını alarak da aynı yere varılır; bu kez **çarpım** ve **bölüm** kuralları devreye giriyor. Bu yol kuralların birlikte nasıl çalıştığını gösteriyor.

**Adım 1 — İki tarafın logaritmasını al.**

$$
\ln (1000 \cdot 1.08^t) = \ln 2500
$$

**Adım 2 — Soldaki çarpımı ayır.** Çarpım kuralı: $\ln (xy) = \ln x + \ln y$. Sonra kuvvet kuralı üssü öne indirir:

$$
\begin{aligned}
\ln 1000 + \ln (1.08^t) &= \ln 2500 \\
\ln 1000 + t \ln 1.08 &= \ln 2500
\end{aligned}
$$

**Adım 3 — $t$'yi yalnız bırak.** $\ln 1000$'i karşıya at, sonra $\ln 1.08$'e böl:

$$
t = \frac{\ln 2500 - \ln 1000}{\ln 1.08}
$$

**Adım 4 — Payı sadeleştir.** Bölüm kuralı: $\ln x - \ln y = \ln \frac{x}{y}$.

$$
\ln 2500 - \ln 1000 = \ln \frac{2500}{1000} = \ln 2.5
$$

Birinci yoldaki formülün aynısına ulaştık:

$$
t = \frac{\ln 2.5}{\ln 1.08} \approx 11.91
$$

**Neden aynı sonuç?** İlk yoldaki bölme işlemi burada bölüm kuralının içinde saklı. Kurallar doğru uygulanırsa hangi sırayla gidildiği fark etmiyor.

**Dikkat:** $\ln (1000 \cdot 1.08^t)$'yi $t \cdot \ln (1000 \cdot 1.08)$ diye açmak **yanlış**. Üs yalnızca $1.08$'in üstünde; 1000 üsten etkilenmiyor.

**Cevap:** yaklaşık 11.91 yıl.
