`main.py`'deki kitap API'si hazır (salt okunur). `test_main.py`'ye **en az
üç** test yaz:

1. `POST /books` geçerli kitapla `201` ve
   `{"id": 1, "title": ..., "year": ...}` dönüyor.
2. Olmayan kitap (`GET /books/999`) `404` dönüyor.
3. Boş başlık (`{"title": "", ...}`) `422` dönüyor.

Testlerin uygulamanın bozuk hâllerine karşı da çalıştırılacak: her
hatada en az biri düşmeli.
