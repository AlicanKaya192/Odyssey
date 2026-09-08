# Alt Sorgular

Bir sorgunun cevabını başka bir sorguda kullanmak istiyorsun:
"ortalamadan pahalı ürünler", "hiç satılmamış ürünler", "en çok sipariş
veren müşteri".

Bunların hepsi iki adım: önce bir şeyi hesapla, sonra ona göre süz. **Alt
sorgu** o iki adımı tek sorguda birleştiriyor.

## En basit hâli: tek bir değer

```sql
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

Parantez içindeki sorgu **tek bir sayı** üretiyor ve dış sorgu onu sabit
bir değer gibi kullanıyor. Sonuç üç satır.

Buna **skaler alt sorgu** deniyor: tek satır, tek sütun.

İki adımda yazmayı da denerdin — önce ortalamayı öğren, sonra elle yaz —
ama o zaman veri değiştiğinde sorgu yanlış olurdu. Alt sorgu her
çalıştırmada yeniden hesaplıyor.

### SELECT içinde de kullanılıyor

```sql
SELECT c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
FROM customers c;
```

İçerideki sorgu **dış sorgunun her satırı için** yeniden çalışıyor:
`c.id` her seferinde başka bir müşteri.

Buna **ilişkili alt sorgu** deniyor — dışarıdaki satıra bağlı olduğu için
tek başına çalıştırılamıyor.

Aynı sonucu `LEFT JOIN` + `GROUP BY` ile de alıyorsun. Hangisini
seçeceğine birazdan bakacağız.

## Listeden seçmek: IN

Üçüncü bölümde `IN` yazarken listeyi elle yazmıştın. Liste bir sorgudan da
gelebiliyor:

```sql
SELECT name
FROM products
WHERE supplier_code IN (SELECT code FROM suppliers WHERE country = 'Turkey');
```

İçerideki sorgu birden çok satır döndürebiliyor; `IN` de zaten bir liste
bekliyor.

## Tuzak: NOT IN ve boş değerler

Üçüncü bölümde bu tuzağı görmüştün ama listeyi sen yazıyordun ve içine
`NULL` koymuyordun. **Liste bir sorgudan geldiğinde iş değişiyor.**

"Hiç ürünü olmayan tedarikçiler" sorusu:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Boş sonuç veriyor</h4>
      <pre><code>SELECT name FROM suppliers
WHERE code NOT IN (
  SELECT supplier_code
  FROM products);</code></pre>
    </div>
    <div class="ok">
      <h4>Doğru cevabı veriyor</h4>
      <pre><code>SELECT name FROM suppliers s
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE p.supplier_code = s.code);</code></pre>
    </div>
  </div>
  <figcaption>Soldaki sıfır satır, sağdaki bir satır (Rhine Components) döndürüyor. Sebep: üç üründe supplier_code boş olduğu için alt sorgunun listesinde NULL var ve NOT IN o durumda hiçbir zaman doğru olamıyor.</figcaption>
</figure>

Hata yok, uyarı yok — sorgu çalışıyor ve "hiç ürünü olmayan tedarikçi
yok" diyor. Oysa var.

İki çözüm var:

```sql
-- 1. listeyi temizle
WHERE code NOT IN (
  SELECT supplier_code FROM products WHERE supplier_code IS NOT NULL)

-- 2. NOT EXISTS kullan
WHERE NOT EXISTS (
  SELECT 1 FROM products p WHERE p.supplier_code = s.code)
```

İkincisi tercih ediliyor: `NOT EXISTS` boş değerlerden etkilenmiyor ve
niyeti daha açık anlatıyor.

## EXISTS: var mı yok mu

`EXISTS` bir soruya cevap veriyor: "içerideki sorgu **en az bir** satır
döndürüyor mu?"

```sql
SELECT name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

Sipariş vermiş müşteriler — beş satır.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT 1</span><span class="anat-body">Ne seçildiğinin <b>önemi yok</b>. <code>EXISTS</code> satırın var olup olmadığına bakıyor, içeriğine değil. Gelenek <code>1</code> yazmak.</span></div>
    <div class="anat-row"><span class="anat-label">İlişkili</span><span class="anat-body">İçerideki sorgu <code>c.id</code> kullanıyor; dış sorgunun her satırı için yeniden çalışıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Erken çıkıyor</span><span class="anat-body">Bir satır bulur bulmaz duruyor; hepsini saymıyor.</span></div>
  </div>
</figure>

`NOT EXISTS` tersi: "hiç satır yok mu?" Eşleşmeyenleri bulmanın en güvenli
yolu bu.

## Alt sorgu bir tablo gibi: türetilmiş tablo

Alt sorgu `FROM` içinde de durabiliyor. O zaman geçici bir tablo gibi
davranıyor:

```sql
SELECT t.category_code, t.n
FROM (
    SELECT category_code, COUNT(*) AS n
    FROM products
    GROUP BY category_code
) t
WHERE t.n > 2;
```

