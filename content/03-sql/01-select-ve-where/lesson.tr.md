# Sorgu Yazmak: SELECT ve WHERE

Bir önceki bölümde `SELECT * FROM sehirler` yazdın ve tablonun tamamı
geldi. Gerçek işte istediğin bu değil: milyonlarca satırlık bir tablodan
**birkaç sütunu** ve **birkaç satırı** istiyorsun.

Bu bölüm o iki soruyu cevaplıyor: hangi sütunlar, hangi satırlar.

## Sorgunun anatomisi

Her `SELECT` sorgusu aynı üç parçadan kuruluyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT</span><span class="anat-body"><b>Hangi sütunlar?</b> Virgülle ayrılmış sütun adları, ya da hepsi için <code>*</code>.</span></div>
    <div class="anat-row"><span class="anat-label">FROM</span><span class="anat-body"><b>Hangi tablo?</b> Verinin nereden geleceği.</span></div>
    <div class="anat-row"><span class="anat-label">WHERE</span><span class="anat-body"><b>Hangi satırlar?</b> İsteğe bağlı. Yazılmazsa bütün satırlar geliyor.</span></div>
  </div>
  <figcaption>Sıra sabit: SELECT, sonra FROM, sonra WHERE. Yer değiştiremezler.</figcaption>
</figure>

Bu bölümde `urunler` diye bir tabloyla çalışacaksın:

| id | ad | kategori | fiyat | stok |
|---|---|---|---|---|
| 1 | Klavye | Aksesuar | 450.00 | 32 |
| 2 | Monitor | Ekran | 3200.00 | 8 |
| 3 | Fare | Aksesuar | 220.00 | 0 |

## Sütun seçmek

Yıldız her şeyi getiriyor:

```sql
SELECT * FROM urunler;
```

İstediğin sütunları yazarsan yalnızca onlar geliyor:

```sql
SELECT ad, fiyat FROM urunler;
```

**Sıra senin yazdığın sıra.** Tabloda `fiyat` sütunu `ad`'dan sonra
duruyor ama sen tersini istersen tersini yazarsın:

```sql
SELECT fiyat, ad FROM urunler;
```

### Yıldızı neden az kullanıyoruz?

Denerken pratik, ama gerçek işte üç sorunu var:

- **Gereksiz veri taşıyor.** Kırk sütunlu bir tablodan ikisi lazımken
  kırkını da okumak, hem sunucuyu hem ağı boşuna yoruyor.
- **Tablo değişince sorgun da değişiyor.** Birisi tabloya sütun eklerse
  senin sorgun bir gün fazladan sütun döndürmeye başlıyor.
- **Ne istediğin okunmuyor.** `SELECT *` yazan bir sorguya bakan biri,
  senin aslında neye ihtiyacın olduğunu göremiyor.

Kural şu: **denerken `*`, yazdığın sorguda sütun adları.**

## Sütuna başka bir ad vermek: AS

Sonuçtaki sütun başlığını değiştirebiliyorsun:

```sql
SELECT ad AS urun_adi, fiyat AS tutar FROM urunler;
```

Sonuç aynı veri, farklı başlıklar. Bu bir raporda ya da bir programın
okuyacağı sonuçta önem kazanıyor.

`AS` yazmasan da oluyor (`ad urun_adi`) ama **yazmak gerekiyor**: `AS`
olmadan yazılmış bir sorguda unutulan tek bir virgül, iki sütunu sessizce
tek sütuna çeviriyor.

## Satır seçmek: WHERE

`WHERE` bir **koşul** alıyor ve yalnızca koşulu sağlayan satırlar geliyor:

```sql
SELECT ad, fiyat FROM urunler WHERE kategori = 'Aksesuar';
```

Koşulda kullanabileceğin karşılaştırmalar:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">=</span><span class="anat-body">eşit. <b>Tek eşittir</b> — SQL'de <code>==</code> yok.</span></div>
    <div class="anat-row"><span class="anat-label">&lt;&gt;</span><span class="anat-body">eşit değil. <code>!=</code> de çalışıyor ama standart olan <code>&lt;&gt;</code>.</span></div>
    <div class="anat-row"><span class="anat-label">&lt; &gt;</span><span class="anat-body">küçük, büyük</span></div>
    <div class="anat-row"><span class="anat-label">&lt;= &gt;=</span><span class="anat-body">küçük eşit, büyük eşit</span></div>
  </div>
</figure>

## Metin yazarken tek tırnak

SQL'de metin **tek tırnak** içinde yazılıyor:

