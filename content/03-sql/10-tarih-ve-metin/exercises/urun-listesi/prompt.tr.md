Her kategori için ürünlerin adlarını **tek bir hücrede**, alfabetik
sırayla göster.

Sütunlar: `category_code`, `products`. Adlar virgül ve boşlukla (`', '`)
ayrılsın. Kategori koduna göre sırala.

```
category_code  products
-------------  ---------------------------------------------------
ACC            Cable, Headset, Keyboard, Microphone, Mouse, Webcam
COM            Desktop, Laptop
...
```

Satırları tek bir metinde toplamanın işlevi `STRING_AGG`; diğer toplama
işlevleri gibi `GROUP BY` ile çalışıyor.

**Sıra kendiliğinden gelmiyor.** Listenin içindeki sırayı ayrıca söylemen
gerekiyor; sorgunun sonundaki `ORDER BY` yalnızca satırları sıralıyor,
hücrenin içindeki adları değil. Kontrol bu yazımı arıyor.
