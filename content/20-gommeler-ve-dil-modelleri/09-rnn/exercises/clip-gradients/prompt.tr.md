`clip_gradients(grads, max_norm)` türevlerin büyüklüğünü (kareler toplamının
karekökü) hesaplasın. Büyüklük `max_norm`'u aşıyorsa her türevi `max_norm /
büyüklük` ile çarpsın, aşmıyorsa olduğu gibi bıraksın. 3 basamak.

**Beklenen çıktı:**

```
[3.0, 4.0]
[3.0, 4.0]
[0.0, 0.0]
```
