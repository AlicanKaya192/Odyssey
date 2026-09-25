**Ne soruluyor?** Bir katmanda kaybın girdiye ve bir ağırlığa göre türevi.

**Fikir:** Kayıptan başlayıp her halkanın Jacobian'ıyla çarparak geriye yürü: $\frac{\partial L}{\partial \mathbf{a}} \to \frac{\partial L}{\partial \mathbf{z}} \to \frac{\partial L}{\partial \mathbf{x}}$.

**Adım 1 — İleri geçiş.** $\mathbf{z} = (1 + 2, \ 3 - 1) = (3, 2)$, ikisi de pozitif: $\mathbf{a} = (3, 2)$.

**Adım 2 — Kayıptan geri.** $\frac{\partial L}{\partial \mathbf{a}} = \mathbf{a} - \mathbf{y} = (2, 1)$. ReLU'nun Jacobian'ı birim: $\frac{\partial L}{\partial \mathbf{z}} = (2, 1)$.

**Adım 3 — Girdiye.**

$$
\frac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T} \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 & 3 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 5 \\ 3 \end{bmatrix}
$$

**Adım 4 — Ağırlığa.** $\frac{\partial L}{\partial W_{12}} = \frac{\partial L}{\partial z_1} \cdot x_2 = 2 \cdot 1 = 2$.

**Sağlama:** $x_1$'i $0{,}01$ artır: $\mathbf{z} = (3{,}01; 2{,}03)$, $L = \frac{1}{2}(2{,}01^2 + 1{,}03^2) \approx 2{,}5506$; eski $L = 2{,}5$. Fark bölü $0{,}01 \approx 5{,}06$ ✓.

**Dikkat:** $W$ yerine $W^\mathsf{T}$ kullanmak şart; $W(2, 1) = (4, 5)$ yanlış cevap verir.

**Cevap:** $5$, $3$ ve $2$.
