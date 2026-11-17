Resimler geçici klasöre yazılmış. `data`'yı tek kanallı ve [0, 1] aralığında
veren bir `ImageFolder` olarak kur (`v2.ToImage`, `v2.Grayscale`,
`v2.ToDtype`), `loader`'ı yığın 8 ve
`generator=torch.Generator().manual_seed(0)` ile karıştıran bir `DataLoader`
yap.

**Beklenen çıktı:**

```
40 5
(8, 1, 16, 16) torch.int64
True
```
