Bir anahtarın, parolanın ya da jetonun depoya, kayıtlara ya da bir sohbete
düştüğü fark edildiğinde sıra önemlidir.

## Adımlar

1. **Değiştir (döndür).** Yeni sır üretilir, kullanan sistemler yenisine
   geçirilir, eskisi **iptal edilir**. İlk ve en önemli adım budur.
2. **Kaydı temizle.** Dosyadan ve gerekiyorsa depo geçmişinden kaldırılır.
   Bu tek başına yetmez: depo kopyalanmış, kayıt okunmuş olabilir.
3. **Etkiye bak.** Sır sızdığı süre içinde kullanıldı mı? Erişim
   kayıtları incelenir.
4. **Nedeni kapat.** Sır neden koda girdi? Commit öncesi tarayıcı,
   ortam değişkeni, sır kasası.

## Neden önce değiştirmek

Silmek "görünmez" yapar, "kullanılamaz" yapmaz. Sırrı görmüş biri onu
silindikten sonra da kullanabilir. Değiştirilen sır ise artık hiçbir işe
yaramaz.

## Önlemek

| Önlem | Ne yapar |
|---|---|
| `.gitignore` | Sır dosyalarını (`.env`) depoya almaz |
| Commit öncesi tarayıcı | Tırnak içindeki sırları commit'ten önce yakalar |
| Sır kasası | Sırları koddan ayrı, erişimi kayıtlı bir yerde tutar |
| Kısa ömürlü jetonlar | Sızan jetonun işe yarayacağı süreyi kısaltır |
| En az yetki | Sızan sırrın açtığı kapıları azaltır (En Az Yetki ve Görev Ayrılığı bölümü) |
