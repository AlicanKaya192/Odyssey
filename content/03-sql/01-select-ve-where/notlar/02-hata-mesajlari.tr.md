Sunucunun verdiği hata mesajları kısa ve İngilizce. Bu bölümde
karşılaşacağın beş tanesi ve ne demek istedikleri.

## Invalid column name 'X'

**Böyle bir sütun yok.** Üç ihtimal, sırayla bak:

1. **Yazım hatası.** `fiyt` yazdın, `fiyat` olacaktı.
2. **Çift tırnak kullandın.** `WHERE kategori = "Ekran"` yazdıysan sunucu
   `Ekran` adında bir sütun arıyor. Metin **tek tırnakla** yazılıyor.
3. **`SELECT`'teki takma adı `WHERE`'de kullandın.** Sunucu önce `WHERE`'i
   çalıştırıyor; o sırada takma ad henüz yok.

```sql
-- calismaz
SELECT fiyat AS tutar FROM urunler WHERE tutar > 1000;
-- calisir
SELECT fiyat AS tutar FROM urunler WHERE fiyat > 1000;
```

## Invalid object name 'X'

**Böyle bir tablo yok.** Genellikle tablo adında yazım hatası, ya da
yanlış veritabanına bağlısın (SSMS'te üstteki açılır kutu).

## Incorrect syntax near 'X'

**Cümle kurulamadı.** Sunucu `X`'i gördüğü yerde ne yapacağını
bilemiyor. En sık sebepleri:

- Virgül unutulmuş: `SELECT ad fiyat FROM ...`
- Virgül fazladan: `SELECT ad, FROM ...`
- Anahtar kelime yanlış yazılmış: `SELCT`, `FORM`, `WEHRE`
- Tırnak kapatılmamış: `WHERE kategori = 'Ekran`

Hata **`X`'in kendisinde değil, ondan hemen öncesinde** olabiliyor —
sunucu sorunu ancak oraya gelince fark ediyor.

## Conversion failed when converting the varchar value 'X' to data type int

**Metni sayıyla karşılaştırdın.** `WHERE stok = 'bes'` gibi. Sunucu metni
sayıya çevirmeye çalışıyor ve başaramıyor.

## Ambiguous column name 'X'

**Bu ad iki yerde birden var.** Bu bölümde tek tabloyla çalıştığın için
çıkmıyor; iki tabloyu birleştirdiğinde (`JOIN`) ortaya çıkacak.

---

## Hata yokken de yanlış olabilir

En tehlikeli durum bu: sorgu çalışıyor, sonuç geliyor, ama **yanlış**
sonuç. Sunucu bunu söyleyemez.

En sık sebebi `AND` / `OR` parantezi. Kontrol yolu: **kaç satır
beklediğini önceden söyle**, sonra gelen sayıya bak. Tutmuyorsa koşulu
parça parça çalıştır.
