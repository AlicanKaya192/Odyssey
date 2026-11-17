Tensör işlemlerinde sonucun türü (dtype) bazen şaşırtır. Dersteki `torch`
ile birkaç örnek:

```python
i = torch.tensor([1, 2, 3])
print((i / 2).dtype, (i // 2).tolist(), (i * 0.5).dtype)
print(torch.tensor([1, 2.5]).dtype, torch.tensor([True, False]).dtype)
try:
    i.mean()
except RuntimeError as error:
    print(str(error).split(".")[0])
print(i.float().mean().item())
```

```text
torch.float32 [0, 1, 1] torch.float32
torch.float32 torch.bool
mean(): could not infer output dtype
2.0
```

- `/` her zaman ondalıklı sonuç veriyor (`float32`); `//` tam sayı bölmesi,
  tam sayı kalıyor.
- Tam sayı ile ondalık karışınca sonuç ondalık oluyor. Listede tek bir
  ondalık sayı varsa bütün tensör `float32`.
- Karşılaştırmalar (`>`, `==`) `bool` tensör veriyor.
- `mean` gibi ortalama alan işlemler tam sayı tensörde çalışmıyor; önce
  `.float()`.

Kısa kural: modele giden her şey `float32`, sınıf etiketleri `int64`.
Bir hata mesajında `Long` görürsen `int64`, `Float` görürsen `float32`,
`Double` görürsen `float64` anlaşılır.
