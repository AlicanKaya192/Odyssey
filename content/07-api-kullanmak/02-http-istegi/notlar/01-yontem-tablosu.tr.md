HTTP yöntemleri ve özellikleri tek tabloda.

| Yöntem | İş | Gövde | Güvenli | Tekrarlanabilir |
|---|---|---|---|---|
| `GET` | Getir | Yok | Evet | Evet |
| `HEAD` | Yalnızca başlıkları getir | Yok | Evet | Evet |
| `OPTIONS` | Hangi yöntemler kullanılabilir? | Yok | Evet | Evet |
| `POST` | Yeni oluştur | Var | Hayır | **Hayır** |
| `PUT` | Tamamen değiştir | Var | Hayır | Evet |
| `PATCH` | Kısmen değiştir | Var | Hayır | Genellikle hayır |
| `DELETE` | Sil | Genellikle yok | Hayır | Evet |

## İki kelimeyi karıştırma

- **Güvenli:** sunucuda hiçbir şeyi değiştirmez. Okumak güvenli.
- **Tekrarlanabilir:** bir kez de on kez de gönderilse sonuç aynı. `DELETE`
  güvenli değil (siliyor) ama tekrarlanabilir (ikinci silme bir şey
  değiştirmiyor).

## Bunun pratikteki anlamı

Bağlantı koptu ve yanıt gelmedi. İstek sunucuya ulaştı mı, bilmiyorsun.

- `GET`, `PUT`, `DELETE` → yeniden gönder; en kötü ihtimalle aynı şey bir
  kez daha olur.
- `POST` → yeniden göndermeden önce dur. Sipariş iki kez oluşabilir. API
  bunun için bir çözüm sunuyorsa (örneğin her isteğe tek kullanımlık bir
  kimlik koymak) belgesinde yazar.

## PUT mu PATCH mi?

Kayıt: `{"title": "Emma", "author": "Austen", "price": 12}`

- `PATCH /books/42` gövde `{"price": 10}` → yalnızca fiyat değişir.
- `PUT /books/42` gövde `{"price": 10}` → kayıt **yalnızca fiyattan**
  oluşan bir kayıtla değiştirilir; başlık ve yazar kaybolabilir.

Kısmi değişiklik için `PATCH`; kaydın tamamını gönderiyorsan `PUT`.
