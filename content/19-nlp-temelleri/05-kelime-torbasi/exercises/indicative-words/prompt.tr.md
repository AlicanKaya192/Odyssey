`indicative(label_a, label_b, k)` her kelime için `label_a` yorumlarındaki
payının `label_b` yorumlarındaki payına log oranını hesaplasın (iki sayıma da
+1 yumuşatma) ve oranı en büyük `k` kelimeyi büyükten küçüğe bir liste olarak
döndürsün. Dersteki hesabın genel hâli.

Çıktının ilk satırına bak: nötr yorumları en çok işaret edenler yazım
hataları ve sayılar. Bir sınıfta bir iki kez geçen nadir kelimelerin oranı
yapay olarak yüksek çıkıyor; 04'teki `min_df` bunun için.

Eşit puanlı kelimeler abece sırasıyla gelsin: `np.argsort(-puan,
kind="stable")` büyükten küçüğe sıralar ve eşitleri yerinde bırakır,
böylece sıra her bilgisayarda aynı olur.

**Beklenen çıktı:**

```
deos, 30, 11, battrey, bluetotoh
but, be, to, all, at
```
