Bir REST API'yi okurken ve tasarlarken elinin altında dursun.

## Adres kalıpları

| Kalıp | Örnek | Anlam |
|---|---|---|
| `/kaynaklar` | `/books` | Koleksiyon |
| `/kaynaklar/<id>` | `/books/42` | Tek öğe |
| `/kaynaklar/<id>/alt-kaynaklar` | `/authors/6/books` | İlişkili koleksiyon |
| `/kaynaklar?süzgeç=...` | `/books?author=Austen` | Süzülmüş koleksiyon |
| `/v2/kaynaklar` | `/v2/books` | Sürüm |

## Yöntem × adres

| | Koleksiyon `/books` | Öğe `/books/42` |
|---|---|---|
| `GET` | Listele (200) | Getir (200 / 404) |
| `POST` | Oluştur (201) | Genellikle 405 |
| `PUT` | Genellikle 405 | Tamamen değiştir (200) |
| `PATCH` | Genellikle 405 | Kısmen değiştir (200) |
| `DELETE` | Nadiren (hepsini sil) | Sil (204) |

## Adlandırma

- Çoğul isimler: `/books`, `/authors` (tekil `/book` değil).
- Küçük harf, kelimeler arası tire: `/reading-lists`.
- Fiil yok: `/books/42/delete` değil, `DELETE /books/42`.
- Dosya uzantısı yok: `/books.json` değil; biçimi `Accept` başlığı söyler.

## Kontrol soruları

Bir uç noktayı değerlendirirken sor:

1. Adreste fiil var mı?
2. Yöntem işi doğru anlatıyor mu? (`GET` bir şeyi değiştiriyor mu?)
3. Başarı ve hata kodları anlamlı mı? (hata için `200` dönüyor mu?)
4. Süzme sorguda mı, yeni bir adreste mi?
5. İstek kendi başına anlaşılıyor mu? (kimlik her istekte mi?)
