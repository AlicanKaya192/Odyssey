# Dizinler

Şimdiye kadarki her sorgu anında döndü, çünkü tablolar on satırlıktı. Bu
bölümde şemaya dokuzuncu bir tablo ekleniyor: 20 000 satırlık `events` —
müşterilerin sitedeki hareketleri. Soru şu: sunucu aradığı satırı nasıl
buluyor, ve bazen neden bulamıyor?

```
events: id, customer_id, product_id, event_type, session_code, created_at, amount
```

Her 25 dakikada bir olay, 1 Ocak 2025'ten 14 Aralık 2025'e: günde 58
olay. Dört türün (`view`, `click`, `cart`, `purchase`) her biri 5 000
satır; `amount` yalnızca satın almalarda dolu.

## Nasıl ölçülüyor

Bu bölümdeki sayılar **okuma**: sunucunun bir sorgu için baktığı 8 KB'lık
sayfa sayısı. Süre makineden makineye değişiyor, okuma değişmiyor.
Sunucuya `SET STATISTICS IO ON` denince her sorgudan sonra şöyle bir
mesaj veriyor (ölçüldü):

```
Table 'events'. Scan count 1, logical reads 150, physical reads 0, ...
```

`events` tablosunun verisi 150 sayfa. Uygulamanın sonuç tablosu bu
mesajları göstermiyor; bu bölümün ölçümleri SQL Server'da ayrıca yapıldı.
SQL Server Management Studio kullanıyorsan aynı komutla kendin de
görebilirsin.

## Dizin ne

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Kümelenmiş dizin</span><span class="anat-body">Tablonun kendisi, birincil anahtara göre sıralı. <code>PRIMARY KEY</code> bunu kendiliğinden kuruyor — ölçüldü, dokuz tablonun dokuzunda.</span></div>
    <div class="anat-row"><span class="anat-label">Kümelenmemiş dizin</span><span class="anat-body">Ayrı, sıralı bir liste: seçilen sütunun değerleri ve her birinin satıra işareti. Kitabın sonundaki fihrist.</span></div>
    <div class="anat-row"><span class="anat-label">Seek (arama)</span><span class="anat-body">Sıralı listede doğrudan doğru yere gitmek.</span></div>
    <div class="anat-row"><span class="anat-label">Scan (tarama)</span><span class="anat-body">Baştan sona okumak — tablonun ya da dizinin.</span></div>
    <div class="anat-row"><span class="anat-label">Key Lookup</span><span class="anat-body">Dizinde olmayan bir sütun için tabloya geri dönmek. Satır başına bir kez.</span></div>
  </div>
</figure>

`id = 10000` gibi birincil anahtarla arama zaten hızlı: 2 okuma,
*Clustered Index Seek*. Tablo `id` sırasında durduğu için sunucu doğrudan
o sayfaya gidiyor.

## İlk dizin

Bir günün olayları:

