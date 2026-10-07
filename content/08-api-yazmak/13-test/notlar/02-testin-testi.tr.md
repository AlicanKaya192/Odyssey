Bir testin geçmesi tek başına bir şey kanıtlamaz: hiçbir şeyi denetlemeyen
bir test de geçer. İyi bir test **bozuk kodda düşer**.

## Kendine sor: bu satırı bozsam test düşer mi?

```python
@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
```

| Bozulma | Hangi test yakalar? |
|---|---|
| `raise` satırı silindi | Olmayan kitap → `404` bekleyen test |
| `404` yerine `400` yazıldı | Aynı test, kodu da denetliyorsa |
| `return books[book_id]` yerine `return {}` | Gövdeyi denetleyen test |

Yalnızca `assert r.status_code == 200` yazan test üçüncüsünü yakalamaz.

## Odyssey'nin yaptığı

Bu bölümün alıştırmalarında testlerin önce olduğu gibi, sonra uygulamanın
**kasıtlı olarak bozulmuş** hâllerine karşı çalıştırılıyor. Her bozuk hâlde
en az bir testin düşmesi gerekiyor; düşmezse terminal hangi hatayı
kaçırdığını söylüyor (örneğin "olmayan kitap 404 yerine 200 dönüyor").

Buna yazılım dünyasında **mutasyon testi** deniyor: kodu küçük küçük
değiştirip testlerin fark edip etmediğine bakmak.

## Neyi test etmemeli?

- FastAPI'nin kendisini: `422`'nin `detail` listesindeki her alanı tek tek
  denetlemeye gerek yok; durum kodu yeter.
- Rastgele değerlerin kendisini: jetonun içeriği her seferinde farklı;
  uzunluğuna ya da varlığına bak.
