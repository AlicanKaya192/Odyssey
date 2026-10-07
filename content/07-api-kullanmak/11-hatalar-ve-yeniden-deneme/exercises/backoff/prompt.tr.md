Yeniden denemeyi bir fonksiyona dönüştür; bekleme her denemede katlansın ve
düzeltilmesi gereken hatalarda hiç beklenmesin.

**Yapman gerekenler:**

1. `get_with_retry(url, attempts)` fonksiyonunu yaz:
   - her denemede `timeout=5` ile istek göndersin,
   - kod 500'den küçükse yanıtı hemen **döndürsün** (başarı ya da 4xx),
   - `5xx`, `Timeout` ya da `ConnectionError`'da beklesin ve yeniden
     denesin; ilk bekleme **0.5** saniye, her seferinde iki katı,
   - son denemeden sonra beklemesin; denemeler biterse `None` döndürsün.
2. Üç adresi dene ve sonucu yazdır: `/flaky` (4 deneme), `/books/99` (4
   deneme), `/broken` (3 deneme). Yanıt varsa kodunu, `None` ise `gave up`
   yaz.

**Beklenen çıktı:**

```
/flaky -> 200
/books/99 -> 404
/broken -> gave up
```

Kontrol `/books/99` için **yalnızca bir** istek atıldığına ve `/flaky`
denemeleri arasında beklendiğine bakıyor.
