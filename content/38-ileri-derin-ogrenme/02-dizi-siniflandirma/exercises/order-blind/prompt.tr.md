`order_blind(seqs)` eğitilmemiş iki model (tohum hazır) kuruyor: kelime
torbası ve LSTM. Dizileri `flip(dims=[1])` ile tersine çevir ve her model
için, düz ve ters dizilerdeki çıkışların `torch.allclose` ile aynı olup
olmadığını `[bag_same, lstm_same]` olarak döndür. Çıkışları `torch.no_grad()`
içinde hesapla.

**Beklenen çıktı:**

```
[True, False]
```
