`test_main.py`'deki üç test tek tek çalışınca geçiyor, birlikte
çalışınca ikisi düşüyor: `books` sözlüğü testler arasında paylaşılıyor.

**Yapman gereken:** testlere dokunmadan, her testten önce (ve sonra)
`books`'u temizleyen bir `autouse` fixture ekle.
