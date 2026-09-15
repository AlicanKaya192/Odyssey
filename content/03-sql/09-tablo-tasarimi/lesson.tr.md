# Tablo Tasarımı

Sekiz bölümdür hazır tablolarla çalıştın. Bu bölümde tabloyu **kendin
kuruyorsun**.

Bir tablo yalnızca verinin durduğu yer değil; verinin uyması gereken
**kuralların** da yazıldığı yer. Kural tabloya yazılınca her `INSERT`, her
`UPDATE` ona uymak zorunda kalıyor — kimse unutamıyor, kimse atlayamıyor.

## CREATE TABLE

```sql
CREATE TABLE warehouses (
    code NVARCHAR(10) PRIMARY KEY,
    city NVARCHAR(30) NOT NULL,
    capacity INT NOT NULL
);
```

Her sütun üç şey söylüyor: **adı**, **tipi** ve **kuralları**. Sütunlar
virgülle ayrılıyor.

Aynı adda bir tablo zaten varsa sunucu durduruyor:
`There is already an object named 'products' in the database.`

## Veri tipleri

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">INT</span><span class="anat-body">Tam sayı: kimlik, adet, stok.</span></div>
    <div class="anat-row"><span class="anat-label">DECIMAL(10,2)</span><span class="anat-body">Ondalıklı, <b>kesin</b> sayı: toplam 10 basamak, virgülden sonra 2. Para için bu.</span></div>
    <div class="anat-row"><span class="anat-label">NVARCHAR(n)</span><span class="anat-body">En fazla <code>n</code> karakterlik metin, her dilde.</span></div>
    <div class="anat-row"><span class="anat-label">DATE</span><span class="anat-body">Tarih, saatsiz: <code>'2026-09-15'</code>.</span></div>
  </div>
</figure>

Tip bir kural gibi davranıyor; uymayan değeri ya düzeltiyor ya reddediyor.
Üçü de ölçüldü:

| Değer | Sütun | Sonuç |
|---|---|---|
| `12.345` | `DECIMAL(10,2)` | `12.35` olarak yazıldı — **yuvarlandı** |
| `1234.5` | `DECIMAL(5,2)` | Hata: `Arithmetic overflow error` |
| `'ABCDEFG'` | `NVARCHAR(5)` | Hata: `String or binary data would be truncated ... Truncated value: 'ABCDE'` |

Dikkat edilecek olan ilki: yuvarlama **sessiz**. Kuruşların önemli olduğu
bir yerde virgülden sonraki basamak sayısını baştan doğru seçmek gerekiyor.

### NVARCHAR mı VARCHAR mı

İkisi de metin tutuyor. Fark şurada: `VARCHAR` karakterleri sunucunun **dil
ayarına** göre saklıyor, `NVARCHAR` her dilin her harfini.

Ölçüldü — Latin dil ayarlı bir `VARCHAR` sütuna `Şişli ğ ı` yazılınca
tabloya **`Sisli g i`** girdi. Hata yok, uyarı yok; harfler sessizce
değişti. Aynı değer `NVARCHAR` sütunda olduğu gibi kaldı.

Bu makinedeki sunucu Türkçe ayarlı olduğu için orada `VARCHAR` da Türkçe
harfleri tutuyor. Ama yazdığın tablo başka bir sunucuya taşındığı gün
bozulur. **Metin için `NVARCHAR` seç.**

Metni yazarken başına `N` koymak da aynı sebepten:

```sql
INSERT INTO t (name) VALUES (N'Şişli');   -- guvenli
INSERT INTO t (name) VALUES ('Şişli');    -- sunucunun diline bagli
```

`N` olmadan yazılan `'日本'` bir `NVARCHAR` sütuna `??` olarak girdi
(ölçüldü): metin sütuna ulaşmadan sunucunun diline çevriliyor.

## Kurallar

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NOT NULL</span><span class="anat-body">Boş kalamaz.</span></div>
    <div class="anat-row"><span class="anat-label">PRIMARY KEY</span><span class="anat-body">Her satırı tek başına tanımlar: boş olamaz, tekrarlanamaz. Tabloda bir tane.</span></div>
    <div class="anat-row"><span class="anat-label">UNIQUE</span><span class="anat-body">Tekrarlanamaz — e-posta, ürün kodu.</span></div>
    <div class="anat-row"><span class="anat-label">CHECK (...)</span><span class="anat-body">Koşulu sağlamayan değer girmez: <code>CHECK (price &gt; 0)</code>.</span></div>
    <div class="anat-row"><span class="anat-label">DEFAULT ...</span><span class="anat-body">Değer verilmezse bu yazılır.</span></div>
    <div class="anat-row"><span class="anat-label">REFERENCES</span><span class="anat-body">Başka bir tablodaki bir satırı göstermek zorunda (yabancı anahtar).</span></div>
  </div>
