Bir dosyadan okunmuş gibi bir fiyat var, ama **metin** olarak:

```python
value = "12.75"
```

Üç değişken oluştur:

- `whole`: sayının tam kısmı, **tam sayı** olarak (`12`)
- `doubled`: fiyatın iki katı, **ondalıklı sayı** olarak (`25.5`)
- `label`: `whole` ile `" pieces"` metni birleşmiş hâlde (`"12 pieces"`)

ve şunları yazdır:

```
12
25.5
12 pieces
```

İlk denemende büyük ihtimalle `int(value)` yazacaksın ve hata alacaksın.
Neden? `int()` yalnızca rakamlardan oluşan bir metni tam sayıya
çevirebilir; içinde nokta olan metni çeviremez. Önce metni ondalıklı sayıya
(`float`) çevirip sonra onu tam sayıya çevirmen gerekiyor.

> Dikkat: `int()` ondalıklı sayıyı **yuvarlamaz, keser**: `int(12.75)`
> sonucu `12`, `13` değil.
