Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Okuma

| Kavram | Anlamı |
|---|---|
| Boyut $m \times n$ | $m$ satır, $n$ sütun (önce satır) |
| $a_{ij}$ | $i$. satır, $j$. sütundaki eleman |
| $\mathbb{R}^{m \times n}$ | $m \times n$ gerçek sayılı matrisler |
| Sütun vektörü | $n \times 1$ matris; "vektör" denince bu |
| Satır vektörü | $1 \times n$ matris; $\mathbf{x}^\mathsf{T}$ |
| Köşegen | $a_{11}, a_{22}, \dots$ (yalnızca kare matriste) |

## Özel matrisler

| Adı | Koşul |
|---|---|
| Kare | $m = n$ |
| Sıfır $O$ | her eleman $0$ |
| Köşegen | kare, köşegen dışı $0$ |
| Birim $I$ | köşegen, köşegen $1$ |
| Üst üçgen | kare, köşegenin altı $0$ |
| Alt üçgen | kare, köşegenin üstü $0$ |
| Simetrik | $A^\mathsf{T} = A$, yani $a_{ij} = a_{ji}$ |

## İşlemler

| İşlem | Kural | Boyut şartı |
|---|---|---|
| $A + B$, $A - B$ | eleman eleman | aynı boyut |
| $cA$ | her eleman $c$ ile çarpılır | yok |
| $A^\mathsf{T}$ | $(A^\mathsf{T})_{ij} = a_{ji}$ | $m \times n \to n \times m$ |
| $A\mathbf{x}$ | satırlarla nokta çarpımı | $A$'nın sütun sayısı = $\mathbf{x}$'in boyu |
| $\operatorname{tr} A$ | köşegen toplamı | kare |

## Matris–vektör çarpımının iki bakışı

$$
A\mathbf{x} = \begin{bmatrix} \text{1. satır} \cdot \mathbf{x} \\ \text{2. satır} \cdot \mathbf{x} \\ \vdots \end{bmatrix}
$$

$$
A\mathbf{x} = x_1\,\mathbf{a}_1 + x_2\,\mathbf{a}_2 + \cdots + x_n\,\mathbf{a}_n
$$

Satır bakışı **hesap** için, sütun bakışı **anlam** için:
$A\mathbf{x}$ her zaman $A$'nın sütunlarının bir doğrusal kombinasyonu.

## Kurallar

- $A + B = B + A$, $\;(A + B) + C = A + (B + C)$
- $c(A + B) = cA + cB$, $\;(c + d)A = cA + dA$
- $(A^\mathsf{T})^\mathsf{T} = A$, $\;(A + B)^\mathsf{T} = A^\mathsf{T} + B^\mathsf{T}$, $\;(cA)^\mathsf{T} = cA^\mathsf{T}$
- $A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y}$, $\;A(c\mathbf{x}) = c\,A\mathbf{x}$
- $I\mathbf{x} = \mathbf{x}$
- $\mathbf{a} \cdot \mathbf{b} = \mathbf{a}^\mathsf{T}\mathbf{b}$

## Pratik ipuçları

- Boyutları çarpımın altına yaz: $(2 \times 3)(3 \times 1)$. İçteki iki
  sayı eşit olmalı, dıştaki iki sayı sonucun boyutu.
- Devrik almadan önce boyutu değiştir: $2 \times 3$ ise sonuç $3 \times 2$
  olacak; boş tabloyu çizip doldur.
- Simetriklik için yalnızca köşegenin bir yanına bak: her $a_{ij}$ karşı
  taraftaki $a_{ji}$'ye eşit mi?
- ML'de $X$'in satırları örnek, sütunları özellik: $n \times d$.
