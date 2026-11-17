`warmup_rates(base, warm, epochs)` oranı ilk `warm` turda doğrusal olarak
yükselten bir ısınma kursun: tur `e`'de katsayı `min(1, (e + 1) / warm)`.
`lr_scheduler.LambdaLR(optimizer, fonksiyon)` katsayıyı veren bir fonksiyon
alır. Başlangıç kodu oranları zaten topluyor; zamanlayıcıyı ekle.

**Beklenen çıktı:**

```
[0.025, 0.05, 0.075, 0.1, 0.1, 0.1]
```
