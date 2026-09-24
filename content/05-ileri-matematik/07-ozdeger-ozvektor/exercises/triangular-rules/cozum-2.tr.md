**Fikir:** Özdeğerleri hiç bulmadan ilk iki soruyu cevaplamak mümkün: toplam her zaman iz, çarpım her zaman determinant. Üçüncüsü için ise özdeğerleri bilmek gerekiyor.

**Adım 1 — İz.** Köşegen toplamı:

$$
\operatorname{tr} A = 2 + 3 + (-1) = 4
$$

**Adım 2 — Determinant.** İlk sütun boyunca aç; yalnızca $2$ sıfır değil:

$$
\det A = 2 \cdot \begin{vmatrix} 3 & 5 \\ 0 & -1 \end{vmatrix} = 2 \cdot (-3 - 0) = -6
$$

**Adım 3 — $A^2$ için özdeğerler gerekiyor.** Karakteristik polinom:

$$
\det(A - \lambda I) = (2 - \lambda)(3 - \lambda)(-1 - \lambda)
$$

Kökler $2, 3, -1$. $A^2$'nin özdeğerleri kareleri: $4, 9, 1$; en büyüğü $9$.

**Dikkat:** "En büyük özdeğerin karesi" her zaman $A^2$'nin en büyük özdeğeri değildir. Örneğin özdeğerler $2$ ve $-3$ olsaydı en büyük özdeğer $2$ ama $A^2$'nin en büyüğü $(-3)^2 = 9$ olurdu. Mutlak değere bakmak gerekiyor.

**Cevap:** $4$, $-6$, $9$.
