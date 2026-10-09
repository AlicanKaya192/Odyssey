## Katmanlar ve etkinleştirmeler

| Etkinleştirme | Formül | Türev | Nerede |
|---|---|---|---|
| Sigmoid | `1 / (1 + e^(−z))` | `σ (1 − σ)` | ikili çıkış |
| tanh | `(e^z − e^(−z)) / (e^z + e^(−z))` | `1 − tanh²` | gizli katman (küçük ağlar) |
| ReLU | `max(0, z)` | `z > 0` ise 1, değilse 0 | gizli katman (derin ağlar) |
| Softmax | `e^(z_i) / Σ e^(z_j)` | çapraz entropiyle `p − y` | çok sınıflı çıkış |

Etkinleştirme olmasaydı katmanlar üst üste çarpılıp yine tek bir doğrusal
dönüşüm olurdu; derinliğin anlamı kalmazdı.

## Geri yayılım (bir gizli katman)

| Adım | Formül |
|---|---|
| İleri | `H = f(X W₁ + b₁)`, `p = σ(H W₂ + b₂)` |
| Çıkış | `dz₂ = (p − y) / n` |
| Çıkış ağırlıkları | `dW₂ = Hᵀ dz₂`, `db₂ = Σ dz₂` |
| Gizli | `dz₁ = (dz₂ W₂ᵀ) ⊙ f′(…)` |
| Gizli ağırlıklar | `dW₁ = Xᵀ dz₁`, `db₁ = Σ dz₁` |

## Pratikte

- scikit-learn: `MLPClassifier(hidden_layer_sizes=(10,), activation="tanh")`.
- Derin öğrenme kütüphaneleri (PyTorch, TensorFlow) türevleri **otomatik**
  hesaplar (autograd); geri yayılımı elle yazmak gerekmez.
- Girdileri ölçekle; ağırlıkları küçük rastgele sayılarla başlat.
- Öğrenme hızı ve dönem sayısı en önemli ayarlar; doğrulama kaybını izle.

## Sık hatalar

- Ağırlıkları sıfırla (ya da hepsini aynı sayıyla) başlatmak: bütün
  nöronlar aynı kalır (notta ölçüldü).
- Ölçeklememek: tanh ve sigmoid büyük girdide doyar, türev sıfıra iner.
- Türevi elle yazıp denetlememek: sayısal türevle karşılaştır.
- Eğitim doğruluğuna bakıp durmak: test ya da doğrulama kümesi şart.
