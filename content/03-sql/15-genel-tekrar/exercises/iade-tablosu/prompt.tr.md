İadeleri tutan bir tablo kur ve iki iade ekle.

| Sütun | Tip | Kural |
|---|---|---|
| `id` | `INT` | kendiliğinden artan, birincil anahtar |
| `order_id` | `INT` | boş kalamaz, `orders` tablosuna bağlı |
| `reason` | `NVARCHAR(100)` | boş kalamaz |
| `quantity` | `INT` | boş kalamaz, 0'dan büyük |

Eklenecekler:

| order_id | reason | quantity |
|---|---|---|
| 1005 | `Damaged screen` | 1 |
| 1009 | `Wrong item` | 1 |

Denetim dört şeye bakıyor: sütunlar ve tipleri, `order_id`'nin `orders`'a
bağı, eklenen iki satır, ve kuralların çalışması — olmayan bir siparişe
(9999) ve 0 adete iade eklemek **reddedilmeli**.

Bu şemada hiç yabancı anahtar yok: 1 numaralı müşteri silindiğinde 3
siparişi öksüz kaldı (ölçüldü). Senin tablon bunu kendi için önlesin.
Bölümler: tablo tasarımı (09), veri eklemek (08).
