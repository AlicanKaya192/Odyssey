**Ne soruluyor?** $A$'nın birim çemberi götürdüğü elipsin yarı eksen uzunlukları.

**Fikir:** $A = U\Sigma V^\mathsf{T}$ ise $A^\mathsf{T}A = V(\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}$. Yani $A^\mathsf{T}A$'nın özdeğerleri tekil değerlerin **kareleri**. Özdeğerleri bulup karekök alacağız.

**Adım 1 — $A^\mathsf{T}A$.** $A^\mathsf{T}$'nin satırları $A$'nın sütunları; her eleman iki sütunun nokta çarpımı:

$$
\begin{aligned}
A^\mathsf{T}A &= \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix} \\
&= \begin{bmatrix} 9 + 16 & 0 + 20 \\ 0 + 20 & 0 + 25 \end{bmatrix} = \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix}
\end{aligned}
$$

**Adım 2 — Özdeğerler.** İz $50$, determinant $625 - 400 = 225$:

$$
\begin{aligned}
\lambda^2 - 50\lambda + 225 &= 0 \\
(\lambda - 45)(\lambda - 5) &= 0
\end{aligned}
$$

($45 \cdot 5 = 225$, $45 + 5 = 50$.)

**Adım 3 — Karekök.**

$$
\begin{aligned}
\sigma_1 &= \sqrt{45} = 3\sqrt{5} \approx 6.71 \\
\sigma_2 &= \sqrt{5} \approx 2.24
\end{aligned}
$$

**Sağlama:** $\sigma_1\sigma_2 = \sqrt{225} = 15 = |\det A| = |15 - 0|$ ✓. Ayrıca $\sigma_1^2 + \sigma_2^2 = 50 = 9 + 0 + 16 + 25$ (elemanların kareleri toplamı) ✓.

**Dikkat:** $A$ üçgen bir matris ve özdeğerleri $3$ ile $5$; ama tekil değerler bunlar **değil**. Tekil değerler özdeğerlerle yalnızca simetrik (ve özdeğerleri negatif olmayan) matrislerde çakışır.

**Cevap:** $\sigma_1 \approx 6.71$, $\sigma_2 \approx 2.24$.
