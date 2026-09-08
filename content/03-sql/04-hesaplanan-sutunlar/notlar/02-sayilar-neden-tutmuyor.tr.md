Bir raporda sayı tutmadığında sebep neredeyse her zaman şu beş şeyden
biri. Hepsi **sessiz**: sorgu çalışıyor, hata yok, sayı yanlış.

## 1. Tam sayı bölmesi

En sık olanı.

```sql
SELECT satilan / toplam * 100 AS yuzde
```

`satilan` ve `toplam` tam sayıysa bölme **önce** yapılıyor ve sonuç 0 ya
da 1 çıkıyor; 100 ile çarpınca 0 ya da 100 oluyor. Arada hiçbir değer yok.

Düzeltme:

```sql
SELECT satilan * 100.0 / toplam AS yuzde
```

Çarpmayı öne almak hem ondalıklıya çeviriyor hem hassasiyeti koruyor.

## 2. NULL bulaşması

```sql
SELECT fiyat + kargo AS toplam
```

Kargo boşsa toplam da boş. Rapor toplamında o satır **hiç görünmüyor** ya
da boş çıkıyor.

```sql
SELECT fiyat + ISNULL(kargo, 0) AS toplam
```

## 3. Yuvarlama farkı

`ROUND(2.5, 0)` SQL Server'da **3**, Python'da **2**.

SQL yarımları sıfırdan uzağa, Python çift sayıya yuvarlıyor. Aynı hesabı
iki yerde yapıp karşılaştıran biri kuruş farkları görüyor ve sebebini
bulamıyor.

Muhasebe hesaplarında bu fark birikebiliyor; hangi tarafın yuvarladığına
baştan karar vermek gerekiyor.

## 4. `+` ile birleştirme

```sql
SELECT ad + ' ' + soyad AS tam_ad
```

Soyadı boş olan kişilerde `tam_ad` **tamamen boş** çıkıyor — adı da
kayboluyor. `CONCAT` bunu yapmıyor.

## 5. Ondalık türlerin hassasiyeti

`DECIMAL(10,2)` iki basamak tutuyor. Bir bölme sonucunu ona atarsan
üçüncü basamak kayboluyor:

```sql
SELECT CAST(1.0/3 AS DECIMAL(10,2))   -- 0.33
```

Ara hesaplarda daha geniş bir tür kullanıp **yalnızca sonuçta**
yuvarlamak daha doğru.

`FLOAT` ise bambaşka bir konu: ikilik tabanda tutulduğu için `0.1 + 0.2`
tam olarak `0.3` etmiyor. Para tutan sütunlarda `FLOAT` kullanılmaz,
`DECIMAL` kullanılır.

---

## Kontrol alışkanlığı

Hesaplanan bir sütun yazdığında üç soru sor:

1. **Bölme var mı?** Varsa iki taraf da tam sayı mı?
2. **Sütunlardan biri `NULL` olabilir mi?** Olabiliyorsa ne olmasını
   istiyorsun?
3. **Bir satır elle hesaplandığında aynı çıkıyor mu?** Tek bir satırı
   hesap makinesiyle doğrulamak, on beş dakikalık aramayı önlüyor.