**Takma ad zorunlu.** `t` yazmazsan sözdizimi hatası alıyorsun; sunucu bu
geçici tabloya bir ad verilmesini istiyor.

Bu kalıp "gruplama sonucunu tekrar süzmek" için kullanılıyor. Basit
durumlarda `HAVING` daha kısa; ama gruplama sonucunu **başka bir tabloyla
birleştirmek** gerektiğinde türetilmiş tablo tek yol oluyor.

## İlişkili mi, değil mi?

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>İlişkisiz</h4>
      <pre><code>WHERE price > (
  SELECT AVG(price)
  FROM products)</code></pre>
      <p>Bir kez çalışıyor, sonucu herkes için aynı.</p>
    </div>
    <div class="ok">
      <h4>İlişkili</h4>
      <pre><code>WHERE p.price > (
  SELECT AVG(p2.price)
  FROM products p2
  WHERE p2.category_code =
        p.category_code)</code></pre>
      <p>Her satır için yeniden çalışıyor; dış satıra bağlı.</p>
    </div>
  </div>
  <figcaption>Soldaki "ortalamadan pahalı ürünler" (3 satır), sağdaki "kendi kategorisinin ortalamasından pahalı ürünler" (6 satır). İkisi farklı soru.</figcaption>
</figure>

İlişkili alt sorguyu tek başına çalıştıramıyorsun: içinde dış sorgunun
takma adı geçiyor.

## Alt sorgu mu, JOIN mi?

Çoğu soru ikisiyle de çözülüyor. Seçim okunabilirlikle ilgili:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Sütun ekleyeceksen</span><span class="anat-body"><b>JOIN.</b> Başka tablodan sütun getirmek `JOIN`'in işi.</span></div>
    <div class="anat-row"><span class="anat-label">Yalnızca süzeceksen</span><span class="anat-body"><b>EXISTS</b> ya da <b>IN</b>. Sütun almadığın için birleştirmeye gerek yok ve satır çoğalması riski de yok.</span></div>
    <div class="anat-row"><span class="anat-label">Eşleşmeyeni arıyorsan</span><span class="anat-body"><b>NOT EXISTS.</b> <code>LEFT JOIN ... IS NULL</code> de çalışıyor ama <code>NOT EXISTS</code> niyeti daha açık söylüyor.</span></div>
    <div class="anat-row"><span class="anat-label">Tek bir sayı gerekiyorsa</span><span class="anat-body"><b>Skaler alt sorgu.</b> Ortalama, toplam, en büyük değer.</span></div>
  </div>
</figure>

**Hız açısından** aralarında genelde fark olmuyor: sunucu ikisini de aynı
plana çevirebiliyor. "Alt sorgu yavaştır" yaygın ama artık doğru olmayan
bir söz.

Tek gerçek fark satır çoğalması: `JOIN` satırları çoğaltabiliyor,
`EXISTS` çoğaltmıyor. Yalnızca süzmek istiyorsan `EXISTS` bu yüzden daha
güvenli.

## Alt sorgu nerelerde kullanılabiliyor?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">WHERE</span><span class="anat-body">En yaygın yer. <code>IN</code>, <code>EXISTS</code> ya da karşılaştırma.</span></div>
    <div class="anat-row"><span class="anat-label">SELECT</span><span class="anat-body">Hesaplanan bir sütun olarak. Tek değer döndürmek zorunda.</span></div>
    <div class="anat-row"><span class="anat-label">FROM</span><span class="anat-body">Türetilmiş tablo. Takma ad zorunlu.</span></div>
    <div class="anat-row"><span class="anat-label">HAVING</span><span class="anat-body">Grup koşulunda bir eşik olarak.</span></div>
  </div>
</figure>

`SELECT` içindeki alt sorgu **tek satır tek sütun** döndürmek zorunda.
Birden fazla satır dönerse sunucu hata veriyor:
`Subquery returned more than 1 value`.

## Özet

- Alt sorgu, bir sorgunun içindeki sorgu; parantez içinde yazılıyor.
- **Skaler** alt sorgu tek değer döndürüyor ve sabit gibi kullanılıyor.
- `IN (SELECT ...)` listeyi bir sorgudan alıyor.
- **`NOT IN` + alt sorgu tehlikeli:** listede tek bir `NULL` varsa sonuç
  her zaman boş. `NOT EXISTS` kullan.
- `EXISTS` "en az bir satır var mı" diye soruyor; içinde ne seçildiğinin
  önemi yok.
- `FROM` içindeki alt sorgu geçici bir tablo; **takma adı zorunlu.**
- **İlişkili** alt sorgu dış satıra bağlı ve her satır için yeniden
  çalışıyor.
- Sütun getirecekseniz `JOIN`, yalnızca süzecekseniz `EXISTS`.
