**Fikir:** Aynı soruyu şekille düşünelim. İki vektörü aynı noktadan çizersek bir paralelkenar oluşur: $\mathbf{a} - \mathbf{b}$ uçları birleştiren kısa köşegen, $\mathbf{a} + \mathbf{b}$ öteki köşegen. Kenarları ve aradaki açıyı bilirsek köşegenleri kosinüs teoremiyle buluruz.

**Adım 1 — Aradaki açının kosinüsü.** Nokta çarpımının geometrik anlamından:

$$
\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|} = \frac{6}{3 \cdot 5} = \frac{6}{15} = 0.4
$$

**Adım 2 — Fark (kısa köşegen).** $\mathbf{a}$, $\mathbf{b}$ ve $\mathbf{a} - \mathbf{b}$ bir üçgen oluşturur; $\mathbf{a} - \mathbf{b}$ açının karşısındaki kenar. Kosinüs teoremi: $c^2 = x^2 + y^2 - 2xy\cos\theta$.

$$
\begin{aligned}
\|\mathbf{a} - \mathbf{b}\|^2 &= 3^2 + 5^2 - 2 \cdot 3 \cdot 5 \cdot 0.4 \\
&= 9 + 25 - 12 = 22 \\
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{22} \approx 4.69
\end{aligned}
$$

**Adım 3 — Toplam (uzun köşegen).** Paralelkenarda komşu açılar $180°$'ye tamamlanır. Uzun köşegenin karşısındaki açı $180° - \theta$ ve $\cos(180° - \theta) = -\cos\theta$, yani işaret artıya döner:

$$
\begin{aligned}
\|\mathbf{a} + \mathbf{b}\|^2 &= 3^2 + 5^2 + 2 \cdot 3 \cdot 5 \cdot 0.4 \\
&= 9 + 25 + 12 = 46 \\
\|\mathbf{a} + \mathbf{b}\| &= \sqrt{46} \approx 6.78
\end{aligned}
$$

**Neden aynı sayılar?** Derste nokta çarpımının geometrik hâli zaten kosinüs teoreminden çıkmıştı. Birinci yoldaki $2\,\mathbf{a} \cdot \mathbf{b}$ terimi, buradaki $2 \cdot 3 \cdot 5 \cdot \cos\theta$ ile aynı şey.

**Cevap:** $6.78$ ve $4.69$.
