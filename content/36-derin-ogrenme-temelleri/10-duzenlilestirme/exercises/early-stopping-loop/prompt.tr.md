Büyük ağ 80 örnekle eğitiliyor ve her turda doğrulama kaybı ölçülüyor. Döngünün
sonuna erken durdurmayı yaz: kayıp en iyiden düşükse `best`, `best_epoch`'u
güncelle ve `waited`'ı sıfırla; değilse `waited`'ı artır ve `patience`'a
ulaşınca döngüden çık.

**Beklenen çıktı:**

```
True True
True
```
