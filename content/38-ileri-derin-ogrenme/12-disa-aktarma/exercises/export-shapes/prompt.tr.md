`export_shapes(batches)` hazır modeli 4 satırlık örnek girdiyle dışa
aktarıyor ve verilen her grup boyuyla çağırıp çıkış şeklini döndürüyor. Şu
hâliyle 4 dışındaki boylarda düşüyor: grup boyunu (0. boyut)
`torch.export.Dim` ve `dynamic_shapes` ile serbest bırak.

**Beklenen çıktı:**

```
[[3, 2], [7, 2]]
```
