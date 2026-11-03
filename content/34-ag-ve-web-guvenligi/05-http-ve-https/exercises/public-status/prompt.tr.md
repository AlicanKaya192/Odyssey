`public_status(found, allowed, logged_in)` bir kaynak isteğine verilecek
durum kodunu döndürsün. Giriş yapılmamışsa `401`. Giriş yapılmışsa ve
kaynak yoksa **ya da** kişinin yetkisi yoksa `404`: başkasına ait
kaynağın var olduğu ele verilmez. İkisi de tamamsa `200`.

**Beklenen çıktı:**

```
401
200
404
404
```
