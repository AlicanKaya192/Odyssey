Yanına `orders.json` dosyası konuldu: bir dükkânın siparişleri, her
siparişin içinde ürünlerin listesi. Yapısı:

- `data["shop"]`: dükkânın adı
- `data["orders"]`: siparişlerin listesi
- her siparişte `customer` (müşteri) ve `items` (ürünlerin listesi)
- her üründe `name`, `price` (fiyat) ve `qty` (adet)

**Yapman gerekenler:**

1. Dosyayı `json.load` ile `data` adında bir değişkene oku.
2. Önce dükkânın adını yazdır.
3. Her sipariş için ürünlerin `price * qty` toplamını hesapla; müşterinin
   adını ve tutarı yazdır, ve `totals` adında bir sözlüğe koy (anahtar
   müşteri, değer tutar).
4. En sonda bütün siparişlerin toplamını yazdır.

**Beklenen çıktı:**

```text
Book Corner
Ada 22
Alan 30
Grace 30
82
```

İki döngü iç içe: dıştaki siparişleri, içteki o siparişin ürünlerini
dolaşıyor.
