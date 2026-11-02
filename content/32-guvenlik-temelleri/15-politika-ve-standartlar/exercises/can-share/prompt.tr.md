`channel_max` her kanalın taşıyabileceği en yüksek düzeyi tutuyor.

`can_share(level, channel, channel_max)` düzey kanalın sınırını aşmıyorsa
`True` döndürsün. Bilinmeyen kanal ya da `LEVELS`'ta olmayan düzey
`False`: varsayılan ret.

**Beklenen çıktı:**

```
True
False
False
False
```