</figure>

```sql
CREATE TABLE parts (
    id INT PRIMARY KEY,
    sku NVARCHAR(20) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    status NVARCHAR(20) NOT NULL DEFAULT 'active'
);
```

Kurala uymayan her yazma komutu reddediliyor. Hata metinleri ölçüldü:

| Kural | Mesaj |
|---|---|
| `NOT NULL` | `Cannot insert the value NULL into column 'city' ...` |
| `UNIQUE` | `Violation of UNIQUE KEY constraint ... The duplicate key value is (a@x.com).` |
| `CHECK` | `The INSERT statement conflicted with the CHECK constraint ... column 'price'.` |

### Üç ince nokta

Üçü de ölçüldü ve üçü de insanı şaşırtıyor:

- **`CHECK` boş değeri geçiriyor.** `CHECK (price > 0)` olan ama boş
  kalabilen bir sütuna `NULL` yazılınca kabul edildi: `NULL > 0`
  "bilinmiyor", ve `CHECK` yalnızca kesin "yanlış"ı reddediyor. Boş
  olmasın istiyorsan ayrıca `NOT NULL`.
- **SQL Server'da `UNIQUE` sütun yalnızca bir tane `NULL` alıyor.** İkinci
  boş telefon numarası `Violation of UNIQUE KEY constraint ... (<NULL>)`
  hatası verdi. Başka veritabanlarında bu serbest; SQL Server'ın kendine
  özgü davranışı.
- **`DEFAULT` yalnızca sütun hiç yazılmazsa devreye giriyor.** Açıkça
  `NULL` yazılınca (ve sütun boş kalabiliyorsa) tabloya `NULL` girdi,
  varsayılan değer değil.

### Kurallara ad vermek

Ad vermezsen sunucu kendisi uyduruyor ve hata metnine o giriyor:
`CK__items__price__6B24EA82`. Ad verirsen hata ne olduğunu söylüyor:

```sql
price DECIMAL(10,2) NOT NULL
    CONSTRAINT ck_items_price CHECK (price > 0)
```

Hata artık `... the CHECK constraint "ck_items_price"` diyor (ölçüldü).

## IDENTITY: kendiliğinden artan numara

```sql
CREATE TABLE tickets (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(60) NOT NULL
);

INSERT INTO tickets (title) VALUES ('a'), ('b'), ('c');
```

`IDENTITY(1,1)`: 1'den başla, birer artır. Numaraları sunucu veriyor:
1, 2, 3 (ölçüldü). `INSERT` içinde `id` yazılmıyor — yazılırsa hata:
`Cannot insert explicit value for identity column ... when IDENTITY_INSERT
is set to OFF.`

**Silinen numara geri gelmiyor.** 2'yi silip yeni bir satır ekleyince yeni
satır 3 oldu, tabloda 1 ve 3 kaldı (ölçüldü). Bu bir hata değil:
numaranın tek görevi satırı tanımlamak, sıra saymak değil.

## FOREIGN KEY: bağı tanımlamak

Önceki bölümde bir sipariş silinip kalemleri kalınca **öksüz satırlar**
oluşuyordu ve sunucu hiçbir şey demiyordu — çünkü bağ tanımlı değildi.
Bağı tanımlayınca sunucu onu korumaya başlıyor:

```sql
CREATE TABLE teams (
    id INT PRIMARY KEY,
    name NVARCHAR(30) NOT NULL
);

CREATE TABLE members (
    id INT PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(id)
);
```

Ölçüldü:

| Deneme | Sonuç |
|---|---|
| Olmayan bir takıma üye eklemek | `The INSERT statement conflicted with the FOREIGN KEY constraint ...` |
| Üyesi olan takımı silmek | `The DELETE statement conflicted with the REFERENCE constraint ...` |
| `team_id` boş olan üye (sütun boş kalabiliyorsa) | kabul edildi |

### Ebeveyn silinince çocuklar ne olsun

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Varsayılan: reddet</h4>
      Çocuğu olan ebeveyn silinemez. Önce çocukları sen silersin, sonra ebeveyni. Yanlışlıkla veri kaybetmek imkânsız.
    </div>
    <div>
      <h4>ON DELETE CASCADE</h4>
      Ebeveyn silinince çocukları da kendiliğinden gider. Rahat, ama tek bir <code>DELETE</code> beklediğinden çok satır götürebilir.
    </div>
  </div>
</figure>

```sql
team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE
```

