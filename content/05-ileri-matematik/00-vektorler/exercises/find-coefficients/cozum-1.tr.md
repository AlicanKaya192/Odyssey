**Ne soruluyor?** $(1, 2)$ vektöründen $a$ tane, $(3, 1)$ vektöründen $b$ tane alıp toplayınca $(7, 9)$ çıkıyor. Bu "kaç tane"leri, yani $a$ ile $b$'yi arıyoruz.

**Fikir:** İki vektör ancak her bileşeni eşitse eşittir. Sol tarafı bileşenlerine ayırıp sağ tarafla karşılaştırınca iki bilinmeyenli iki denklem çıkar. Sonra birini yalnız bırakıp ötekine koyarız (yerine koyma).

**Adım 1 — Sol tarafı aç.** Önce skalerle çarp, sonra topla:

$$
\begin{aligned}
a\,(1, 2) + b\,(3, 1) &= (a,\ 2a) + (3b,\ b) \\
&= (a + 3b,\ 2a + b)
\end{aligned}
$$

**Adım 2 — Bileşenleri eşitle.** Bu vektörün $(7, 9)$ olması için iki bileşenin de tutması gerekiyor:

$$
\begin{aligned}
a + 3b &= 7 \quad (x \text{ bileşeni}) \\
2a + b &= 9 \quad (y \text{ bileşeni})
\end{aligned}
$$

**Adım 3 — Bir bilinmeyeni yalnız bırak.** İkinci denklemde $b$'nin önünde sayı yok (katsayısı 1), onu çekmek en kolayı:

$$
b = 9 - 2a
$$

**Adım 4 — Birinci denkleme koy.** $b$ yerine $9 - 2a$ yazınca tek bilinmeyen kalıyor:

$$
\begin{aligned}
a + 3(9 - 2a) &= 7 \\
a + 27 - 6a &= 7 \\
-5a &= 7 - 27 \\
-5a &= -20 \\
a &= 4
\end{aligned}
$$

**Adım 5 — $b$'yi bul.** Adım 3'teki formüle $a = 4$ koy: $b = 9 - 2 \cdot 4 = 1$.

**Sağlama:** Bulduklarını baştaki eşitliğe koy:

$$
\begin{aligned}
4\,(1, 2) + 1\,(3, 1) &= (4, 8) + (3, 1) \\
&= (7, 9)
\end{aligned}
$$

Tutuyor. ✓

**Cevap:** $a = 4$, $b = 1$.
