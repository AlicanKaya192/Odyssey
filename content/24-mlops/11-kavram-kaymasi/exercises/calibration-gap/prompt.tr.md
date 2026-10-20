Dersteki kalibrasyon sınamasını yapan `calibration_gap(probabilities, labels)` fonksiyonunu yaz:

- `probabilities`: modelin verdiği iptal olasılıkları.
- `labels`: gerçekleşen sonuçlar (`1` iptal, `0` kaldı).
- Olasılıkların ortalamasından etiketlerin ortalamasını çıkar, üç basamağa yuvarla.

Artı sonuç modelin fazla iptal beklediğini gösterir.

**Beklenen çıktı:**

```
0.067
0.0
-0.4
```