Üç üyeli bir tabloda 1 numaralı takımı silince o takımın iki üyesi de
gitti, diğer takımın üyesi kaldı (ölçüldü).

`CASCADE` bir üyelik ya da bir siparişin notları gibi **ebeveynsiz anlamı
olmayan** satırlar için doğru. Bir müşterinin siparişleri gibi kendi başına
değerli kayıtlarda varsayılan "reddet" daha güvenli.

### Önceki bölümün sözü

Sipariş veritabanında bağlar tanımlı değildi. Tanımlayınca:

```sql
ALTER TABLE order_items
ADD CONSTRAINT fk_items_order
    FOREIGN KEY (order_id) REFERENCES orders(id);

DELETE FROM orders WHERE id = 1006;
```

`The DELETE statement conflicted with the REFERENCE constraint
"fk_items_order"` — sunucu siparişi silmeyi **reddetti** (ölçüldü). Önce
kalemleri, sonra siparişi silince iş tamam: dokuz sipariş kaldı.

Bir uyarı: tabloda **zaten** öksüz satır varsa bağ eklenemiyor. Siparişi
önce silip sonra bağı eklemeye çalışınca `The ALTER TABLE statement
conflicted with the FOREIGN KEY constraint` hatası geldi. Önce öksüzleri
temizlemek gerekiyor.

## ALTER TABLE: var olan tabloyu değiştirmek

```sql
-- sutun eklemek
ALTER TABLE customers ADD phone NVARCHAR(20) NULL;

-- sutun silmek
ALTER TABLE customers DROP COLUMN phone;

-- kural eklemek
ALTER TABLE products ADD CONSTRAINT ck_price CHECK (price > 0);
```

Dolu bir tabloda üç durum ölçüldü:

- **Boş kalabilen sütun** eklenince eski satırlarda değeri `NULL`.
- **`NOT NULL` sütun** varsayılan değer olmadan eklenemiyor: eski satırlara
  ne yazılacağı belli değil. `DEFAULT 'standard'` ile eklenince eski altı
  müşterinin hepsine `standard` yazıldı.
- **Mevcut veriye uymayan kural** eklenemiyor. `CHECK (stock > 0)`
  reddedildi, çünkü stoğu sıfır olan iki ürün var.

Yani sunucu, eklediğin kuralın **bugünkü veriye** de uymasını istiyor.

### Yeni sütun ve GO

```sql
ALTER TABLE customers ADD phone NVARCHAR(20) NULL;
UPDATE customers SET phone = '555' WHERE id = 1;
```

Bu `Invalid column name 'phone'` hatası veriyor (ölçüldü). Sunucu komutları
çalıştırmadan önce hepsini birlikte okuyor ve o anda `phone` diye bir sütun
yok.

Çözüm araya `GO` koymak: komutları iki ayrı parçaya bölüyor.

```sql
ALTER TABLE customers ADD phone NVARCHAR(20) NULL;
GO
UPDATE customers SET phone = '555' WHERE id = 1;
```

Böyle çalıştı. Odyssey de SSMS gibi `GO`'yu tanıyor.

## DROP TABLE

```sql
DROP TABLE warehouses;
```

Tablo ve içindeki her şey gidiyor. Başka bir tablonun bağıyla gösterilen
bir tablo ise silinemiyor: `Could not drop object 'orders' because it is
referenced by a FOREIGN KEY constraint.` (ölçüldü). Bağlar burada da
koruyor.

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Metin</span><span class="anat-body"><code>NVARCHAR(n)</code> ve <code>N'...'</code></span></div>
    <div class="anat-row"><span class="anat-label">Para</span><span class="anat-body"><code>DECIMAL(10,2)</code> — yuvarlama sessiz</span></div>
    <div class="anat-row"><span class="anat-label">Kimlik</span><span class="anat-body"><code>INT IDENTITY(1,1) PRIMARY KEY</code></span></div>
    <div class="anat-row"><span class="anat-label">Kural</span><span class="anat-body"><code>NOT NULL</code>, <code>UNIQUE</code>, <code>CHECK</code>, <code>DEFAULT</code></span></div>
    <div class="anat-row"><span class="anat-label">Bağ</span><span class="anat-body"><code>REFERENCES</code> — gerekiyorsa <code>ON DELETE CASCADE</code></span></div>
    <div class="anat-row"><span class="anat-label">Değiştirmek</span><span class="anat-body"><code>ALTER TABLE</code>; yeni sütunu kullanmadan önce <code>GO</code></span></div>
  </div>
</figure>

Bir sonraki bölümde tarihlerle ve metinle çalışacaksın: gün farkı, ay
başı, metni parçalamak ve birleştirmek.
