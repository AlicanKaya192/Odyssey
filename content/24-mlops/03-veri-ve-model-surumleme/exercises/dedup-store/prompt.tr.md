İçerik adresli küçük bir depo yaz. Depo bir sözlük: `{"objects": {özet: metin}, "names": {ad: özet}}`.

`add(store, name, text)` fonksiyonu:

- Metnin özetini hesaplasın (UTF-8 baytlarının SHA-256'sı, onaltılık yazımın tamamı).
- `store["names"][name]` değerini bu özet yapsın (ad her zaman kaydedilir).
- Özet `store["objects"]` içinde zaten varsa metni **yeniden saklamasın** ve `"already stored"` döndürsün.
- Yoksa `store["objects"][özet] = text` yazıp `"stored"` döndürsün.

**Beklenen çıktı:**

```
stored
stored
already stored
names: 3 objects: 2
```
