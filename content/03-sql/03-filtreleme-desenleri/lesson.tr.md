# Filtreleme Desenleri

`WHERE` ile tek tek karşılaştırma yapmayı biliyorsun. Bu bölüm dört yeni
araç veriyor: metin içinde **desen** aramak, bir **listeden** seçmek, bir
**aralık** vermek ve **değeri olmayan** satırları bulmak.

Sonuncusu — `NULL` — yalnızca bir araç değil, SQL'i başka dillerden ayıran
bir davranış. Bölümün yarısı ona ayrıldı.

Bu bölümde `products` tablosu biraz büyüdü: artık bir de `supplier_code`
sütunu var ve **bazı ürünlerde bu sütun boş.**

## LIKE: metin deseni

Tam eşitlik yerine "şununla başlayan", "şunu içeren" demek istiyorsun:

```sql
SELECT name FROM products WHERE name LIKE 'K%';
```

İki joker karakter var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">%</span><span class="anat-body"><b>Sıfır ya da daha fazla</b> karakter. <code>'M%'</code> M ile başlayan her şey (Monitor, Mouse, Microphone), <code>'%top'</code> top ile biten (Laptop, Desktop), <code>'%ead%'</code> içinde ead geçen (Headset).</span></div>
    <div class="anat-row"><span class="anat-label">_</span><span class="anat-body"><b>Tam bir</b> karakter. <code>'M_use'</code> beş harfli, M ile başlayıp use ile biten şeyler (Mouse).</span></div>
  </div>
</figure>

Harf büyüklüğü varsayılan kurulumda önemsiz: `'k%'` ile `'K%'` aynı
sonucu veriyor.

### Jokerin kendisini aramak

Metnin içinde gerçekten `%` işareti arıyorsan `ESCAPE` ile bir kaçış
karakteri tanımlıyorsun:

```sql
WHERE aciklama LIKE '%50!%%' ESCAPE '!'
```

Burada `!%` gerçek bir yüzde işareti demek; sondaki `%` hâlâ joker.
Nadiren gerekiyor ama gerektiğinde başka yolu yok.

### `LIKE 'x%'` ile `LIKE '%x'` aynı şey değil

Performans açısından bunlar çok farklı. `'K%'` — yani **başı belli** olan
bir desen — indeksten yararlanabiliyor. `'%K'` ya da `'%K%'` ise her satıra
tek tek bakmayı gerektiriyor. Küçük tablolarda fark edilmiyor, milyonluk
tablolarda saniyelerle ölçülüyor.

## IN: listeden biri

Uzun `OR` zincirleri yerine:

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>Uzun hâli</h4>
      <pre><code>WHERE category = 'Display'
   OR category = 'Accessory'
   OR category = 'Software'</code></pre>
    </div>
    <div class="ok">
      <h4>Kısa hâli</h4>
      <pre><code>WHERE category IN
  ('Display', 'Accessory', 'Software')</code></pre>
    </div>
  </div>
  <figcaption>İkisi tamamen aynı işi yapıyor. Sağdaki hem kısa hem parantez tuzağından uzak: OR zincirini AND ile birleştirirken parantez unutmak en sık yapılan hatalardan.</figcaption>
</figure>

Tersi de var: `NOT IN`. Ama **`NOT IN` ile `NULL` bir arada tehlikeli** —
biraz sonra.

## BETWEEN: aralık

```sql
SELECT name, price FROM products WHERE price BETWEEN 500 AND 3000;
```

**İki uç da dahil.** Yani bu sorgu `price >= 500 AND price <= 3000`
demek. Tam 500 ve tam 3000 olan satırlar geliyor.

Bu, en sık yanlış hatırlanan ayrıntı. "500 ile 3000 arası" derken 3000'i
dışarıda bırakmak istiyorsan `BETWEEN` doğru araç değil:

```sql
WHERE price >= 500 AND price < 3000
```

Sıra da önemli: `BETWEEN 3000 AND 500` **hiçbir satır döndürmüyor**, hata
da vermiyor. Küçük değer önce yazılıyor.

## NULL: değer yok

Şimdi bölümün asıl konusu.

`NULL` **boş dize değil, sıfır değil.** "Bu hücrede bir değer yok" demek —
daha doğrusu **"değeri bilinmiyor"**.

