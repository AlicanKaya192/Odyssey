`resize_boxes(boxes, old_size, new_size)` kare bir resim `old_size`'tan
`new_size`'a ölçeklenince kutuları aynı oranla çarpsın ve
`clip_boxes_to_image` ile yeni resmin içine kırpsın (liste döndürür).

**Beklenen çıktı:**

```
64 [8.0, 12.0, 28.0, 24.0]
64 [50.0, 40.0, 62.0, 60.0]
16 [2.0, 3.0, 7.0, 6.0]
16 [12.5, 10.0, 15.5, 15.0]
```
