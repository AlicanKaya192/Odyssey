`suppliers` tablosuna yeni bir tedarikçi ekle.

| Sütun | Değer |
|---|---|
| `code` | `S5` |
| `name` | `Baltic Parts` |
| `city` | `Gdansk` |
| `country` | `Poland` |

Bu bölümün ilk yazma işlemi. Buraya kadar hep `SELECT` yazdın; bu sefer
tabloda gerçekten bir satır oluşacak.

**Sütun listesini yaz.** Yazmadan da çalışıyor — değerler tablodaki sütun
sırasına göre dağıtılıyor — ama o yazım, tabloya yarın bir sütun eklendiği
gün sessizce yanlış yere yazmaya başlıyor.

Merak etme: çalıştırma bittiğinde bu satır geri alınıyor. Bir sonraki
denemende `suppliers` yine dört satır.
