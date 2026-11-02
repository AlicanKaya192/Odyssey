Küçük bir okul sisteminin risk kaydından bir parça. Puanlar ve düzeyler
Python ile hesaplandı (düzey sınırları derstekiyle aynı).

| Risk | Olasılık | Etki | Puan | Düzey | Sahip | Cevap |
|---|---|---|---|---|---|---|
| Öğretmen hesabının parolası tahmin edilir | 4 | 4 | 16 | Yüksek | Ayşe | Azalt: ikinci adım (MFA) |
| Not veritabanı sızar | 2 | 5 | 10 | Yüksek | Mehmet | Azalt: şifreleme, erişim gözden geçirme |
| Sınav günü site çöker | 3 | 3 | 9 | Orta | Can | Azalt: ikinci sunucu |
| Sunucu odasında yangın | 1 | 5 | 5 | Orta | Zeynep | Aktar: sigorta; ayrıca yedek |
| Eski test sunucusunda küçük açık | 2 | 2 | 4 | Düşük | Can | Kabul: 3 ay sonra yeniden bak |

## Sütunlar

- **Risk:** kısa ve somut bir ad. "Siber saldırı" değil, "öğretmen
  hesabının parolası tahmin edilir".
- **Olasılık, etki, puan:** puan her zaman çarpım; elle yazılmaz.
- **Sahip:** riskten sorumlu tek kişi. "Bilgi işlem" değil, bir ad.
- **Cevap:** azalt, aktar, kaçın ya da kabul et; yanında ne yapılacağı.

## Nasıl okunur?

1. En yüksek puandan başla.
2. Kritik ve yüksek düzeydekilerin her birinin bir cevabı ve tarihi var mı?
3. Kabul edilenlerin kim tarafından ve ne zaman kabul edildiği yazılı mı?
4. Bir önlem uygulandıktan sonra olasılık ya da etki yeniden puanlanır;
   eski puan silinmez, yanına yenisi yazılır. Böylece önlemin işe yarayıp
   yaramadığı görünür.

## Ne zaman güncellenir?

- Düzenli aralıklarla (örneğin üç ayda bir).
- Yeni bir sistem, yeni bir veri türü ya da yeni bir tedarikçi gelince.
- Bir olay yaşandıktan sonra: olay kayıtta olmayan bir riski gösterdiyse
  kayda eklenir.
