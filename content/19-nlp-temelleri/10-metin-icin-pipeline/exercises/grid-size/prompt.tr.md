Parametre ızgarası bir sözlük: anahtar `adım__parametre`, değer denenecek
değerlerin listesi.

- `count_fits(grid, folds)`: kaç model eğitilir? Bütün değer sayılarının
  çarpımı × kat sayısı (son yeniden eğitim hariç).
- `step_names(grid)`: ızgarada geçen adım adları (`__`'dan önceki kısım),
  tekrarsız ve sıralı.

**Beklenen çıktı:**

```
60
['model', 'tfidf']
```
