`next_word(dialogues, context)` dersteki modeli küçük ölçekte kursun.
Her diyaloğu (boşlukla ayrılmış metin) token'lara böl; her konumda önceki
1–7 token'ı bağlam olarak alıp ardından gelen token'ı say. Sonra verilen
`context` metninin en uzun tanıdık son kısmını bul ve o bağlamdan sonra en
sık gelen token'ı döndür (eşitlikte abece sırasında önce gelen).

**Beklenen çıktı:**

```
hello
hello
```