Aradaki fark somut: bir ürünün tedarikçisi `NULL` ise "tedarikçisi yok"
demiyoruz, "tedarikçisinin kim olduğu kayıtlı değil" diyoruz.

### `= NULL` hiçbir zaman doğru olmuyor

```sql
WHERE supplier_code = NULL      -- her zaman boş sonuç
```

Bu sorgu hata vermiyor, **hiçbir satır döndürmüyor.** Sebebi şu:
bilinmeyen bir değerle yapılan her karşılaştırmanın sonucu da bilinmiyor.

SQL'de mantık **üç değerli**: doğru, yanlış ve **bilinmiyor**. `WHERE`
yalnızca **doğru** olan satırları alıyor; "bilinmiyor" da "yanlış" gibi
eleniyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NULL = NULL</span><span class="anat-body">bilinmiyor — iki bilinmeyen değerin eşit olup olmadığı da bilinmiyor</span></div>
    <div class="anat-row"><span class="anat-label">NULL &lt;&gt; 5</span><span class="anat-body">bilinmiyor</span></div>
    <div class="anat-row"><span class="anat-label">NULL &gt; 100</span><span class="anat-body">bilinmiyor</span></div>
    <div class="anat-row"><span class="anat-label">NULL IS NULL</span><span class="anat-body"><b>doğru</b> — tek çalışan yol bu</span></div>
  </div>
</figure>

### Doğrusu: IS NULL

```sql
SELECT name FROM products WHERE supplier_code IS NULL;
SELECT name FROM products WHERE supplier_code IS NOT NULL;
```

`IS NULL` bir karşılaştırma değil, bir **durum sorusu**: "bu hücre boş
mu?" Cevabı her zaman doğru ya da yanlış oluyor.

### Sessiz tuzak: NOT IN ve NULL

Bu, SQL'de en çok can yakan davranışlardan biri.

```sql
WHERE supplier_code NOT IN ('T1', 'T2', NULL)
```

Bu sorgu **hiçbir satır döndürmüyor.** Hata da vermiyor.

Sebebi: `x NOT IN (a, b, c)` aslında
`x <> a AND x <> b AND x <> c` demek. Listede `NULL` varsa o
karşılaştırmalardan biri her zaman "bilinmiyor" oluyor ve `AND` zinciri
asla "doğru" olamıyor.

Listeyi sen yazdığında `NULL` koymazsın; ama liste **başka bir sorgudan**
geldiğinde (ileride göreceğin alt sorgular) içinde `NULL` olabiliyor ve
sorgu sessizce boş dönüyor.

Korunma yolu iki tane: listeyi üreten sorguya `WHERE ... IS NOT NULL`
eklemek, ya da `NOT IN` yerine `NOT EXISTS` kullanmak. İkincisi alt
sorgular bölümünün konusu.

### NULL ve sıralama

Geçen bölümde geçmişti: SQL Server `NULL`'u en küçük sayıyor. Artan
sıralamada başa, azalanda sona geliyor.

## Hepsini bir arada

```sql
SELECT name, price
FROM products
WHERE category IN ('Accessory', 'Display')
  AND price BETWEEN 200 AND 2000
  AND supplier_code IS NOT NULL
  AND name LIKE '%a%'
ORDER BY price DESC;
```

Dördü de `AND` ile bağlanıyor ve hepsi aynı `WHERE` içinde duruyor.

## Özet

- `LIKE` deseni arıyor: `%` çok karakter, `_` tek karakter.
- Desenin **başı belliyse** (`'K%'`) sorgu hızlı; `'%K%'` her satıra bakar.
- `IN` uzun `OR` zincirinin kısası; `BETWEEN` iki uç **dahil** bir aralık.
- `BETWEEN` sınırları dışarıda bırakmıyor; bırakmak istiyorsan `>=` ve `<`
  yaz.
- `NULL` "bilinmiyor" demek; boş dize ya da sıfır değil.
- `= NULL` **hiçbir zaman** doğru olmuyor. `IS NULL` / `IS NOT NULL` yaz.
- İçinde `NULL` olan bir listeyle `NOT IN` **her zaman boş** döner.
