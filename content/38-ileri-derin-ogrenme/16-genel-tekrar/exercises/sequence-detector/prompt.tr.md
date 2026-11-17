Dizilerde art arda "3, 5" arayan ağ ve veri hazır.

1. 20 dönem eğit: her dönemde `torch.randperm(500, generator=gen)` ile karıştır,
   50'lik gruplarla `cross_entropy`.
2. `model.eval()`; grup boyunu `torch.export.Dim` ile serbest bırakarak dışa
   aktar ve `detector.pt2` dosyasına kaydet.

Sondaki hazır kod dosyayı yükleyip altın çıktıyla karşılaştırıyor.

**Beklenen çıktı:**

```
True
True torch.Size([3, 2])
```
