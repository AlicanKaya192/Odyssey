Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Formül |
|---|---|
| kısmi türev | $\dfrac{\partial f}{\partial x}$: öteki değişkenler sabit |
| gradyan | $\nabla f = \left(\dfrac{\partial f}{\partial x}, \dfrac{\partial f}{\partial y}, \ldots\right)$ |
| yönlü türev | $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$, $\lVert \mathbf{u} \rVert = 1$ |
| en hızlı artış | $\nabla f$ yönünde, hızı $\lVert \nabla f \rVert$ |
| en hızlı azalış | $-\nabla f$ yönünde |

## Kısmi türev almak

| İfade | $\partial / \partial x$ | $\partial / \partial y$ |
|---|---|---|
| $x^2 y$ | $2xy$ | $x^2$ |
| $3y$ | $0$ | $3$ |
| $e^{xy}$ | $y e^{xy}$ | $x e^{xy}$ |
| $x^2 + y^2$ | $2x$ | $2y$ |

## Gradyanın geometrisi

| Özellik | Açıklama |
|---|---|
| yön | en dik çıkış |
| eş yükselti eğrisi | gradyan eğriye dik |
| $\theta = 90°$ | o yönde değişim yok |

## Gradyanın sıfır olduğu noktalar

| Tür | Örnek ($(0, 0)$'da) |
|---|---|
| en küçük | $x^2 + y^2$ |
| en büyük | $-x^2 - y^2$ |
| eyer | $x^2 - y^2$ |

## Makine öğrenmesi

| Kavram | Formül |
|---|---|
| doğrusal model, tek örnek | $\dfrac{\partial L}{\partial w_j} = 2(\hat{y} - y) x_j$ |
| vektör hâli | $\nabla_{\mathbf{w}} L = 2(\hat{y} - y) \mathbf{x}$ |
| gradyan inişi | $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$ |

## Pratik ipuçları

- Kısmi türevde öteki değişkenler çarpan olarak kalır; tek başına duruyorsa türevi $0$.
- Yönlü türevde yön vektörünü önce birim yap.
- Karışık türevlerde sıra önemli değil: $f_{xy} = f_{yx}$.
