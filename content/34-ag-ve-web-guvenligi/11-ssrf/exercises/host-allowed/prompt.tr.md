`allowed(url, hosts)` adresi `urlsplit` ile ayrıştırsın; şeması `http`
ya da `https` **ve** ana bilgisayarı `hosts` listesinde birebir varsa
`True`, değilse `False` döndürsün. Başlangıç kodu metin aramasıyla
denetliyor ve `@` içeren adrese kanıyor.

**Beklenen çıktı:**

```
True
False
False
False
```
