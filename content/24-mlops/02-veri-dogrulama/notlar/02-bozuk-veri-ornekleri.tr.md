Gerçek projelerde sık görülen veri hataları ve onları yakalayan
denetim:

| Ne oldu | Veride nasıl görünür | Yakalayan |
|---|---|---|
| Birim değişti | Ücret 29,90 yerine 2990 | Aralık |
| Yazım değişti | `"pro"` yerine `"PRO"` ya da `"Pro "` | İzin verilen değerler |
| Yeni kategori eklendi | `"gold"` paketi | İzin verilen değerler |
| Sütunun adı değişti | `tenure` yok, `tenure_months` var | Eksik değer (her satırda) |
| Sayı metin olarak geldi | `"29.90"` | Tür |
| Alan boş geldi | `None` | Eksik değer |
| Kaynak sistem bozuldu | Bütün destek aramaları `0` | Profil |
| Veri yarım geldi | 1000 yerine 120 satır | Satır sayısı |
| Aynı satır iki kez geldi | Aynı `id` iki kez | Eşsizlik |

Son iki satırdaki denetimler bu bölümün kodunda yok ama aynı fikirle
yazılır: partinin satır sayısı beklenen aralıkta mı, `id` sütununda
tekrar var mı (`len(ids) == len(set(ids))`).

## Hata çıkmadı diye veri sağlam değildir

Dersteki ölçümde üç bozuk partinin hiçbiri hata vermedi:

| Bozulma | Hata | Sonuç |
|---|---|---|
| Ücret kuruş cinsinden | Yok | Doğruluk düştü |
| Paket adı büyük harf | Yok | Bütün müşteriler `basic` sayıldı |
| Kullanım süresi boş | Yok | scikit-learn'ün ağaçları boş değeri kendisi işledi |

## Kontrol listesi

- Her sütun için yazılı bir kural var mı?
- Kurallar veriyi gönderen ekiple birlikte gözden geçirildi mi?
- Referans veriden çıkarılan aralıklara pay bırakıldı mı?
- Doğrulama eğitimden **önce**, hattın ayrı bir adımı olarak mı çalışıyor?
- Bozuk satırların payı için bir sınır var mı? Sınır geçilince hat
  duruyor mu?
- Karantinadaki satırlar bir yerde saklanıyor ve inceleniyor mu?
- Tahmin anında da aynı kurallar uygulanıyor mu?

## Yapma

- Bozuk satırları sessizce silip devam etme: kaç satır gittiği ve neden
  gittiği bilinmeli.
- Kuralları referans verinin tam en küçük ve en büyük değerine sabitleme;
  gerçek ama biraz farklı müşteriler reddedilir.
- Profil uyarısını otomatik ret gibi kullanma; önce bir insan baksın.
