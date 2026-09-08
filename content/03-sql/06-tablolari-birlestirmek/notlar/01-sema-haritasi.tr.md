Orta Seviye boyunca aynı sekiz tabloyla çalışacaksın. Bu not haritayı tek
sayfada tutuyor; sorgu yazarken buraya dönmen normal.

## Tablolar

| Tablo | Ne tutuyor | Satır |
|---|---|---|
| `categories` | ürün kategorileri | 4 |
| `suppliers` | tedarikçiler | 4 |
| `products` | ürünler | 12 |
| `customers` | müşteriler | 6 |
| `employees` | çalışanlar | 6 |
| `orders` | siparişler | 10 |
| `order_items` | sipariş kalemleri | 20 |
| `shipments` | kargo kayıtları | 6 |

## Sütunlar

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">categories</span><span class="anat-body"><code>code</code>, <code>name</code></span></div>
    <div class="anat-row"><span class="anat-label">suppliers</span><span class="anat-body"><code>code</code>, <code>name</code>, <code>city</code>, <code>country</code></span></div>
    <div class="anat-row"><span class="anat-label">products</span><span class="anat-body"><code>id</code>, <code>name</code>, <code>category_code</code>, <code>supplier_code</code>, <code>price</code>, <code>stock</code></span></div>
    <div class="anat-row"><span class="anat-label">customers</span><span class="anat-body"><code>id</code>, <code>name</code>, <code>city</code>, <code>country</code>, <code>joined</code></span></div>
    <div class="anat-row"><span class="anat-label">employees</span><span class="anat-body"><code>id</code>, <code>name</code>, <code>title</code>, <code>manager_id</code>, <code>hired</code></span></div>
    <div class="anat-row"><span class="anat-label">orders</span><span class="anat-body"><code>id</code>, <code>customer_id</code>, <code>employee_id</code>, <code>order_date</code>, <code>status</code></span></div>
    <div class="anat-row"><span class="anat-label">order_items</span><span class="anat-body"><code>order_id</code>, <code>product_id</code>, <code>quantity</code>, <code>unit_price</code></span></div>
    <div class="anat-row"><span class="anat-label">shipments</span><span class="anat-body"><code>order_id</code>, <code>shipped_date</code>, <code>carrier</code></span></div>
  </div>
</figure>

## Bağlantılar

Hangi sütunun hangi tabloyu işaret ettiği:

| Bu sütun | Bu tabloya bağlanıyor |
|---|---|
| `products.category_code` | `categories.code` |
| `products.supplier_code` | `suppliers.code` |
| `orders.customer_id` | `customers.id` |
| `orders.employee_id` | `employees.id` |
| `order_items.order_id` | `orders.id` |
| `order_items.product_id` | `products.id` |
| `shipments.order_id` | `orders.id` |
| `employees.manager_id` | `employees.id` (kendi kendine) |

`_id` ve `_code` ekleri tesadüf değil: bir sütun adı başka bir tablonun
anahtarına benziyorsa büyük ihtimalle oraya bağlanıyor. Yabancı bir
veritabanına bakarken ilk aranan şey bu.

## Boş kalabilen bağlantılar

Üç bağlantı `NULL` olabiliyor ve `LEFT JOIN` gerektiren yerler bunlar:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">products.supplier_code</span><span class="anat-body">Üç üründe boş — tedarikçi kayıtlı değil.</span></div>
    <div class="anat-row"><span class="anat-label">orders.employee_id</span><span class="anat-body">İki siparişte boş — internetten gelmiş, temsilcisi yok.</span></div>
    <div class="anat-row"><span class="anat-label">employees.manager_id</span><span class="anat-body">Bir kişide boş — en üstteki.</span></div>
  </div>
</figure>

Ayrıca **her siparişin kargo kaydı yok**: on siparişin altısı kargolanmış.
`orders` ile `shipments` arasında `LEFT JOIN` gerekiyor.

## Sık kullanılan birleştirmeler

```sql
-- urun + kategori adi
FROM products p JOIN categories c ON p.category_code = c.code

-- urun + tedarikci (tedarikcisiz urunler de kalsin)
FROM products p LEFT JOIN suppliers s ON p.supplier_code = s.code

-- siparis + musteri
FROM orders o JOIN customers c ON o.customer_id = c.id

-- siparisin kalemleri + urun adi
FROM orders o
JOIN order_items i ON o.id = i.order_id
JOIN products p ON i.product_id = p.id

-- siparis + kargo (kargolanmamislar da kalsin)
FROM orders o LEFT JOIN shipments s ON o.id = s.order_id

-- calisan + yoneticisi
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id
```

## Kalem tutarı

`order_items` tablosunda satır başına tutar **yazmıyor**; hesaplanıyor:

```sql
i.quantity * i.unit_price
```

`unit_price` ürünün o günkü fiyatı; `products.price` ise bugünkü fiyat.
İkisi farklı olabilir ve bu kasıtlı — fiyat değişince eski siparişlerin
tutarı değişmemeli.
