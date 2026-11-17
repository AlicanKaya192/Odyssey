`DownBlock` kanal sayısını artırıp haritayı yarıya indiren bir artık blok. Ana
yol hazır; `self.shortcut`'ı yaz: `x`'i ana yolun çıktısıyla aynı şekle
getiren bir `nn.Sequential`: `Conv2d(in_ch, out_ch, kernel_size=1,
stride=2, bias=False)` ve `BatchNorm2d(out_ch)`.

**Beklenen çıktı:**

```
(2, 32, 4, 4)
576
```
