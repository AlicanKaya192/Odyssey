Bir soruyu parametrelere çevirmek: alıştırma sunucusundan örnekler.

| Soru | `params` |
|---|---|
| Austen'ın bütün kitapları | `{"author": "Austen"}` |
| En ucuz 3 klasik | `{"tag": "classic", "sort": "price", "per_page": 3}` |
| En yeni bilimkurgu | `{"tag": "scifi", "sort": "-year", "per_page": 1}` |
| 1900–1930 arası, yıla göre | `{"year_min": 1900, "year_max": 1930, "sort": "year"}` |
| Başlığında "dune" geçenler | `{"q": "dune"}` |
| Hem bilimkurgu hem mizah | `{"tag": ["scifi", "humor"]}` |

## Bir soruyu çözmenin sırası

1. **Ne istiyorum?** Kayıtların hangisi (süzme), hangi sırayla (sıralama),
   kaç tane (sınır)?
2. **Belgede hangi parametre var?** Ad ve değer biçimi (`sort=-year` mı,
   `order=desc` mi?).
3. **İsteği gönder, `r.url`'ye bak.** Giden adres istediğinle aynı mı?
4. **Sonucu denetle.** Sayı ve sıra beklediğin gibi mi? `meta.total` kaç?

## Sunucunun yapamadığı süzme

Alıştırma sunucusu fiyat aralığıyla süzmüyor (`price_max` yok). O zaman:

```python
params = {"tag": "classic", "per_page": 20}
books = requests.get(BASE + "/books", params=params).json()["data"]
cheap = [b for b in books if b["price"] < 10]
```

Önce sunucunun yapabildiği kadar daralt (`tag=classic`), kalanını Python'da
süz. Böylece gereğinden fazla kayıt indirmezsin.
