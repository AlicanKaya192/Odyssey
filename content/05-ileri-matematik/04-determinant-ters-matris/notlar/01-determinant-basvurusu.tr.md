Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Determinant

$$
\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
$$

$$
\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
= a(ei - fh) - b(di - fg) + c(dh - eg)
$$

| Değer | Anlamı |
|---|---|
| $\lvert\det A\rvert$ | Alan (3 boyutta hacim) kaç katına çıkıyor |
| $\det A < 0$ | Yön ters döndü (aynalanma var) |
| $\det A = 0$ | Düzlem ezildi; sütunlar aynı doğruda; ters yok |
| $\det A = 1$ | Alan korunuyor (döndürme, kaydırma) |

**Açılımda işaret deseni:** $\begin{bmatrix} + & - & + \\ - & + & - \\ + & - & + \end{bmatrix}$. En çok sıfırı olan satırı ya da sütunu seç.

**Üçgen ya da köşegen matris:** determinant köşegen çarpımı.

## Determinantın kuralları

| Kural | Sonuç |
|---|---|
| $\det(AB)$ | $\det A \cdot \det B$ |
| $\det(A^\mathsf{T})$ | $\det A$ |
| $\det(cA)$, $A$ $n \times n$ | $c^n \det A$ |
| $\det(A^{-1})$ | $1 / \det A$ |
| $\det I$ | $1$ |
| İki satırın yerini değiştir | işaret değişir |
| Bir satırı $c$ ile çarp | $\det$ da $c$ ile çarpılır |
| Bir satıra başka satırın katını ekle | değişmez |
| $\det(A + B)$ | **kural yok** |

## Ters matris

$$
A A^{-1} = A^{-1} A = I
$$

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

Yer değiştir ($a \leftrightarrow d$), işaret çevir ($-b$, $-c$), determinanta böl.

| Kural | Sonuç |
|---|---|
| Ters var mı? | ancak ve ancak $\det A \ne 0$ |
| $(A^{-1})^{-1}$ | $A$ |
| $(AB)^{-1}$ | $B^{-1} A^{-1}$ (sıra ters) |
| $(A^\mathsf{T})^{-1}$ | $(A^{-1})^\mathsf{T}$ |
| $(cA)^{-1}$ | $\frac{1}{c} A^{-1}$ |

## Dönüşümlerin tersleri

| Dönüşüm | $\det$ | Tersi |
|---|---|---|
| $\theta$ döndürme | $1$ | $-\theta$ döndürme |
| Yansıma | $-1$ | kendisi |
| $\begin{bmatrix} s_1 & 0 \\ 0 & s_2 \end{bmatrix}$ ölçekleme | $s_1 s_2$ | $\begin{bmatrix} 1/s_1 & 0 \\ 0 & 1/s_2 \end{bmatrix}$ |
| $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ kaydırma | $1$ | $\begin{bmatrix} 1 & -k \\ 0 & 1 \end{bmatrix}$ |
| İzdüşüm | $0$ | yok |

## Denklem çözmek

$$
A\mathbf{x} = \mathbf{b} \quad \Rightarrow \quad \mathbf{x} = A^{-1}\mathbf{b}
$$

- $\det A \ne 0$: tam bir çözüm.
- $\det A = 0$: ya hiç çözüm yok ya da sonsuz çözüm (Gauss eleme bölümü).
- $A^{-1}$ ile **soldan** çarpılır.

## Pratik ipuçları

- Tersi yazmadan önce determinantı hesapla; sıfırsa dur.
- Kesirlerle uğraşmamak için $\frac{1}{\det}$'i en sona bırak.
- Bulduğun tersi mutlaka $AA^{-1} = I$ ile sına; tek çarpım yeter.
- $3 \times 3$ determinantta bir satırda iki sıfır varsa o satırı aç; tek terim kalır.
- ML'de $\det(X^\mathsf{T}X) \approx 0$ ise sütunlardan biri ötekilerin tekrarı olabilir.
