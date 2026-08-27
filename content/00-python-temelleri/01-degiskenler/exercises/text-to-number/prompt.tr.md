Sana iki değişken verildi:

- `price_text` — bir **metin**, içinde `"45"` yazıyor
- `count` — bir **sayı**, `3`

Yapman gerekenler:

1. `price_text` metnini tam sayıya çevir.
2. `count` ile çarp ve sonucu `total` adında bir değişkende tut.
3. Sonucu f-string kullanarak yazdır.

Beklenen çıktı:

```
Total: 135
```

> Neden çevirmek gerekiyor? Bir metni sayıyla çarparsan Python onu tekrar eder: `"45" * 3` sonucu `"454545"` olur, `135` değil.
