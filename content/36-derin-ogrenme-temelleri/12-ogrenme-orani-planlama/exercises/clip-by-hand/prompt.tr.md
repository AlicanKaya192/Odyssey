`clip_by_norm(grads, max_norm)` her parametrenin gradyanını bir sayı listesi
olarak alıyor. Bütün sayıların karelerinin toplamının karekökü toplam
normdur. Norm `max_norm`'u aşıyorsa her sayıyı `max_norm / norm` ile çarp,
aşmıyorsa dokunma. `[norm, kırpılmış listeler]` döndür, sayılar 4 basamaklı.

**Beklenen çıktı:**

```
[5.0, [[0.6, 0.8]]]
[3.0, [[1.0], [2.0, 2.0]]]
```
