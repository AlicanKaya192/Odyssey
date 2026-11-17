Karıştırmanın sırası bir rastgele üreteçten geliyor. Üreteci tohumla
sabitlersen aynı sıra her çalıştırmada tekrarlanır:

```python
small = TensorDataset(torch.arange(10))
for seed in [0, 0, 1]:
    loader = DataLoader(small, batch_size=4, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    print(seed, [b[0].tolist() for b in loader])
print("-", [b[0].tolist() for b in DataLoader(small, batch_size=4)])
```

```text
0 [[3, 7, 5, 2], [0, 8, 1, 6], [9, 4]]
0 [[3, 7, 5, 2], [0, 8, 1, 6], [9, 4]]
1 [[4, 6, 9, 2], [3, 1, 0, 7], [8, 5]]
- [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
```

- Aynı tohum (0, 0) aynı sırayı verdi; başka tohum (1) başka sırayı.
- Karıştırmasız (`shuffle` yazılmadı, varsayılanı `False`) sıra veri
  setindeki sıra.
- Tek elemanlı bir `TensorDataset`'te bile her örnek bir demet; bu yüzden
  `b[0]`.

Kural: **eğitim** yükleyicisinde `shuffle=True` (ve sabit üreteç),
**doğrulama ve test** yükleyicisinde `shuffle=False`. Değerlendirmede sıra
sonucu değiştirmez ama sabit sıra, tahminleri etiketlerle yan yana koymayı
ve hataları bulmayı kolaylaştırır.
