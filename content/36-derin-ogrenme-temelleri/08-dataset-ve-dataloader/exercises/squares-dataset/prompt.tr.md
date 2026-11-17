`SquaresDataset(n)` `0`'dan `n − 1`'e kadar her `i` için `(x, x²)` çifti vermeli:
ikisi de tek elemanlı ondalık tensör (`torch.tensor([float(i)])`). Sınıfa
`__len__` ve `__getitem__` metotlarını yaz.

**Beklenen çıktı:**

```
[5, 3.0, 9.0]
[10, 0.0, 0.0]
```
