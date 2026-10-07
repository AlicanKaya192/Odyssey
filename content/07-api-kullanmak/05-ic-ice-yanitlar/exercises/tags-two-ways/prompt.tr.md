Kitapların `tags` alanı bir liste. Onu iki farklı biçimde tabloya dökeceksin.

**Yapman gerekenler:**

1. **Tek hücre:** her kitap için başlığı ve etiketlerini `|` ile birleşik
   yazdır. Etiketi yoksa birleşim boş kalır.
2. **Ayrı satırlar:** her kitap–etiket çifti için `{"book_id": ..., "tag": ...}`
   sözlüğünü `pairs` listesine ekle.
3. `pairs`'i kullanarak her etiketin kaç kitapta geçtiğini `tag_counts`
   sözlüğünde say. Etiketleri abece sırasıyla `tag: sayı` biçiminde yazdır.

**Beklenen çıktı:**

```
Emma: classic|novel
Dune: scifi|classic
Ulysses:
Solaris: scifi
Persuasion: classic|romance|novel
pairs: 8
classic: 3
novel: 2
romance: 1
scifi: 2
```
