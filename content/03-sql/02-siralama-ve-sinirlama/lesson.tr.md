# Sıralama ve Sınırlama

Bir önceki bölümde hangi sütunları ve hangi satırları istediğini söylemeyi
öğrendin. Sonuç geldi ama **sırası sana ait değildi**.

Bu bölümde üç şey var: sonucu sıralamak (`ORDER BY`), baştan birkaç satır
almak (`TOP`) ve tekrar edenleri elemek (`DISTINCT`).

Aynı `products` tablosuyla devam ediyoruz.

## Sunucu sıra garantisi vermiyor

Önce bunu netleştirelim, çünkü çoğu hata buradan çıkıyor.

`ORDER BY` yazmadığın bir sorguda satırların hangi sırayla geleceği
**belirsizdir.** Bugün `id` sırasında gelebilir, yarın tablo büyüdüğünde
başka bir sırada gelir. Sunucu en hızlı bulduğu yoldan okuyor ve o yol
değişebiliyor.

Yani: **sıra önemliyse `ORDER BY` yazmak zorundasın.** "Zaten sıralı
geliyor" diye bırakılan sorgular, aylar sonra sebepsiz bozulan
raporların en yaygın sebebi.

## ORDER BY

Sıralanacak sütunu yazıyorsun:

```sql
SELECT name, price FROM products ORDER BY price;
```

Varsayılan **artan** (küçükten büyüğe). Açıkça yazmak istersen `ASC`,
tersi için `DESC`:

```sql
SELECT name, price FROM products ORDER BY price DESC;
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ASC</span><span class="anat-body">artan — küçükten büyüğe, A'dan Z'ye. <b>Varsayılan</b>, yazılmasa da bu uygulanıyor.</span></div>
    <div class="anat-row"><span class="anat-label">DESC</span><span class="anat-body">azalan — büyükten küçüğe, Z'den A'ya.</span></div>
  </div>
</figure>

### Birden çok sütunla sıralamak

Virgülle ekliyorsun. **Sıra önemli:** önce yazılan sütuna göre
sıralanıyor, o sütunda eşit olanlar kendi aralarında ikinciye göre:

```sql
SELECT category, name, price
FROM products
ORDER BY category, price DESC;
```

Bu sorgu önce kategorileri alfabetik diziyor, sonra her kategorinin içinde
pahalıdan ucuza sıralıyor.

**Her sütunun kendi yönü var.** `ORDER BY category, price DESC` yazdığında
`DESC` yalnızca `price` için geçerli; `category` hâlâ artan. İkisini de
tersine çevirmek istersen ikisine de yazman gerekiyor.

## ORDER BY en son çalışıyor

Geçen bölümde `WHERE` içinde takma ad kullanamadığını gördün. `ORDER BY`
bunun **tersi**:

<figure class="fig">
  <div class="flow">
    <span class="node">FROM</span>
    <span class="arrow">-&gt;</span>
    <span class="node">WHERE</span>
    <span class="arrow">-&gt;</span>
    <span class="node">SELECT</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">ORDER BY</span>
  </div>
  <figcaption>ORDER BY en sonda çalışıyor; SELECT'in ürettiği takma adlar o sırada hazır.</figcaption>
</figure>

```sql
SELECT name, price AS amount
FROM products
ORDER BY amount DESC;
```

Bu çalışıyor. Aynı takma adı `WHERE` içinde kullansaydın hata alacaktın.
Tek bir kuralın iki farklı sonucu: **`WHERE` erken, `ORDER BY` geç.**

### Sütun numarasıyla sıralamak

`ORDER BY 2` yazmak da mümkün — "`SELECT` listesindeki ikinci sütun"
demek. Kısa ama **kullanma**: biri `SELECT` listesine sütun eklediğinde
sorgu sessizce başka bir sütuna göre sıralanmaya başlıyor. Adını yaz.

## TOP: baştan birkaç satır

```sql
SELECT TOP 3 name, price
FROM products
ORDER BY price DESC;
```

En pahalı üç ürün. `TOP` **`SELECT`'ten hemen sonra** yazılıyor; bu
T-SQL'e özgü — başka veritabanlarında `LIMIT` var.

**`TOP`'u `ORDER BY` olmadan yazma.** "İlk 3" diye bir şey yok: sıra
belirsizse hangi üçünün geleceği de belirsiz. Sorgu hata vermiyor, her
çalıştırmada farklı sonuç verebiliyor.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Anlamsız</h4>
      <pre><code>SELECT TOP 3 name
FROM products;</code></pre>
    </div>
    <div class="ok">
      <h4>Anlamlı</h4>
      <pre><code>SELECT TOP 3 name
FROM products
ORDER BY price DESC;</code></pre>
    </div>
  </div>
  <figcaption>Soldaki "rastgele üç ürün" demek. Sağdaki "en pahalı üç ürün" demek. İkisi de çalışıyor, yalnızca biri bir soruyu cevaplıyor.</figcaption>
</figure>

İki eki var:

- `TOP 10 PERCENT` — satır sayısının onda biri.
- `TOP 3 WITH TIES` — üçüncüyle **eşit değerde** olanlar da geliyor.
  Sıralama değerinde beraberlik varsa sonuç üçten fazla satır olabiliyor.

## DISTINCT: tekrar edenleri elemek

```sql
SELECT DISTINCT category FROM products;
```

Sekiz üründen üç kategori geliyor: `Accessory`, `Computer`, `Display`.

**`DISTINCT` tek bir sütuna değil, seçilen satırın tamamına bakıyor.** Bu
en sık yanlış anlaşılan yer:

```sql
SELECT DISTINCT category, name FROM products;
```

Bu sorgu üç satır **döndürmüyor**. Her `name` farklı olduğu için
`(category, name)` çiftlerinin hepsi benzersiz — sekiz satırın sekizi de
geliyor. `DISTINCT` bir sütunu değil, satırı süzüyor.

Bir sütunun benzersiz değerlerini sayarken de işe yarıyor:

```sql
SELECT COUNT(DISTINCT category) FROM products;
```

Sayma işlemlerini bir sonraki bölümde göreceksin; burada aklında dursun.

## NULL nereye gidiyor?

Bir sütunda değer yoksa (`NULL`) SQL Server onu **en küçük** sayıyor: artan
sıralamada başa, azalanda sona geliyor. Bu davranış veritabanları arasında
değişiyor — PostgreSQL tersini yapıyor. Sıralamada `NULL` varsa nereye
düştüğünü kontrol et.

## Sıra

Anahtar kelimelerin yazılış sırası sabit:

```sql
SELECT   [DISTINCT] [TOP n] sütunlar
FROM     tablo
WHERE    koşul
ORDER BY sütun [ASC|DESC];
```

`ORDER BY` her zaman en sonda. `WHERE`'i `ORDER BY`'dan sonra yazmak
sözdizimi hatası veriyor.

## Özet

- `ORDER BY` yazmazsan sıra **belirsiz**; "zaten sıralı geliyordu" bir
  garanti değil.
- Varsayılan `ASC`; `DESC` yalnızca yazıldığı sütuna uygulanıyor.
- Birden çok sütunda sıra önemli: önce yazılan baskın.
- `ORDER BY` en son çalıştığı için **takma adı kullanabiliyor** —
  `WHERE`'in yapamadığı şey.
- Sütun numarasıyla sıralama (`ORDER BY 2`) kırılgan; adını yaz.
- `TOP`, `ORDER BY` olmadan anlamsız.
- `DISTINCT` bir sütuna değil, **seçilen satırın tamamına** bakıyor.
