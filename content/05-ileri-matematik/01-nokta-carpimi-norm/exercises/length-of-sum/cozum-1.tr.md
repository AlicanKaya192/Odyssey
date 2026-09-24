**Ne soruluyor?** Vektörlerin kendisini bilmiyoruz; yalnızca uzunluklarını ve nokta çarpımlarını biliyoruz. Bunlarla toplamın ve farkın uzunluğunu bulacağız.

**Fikir:** Bir vektörün kendisiyle nokta çarpımı, uzunluğunun karesi:

$$
\mathbf{v} \cdot \mathbf{v} = \|\mathbf{v}\|^2
$$

$\mathbf{a} + \mathbf{b}$'yi kendisiyle çarpıp parantezleri sayılardaki gibi açarsak, içinden yalnızca bildiğimiz üç şey çıkar: $\|\mathbf{a}\|^2$, $\|\mathbf{b}\|^2$ ve $\mathbf{a} \cdot \mathbf{b}$.

**Adım 1 — Toplamın uzunluğunun karesini aç.** Nokta çarpımı çarpma gibi dağılır ve $\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$ olduğundan ortadaki iki terim birleşir ($(x + y)^2 = x^2 + 2xy + y^2$'ye benziyor):

$$
\begin{aligned}
\|\mathbf{a} + \mathbf{b}\|^2 &= (\mathbf{a} + \mathbf{b}) \cdot (\mathbf{a} + \mathbf{b}) \\
&= \mathbf{a} \cdot \mathbf{a} + 2\,\mathbf{a} \cdot \mathbf{b} + \mathbf{b} \cdot \mathbf{b} \\
&= \|\mathbf{a}\|^2 + 2\,\mathbf{a} \cdot \mathbf{b} + \|\mathbf{b}\|^2
\end{aligned}
$$

**Adım 2 — Sayıları koy.** $\|\mathbf{a}\|^2 = 9$, $\|\mathbf{b}\|^2 = 25$, $2\,\mathbf{a} \cdot \mathbf{b} = 12$:

$$
\begin{aligned}
\|\mathbf{a} + \mathbf{b}\|^2 &= 9 + 12 + 25 = 46 \\
\|\mathbf{a} + \mathbf{b}\| &= \sqrt{46} \approx 6.78
\end{aligned}
$$

**Adım 3 — Fark.** Aynı açılım; yalnızca ortadaki terimin işareti eksi olur ($(x - y)^2 = x^2 - 2xy + y^2$ gibi):

$$
\begin{aligned}
\|\mathbf{a} - \mathbf{b}\|^2 &= 9 - 12 + 25 = 22 \\
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{22} \approx 4.69
\end{aligned}
$$

**Sağlama (paralelkenar kuralı):** İki sonucun karelerini toplarsak ortadaki terimler birbirini götürür ve $2\,(\|\mathbf{a}\|^2 + \|\mathbf{b}\|^2)$ kalmalı:

$$
46 + 22 = 68 = 2 \cdot (9 + 25)
$$

Tutuyor. ✓

**Dikkat:** En sık hata $\|\mathbf{a} + \mathbf{b}\| = 3 + 5 = 8$ yazmak. Uzunluklar ancak iki vektör aynı yöne bakıyorsa toplanır.

**Cevap:** $6.78$ ve $4.69$.
