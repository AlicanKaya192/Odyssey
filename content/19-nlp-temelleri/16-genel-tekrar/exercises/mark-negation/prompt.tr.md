Kelime torbası olumsuzlamayı görmez. Klasik bir hile: olumsuzlayıcıdan sonra
gelen token'ların başına `NOT_` eklemek. `mark_negation(tokens)`:

- `NEGATORS`'tan bir token işareti **açar** (kendisi değişmez),
- `PUNCT`'tan bir token işareti **kapatır** (kendisi değişmez),
- işaret açıkken diğer token'lar `NOT_` önekini alır.

**Beklenen çıktı:**

```
it is not NOT_good NOT_at NOT_all . love it
```
