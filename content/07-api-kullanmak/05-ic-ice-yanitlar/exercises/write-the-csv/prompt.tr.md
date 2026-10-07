Son adım: düzleştirdiğin satırları bir dosyaya yazmak. CSV dosyasını Excel de,
pandas da açabilir.

**Yapman gerekenler:**

1. Her kitaptan `id`, `title`, `price` (**float**), `author_name` ve `tags`
   (`|` ile birleşik) sütunlarından oluşan bir satır kur.
2. Satırları `csv.DictWriter` ile `books.csv` dosyasına yaz: önce başlık
   satırı (`writeheader`), sonra satırlar (`writerows`). Dosyayı
   `newline=""` ve `encoding="utf-8"` ile aç.
3. Dosyayı yeniden açıp içeriğini olduğu gibi yazdır.

**Beklenen çıktı:**

```
id,title,price,author_name,tags
1,Emma,12.5,Austen,classic|novel
2,Dune,9.99,Herbert,scifi|classic
3,Ulysses,15.0,Joyce,
4,Solaris,11.2,Lem,scifi
5,Persuasion,8.75,Austen,classic|romance|novel
```

Ulysses'in etiketi olmadığı için son sütunu boş: satır virgülle bitiyor.
