Markete gitmeden önce alınacakların listesini çıkardığını düşün.

Kullanıcı girdiyi bitirene kadar (`Ctrl+D`, `EOFError`) satır satır ürün isteyen bir program yaz. Sonra listeyi **büyük harfle**, ürün adına göre **abece sırasıyla** yaz; her satırın başında o ürünün kaç kez yazıldığı olsun: `2 MILK`. Ürünü çoğul yapmaya gerek yok; büyük/küçük harfe bakma. (CS50'de dosyanın adı `grocery.py`.)

İpucu: sayıları bir sözlükte tut (ürün → kaç kez). `sorted(counts)` sözlüğün anahtarlarını abece sırasıyla verir.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `mango`, `strawberry` → çıktı `1 MANGO`, `1 STRAWBERRY`
- Girdi `milk`, `milk` → çıktı `2 MILK`
- Girdi `tortilla`, `sweet potato` → çıktı `1 SWEET POTATO`, `1 TORTILLA`
- Girdi `Apple`, `banana`, `apple`, `APPLE` → çıktı `3 APPLE`, `1 BANANA`
