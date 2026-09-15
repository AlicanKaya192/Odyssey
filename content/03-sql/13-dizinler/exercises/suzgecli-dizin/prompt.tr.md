`events` tablosunda `amount` yalnızca satın almalarda dolu: 20 000
satırın 15 000'inde boş (`NULL`). Tutara göre arama yapan sorgular için
`amount` üzerine bir dizin kur, ama dizin **yalnızca `amount`'u dolu olan
satırları** tutsun.

Ölçüldü:

| Dizin | Dizinlerin kapladığı yer |
|---|---|
| `amount` üzerine, süzgeçsiz | 408 KB |
| `amount` üzerine, `amount IS NOT NULL` süzgeçli | **128 KB** |

Süzgeçli dizinle `WHERE amount > 490` 2 okuma. Boş satırlar dizinde
olmadığı için `WHERE amount IS NULL` o dizini kullanamıyor — zaten
kullanması da gerekmiyor.

Denetim dizinin süzgecine de bakıyor: koşul `amount` üzerinde olmalı.
