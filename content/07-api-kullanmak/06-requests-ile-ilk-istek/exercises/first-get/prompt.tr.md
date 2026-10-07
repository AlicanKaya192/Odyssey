İlk gerçek isteğini gönderiyorsun. Alıştırma sunucusunda 1 numaralı kitabı iste.

**Yapman gerekenler:**

1. `requests.get` ile `http://api.odyssey.test/books/1` adresine istek gönder.
2. Durum kodunu, `ok` değerini, kitabın başlığını ve yazarının adını
   aşağıdaki biçimde yazdır. Yazar, kitabın içindeki `author` sözlüğünde.

**Beklenen çıktı:**

```
status: 200
ok: True
title: Emma
author: Austen
```

Çalıştırınca terminalde isteğin de görünecek: `→ GET /books/1  200`.
