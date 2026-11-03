## Anahtar üretimi

| Adım | Formül | Oyuncak örnek |
|---|---|---|
| İki asal | `p`, `q` | 61, 53 |
| Modül | `n = p * q` | 3233 |
| `phi` | `(p - 1) * (q - 1)` | 3120 |
| Açık üs | `gcd(e, phi) == 1` | 17 (gerçekte 65537) |
| Özel üs | `d = pow(e, -1, phi)` | 2753 |

- **Açık anahtar:** `(e, n)`. Herkese verilir.
- **Özel anahtar:** `(d, n)`. `p`, `q` ve `phi` de gizlidir.

## Şifreleme ve çözme

| İşlem | Formül | Örnek |
|---|---|---|
| Şifrele | `c = pow(m, e, n)` | `pow(65, 17, 3233) = 2790` |
| Çöz | `m = pow(c, d, n)` | `pow(2790, 2753, 3233) = 65` |

- `m < n` olmalı; büyük mesaj doğrudan şifrelenmez.
- Metin → sayı: `int.from_bytes(veri, "big")`; geri: `sayi.to_bytes(uzunluk, "big")`.

## Neden güvenli

`n`'den `d`'yi bulmak için `phi`, onun için de `p` ve `q` gerekir. Büyük
bir `n`'i asallarına ayırmanın bilinen hızlı bir yolu yoktur. Güvenlik
bütünüyle `n`'in **büyüklüğüne** bağlıdır.

## Ders kitabı RSA'sının sorunu

- Belirleyicidir: aynı mesaj → aynı şifreli metin.
- Olası mesajlar azsa herkes açık anahtarla deneyip karşılaştırabilir.
- Çözüm: şifrelemeden önce rastgele dolgu, **OAEP**.
