**Ne soruluyor?** Bir vektör fonksiyonunun Jacobian'ının iki elemanı ve determinantı.

**Fikir:** Satır = çıktı, sütun = girdi. Her elemanı bir kısmi türev olarak hesapla, noktayı koy.

**Adım 1 — Matris.**

$$
J = \begin{bmatrix} 2xy & x^2 \\ 1 & 3 \end{bmatrix} \;\to\; \begin{bmatrix} 4 & 1 \\ 1 & 3 \end{bmatrix}
$$

**Adım 2 — Determinant.** $4 \cdot 3 - 1 \cdot 1 = 11$.

**Sağlama:** $\det J > 0$: $F$ bu noktada yönleri ters çevirmiyor ve küçük alanları yaklaşık $11$ katına çıkarıyor.

**Dikkat:** $J_{12}$, birinci çıktının **ikinci girdiye** göre türevi: $\frac{\partial (x^2 y)}{\partial y} = x^2 = 1$. Satır ve sütunu karıştırmak $J_{12}$ yerine $J_{21} = 1$ vermiş olur; burada tesadüfen aynı sayı, genelde değil.

**Cevap:** $4$, $1$ ve $11$.
