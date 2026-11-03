`digest` hazır. `sign(message, d, n)` mesajın özetini **özel üs** `d` ile
imzalasın: `pow(özet, d, n)`. Başlangıç kodu açık üs 65537'yi kullanıyor;
açık anahtarla "imzalamak" herkesin yapabileceği bir şeydir ve
doğrulamadan geçmez.

**Beklenen çıktı:**

```
True
```
