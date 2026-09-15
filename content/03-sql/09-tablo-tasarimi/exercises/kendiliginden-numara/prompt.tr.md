Numarasını kendisi veren, durumu verilmezse `open` yazan bir tablo kur;
sonra iki kayıt ekle.

| Sütun | Tip | Kural |
|---|---|---|
| `id` | `INT` | 1'den başlayıp kendiliğinden artsın, birincil anahtar |
| `title` | `NVARCHAR(60)` | boş kalamaz |
| `status` | `NVARCHAR(20)` | boş kalamaz, verilmezse `'open'` |

Eklenecek iki kaydın yalnızca başlığını ver: `Printer is offline` ve
`VPN is slow`.

Asıl konu bu: `INSERT` içinde `id` ve `status` **yazılmıyor**. Numarayı
sunucu veriyor, durumu varsayılan değer dolduruyor. Kontrol hem satırlara
hem de bu iki işi gerçekten tablonun yapıp yapmadığına bakıyor.
