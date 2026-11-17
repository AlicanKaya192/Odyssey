Dersteki modelin içinde ne var? `print(model)` katmanları sırayla
gösteriyor; `named_parameters()` her parametrenin adını ve şeklini veriyor:

```python
print(model)
for name, p in model.named_parameters():
    print(name, tuple(p.shape))
print(sum(p.numel() for p in model.parameters()))
```

```text
Sequential(
  (0): Linear(in_features=64, out_features=32, bias=True)
  (1): ReLU()
  (2): Linear(in_features=32, out_features=10, bias=True)
)
0.weight (32, 64)
0.bias (32,)
2.weight (10, 32)
2.bias (10,)
2410
```

- `0.weight` birinci katmanın (sırası 0) ağırlıkları: `32 × 64`, yani her
  çıktı için 64 ağırlık. `0.bias` 32 sabit.
- ReLU'nun (sırası 1) parametresi yok; listede görünmüyor.
- `2.weight` `10 × 32`, `2.bias` 10 sabit.
- Toplam `32·64 + 32 + 10·32 + 10` = 2410 sayı. Eğitim bu
  sayıların hepsini ayarlıyor. Büyük dil ve görüntü modellerinde bu sayı
  milyarları buluyor; fikir aynı.

`p.numel()` bir tensördeki eleman sayısı (number of elements). Bir
katmanın ağırlık şekli `(çıktı, girdi)` sırasında yazılıyor; ilk bakışta
ters gibi görünür, ama hep böyle.
