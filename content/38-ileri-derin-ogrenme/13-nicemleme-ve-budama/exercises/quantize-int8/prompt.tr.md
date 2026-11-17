`quantize_int8(values)` simetrik, tensör başına nicemleme yapsın: ölçek
`en büyük |w| / 127`, `round(w / ölçek)`, `[-127, 127]`'ye kırp, `int8`.
`[int8 değerlerin listesi, ölçek]` döndürsün; ölçeği 4 basamakla
(`round(scale.item(), 4)`).

**Beklenen çıktı:**

```
[[50, -127, 1], 0.01]
```
