`real_host(url)` adresin gerçek ana bilgisayarını küçük harfle
döndürsün; bulunamazsa boş metin (`""`). `urllib.parse.urlsplit(url).hostname`
kullan. Başlangıç kodu adresi `/` ile bölüyor ve `@` hilesine
kanıyor.

**Beklenen çıktı:**

```
'shop.example.com'
'203.0.113.66'
'shop.example.com'
''
```
