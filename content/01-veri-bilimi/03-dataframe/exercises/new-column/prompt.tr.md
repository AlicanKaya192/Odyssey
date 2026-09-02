Tabloya hesaplanmış iki sütun ekleyeceksin — **döngü yazmadan**.

**Yapman gerekenler:**

1. Notu **75 ve üstünde** olanlar için `True` taşıyan `passed` sütunu ekle.
2. Herkesin notuna 10 ekleyen `bonus` sütunu ekle.
3. `name`, `score`, `passed` ve `bonus` sütunlarını birlikte yazdır.
4. Kaç kişinin geçtiğini yazdır.

**Beklenen çıktı:**

```
    name  score  passed  bonus
0    Ada     82    True     92
1  Kerem     74   False     84
2   Mina     91    True    101
3  Deniz     68   False     78
4    Efe     88    True     98
3
```

**Dikkat:** dört sütunu birlikte seçerken **iç içe köşeli parantez**
gerekiyor: `data[["name", "score", "passed", "bonus"]]`. Tek parantez tek
sütun demek.

Son satırda `True` değerleri toplanıyor — `True` toplamada 1 sayılıyor.
