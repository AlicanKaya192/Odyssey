`check(expected, sent)` sunucudaki jetonla (`expected`) formdan gelen
jetonu (`sent`) karşılaştırsın. İkisi de boş olmayan birer metinse ve
eşitse `True`, aksi hâlde `False` döndürsün. Karşılaştırma
`hmac.compare_digest` ile. Başlangıç kodu `==` kullanıyor ve iki boş
değeri eşit sayıyor.

**Beklenen çıktı:**

```
True
False
False
False
```
