**Fikir:** İzi, elemanların hangi çiftlerinin çarpılıp toplandığına bakarak tek bir toplam olarak yazalım. $\operatorname{tr}(AB)$'nin içinde $A$'nın her elemanı, $B$'nin "ayna" konumundaki elemanıyla bir kez çarpılıyor:

$$
\operatorname{tr}(AB) = \sum_{i} \sum_{k} a_{ik}\, b_{ki}
$$

**Adım 1 — Çiftleri eşleştir.** $a_{ik}$'nın eşi $b_{ki}$ (satır ve sütun numaraları yer değiştirmiş). $A$ $2 \times 3$ olduğu için 6 çift var:

$$
\begin{aligned}
a_{11} b_{11} &= 1 \cdot 3 = 3 \\
a_{12} b_{21} &= 0 \cdot 2 = 0 \\
a_{13} b_{31} &= 2 \cdot 1 = 2 \\
a_{21} b_{12} &= -1 \cdot 1 = -1 \\
a_{22} b_{22} &= 3 \cdot 1 = 3 \\
a_{23} b_{32} &= 1 \cdot 0 = 0
\end{aligned}
$$

**Adım 2 — Topla.**

$$
3 + 0 + 2 - 1 + 3 + 0 = 7
$$

**Adım 3 — $BA$ için aynı toplam.** $\operatorname{tr}(BA) = \sum_k \sum_i b_{ki}\, a_{ik}$: çarpılan çiftler **tam olarak aynı** altı çift, yalnızca toplama sırası farklı. Öyleyse $\operatorname{tr}(BA) = 7$.

**Neden işe yarar?** Bu yol hem iki izi birden veriyor hem de $\operatorname{tr}(AB) = \operatorname{tr}(BA)$ kuralının nedenini gösteriyor. Özdeğerler bölümünde izin özdeğerlerin toplamı olduğunu görünce bu kural yeniden karşına çıkacak.

**Cevap:** $7$ ve $7$.
