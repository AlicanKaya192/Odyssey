Pencere fonksiyonlarının hatalarının çoğu hata mesajı vermiyor: sorgu
çalışıyor, sonuç makul görünüyor ve yanlış. Bu not, bu bölümde ölçülen
tuzakları ve her birinin çaresini topluyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Eşitlikte ROW_NUMBER</span><span class="anat-body">Sıra sütununa ayırt edici bir sütun ekle.</span></div>
    <div class="anat-row"><span class="anat-label">Varsayılan çerçeve</span><span class="anat-body">Birikimli toplamda <code>ROWS UNBOUNDED PRECEDING</code> yaz.</span></div>
    <div class="anat-row"><span class="anat-label">LAST_VALUE</span><span class="anat-body">Çerçeveyi grubun sonuna kadar aç.</span></div>
    <div class="anat-row"><span class="anat-label">Sonradan süzmek</span><span class="anat-body">Numaralandırmadan önce, iç sorguda süz.</span></div>
    <div class="anat-row"><span class="anat-label">Tam sayı ortalama</span><span class="anat-body">Ortalamadan önce <code>DECIMAL</code>'e çevir.</span></div>
    <div class="anat-row"><span class="anat-label">Sonucun sırası</span><span class="anat-body">Sorgunun sonuna ayrıca <code>ORDER BY</code>.</span></div>
  </div>
</figure>

## 1. Eşitlikte ROW_NUMBER

Stoğu 99 olan iki ürün var. Aynı `ROW_NUMBER() OVER (ORDER BY stock
DESC)` iki ayrı sorguda çalıştırıldı:

| Sorgu | 1 numara | 2 numara |
|---|---|---|
| sonunda `ORDER BY stock DESC, name` olan | Antivirus | Office Suite |
| sonunda `ORDER BY` olmayan | Office Suite | Antivirus |

Veri aynı, pencere aynı, sonuç farklı. Sunucu eşitler arasında bir sıra
seçmek zorunda ve bu seçim sorgunun geri kalanına bağlı.

"Her kategoriden bir ürün" gibi işlerde bu, sorgunun her çalıştığında
başka bir ürünü getirebileceği anlamına geliyor.

**Çare:** sırayı eşitsiz yap — `ORDER BY stock DESC, name` ya da
`ORDER BY stock DESC, id`. `RANK` ve `DENSE_RANK` bu tuzağa düşmüyor,
çünkü eşitlere zaten aynı numarayı veriyorlar.

## 2. Varsayılan çerçeve

`OVER (ORDER BY ...)` yazıp çerçeve yazmamak "baştan **bu değere** kadar"
demek. Sipariş kalemlerinde `ORDER BY order_id`:

| order_id | line | varsayılan | `ROWS UNBOUNDED PRECEDING` |
|---|---|---|---|
| 1001 | 900.00 | **1815.00** | 900.00 |
| 1001 | 440.00 | **1815.00** | 1340.00 |
| 1001 | 475.00 | 1815.00 | 1815.00 |

Aynı `order_id`'deki üç satır "aynı değer" sayılıp birlikte girdi. Tarih
sırasında da aynı şey olur: aynı gün iki sipariş varsa ikisi de günün
toplamını gösterir.

**Çare:** birikimli toplamda çerçeveyi açıkça yaz ve eşitleri ayır:
`ORDER BY order_id, product_id ROWS UNBOUNDED PRECEDING` — ölçüldü, 900,
1340, 1815.

## 3. LAST_VALUE

ACC ürünleri fiyata göre sıralı; `LAST_VALUE(name) OVER (ORDER BY price)`
her satırda satırın **kendi adını** verdi. Varsayılan çerçeve o satırda
bittiği için çerçevenin sonu satırın kendisi.

**Çare:** `LAST_VALUE(name) OVER (ORDER BY price ROWS BETWEEN UNBOUNDED
PRECEDING AND UNBOUNDED FOLLOWING)` → her satırda Microphone. Ya da
sırayı ters çevirip `FIRST_VALUE` kullan; o, çerçeve baştan başladığı
için bu tuzağa düşmüyor.

## 4. Sonradan süzmek

"Her müşterinin en büyük siparişi" sorgusu 1. müşteri için **1006**'yı
(`2400.00`) getirdi. 1006 iptal edilmiş bir sipariş.

| Süzme nerede | 1. müşteri için sonuç |
|---|---|
| hiç yok | 1006 — iptal edilmiş |
| dışarıda: `WHERE rk = 1 AND status <> 'cancelled'` | **hiç satır yok** — müşteri sonuçtan düştü |
| içeride, numaralandırmadan önce | 1003 (`2340.00`) — doğru |

Dışarıda süzmek daha da kötü: 1 numarayı iptal edilen sipariş aldığı ve
sonra elendiği için müşterinin hiç satırı kalmıyor.

**Çare:** hangi satırların yarışacağını numaralandırmadan **önce** seç;
`WHERE`'i iç sorguya yaz.

## 5. Tam sayı ortalama

`AVG(stock) OVER ()` ACC'de **19** verdi; doğrusu 19,33. Pencere, tam
sayıların ortalamasının tam sayı olması kuralını değiştirmiyor.

**Çare:** `AVG(CAST(stock AS DECIMAL(10,2))) OVER ()` → `19.333333`.

## 6. OVER'daki sıra sonucun sırası değil

`OVER (ORDER BY price DESC)` yalnızca numaranın neye göre verileceğini
söylüyor. Ölçümde sonuç o sırayla geldi, ama bu sunucunun o anki planı.

**Çare:** sonucun sırası önemliyse sorgunun sonuna `ORDER BY` yaz.

## 7. NULL da bir grup

Çalışan başına sipariş sayısı sıralanınca çalışanı olmayan iki sipariş
(`employee_id` `NULL`) de bir grup oldu ve **3.** sırayı aldı.

**Çare:** sıralamaya yalnızca gerçek grupların girmesi gerekiyorsa
`WHERE employee_id IS NOT NULL`.

## Kontrol sorusu

Bir pencere sorgusu yazınca iki şey sor:

- **"Sıra sütununda eşitlik olabilir mi?"** Olabiliyorsa ayırt edici bir
  sütun ekle ve birikimli hesapta `ROWS` yaz.
- **"Hangi satırlar yarışmalı?"** Süzmeyi numaralandırmadan önce yap.
