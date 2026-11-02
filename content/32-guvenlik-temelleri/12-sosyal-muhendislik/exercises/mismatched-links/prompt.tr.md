Her bağlantı `[metin, adres]`. Görünen metin bir alan adı ya da adres gibi
duruyorsa (içinde nokta varsa) ve gösterdiği sunucu adresin gittiği
sunucudan farklıysa bağlantı yanıltıcıdır.

`mismatched_links(links)` yanıltıcı bağlantıların **adreslerini** listedeki
sırayla döndürsün.

- Metnin sunucusu: başında `http://` ya da `https://` varsa at, ilk `/`'ye
  kadar al, küçük harfe çevir.
- Adresin sunucusu: `urlsplit(adres).hostname`.
- İçinde nokta olmayan metin ("Click here") karşılaştırılmaz.

**Beklenen çıktı:**

```
https://bank-example.test/pay
```
