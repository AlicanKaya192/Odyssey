Bir programın gün boyunca istek attığı adresler kayıtta. İki soru soruyorsun:
hangileri **şifresiz** (`http`) gidiyor ve hangi bilgisayara kaç istek
gitmiş?

Kendi bilgisayarına (`localhost` ya da `127.0.0.1`) giden `http` istekleri
sorun değil; trafik bilgisayarından çıkmıyor.

**Yapman gerekenler:**

1. `insecure` adlı bir listeye, şeması `http` olan **ve** ana makinesi
   `localhost` ya da `127.0.0.1` olmayan adresleri topla (sırayı koru).
2. `Insecure:` yazdır, altına bu adresleri birer satırda yazdır.
3. `Requests per host:` yazdır, altına her ana makineyi ve istek sayısını
   ana makine adına göre **sıralı** yazdır.

**Beklenen çıktı:**

```
Insecure:
http://api.example.com/v1/login?user=ada
http://data.example.org/export?format=csv
Requests per host:
127.0.0.1 1
api.example.com 2
api.github.com 1
data.example.org 1
localhost 1
```
