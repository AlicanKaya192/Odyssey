`movie` sözlüğünü JSON metnine çevir.

**Yapman gerekenler:**

1. `json.dumps` ile `movie`'yi `text` adında bir metne çevir; `text`'in
   türünü ve kaç karakter olduğunu (`len`) yazdır.
2. Aynı sözlüğü `indent=2` ile `pretty` adında okunur bir metne çevir ve
   yazdır.

**Beklenen çıktı:**

```text
<class 'str'>
96
{
  "title": "Arrival",
  "year": 2016,
  "genres": [
    "drama",
    "sci-fi"
  ],
  "seen": false,
  "rating": null
}
```

`False` ve `None`'ın JSON'da nasıl yazıldığına bak.
