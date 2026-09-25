Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Tanım | Boyut |
|---|---|---|
| gradyan | $\nabla f$, tek çıktının kısmi türevleri | $n$ |
| Jacobian | $J_{ij} = \dfrac{\partial F_i}{\partial x_j}$ | $m \times n$ |
| Hessian | $H_{ij} = \dfrac{\partial^2 f}{\partial x_i \, \partial x_j}$ | $n \times n$, simetrik |

## Yaklaşımlar

| Derece | Formül |
|---|---|
| birinci (Jacobian) | $F(\mathbf{p} + \mathbf{h}) \approx F(\mathbf{p}) + J \mathbf{h}$ |
| ikinci (Hessian) | $f(\mathbf{p} + \mathbf{h}) \approx f(\mathbf{p}) + \nabla f \cdot \mathbf{h} + \tfrac{1}{2} \mathbf{h}^\mathsf{T} H \mathbf{h}$ |

## Zincir kuralı

| Durum | Formül |
|---|---|
| $z = f(x(t), y(t))$ | $\dfrac{dz}{dt} = f_x \, x' + f_y \, y'$ |
| bileşke | $J_{g \circ f} = J_g \, J_f$ |
| doğrusal katman geri | $\dfrac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T} \dfrac{\partial L}{\partial \mathbf{z}}$ |
| ağırlığa göre | $\dfrac{\partial L}{\partial W} = \dfrac{\partial L}{\partial \mathbf{z}} \, \mathbf{x}^\mathsf{T}$ |

## Kritik nokta (gradyan sıfır)

| Hessian | Nokta |
|---|---|
| özdeğerler hepsi $> 0$ | en küçük |
| özdeğerler hepsi $< 0$ | en büyük |
| karışık işaret | eyer |
| iki değişken: $\det H > 0$, $f_{xx} > 0$ | en küçük |
| iki değişken: $\det H > 0$, $f_{xx} < 0$ | en büyük |
| iki değişken: $\det H < 0$ | eyer |

## Hazır Jacobianlar

| Fonksiyon | Jacobian |
|---|---|
| $W\mathbf{x} + \mathbf{b}$ | $W$ |
| eleman eleman $\sigma(\mathbf{z})$ | köşegen, $\sigma'(z_i)$ |
| ReLU | köşegen, $0$ ya da $1$ |

## Makine öğrenmesi

- Kararlı öğrenme oranı: $\eta < \dfrac{2}{\lambda_{\max}}$ (yaklaşık).
- Newton: $\Delta = -H^{-1} \nabla f$.
