`categories` tablosuna iki kategori ekle.

| `code` | `name` |
|---|---|
| `NET` | `Networking` |
| `PRN` | `Printing` |

**Tek bir `INSERT` ile.** İki ayrı komut yazarsan kontrol geçmiyor.

Sebebi bir kural değil, ölçülebilir bir fark: tek komut çalıştığında
sunucu "**2** satır etkilendi" diyor, iki ayrı komutta sonuncusu için
"**1**" diyor. Kontrol bu sayıya bakıyor.

Peki neden tek komut? Çünkü ya ikisi birden giriyor ya hiçbiri. İkinci
satırda bir sorun çıkarsa ilki de girmemiş oluyor — yarım kalmış veri
olmuyor.
