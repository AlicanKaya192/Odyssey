`shift_view(image, dx, dy, flip)` iki boyutlu bir görüntüyü (`(H, W)` liste)
`torch.roll` ile satırlarda `dy`, sütunlarda `dx` kadar kaydırsın; `flip`
doğruysa sonra yatay çevirsin (`flip(-1)`). Liste döndürsün.

**Beklenen çıktı:**

```
[[3.0, 1.0, 2.0], [6.0, 4.0, 5.0]]
[[6.0, 5.0, 4.0], [3.0, 2.0, 1.0]]
```
