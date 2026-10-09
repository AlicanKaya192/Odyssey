`Movie` TypedDict'i hazır: `title`, `year` ve olmayabilen `rating`.
`make_movie(title: str, year: int, rating: float | None = None) -> Movie`
fonksiyonunu yaz: `title` ve `year` her zaman, `rating` yalnızca `None`
değilse sözlükte olsun.

**Beklenen çıktı:**

```
['title', 'year']
8.4
```
