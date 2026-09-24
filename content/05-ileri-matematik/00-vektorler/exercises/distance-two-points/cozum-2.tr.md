**Fikir:** Fark vektörünü bulduktan sonra kare ve karekök hesabına girmeden bir kısayol var: bir vektörü bir sayıyla çarpmak, uzunluğunu da aynı sayıyla çarpar. Tanıdık bir küçük vektöre indirip onun uzunluğunu büyütebiliriz.

**Adım 1 — Fark vektörü.** Birinci yoldaki gibi $\overrightarrow{AB} = (6, 8)$.

**Adım 2 — Ortak çarpanı dışarı al.** $6$ ve $8$'in ikisi de 2'ye bölünüyor:

$$
(6,\ 8) = 2 \cdot (3,\ 4)
$$

**Adım 3 — Tanıdık üçgen.** Kenarları 3 ve 4 olan dik üçgenin hipotenüsü 5, çünkü $3^2 + 4^2 = 9 + 16 = 25$. Vektörümüz $(3, 4)$'ün 2 katı olduğu için uzunluğu da 2 katı:

$$
\begin{aligned}
\|2 \cdot (3, 4)\| &= 2 \cdot \|(3, 4)\| \\
&= 2 \cdot 5 = 10
\end{aligned}
$$

**Neden doğru?** Her bileşen $c$ ile çarpılınca karelerin hepsi $c^2$ ile çarpılır; karekök de bunu $|c|$'ye geri indirir:

$$
\|c\,\mathbf{v}\| = |c| \cdot \|\mathbf{v}\|
$$

**İpucu:** Sık karşılaşılan dik üçgen kenarları: 3-4-5, 5-12-13, 8-15-17. Bunları tanımak hesabı çok hızlandırır.

**Cevap:** 10.
