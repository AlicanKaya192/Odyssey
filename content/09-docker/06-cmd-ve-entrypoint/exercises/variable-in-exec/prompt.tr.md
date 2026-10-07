Bu imaj `hi Ada` yazmalı ama `hi $NAME` yazıyor: exec biçiminde değişkeni
açacak bir kabuk yok.

**Yapman gereken:** `CMD`'yi exec biçiminde bırakarak kabuğu açıkça çağır:
`sh -c` ile `echo hi $NAME` çalışsın.

**Beklenen çıktı:**

```
hi Ada
```