```sql
SELECT id, created_at FROM events
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

Tablo `id` sırasında; `created_at`'e göre bir düzen yok. Sunucu 58 satır
için 150 sayfanın hepsine bakıyor. Dizin:

```sql
CREATE INDEX ix_events_created ON events (created_at);
```

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Dizinsiz</h4>
      <p><strong>150 okuma</strong></p>
      <p>Clustered Index Scan: tablonun bütün sayfaları.</p>
    </div>
    <div>
      <h4>created_at dizini</h4>
      <p><strong>2 okuma</strong></p>
      <p>Index Seek: sıralı listede 1 Haziran'ın başladığı yer.</p>
    </div>
  </div>
</figure>

Aynı 58 satır. Bedeli yer: `sp_spaceused` dizinlerin kapladığı alanı
16 KB'tan 352 KB'a çıkmış gösterdi.

## Sütuna işlev: dizin kör oluyor

Dizin `created_at` değerlerine göre sıralı — `YEAR(created_at)`'e göre
değil. Sütun bir işlevin içine girince sunucu sıralı listede doğrudan yere
gidemiyor; her değer için işlevi hesaplayıp bakmak zorunda. Ölçüldü, dizin
varken:

| `WHERE` | Okuma | Plan |
|---|---|---|
| `created_at >= '2025-06-01' AND created_at < '2025-06-02'` | 2 | Index Seek |
| `YEAR(created_at) = 2025 AND MONTH(created_at) = 6 AND DAY(created_at) = 1` | 42 | Index Scan |
| `DATEADD(day, 1, created_at) >= '2025-06-02' AND ... < '2025-06-03'` | 42 | Index Scan |
| `CAST(created_at AS DATE) = '2025-06-01'` | 2 | Index Seek |

42, dizinin tamamı: tablodan küçük olduğu için 150'den az, ama aramanın
2'sinden yirmi kat fazla. `CAST(... AS DATE)` bir istisna — sunucu bu
dönüşümü tanıyor ve yine arayabiliyor (ölçüldü). Bunu genelleme: kural
**sütunu çıplak bırakmak**, işlevi karşı tarafa yazmak.

Metinde de aynısı (`session_code` üzerinde bir dizinle):

| `WHERE` | Okuma | Plan |
|---|---|---|
| `session_code = 'S010000'` | 2 | Index Seek |
| `session_code LIKE 'S0050%'` | 3 | Index Seek |
| `session_code LIKE '%0050'` | 54 | Index Scan |
| `UPPER(session_code) = 'S010000'` | 54 | Index Scan |

Başı belli bir `LIKE` sıralı listede aranabiliyor; başı `%` olan
aranamıyor — fihriste "sonu *-ler* ile biten kelimeler" diye bakılamaz.

Onuncu bölümdeki yarı açık aralığın artık ikinci bir sebebi var.

## Dizin var ama kullanılmıyor

`created_at` dizini dururken:

| Sorgu (1 Haziran) | Satır | Okuma | Plan |
|---|---|---|---|
| `SELECT id, created_at` | 58 | 2 | Index Seek |
| `SELECT *` | 58 | **150** | Clustered Index Scan |
| `SELECT created_at, amount` | 58 | **150** | Clustered Index Scan |
| satın almalar: `SELECT id, created_at, amount ... AND event_type = N'purchase'` | 15 | 130 | Index Seek + Key Lookup |

Dizin yalnızca `created_at`'i (ve satırı bulmak için `id`'yi) tutuyor.
Başka bir sütun istenince her satır için tabloya geri dönmek gerekiyor.
58 satırda sunucu 58 geri dönüşü tarama kadar pahalı buldu ve **dizini
hiç kullanmadı**; 15 satırda dizini kullanıp her biri için geri döndü
(130 okuma). Kararı sunucu veriyor: dizinin var olması kullanılacağı
anlamına gelmiyor.

Seçiciliği düşük sütunlarda da aynısı. `event_type` dört değer alıyor;
`'purchase'` tablonun dörtte biri (5 000 satır). O sütuna dizin kurulunca
`SELECT id` 22 okumayla dizinden geldi, `SELECT *` yine tabloyu taradı
(150).

## Kapsayan dizin: INCLUDE

Sorgunun istediği her şey dizindeyse tabloya dönmek gerekmiyor:

```sql
CREATE INDEX ix_events_created ON events (created_at) INCLUDE (amount);
```

`SELECT created_at, amount` bir gün için: `created_at` dizini varken 150
(tarama), `INCLUDE (amount)` ile **3** (Index Seek). `INCLUDE`'daki sütun
sıralamaya girmiyor, yalnızca dizinin içinde duruyor. `(created_at,
amount)` diye iki sütunlu bir anahtar da aynı sorguda 3 okuma verdi;
fark, `amount`'un orada sıralamanın parçası olması.

## Bileşik dizin: sıra önemli

Telefon rehberi soyada, sonra ada göre sıralı. Soyadı bilinince doğru
sayfaya gidilir; yalnızca ad bilinince rehberin tamamı okunur. İki
sütunlu bir dizin de böyle. Ölçüldü:

| Sorgu | `(customer_id, created_at)` | `(created_at, customer_id)` |
|---|---|---|
| müşteri 3, bir gün | 2 — seek | 2 — seek |
| yalnız müşteri 3 (3 334 satır) | 11 — seek | 52 — tarama |
| yalnız bir gün | 52 — tarama | 2 — seek |

Dizin, **ilk sütunu** bilinen aramalarda doğrudan yere gidebiliyor. İki
sütun birlikte arandığında iki sıra da yetti; fark tek sütunla aramada
çıkıyor. Alışkanlık: eşitlikle aranan sütun (`customer_id = 3`) önde,
aralıkla aranan (`created_at >= ...`) arkada — böylece aynı müşterinin
satırları bir arada ve tarih sırasında duruyor.

## Süzgeçli dizin

`amount` 20 000 satırın 15 000'inde boş. Dizin yalnızca dolu olanları
tutabilir:

```sql
CREATE INDEX ix_events_amount ON events (amount) WHERE amount IS NOT NULL;
```

| | Ölçülen |
|---|---|
| `WHERE amount > 490` (120 satır) | 2 okuma, Index Seek |
| `WHERE amount IS NULL` | 150 okuma — o satırlar dizinde yok |
| dizinlerin kapladığı yer, süzgeçli | 128 KB |
| aynı dizin süzgeçsiz | 408 KB |

## Benzersiz dizin

`UNIQUE` bir dizin tekrarı kabul etmiyor — hem kurulurken hem sonra
(ölçüldü):

| Yazım | Sonuç |
|---|---|
| `CREATE UNIQUE INDEX ... ON customers (city)` | `The CREATE UNIQUE INDEX statement terminated because a duplicate key was found ... The duplicate key value is (Istanbul).` |
| `CREATE UNIQUE INDEX ... ON customers (name)` | kuruldu |
| aynı adla ikinci bir müşteri eklemek | `Cannot insert duplicate key row in object 'dbo.customers' with unique index 'ux_customers_name'. The duplicate key value is (Nova Retail).` |

Dokuzuncu bölümdeki `UNIQUE` kuralı da arka planda aynı şeyi kuruyor:
`ALTER TABLE customers ADD CONSTRAINT uq_customers_name UNIQUE (name)`
sonrasında `sys.indexes` benzersiz, kümelenmemiş bir dizin gösterdi. O
dizin `DROP INDEX` ile silinemiyor — kural onu kullanıyor (`An explicit
DROP INDEX is not allowed ...`); kuralın kendisi kaldırılıyor.

## Bedeli

Her dizin, satır eklenince, silinince ya da değişince **o da**
güncelleniyor. Tek bir satır eklemek (ölçüldü):

| Tabloda | Okuma |
|---|---|
| yalnızca birincil anahtar | 2 |
| birincil anahtar + beş dizin | 22 |

Bir de yer. Bu yüzden dizin "her sütuna" değil, **gerçekten sık çalışan
sorgulara** kuruluyor.

## Dizinleri görmek ve kaldırmak

```sql
SELECT name, type_desc
FROM sys.indexes
WHERE object_id = OBJECT_ID('events') AND type > 0;
```

`created_at` dizininden sonra iki satır geldi: birincil anahtarın
`CLUSTERED` dizini ve `ix_events_created` (`NONCLUSTERED`).

```sql
DROP INDEX ix_events_created ON events;
```

| Yazım | Hata |
|---|---|
| `DROP INDEX ix_events_created` (tablo yok) | `Must specify the table name and index name for the DROP INDEX statement.` |
| olmayan bir dizini silmek | `Cannot drop the index 'events.ix_yok', because it does not exist ...` |
| aynı adla ikinci dizin | `The operation failed because an index or statistics with name ... already exists on table ...` |

Bu uygulamada her çalıştırma sonunda geri alındığı için alıştırmalarda
kurduğun dizin bir sonraki çalıştırmada durmuyor (ölçüldü: işlem içinde
kurulan dizin geri almadan sonra `sys.indexes`'te yoktu).

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">CREATE INDEX</span><span class="anat-body">Seçilen sütunların sıralı bir kopyası; arama 150 okumadan 2'ye iniyor.</span></div>
    <div class="anat-row"><span class="anat-label">Sütunu çıplak bırak</span><span class="anat-body"><code>YEAR(sütun)</code>, <code>UPPER(sütun)</code>, <code>LIKE '%...'</code> dizini taramaya düşürüyor.</span></div>
    <div class="anat-row"><span class="anat-label">INCLUDE</span><span class="anat-body">Sorgunun istediği sütunları dizine ekle; tabloya dönüş kalmıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Sıra</span><span class="anat-body">Bileşik dizin ilk sütunuyla aranabiliyor; eşitlik önde, aralık arkada.</span></div>
    <div class="anat-row"><span class="anat-label">Süzgeç</span><span class="anat-body"><code>WHERE</code> ile yalnızca gerekli satırlar; daha küçük dizin.</span></div>
    <div class="anat-row"><span class="anat-label">Bedel</span><span class="anat-body">Her dizin yazmayı yavaşlatıyor ve yer kaplıyor.</span></div>
  </div>
</figure>

Sıradaki bölüm görünümler ve saklı yordamlar: sık yazılan bir sorguyu
veritabanının içinde bir ada bağlamak.
