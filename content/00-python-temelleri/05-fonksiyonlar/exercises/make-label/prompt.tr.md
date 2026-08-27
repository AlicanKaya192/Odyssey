Kayıt satırlarının başına etiket koyan bir fonksiyon yaz.

`make_label` adında bir fonksiyon tanımla. İki parametre alsın:

| Parametre | Anlamı |
|---|---|
| `text` | etiketlenecek metin |
| `prefix` | başa gelecek etiket — **varsayılan değeri `INFO`** |

Fonksiyon şu biçimde bir metin **döndürsün**: etiket, iki nokta, boşluk, metin.

Sonra iki kez çağır:

- `first` değişkenine, `Server started` metnini **varsayılan etiketle**.
- `second` değişkenine, `Disk almost full` metnini `WARN` etiketiyle.

İkisini alt alta yazdır. Beklenen çıktı:

```
INFO: Server started
WARN: Disk almost full
```

> Fonksiyonun içinde `print` kullanma; sonucu `return` ile geri ver.
