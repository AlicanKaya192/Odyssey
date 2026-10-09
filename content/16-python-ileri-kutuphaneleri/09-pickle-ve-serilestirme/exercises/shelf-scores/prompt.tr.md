`add_scores(path, pairs)` `shelve` ile her `[ad, puan]` çiftini o adın
listesine eklemeli ve sonda bütün rafı `{ad: [puanlar]}` sözlüğü olarak
(adlar sıralı) döndürmeli. Başlangıç kodu listeleri hep boş bırakıyor:
`db[name].append(...)` diskteki kayda yazılmıyor. Listeyi al, ekle, **geri
ata**.

**Beklenen çıktı:**

```
{'ada': [90, 85], 'alan': [75]}
```
