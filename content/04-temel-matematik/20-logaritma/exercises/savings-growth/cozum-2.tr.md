Bölmeyi atlayıp doğrudan iki tarafın logaritmasını alabilirsin. Soldaki çarpımı **çarpım kuralı** ayırıyor:

$$
\begin{aligned}
\ln (1000 \cdot 1.08^t) &= \ln 2500 \\
\ln 1000 + t \ln 1.08 &= \ln 2500
\end{aligned}
$$

$$
t = \frac{\ln 2500 - \ln 1000}{\ln 1.08}
$$

Payda **bölüm kuralı** var: $\ln 2500 - \ln 1000 = \ln \frac{2500}{1000} = \ln 2.5$. Yani birinci yoldaki formülün aynısına ulaştın:

$$
t = \frac{\ln 2.5}{\ln 1.08} \approx 11.91
$$

Bu yolun dersi: ilk adımda bölmek bir kısayol; kurallar doğru uygulanırsa bölmeden de aynı sonuç çıkıyor.

**Dikkat:** $\ln (1000 \cdot 1.08^t)$ ifadesini $t \cdot \ln (1000 \cdot 1.08)$ diye açmak **yanlış**. Üs yalnızca $1.08$'in üstünde.

**Cevap: yaklaşık 11.91 yıl**
