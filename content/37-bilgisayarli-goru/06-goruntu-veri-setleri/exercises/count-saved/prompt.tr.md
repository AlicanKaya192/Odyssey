`count_saved(n, seed)` `make_shapes(n, seed=seed)` resimlerini geçici bir
klasöre (`tempfile.TemporaryDirectory()`) dersteki düzende (`kök/sınıf/
NNN.png`, gri, `uint8`) kaydetsin ve klasör silinmeden önce `SHAPES`
sırasıyla her sınıf klasöründeki `.png` sayısını liste olarak döndürsün.

**Beklenen çıktı:**

```
[11, 8, 11]
[4, 4, 4]
```
