Aynı bilgi bazen adrese, bazen sorguya yazılabilir. Hangisini seçeceğin
bir tasarım kararı.

| Soru | Yol parametresi | Sorgu parametresi |
|---|---|---|
| Neyi anlatır? | **Hangi** şey (kimlik) | O şeyin **hangi kısmı, hangi sırayla** |
| Örnek | `/books/42` | `/books?year_from=1950&page=2` |
| Gönderilmezse | Adres eksik: başka bir uç nokta | Varsayılan değer |
| Kaç tane? | Az (bir ya da iki) | İstediğin kadar, sırası önemsiz |

## Kural

- **Kaynağı seçen** bilgi yolda: `/books/42`, `/authors/7/books`.
- **Sonucu süzen, sıralayan, sayfalayan** bilgi sorguda: `?author=`,
  `?sort=year`, `?page=2`.
- Sorgu isteğe bağlı olduğu için yeni bir süzgeç eklemek eski istemcileri
  bozmaz; yola yeni bir parça eklemek bozar.

## Örnekler

| İstek | Doğru yer |
|---|---|
| 42 numaralı kitap | yol: `/books/42` |
| 1950'den sonraki kitaplar | sorgu: `/books?year_from=1950` |
| Austen'in kitapları | ikisi de olur: `/authors/austen/books` ya da `/books?author=Austen` |
| Yıla göre sıralı | sorgu: `/books?sort=year` |
| İkinci sayfa | sorgu: `/books?page=2` |

## Akılda kalsın

> Yol "hangisi?" sorusunu, sorgu "nasıl?" sorusunu cevaplar.
