`upsample_cam(cam, size)` küçük bir haritayı `F.interpolate` ile
`mode="nearest"` kullanarak `size × size`'a büyütüp liste listesi olarak
döndürsün.

**Beklenen çıktı:**

```
[1.0, 1.0, 0.0, 0.0]
[1.0, 1.0, 0.0, 0.0]
[0.0, 0.0, 2.0, 2.0]
[0.0, 0.0, 2.0, 2.0]
```
