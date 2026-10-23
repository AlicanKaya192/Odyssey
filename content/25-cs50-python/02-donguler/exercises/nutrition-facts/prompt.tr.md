ABD Gıda ve İlaç Dairesi (FDA), ABD'de en çok yenen 20 çiğ meyvenin besin değerlerini gösteren posterler yayımlıyor. Başlangıç kodundaki `calories` sözlüğü bu posterdeki her meyveyi bir porsiyonunun kalorisine bağlıyor; anahtarlar küçük harfle yazılmış.

Kullanıcıdan bir meyve adı isteyen (büyük/küçük harf fark etmeden) ve o meyvenin bir porsiyonundaki kaloriyi `Calories: 130` biçiminde yazan bir program yaz. Kullanıcının meyveyi posterdeki gibi yazacağını varsay (`strawberry` değil `strawberries`). Meyve değilse **hiçbir şey yazma**. (CS50'de dosyanın adı `nutrition.py`; CS50 sözlüğü öğrencinin kendisinin yazmasını istiyor, burada hazır veriliyor.)

İpucu: `in` bir anahtarın sözlükte olup olmadığını sorar: `"apple" in calories` → `True`.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Apple` → çıktı `Calories: 130`
- Girdi `Avocado` → çıktı `Calories: 50`
- Girdi `Sweet Cherries` → çıktı `Calories: 100`
- Girdi `Tomato` → çıktı (boş)
- Girdi `  KIWIFRUIT ` → çıktı `Calories: 90`
- Girdi `honeydew melon` → çıktı `Calories: 50`
