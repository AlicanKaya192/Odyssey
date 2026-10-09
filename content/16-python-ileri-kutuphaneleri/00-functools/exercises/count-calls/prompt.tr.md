`count_calls(func)` dekoratörünü yaz: sarmalayıcı her çağrıda
`wrapper.calls` sayacını bir artırsın ve asıl fonksiyonun sonucunu
döndürsün; sayaç 0'dan başlasın. `@wraps(func)` ile asıl fonksiyonun adı
korunsun. Alttaki satırlar dekoratörü `square` üstünde deniyor.

**Beklenen çıktı:**

```
5
square 81
```
