**Ne soruluyor?** Seken bir topun bir sekişteki yüksekliği, belli bir ana kadarki yolu ve sonsuza kadarki toplam yolu.

**Fikir:** Sekiş yükseklikleri geometrik dizi: $h_k = 54 \cdot \left( \frac{2}{3} \right)^{k - 1}$. Yol, ilk düşüş artı her sekişin iki katı.

**Adım 1 — Dördüncü sekiş.** $h_4 = 54 \cdot \left( \frac{2}{3} \right)^3 = 54 \cdot \frac{8}{27} = 16$.

**Adım 2 — Beşinci değişe kadar.** İlk değiş düşüşün sonu. Sonraki dört değişten önce dört sekiş var:

$$
\begin{aligned}
54 + 36 + 24 + 16 &= 130 \\
81 + 2 \cdot 130 &= 341
\end{aligned}
$$

Seri formülüyle de: $54 \cdot \frac{1 - (2/3)^4}{1 - 2/3} = 54 \cdot \frac{65/81}{1/3} = 130$.

**Adım 3 — Sonsuza kadar.** $r = \frac{2}{3}$, yani $-1 < r < 1$:

$$
\begin{aligned}
\sum_{k=1}^{\infty} h_k &= \frac{54}{1 - 2/3} = 162 \\
81 + 2 \cdot 162 &= 405
\end{aligned}
$$

**Sağlama:** Beşinci değişe kadar $341$, sonsuz toplam $405$'ten küçük ✓; kalan $64$ metre sonraki sekişlerin toplamı: $2 \cdot \frac{h_5}{1 - 2/3} = 2 \cdot \frac{32/3}{1/3} = 64$ ✓.

**Dikkat:** İlk $81$ m'yi iki kez saymak sık hata: top o yüksekliğe hiç çıkmadı, yalnızca düştü.

**Cevap:** $16$ m, $341$ m, $405$ m.