<figure class="fig">
  <div class="versus">
    <div class="ok">
      <h4>Doğru</h4>
      <pre><code>WHERE kategori = 'Ekran'</code></pre>
    </div>
    <div class="no">
      <h4>Hata verir</h4>
      <pre><code>WHERE kategori = "Ekran"</code></pre>
    </div>
  </div>
  <figcaption>Çift tırnak SQL Server'da metin değil, <b>nesne adı</b> demek. "Ekran" yazdığında sunucu Ekran adında bir sütun arıyor ve bulamıyor.</figcaption>
</figure>

Sayılarda tırnak yok: `WHERE fiyat > 1000`.

Metnin içinde tek tırnak geçiyorsa iki kez yazılıyor:
`WHERE ad = 'Kadin''s'`. Nadiren gerekiyor ama gerektiğinde bilinmezse
saatler yakıyor.

### Büyük-küçük harf

Varsayılan kurulumda SQL Server **harf büyüklüğünü ayırt etmiyor**:
`'aksesuar'` ile `'Aksesuar'` aynı sayılıyor. Bu sunucunun harmanlama
(collation) ayarına bağlı ve değiştirilebiliyor — yani her sunucuda böyle
olduğunu varsayma.

## Birden çok koşul: AND, OR, NOT

```sql
SELECT ad FROM urunler
WHERE kategori = 'Aksesuar' AND fiyat < 300;
```

`AND` ikisini birden, `OR` en az birini istiyor. `NOT` koşulu tersine
çeviriyor.

**`AND`, `OR`'dan önce çalışıyor.** Bu, çarpmanın toplamadan önce
gelmesine benziyor ve aynı şekilde tuzak:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Beklenen bu değil</h4>
      <pre><code>WHERE kategori = 'Ekran'
   OR kategori = 'Aksesuar'
  AND fiyat &lt; 300</code></pre>
    </div>
    <div class="ok">
      <h4>Niyetin buysa</h4>
      <pre><code>WHERE (kategori = 'Ekran'
    OR kategori = 'Aksesuar')
  AND fiyat &lt; 300</code></pre>
    </div>
  </div>
  <figcaption>Soldaki sorgu "bütün ekranlar, artı 300'den ucuz aksesuarlar" diyor. Parantez olmadan AND yalnızca kendi yanındaki iki koşulu bağlıyor.</figcaption>
</figure>

Kural basit: **ikisini bir arada kullanıyorsan parantez koy.** Doğru
çalışsa bile okuyan kişi ne demek istediğini görüyor.

## Sunucu senin yazdığın sırayla çalışmıyor

Sorguyu `SELECT ... FROM ... WHERE ...` diye yazıyorsun ama sunucu şu
sırayla işliyor:

<figure class="fig">
  <div class="flow">
    <span class="node">FROM<br>tabloyu al</span>
    <span class="arrow">-&gt;</span>
    <span class="node">WHERE<br>satırları ele</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">SELECT<br>sütunları seç</span>
  </div>
</figure>

Bu ayrıntı gibi duruyor ama somut bir sonucu var: **`SELECT`'te verdiğin
takma adı `WHERE`'de kullanamıyorsun.**

```sql
SELECT fiyat AS tutar FROM urunler WHERE tutar > 1000;
```

Bu sorgu "tutar diye bir sütun yok" diyor. `WHERE` çalıştığında `SELECT`
henüz çalışmamış, yani `tutar` diye bir şey ortada yok. Doğrusu:

```sql
SELECT fiyat AS tutar FROM urunler WHERE fiyat > 1000;
```

## Noktalı virgül

Sorgunun sonundaki `;` SQL Server'da zorunlu değil, ama **yazmak
alışkanlık edinilmeli**: birden fazla sorgu yazdığında ayıran şey o, ve
bazı komutlar (ileride göreceğin `WITH` gibi) kendinden önceki sorgunun
noktalı virgülle bitmesini istiyor.

## Özet

- `SELECT` sütunları, `FROM` tabloyu, `WHERE` satırları seçiyor.
- Denerken `*`, yazdığın sorguda sütun adları.
- `AS` sonuçtaki başlığı değiştiriyor; yazmayı ihmal etme.
- Metin **tek tırnak** içinde; çift tırnak nesne adı demek.
- Eşitlik tek `=` ile; `==` diye bir şey yok.
- `AND`, `OR`'dan önce çalışıyor — ikisi bir aradaysa parantez koy.
- Sunucu `FROM → WHERE → SELECT` sırasıyla çalışıyor; bu yüzden takma ad
  `WHERE`'de kullanılamıyor.
