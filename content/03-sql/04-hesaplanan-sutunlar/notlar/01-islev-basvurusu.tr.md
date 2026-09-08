Bu bölümde geçen işlevlerin tek sayfalık listesi. Hepsi SQL Server'da
ölçüldü; sonuç sütunundaki değerler gerçek çıktılar.

## Metin

| İşlev | Örnek | Sonuç |
|---|---|---|
| `LEN` | `LEN('Keyboard')` | `6` |
| `LEN` (sondaki boşluk) | `LEN('abc   ')` | `3` |
| `LEN` (baştaki boşluk) | `LEN('   abc')` | `6` |
| `DATALENGTH` | `DATALENGTH('abc   ')` | `6` |
| `UPPER` / `LOWER` | `UPPER('abc')` | `ABC` |
| `TRIM` | `TRIM('  abc  ')` | `abc` |
| `LTRIM` / `RTRIM` | `RTRIM('abc  ')` | `abc` |
| `LEFT` | `LEFT('Keyboard', 3)` | `Kla` |
| `RIGHT` | `RIGHT('Keyboard', 3)` | `vye` |
| `SUBSTRING` | `SUBSTRING('Keyboard', 2, 3)` | `lav` |
| `REPLACE` | `REPLACE('Keyboard','a','A')` | `KlAvye` |
| `CONCAT` | `CONCAT('a', NULL, 'b')` | `ab` |

`SUBSTRING`'de sayma **1'den** başlıyor. Çoğu programlama dilinde 0'dan
başladığı için bu sık karıştırılıyor.

`LEN`'in sondaki boşlukları saymaması ama baştakileri sayması bir
tuhaflık, tasarım kararı değil — eski sürümlerden kalma bir davranış.

## Sayı

| İşlev | Örnek | Sonuç |
|---|---|---|
| `ROUND` | `ROUND(2.5, 0)` | `3` |
| `ROUND` | `ROUND(3.5, 0)` | `4` |
| `ROUND` | `ROUND(2.345, 2)` | `2.35` |
| `CEILING` | `CEILING(2.1)` | `3` |
| `FLOOR` | `FLOOR(2.9)` | `2` |
| `ABS` | `ABS(-5)` | `5` |

`ROUND` yarımları **sıfırdan uzağa** yuvarlıyor. Python'un `round` işlevi
çift sayıya yuvarlıyor (`round(2.5)` = 2), yani aynı hesap iki dilde
farklı çıkabiliyor. Rapor sayıları tutmuyorsa bakılacak yerlerden biri.

## Tür çevirme

| İşlev | Girdi | Sonuç |
|---|---|---|
| `CAST` | `CAST('12' AS INT)` | `12` |
| `CAST` | `CAST('abc' AS INT)` | **hata** |
| `TRY_CAST` | `TRY_CAST('abc' AS INT)` | `NULL` |

`CAST` çeviremediğinde **sorgunun tamamı düşüyor**. Tek bir bozuk satır
bütün raporu durduruyor. `TRY_CAST` o satırda `NULL` verip devam ediyor.

`CONVERT` de var ve SQL Server'a özgü; tarih biçimlendirmede işe yarıyor.
`CAST` standart SQL, taşınabilir olan o.

## Boşluk doldurma

| İşlev | Örnek | Sonuç |
|---|---|---|
| `ISNULL` | `ISNULL(NULL, 'yok')` | `yok` |
| `COALESCE` | `COALESCE(NULL, NULL, 'c')` | `c` |
| `NULLIF` | `NULLIF(5, 5)` | `NULL` |

`ISNULL` iki değer alıyor ve SQL Server'a özgü. `COALESCE` istediğin kadar
alıyor ve standart.

`NULLIF` ters yönde çalışıyor: bir değeri `NULL`'a çeviriyor. En sık
kullanımı sıfıra bölmeyi engellemek — `a / NULLIF(b, 0)` ifadesinde `b`
sıfırsa sonuç hata yerine `NULL` oluyor.

## Aritmetikte iki kural

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Tam sayı bölmesi</span><span class="anat-body"><code>7 / 2</code> → <b>3</b>. İki taraf da tam sayıysa sonuç tam sayı ve ondalık kısım <b>atılıyor</b>. Bir tarafı ondalıklı yap: <code>7.0 / 2</code> → 3.5</span></div>
    <div class="anat-row"><span class="anat-label">NULL bulaşıcı</span><span class="anat-body"><code>5 + NULL</code> → <b>NULL</b>. İçinde boş bir değer geçen her işlem boş sonuç veriyor.</span></div>
  </div>
</figure>

## Birleştirmede `+` ile `CONCAT` farkı

| İfade | Sonuç |
|---|---|
| `'a' + 'b'` | `ab` |
| `'a' + NULL` | `NULL` |
| `'a' + 1` | **hata** |
| `CONCAT('a', NULL, 'b')` | `ab` |
| `CONCAT('a', 1)` | `a1` |

`CONCAT` hem `NULL`'ı atlıyor hem sayıyı kendisi metne çeviriyor.
Birleştirme için varsayılan tercih o olmalı.
