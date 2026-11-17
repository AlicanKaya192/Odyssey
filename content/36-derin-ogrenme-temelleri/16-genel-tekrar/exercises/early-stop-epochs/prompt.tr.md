`early_stop(val_losses, patience)` turların doğrulama kayıplarını sırayla
gezsin (turlar 1'den başlar). Kayıp en iyiden küçükse en iyi olur ve sayaç
sıfırlanır; değilse sayaç artar ve `patience`'a ulaşınca durulur.
`[en iyi tur, durulan tur]` döndür; hiç durulmazsa durulan tur son tur.

**Beklenen çıktı:**

```
[3, 6]
```
