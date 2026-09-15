Siparişlere not tutan bir `order_notes` tablosu kur. Bir sipariş
silinince ona ait notlar da **kendiliğinden** silinsin.

| Sütun | Tip | Kural |
|---|---|---|
| `id` | `INT` | kendiliğinden artsın, birincil anahtar |
| `order_id` | `INT` | boş kalamaz, `orders.id`'ye bağlı |
| `note` | `NVARCHAR(200)` | boş kalamaz |

Siparişi olmayan bir not anlamsız; bu yüzden bağın varsayılan davranışı
("çocuğu olan ebeveyni silme") yerine burada zincirleme silme doğru.

Kontrol bağın varlığını da deniyor: olmayan bir siparişe not eklemek
reddedilmeli. Sonra iki siparişe not ekleyip birini siliyor ve geriye
yalnızca diğerinin notunun kalmasını bekliyor.
