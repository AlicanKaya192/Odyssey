**Ne soruluyor?** Sağ taraftaki $k$'nin, sistemin türünü (çözüm yok / tek / sonsuz) nasıl değiştirdiği.

**Fikir:** Elemeyi $k$ harf olarak dururken yap. Son satır $0 = (\text{bir şey})$ çıkarsa, o "bir şeyin" sıfır olup olmaması her şeyi belirler.

**Adım 1 — Artırılmış matris.**

$$
\left[\begin{array}{cc|c} 1 & 2 & 3 \\ 2 & 4 & k \end{array}\right]
$$

**Adım 2 — $R_2 \to R_2 - 2R_1$.** $(2 - 2,\ 4 - 4 \mid k - 6)$:

$$
\left[\begin{array}{cc|c} 1 & 2 & 3 \\ 0 & 0 & k - 6 \end{array}\right]
$$

**Adım 3 — Son satırı oku.** Son satır $0 = k - 6$ diyor.

- $k = 6$ ise $0 = 0$: bilgi taşımayan bir satır. Geriye tek denklem ($x + 2y = 3$) ve iki bilinmeyen kalıyor; $y$ serbest. **Sonsuz çözüm**: $(3 - 2t,\ t)$.
- $k \ne 6$ ise $0 = k - 6 \ne 0$: imkânsız. **Çözüm yok.**

**Adım 4 — $k = 5$.** $0 = 5 - 6 = -1$: çelişki, çözüm sayısı $0$.

**Dikkat:** Bu sistem $k$ ne olursa olsun **tek** çözümlü olamıyor. Sol taraftaki katsayı matrisinin determinantı $1 \cdot 4 - 2 \cdot 2 = 0$; sağ taraf yalnızca "hiç" ile "sonsuz" arasında seçim yapıyor.

**Cevap:** $k = 6$; $k = 5$ iken $0$ çözüm.
