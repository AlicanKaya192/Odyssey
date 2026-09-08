Sıralama, sınırlama ve tekilleştirmenin tek sayfalık özeti.

## Yazılış sırası

```sql
SELECT   [DISTINCT] [TOP n] sütunlar
FROM     tablo
WHERE    koşul
ORDER BY sütun [ASC|DESC];
```

Bu sıra **sabit**. `WHERE`'i `ORDER BY`'dan sonra yazmak sözdizimi
hatası veriyor.

## ORDER BY

| Yazım | Ne yapıyor |
|---|---|
| `ORDER BY price` | artan (varsayılan) |
| `ORDER BY price ASC` | aynısı, açıkça yazılmış |
| `ORDER BY price DESC` | azalan |
| `ORDER BY category, price DESC` | önce kategori artan, eşitlerde fiyat azalan |
| `ORDER BY 2` | `SELECT` listesinin ikinci sütunu — **kullanma** |

`DESC` **yalnızca yazıldığı sütuna** uygulanıyor. İki sütunun ikisini de
tersine çevirmek için ikisine de yazılması gerekiyor.

## TOP

| Yazım | Ne yapıyor |
|---|---|
| `SELECT TOP 3 ...` | ilk üç satır |
| `SELECT TOP 10 PERCENT ...` | satırların onda biri |
| `SELECT TOP 3 WITH TIES ...` | üçüncüyle eşit değerdekiler de gelir |

`WITH TIES` yalnızca `ORDER BY` varken çalışıyor ve sonucun üçten fazla
satır olmasına yol açabiliyor.

**`TOP`, `ORDER BY` olmadan anlamsız.** Sıra belirsizse "ilk üç" de
belirsiz.

Başka veritabanlarında bu iş `LIMIT` ile yapılıyor (`SELECT ... LIMIT 3`).
SQL Server'ın `TOP`'u `SELECT`'ten hemen sonra gelirken `LIMIT` sorgunun
sonuna yazılıyor.

## DISTINCT

Seçilen **satırın tamamına** bakıyor, tek bir sütuna değil.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Üç satır döner</span><span class="anat-body"><code>SELECT DISTINCT category FROM products</code> — yalnızca kategori seçildiği için tekrar edenler eleniyor.</span></div>
    <div class="anat-row"><span class="anat-label">Sekiz satır döner</span><span class="anat-body"><code>SELECT DISTINCT category, name FROM products</code> — her <code>name</code> farklı, yani her çift benzersiz.</span></div>
  </div>
</figure>

## Sunucunun işleme sırası

```
FROM -> WHERE -> SELECT -> ORDER BY
```

Bunun iki somut sonucu var:

- **`WHERE` takma adı göremiyor.** `SELECT price AS amount ... WHERE amount > 1000`
  hata veriyor.
- **`ORDER BY` takma adı görebiliyor.** Aynı sorguda
  `ORDER BY amount DESC` çalışıyor.

## NULL nereye düşüyor?

SQL Server `NULL`'u en küçük sayıyor:

| Sıralama | NULL nerede |
|---|---|
| `ASC` | başta |
| `DESC` | sonda |

Bu davranış veritabanları arasında değişiyor. Sıralanan sütunda `NULL`
olabiliyorsa nereye düştüğünü kontrol et.
