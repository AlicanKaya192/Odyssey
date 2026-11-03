`hkdf_expand(prk_hex, info_hex, length)` HKDF'nin genişletme adımını
yapsın ve `length` baytı onaltılık döndürsün. Başlangıç kodu tek blok
üretiyor; 32 baytı geçen istekte kısa kalıyor. Bloklar şöyle birleşir:
`counter` 1'den başlar, her blok
`HMAC(prk, önceki_blok + info + bytes([counter]))` (ilk turda önceki
blok boş), çıktı `length`'e ulaşınca kırpılır.

**Beklenen çıktı:**

```
16
80
True
```
