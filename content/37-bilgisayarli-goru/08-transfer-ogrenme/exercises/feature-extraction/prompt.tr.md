Kaynak ağ şekillerde eğitildi. `train_head(model, x, y)` özellik çıkarma
yapsın: gövdeyi (`model[0]`) dondursun, optimizer'a (Adam, `lr=0.005`)
yalnızca başı versin, yığın 8 ve `generator=torch.Generator().manual_seed(0)`
ile 20 tur eğitsin; her turda `model.train()`'den sonra gövdeyi `eval()`'e
alsın. Program gövdenin ağırlığının **ve** BatchNorm istatistiğinin
değişmediğini sınar.

**Beklenen çıktı:**

```
True
True
True
```
