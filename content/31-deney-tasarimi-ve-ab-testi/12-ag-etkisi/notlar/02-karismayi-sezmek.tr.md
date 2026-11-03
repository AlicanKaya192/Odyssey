Karışma kendini haber vermez: test temiz görünür, SRM yoktur, p değeri
küçüktür. Bu yüzden plan yazılırken sorulur.

## Plan aşamasında sorulacaklar

- B'deki bir kullanıcının davranışı, A'daki birinin **kullanabileceği bir
  şeyi** azaltıyor mu? (sürücü, stok, sıra, bütçe)
- B'deki biri A'daki birine bir şey **gönderiyor** mu? (mesaj, davet,
  paylaşım)
- Değişiklik pazarın öbür tarafını (satıcı, sürücü, yazar) etkiliyor mu?

Cevaplardan biri "evet" ise kullanıcı düzeyindeki test etkiyi büyütebilir
ya da küçültebilir.

## Tasarım seçenekleri

| Tasarım | Ne yapılır | Bedeli |
|---|---|---|
| Küme (şehir, bölge) | kümenin herkesi aynı grupta | az küme, çok gürültü |
| Arkadaş kümesi | ağda sık bağlı gruplar birlikte atanır | kümeleri bulmak zor |
| Switchback | bütün pazar sırayla A ve B olur (ör. saat saat) | zamanla değişen etkiler, geçiş anları |

## Belirtiler

- Kontrol grubunun metriği, testten önceki dönemine göre **düştü** (B,
  A'dan aldı).
- Testin etkisi, değişiklik herkese açıldıktan sonra beklenenden çok küçük
  çıktı.
- Etki, B'nin payı arttıkça küçülüyor (Yenilik Etkisi ve Uzun Vadeli Etki
  bölümündeki tutma grubu bunu da gösterebilir).
