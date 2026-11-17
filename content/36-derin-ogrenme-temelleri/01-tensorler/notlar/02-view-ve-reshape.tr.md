PyTorch kodlarında `reshape`'in yanında sık sık `view` görürsün. İkisi de
şekli değiştirir; fark, verinin bellekte nasıl durduğunda:

```python
m = torch.arange(6).reshape(2, 3)
print(m.view(3, 2).shape)
mt = m.T
print(mt.shape, mt.is_contiguous())
try:
    mt.view(6)
except RuntimeError as error:
    print("reshape" in str(error))
print(mt.reshape(6).tolist())
```

```text
torch.Size([3, 2])
torch.Size([3, 2]) False
True
[0, 3, 1, 4, 2, 5]
```

- `view` yeni bir kopya yapmaz; aynı belleğe başka şekilden bakar. Bunun
  için elemanların bellekte sırayla (contiguous) durması gerekir.
- `m.T` (transpoz) satır ile sütunu yer değiştiriyor ama belleği
  taşımıyor; sıra bozuluyor ve `view` hata veriyor. Hata mesajı da
  `reshape` kullanmayı öneriyor.
- `reshape` gerekirse kopyalar, gerekmezse `view` gibi davranır. Emin
  değilsen `reshape` yaz.
