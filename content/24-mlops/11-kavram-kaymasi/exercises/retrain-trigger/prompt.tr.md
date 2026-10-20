Takvim + acil tetikleyici kuralını yazan `should_retrain(alert, months_since, every)` fonksiyonunu yaz:

- `alert`: kalite uyarısı çaldı mı (`True` / `False`).
- `months_since`: son eğitimden bu yana geçen ay.
- `every`: takvimin aralığı (ay).
- Uyarı çaldıysa ya da `months_since` en az `every` ise `"retrain"`, yoksa `"wait"` döndür.

**Beklenen çıktı:**

```
wait
retrain
retrain
```
