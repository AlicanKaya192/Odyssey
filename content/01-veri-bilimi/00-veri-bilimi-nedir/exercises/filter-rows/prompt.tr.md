Ankara'da notu 80 ve üstünde olan kim? Veri işlerinin çoğu böyle bir
soruyla başlıyor.

**Yapman gerekenler:**

1. `records` listesi başlangıç kodunda hazır.
2. Şehri `"Ankara"` **ve** notu 80 veya daha yüksek olan kayıtları bir listede
   topla; adı `selected` olsun.
3. Bu kayıtların yalnızca adlarını `names` adlı bir listede topla.
4. `names` listesini yazdır, sonra kaç kayıt seçildiğini yazdır.

**Beklenen çıktı:**

```
['Ada', 'Mina']
2
```

pandas'ta bu tek satır olacak:
`data[(data["city"] == "Ankara") & (data["score"] >= 80)]`
