Harvard Meydanı'nda en sevilen yerlerden biri Felipe's Taqueria. Menüsü başlangıç kodundaki `menu` sözlüğünde: her yemek dolar cinsinden fiyatına bağlı.

Kullanıcının sipariş vermesini sağlayan bir program yaz: kullanıcı girdiyi bitirene kadar (`Ctrl+D`, programa `EOFError` olarak gelir) satır satır yemek iste. Her yemekten sonra o ana kadarki toplamı, başında dolar işaretiyle ve virgülden sonra iki basamakla yaz: `Total: $6.00`. Büyük/küçük harfe bakma, menüde olmayanı yok say. Menüdeki her yemeğin her kelimesi büyük harfle başlıyor. (CS50'de dosyanın adı `taqueria.py`.)

İpucu: `"baja taco".title()` `"Baja Taco"` verir.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Taco`, `Taco` → çıktı `Total: $3.00`, `Total: $6.00`
- Girdi `Baja Taco`, `Tortilla Salad` → çıktı `Total: $4.25`, `Total: $12.25`
- Girdi `Burger`, `nachos` → çıktı `Total: $11.00`
- Girdi `  super BURRITO `, `bowl` → çıktı `Total: $8.50`, `Total: $17.00`
