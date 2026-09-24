**Fikir:** Bilinmeyenli matrisin devriğini almak yerine, eşitliğin **iki tarafının birden** devriğini alabiliriz. İki kural bunu mümkün kılıyor:

$$
\begin{aligned}
(A + B)^\mathsf{T} &= A^\mathsf{T} + B^\mathsf{T} \\
(A^\mathsf{T})^\mathsf{T} &= A
\end{aligned}
$$

Böylece bilinmeyenli matris devriksiz kalır; devrik yalnızca sayıları bildiğimiz matrislere uygulanır.

**Adım 1 — İki tarafın devriğini al.** Sol taraftaki toplamın devriği, devriklerin toplamı. İlk matris iki kez devrik alındığı için kendisine döner:

$$
\begin{bmatrix} x & 2 \\ y & 5 \end{bmatrix} + \begin{bmatrix} 1 & 3 \\ 0 & z \end{bmatrix}^\mathsf{T} = \begin{bmatrix} 4 & 7 \\ 2 & 9 \end{bmatrix}^\mathsf{T}
$$

**Adım 2 — Bilinen devrikleri hesapla.** Satırları sütun yap:

$$
\begin{bmatrix} x & 2 \\ y & 5 \end{bmatrix} + \begin{bmatrix} 1 & 0 \\ 3 & z \end{bmatrix} = \begin{bmatrix} 4 & 2 \\ 7 & 9 \end{bmatrix}
$$

**Adım 3 — Eleman eleman eşitle.**

$$
\begin{aligned}
x + 1 &= 4 \quad \Rightarrow \quad x = 3 \\
y + 3 &= 7 \quad \Rightarrow \quad y = 4 \\
5 + z &= 9 \quad \Rightarrow \quad z = 4
\end{aligned}
$$

Sağ üst köşe de tutuyor: $2 + 0 = 2$. ✓

**Neden aynı denklemler?** Devrik yalnızca elemanların yerini değiştirir; hangi elemanın hangisiyle toplandığını değiştirmez. Bu yol devriği bilinenlere taşıdı. Devrik kuralları, bir eşitliği en rahat okunduğu biçime getirmeye yarıyor.

**Cevap:** $x = 3$, $y = 4$, $z = 4$.
