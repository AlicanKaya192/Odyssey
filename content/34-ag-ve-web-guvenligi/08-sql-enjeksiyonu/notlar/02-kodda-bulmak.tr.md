Kendi kodunda ya da kod incelemesinde SQL enjeksiyonu açığını bulmak için
saldırı denemek gerekmez; kodu okumak yeter. Aranan tek şey, sorgu
metninin **kullanıcıdan gelebilecek bir değerle birleştirilerek**
kurulduğu yerdir.

## Ne aranır?

- `execute(` çağrısına giden metinde `f"`, `+`, `%`, `.format(`.
- Sorgu metnini bir değişkende hazırlayıp sonra `execute(query)` diyen
  yerler: `query`'nin nasıl kurulduğuna bakılır.
- ORM içinde "ham sorgu" çalıştıran fonksiyonlar.
- Veritabanından okunan bir değerin başka bir sorguda metinle kullanıldığı
  yerler (ikinci dereceden).

## Sık görülen bahaneler

| Bahane | Neden yanlış |
|---|---|
| "Bu değer bir açılır listeden geliyor" | İstek tarayıcı olmadan da yazılabilir (HTTP ve HTTPS bölümü) |
| "Bu değer bizim veritabanımızdan" | Oraya da kullanıcı yazmıştı |
| "Yalnızca yöneticiler kullanıyor" | Yönetici hesabı da ele geçirilebilir |
| "Tırnakları siliyoruz" | Ayıklama bir şeyi unutur; parametre unutmaz |
| "Sütun adı olduğu için parametre olmuyor" | Doğru; çözüm izin listesi |

## Düzeltme sırası

1. Sorguyu yer tutuculu biçime çevir, değerleri ikinci argümanda ver.
2. Sütun ya da tablo adı değişiyorsa izin listesine eşle.
3. `LIKE` varsa joker karakterlerini kaç.
4. Hata mesajlarının kullanıcıya ne gösterdiğine bak.
5. Bu düzeltmeyi bir testle koru: adında `'` olan bir kayıtla sorgu doğru
   çalışmalı.

## Testte kullanılacak masum girdiler

Açık aramak için saldırı yükü gerekmez. Şu girdiler doğru çalışan bir
sorguyu bozmamalı:

- Adında kesme işareti olan biri: `O'Brien`
- Çift tırnak içeren bir ad: `Ann "Jr" Lee`
- Yüzde ve alt çizgi içeren bir arama: `50%`, `plan_b`
- Boş metin
