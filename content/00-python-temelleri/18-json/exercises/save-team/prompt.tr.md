`team` listesini bir JSON dosyasına kaydet ve geri oku.

**Yapman gerekenler:**

1. `team`'i `team.json` dosyasına `json.dump` ile, `indent=2` vererek
   yaz (`"w"` kipi, `encoding="utf-8"`).
2. Dosyayı yeniden açıp `json.load` ile `loaded` adında bir değişkene oku.
3. Sırayla yazdır: `loaded == team`, takımdaki kişi sayısı ve rolü `"dev"`
   olan kişi sayısı (`dev_count`).

**Beklenen çıktı:**

```text
True
3
2
```

İlk satır `True` çıkıyorsa yazdığın liste dosyaya gidip **aynen** geri
gelmiş demektir.
