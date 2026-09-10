Bu bölümün komutları kolay. Zor olan, onları yanlış çalıştırmamak.

Aşağıdakiler kural değil **alışkanlık**: hepsi birkaç saniye sürüyor ve
her biri gerçekten yaşanmış bir kazayı engelliyor.

## 1. Aynı WHERE ile önce bir SELECT

```sql
SELECT * FROM products WHERE category_code = 'ACC';
```

Ekranda tam olarak hangi satırların değişeceğini görüyorsun. Doğruysa
`SELECT *` kısmını `UPDATE ... SET ...` ile değiştiriyorsun; `WHERE`'e
dokunmuyorsun.

Bu tek alışkanlık `UPDATE` ve `DELETE` hatalarının büyük çoğunluğunu
engelliyor, çünkü hataların çoğu komutta değil **koşulda**.

## 2. Satır sayısına bak

Sunucu her yazma komutundan sonra kaç satıra dokunduğunu söylüyor.
O sayıyı **okuma alışkanlığı** edin.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">1 bekliyordun, 40 geldi</span><span class="anat-body">Koşul yeterince daraltmamış. İşlem içindeysen <code>ROLLBACK</code>.</span></div>
    <div class="anat-row"><span class="anat-label">1 bekliyordun, 0 geldi</span><span class="anat-body">Koşul hiçbir şey tutmamış. Yazım hatası ya da değer yanlış.</span></div>
    <div class="anat-row"><span class="anat-label">Beklediğin kadar</span><span class="anat-body">Devam.</span></div>
  </div>
</figure>

## 3. Tehlikeli işi işlem içinde yap

```sql
BEGIN TRANSACTION;

DELETE FROM orders WHERE order_date < '2020-01-01';

SELECT COUNT(*) FROM orders;   -- makul mu?

ROLLBACK;
```

Sayı beklediğin gibiyse `ROLLBACK`'i `COMMIT` yapıp yeniden çalıştırıyorsun.
Değilse hiçbir şey olmamış oluyor.

**Bir uyarı:** açık bir işlem, dokunduğu satırları kilitli tutuyor.
Başkasının sorgusu o satırları beklemeye başlıyor. İşlemi açık bırakıp
kahve içmeye gitmek gerçek bir sorun — açtığın işlemi kapatmadan bırakma.

## 4. `WHERE` yazarken anahtarı kullan

```sql
-- kirilgan
UPDATE customers SET city = 'Ankara' WHERE name = 'Nova Retail';

-- saglam
UPDATE customers SET city = 'Ankara' WHERE id = 1;
```

Ada göre süzmek, aynı adı taşıyan ikinci bir satır olduğu gün iki satırı
birden değiştiriyor. Birincil anahtar tam olarak bir satırı gösteriyor.

Adı kullanman gerekiyorsa önce `SELECT` ile kaç satır tuttuğuna bak.

## 5. Silmeden önce: gerçekten silinmeli mi?

Çoğu sistemde satırlar silinmiyor, **işaretleniyor**:

```sql
-- silmek yerine
UPDATE orders SET status = 'cancelled' WHERE id = 1006;
```

Buna *yumuşak silme* deniyor. Avantajı geri alınabilir olması ve geçmişin
kaybolmaması; bedeli, bundan sonra her sorguya "iptal olmayanlar" koşulu
eklemek zorunda kalman.

Karar duruma göre değişiyor, ama "sil" demeden önce sorulacak soru bu.

## 6. Bir satırı silmek yetmiyor

Bir siparişi sildiğinde kalemleri ne oluyor?

Bu bölümün şemasında bağlar tanımlı değil, o yüzden sunucu hiçbir şey
demiyor: sipariş gidiyor, kalemleri kalıyor ve artık var olmayan bir
siparişi işaret ediyor. Kimse fark etmiyor, çünkü onları bulmanın yolu
olmayan bir siparişi aramaktan geçiyor.

Buna **öksüz satır** deniyor. İki çözümü var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Elle</span><span class="anat-body">Önce çocuk satırları, sonra ana satırı sil. Sırayı hatırlamak sana kalıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Sunucuya bırak</span><span class="anat-body">Bağı tanımla; sunucu ya yanlış sıradaki silmeyi <b>reddediyor</b> ya da çocukları kendisi siliyor.</span></div>
  </div>
</figure>

İkincisi bir sonraki bölümün konusu.

## 7. Yedek

Yukarıdakilerin hepsi başarısız olabilir. Üretim verisinde toplu bir
değişiklik yapmadan önce yedek almak, bu listenin en sıkıcı ve en önemli
maddesi.

## Özet

<figure class="fig">
  <div class="flow">
    <span class="node">SELECT ile prova</span>
    <span class="arrow">→</span>
    <span class="node">BEGIN TRANSACTION</span>
    <span class="arrow">→</span>
    <span class="node">UPDATE / DELETE</span>
    <span class="arrow">→</span>
    <span class="node">satır sayısına bak</span>
    <span class="arrow">→</span>
    <span class="node ok">COMMIT</span>
    <span class="arrow">/</span>
    <span class="node no">ROLLBACK</span>
  </div>
</figure>
