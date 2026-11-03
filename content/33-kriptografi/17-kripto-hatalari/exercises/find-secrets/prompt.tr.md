`find_secrets(source)` kaynak koddaki gömülü sırların satır
numaralarını (1'den başlayarak) döndürsün. Bir satır, adında `key`,
`secret`, `password` ya da `token` geçen bir değişkene **tırnak içinde**
değer atıyorsa sırdır; büyük/küçük harf fark etmez. Başlangıç
kodunun düzenli ifadesi yalnızca `password`'ü arıyor.

**Beklenen çıktı:**

```
[2, 5]
```
