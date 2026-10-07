Bir programın ayarları `DEFAULTS`'ta duruyor; kullanıcı bazılarını bir JSON
dosyasıyla değiştirebiliyor. Yanına iki dosya konuldu:

- `good.json`: `{"theme": "light", "font_size": 14}`
- `broken.json`: sonunda fazladan virgül olan bozuk bir JSON

`missing.json` adında bir dosya **yok**.

**Yapman gerekenler:**

`load_settings(path)` fonksiyonunu yaz:

1. `settings = DEFAULTS.copy()` ile varsayılanların **kopyasını** al.
2. Dosyayı açıp `json.load` ile oku; dosyadaki her anahtarın değerini
   `settings`'e yaz (dosyada olmayanlar varsayılan kalır).
3. Dosya yoksa (`FileNotFoundError`) ya da bozuksa
   (`json.JSONDecodeError`) varsayılanların kopyasını değiştirmeden döndür.
4. `settings`'i döndür.

Sonra fonksiyonu sırayla `good.json`, `missing.json` ve `broken.json` ile
çağır; her sonucun `theme`, `font_size` ve `language` değerlerini bir
satırda yazdır.

**Beklenen çıktı:**

```text
light 14 en
dark 12 en
dark 12 en
```

Neden kopya? `settings = DEFAULTS` yazarsan ikisi **aynı** sözlük olur;
`good.json`'u yüklerken `DEFAULTS` de değişir ve sonraki çağrılar artık
gerçek varsayılanları görmez.
