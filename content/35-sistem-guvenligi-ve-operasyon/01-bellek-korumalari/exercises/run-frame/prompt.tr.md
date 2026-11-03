`run_frame(size, canary, data)` bir çerçeve kursun: `size` sıfır, ardından
kanarya, ardından bir dönüş yeri (`0`). `data`'yı baştan başlayarak
yazsın, ama çerçevenin sonundan öteye **yazmasın** (oyuncak bellek
büyümez). Sonra kanaryaya baksın: yerindeyse `"ok"`, değişmişse
`"detected"` döndürsün.

**Beklenen çıktı:**

```
ok
ok
detected
detected
```
