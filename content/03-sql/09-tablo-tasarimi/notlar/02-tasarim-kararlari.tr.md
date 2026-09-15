Sözdizimi kolay; asıl zor olan, bir tabloyu yıllarca dayanacak şekilde
kurmak. Bu not o kararları topluyor. Sayılar ve hata metinleri gerçek
sunucuda ölçüldü.

## Her bilgi tek yerde

Altıncı bölümde tedarikçinin adı ürün tablosunda değil kendi tablosunda
duruyordu. Sebep hâlâ geçerli: aynı bilgi iki yerde yazılırsa bir gün
ikisinden biri güncellenmeyi unutuluyor ve veri kendi içinde çelişiyor.

Sorulacak soru: **"Bu sütun, satırın kendisini mi anlatıyor, yoksa başka
bir şeyi mi?"** Ürünün fiyatı ürünü anlatıyor; tedarikçinin şehri
tedarikçiyi. Başka bir şeyi anlatan sütun kendi tablosuna gidiyor, geride
yalnızca onu gösteren bir anahtar kalıyor.

## Anahtarı seçmek

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Doğal anahtar</h4>
      Verinin kendisinden: ürün kodu, tedarikçi kodu. Okunaklı; ama gerçek dünyada değişebiliyor ve değiştiğinde onu gösteren her satırın da değişmesi gerekiyor.
    </div>
    <div>
      <h4>Yapay anahtar</h4>
      <code>IDENTITY</code> ile sunucunun verdiği sayı. Hiçbir anlamı yok, o yüzden hiç değişmesi gerekmiyor.
    </div>
  </div>
</figure>

Sık kullanılan ikisi birden: yapay anahtar birincil anahtar olur, doğal
kod `UNIQUE` olarak yanında durur.

```sql
CREATE TABLE parts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sku NVARCHAR(20) NOT NULL UNIQUE,
    ...
);
```

**Harf büyüklüğüne dikkat.** Bu sunucuda anahtar karşılaştırması büyük ve
küçük harfi ayırmıyor: `w1` ile `W1` aynı anahtar sayıldı ve ikincisi
reddedildi (ölçüldü). Kodları tek bir biçimde yazmak bu sürprizi
önlüyor.

## Para için DECIMAL, FLOAT değil

`FLOAT` sayıyı ikili sistemde **yaklaşık** tutuyor. Ölçüldü:

| Hesap | Sonuç | `= 0.3` mü? |
|---|---|---|
| `FLOAT`: `0.1 + 0.2` | `0.30000000000000004` | **hayır** |
| `DECIMAL(10,2)`: `0.1 + 0.2` | `0.3` | evet |

Tek bir kuruş farkı küçük görünüyor ama binlerce satırı toplayınca
büyüyor ve eşitlik karşılaştırmaları sessizce yanlış çıkıyor. Ölçüm,
bilimsel hesap gibi yaklaşık değerin yeterli olduğu yerde `FLOAT`;
parada, miktarda, kesin olması gereken her yerde `DECIMAL`.

## Tarihi tarih olarak sakla

Tarihi metin sütununda tutmak ilk bakışta zararsız. Ölçüldü — metin olarak
sıralanınca:

```
2026-10-01
2026-9-15
2026-9-2
```

Ekim, Eylül'den önce geldi: metin karakter karakter karşılaştırılıyor ve
`1` karakteri `9`'dan küçük. Aynı değerler `DATE` sütununda doğru sıraya
girdi. Üstelik `DATE` olmayan bir günü (`2026-02-30`) **reddetti**; metin
sütunu onu da kabul ederdi.

## Silince ne olsun

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Kendi başına değerli</span><span class="anat-body">Müşteri → siparişleri. <b>Varsayılan (reddet).</b> Müşteri yanlışlıkla silinmeye kalkarsa sunucu durdurur.</span></div>
    <div class="anat-row"><span class="anat-label">Ebeveynsiz anlamsız</span><span class="anat-body">Sipariş → notları, takım → üyelikleri. <code>ON DELETE CASCADE</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Silmek yerine</span><span class="anat-body">Durum sütunu (<code>status = 'cancelled'</code>). Geçmiş kaybolmaz.</span></div>
  </div>
</figure>

Emin değilsen varsayılanda kal. `CASCADE`'i sonradan eklemek kolay; yanlış
bir `CASCADE`'in götürdüğünü geri getirmek değil.

## Birden fazla sütunlu kurallar

Bazı kurallar tek bir sütuna sığmıyor; tablonun sonuna ayrı yazılıyor.

```sql
-- birlesik anahtar: ayni siparis + ayni urun bir kez
PRIMARY KEY (order_id, product_id)

-- iki sutunu karsilastiran kural
CONSTRAINT ck_trip_dates CHECK (ends >= starts)
```

Sipariş kalemlerinde aynı (sipariş, ürün) çiftini ikinci kez eklemek
`... The duplicate key value is (1001, 1).` hatası verdi; bitişi
başlangıçtan önce olan bir gezi `ck_trip_dates` kuralına takıldı
(ölçüldü).

## Kurallara ad ver

Adsız bir kuralın hata metni `CK__items__price__6B24EA82` gibi bir şey
söylüyor. Kısa bir önekle ad vermek hatayı okunur yapıyor:

| Önek | Kural |
|---|---|
| `pk_` | birincil anahtar |
| `fk_` | yabancı anahtar |
| `uq_` | `UNIQUE` |
| `ck_` | `CHECK` |

## Yeni satırın numarasını almak

`IDENTITY` numarayı sunucu veriyor; peki eklediğin satırın numarası neydi?

```sql
INSERT INTO tickets (title)
OUTPUT inserted.id, inserted.title
VALUES ('a'), ('b');
```

`OUTPUT` eklenen satırları numaralarıyla geri döndürdü: `1 a`, `2 b`
(ölçüldü). Birden fazla satır eklendiğinde de her birinin numarasını
verdiği için tek satır döndüren yollardan daha kullanışlı.

## Kurmadan önce kontrol listesi

<figure class="fig">
  <div class="flow">
    <span class="node">Her sütun satırı mı anlatıyor?</span>
    <span class="arrow">→</span>
    <span class="node">Anahtar ne?</span>
    <span class="arrow">→</span>
    <span class="node">Hangisi boş kalamaz?</span>
    <span class="arrow">→</span>
    <span class="node">Hangi değerler geçersiz?</span>
    <span class="arrow">→</span>
    <span class="node">Silince ne olsun?</span>
  </div>
</figure>
