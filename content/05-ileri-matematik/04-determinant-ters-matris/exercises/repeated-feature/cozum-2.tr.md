**Fikir:** $X^\mathsf{T}X = \begin{bmatrix} \mathbf{c}_1 \cdot \mathbf{c}_1 & \mathbf{c}_1 \cdot \mathbf{c}_2 \\ \mathbf{c}_2 \cdot \mathbf{c}_1 & \mathbf{c}_2 \cdot \mathbf{c}_2 \end{bmatrix}$ olduğu için determinantı

$$
\|\mathbf{c}_1\|^2 \, \|\mathbf{c}_2\|^2 - (\mathbf{c}_1 \cdot \mathbf{c}_2)^2
$$

Nokta çarpımının geometrik anlamını ($\mathbf{c}_1 \cdot \mathbf{c}_2 = \|\mathbf{c}_1\|\|\mathbf{c}_2\|\cos\theta$) koyunca:

$$
\det(X^\mathsf{T}X) = \|\mathbf{c}_1\|^2 \, \|\mathbf{c}_2\|^2 \,(1 - \cos^2\theta)
$$

Determinant, sütunlar arasındaki açıya bağlı. $\cos^2\theta = 1$ (sütunlar aynı doğruda) ise sıfır.

**Adım 1 — $X_1$: hesap yapmadan.** $\mathbf{c}_2 = (2, 4, 6) = 2\,\mathbf{c}_1$. Sütunlar aynı yönde, $\theta = 0$, $\cos\theta = 1$. Öyleyse

$$
\det(X_1^\mathsf{T}X_1) = 0
$$

**Adım 2 — $X_2$: formülle.** $\|\mathbf{c}_1\|^2 = 14$, $\|\mathbf{c}_2\|^2 = 4 + 16 + 49 = 69$, $\mathbf{c}_1 \cdot \mathbf{c}_2 = 2 + 8 + 21 = 31$:

$$
\begin{aligned}
\det(X_2^\mathsf{T}X_2) &= 14 \cdot 69 - 31^2 \\
&= 966 - 961 = 5
\end{aligned}
$$

**Adım 3 — Açıya bak.** $\cos\theta = \dfrac{31}{\sqrt{14 \cdot 69}} \approx \dfrac{31}{31.08} \approx 0.997$. Sütunlar arasındaki açı yaklaşık $4°$: neredeyse aynı yönde.

**Neden önemli?** Bu yol, determinantın küçük çıkmasının **nedenini** gösteriyor: iki özellik neredeyse aynı şeyi ölçüyor. Gerçek verilerde bu, çoklu doğrusal bağlantı denen sorun; çözümü ya özelliklerden birini atmak ya da ridge ile köşegene $\lambda$ eklemek.

**Cevap:** $0$ ve $5$.
