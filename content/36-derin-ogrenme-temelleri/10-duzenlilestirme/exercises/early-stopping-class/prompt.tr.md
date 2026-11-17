`EarlyStopping.step(val_loss)` her turun doğrulama kaybını alsın: kayıp şimdiye
kadarki en iyiden düşükse en iyiyi güncelleyip sayacı sıfırlasın ve `False`
döndürsün; değilse sayacı artırsın ve sayaç `patience`'a ulaştıysa `True`
döndürsün.

**Beklenen çıktı:**

```
6
None
```
