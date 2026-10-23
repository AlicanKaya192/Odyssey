David'in çocukken ilk oyuncaklarından biri Little Professor'dı: çözmesi için on matematik sorusu üreten bir "hesap makinesi". Ekranda `4 + 0 =` görünür, David `4` cevabını verir. Yanlış cevaba `EEE` yazar; aynı soruda üç yanlıştan sonra doğru cevabı gösterir (`4 + 0 = 4`).

Şu programı yaz:

- Kullanıcıdan bir seviye (`n`) ister; 1, 2 ya da 3 değilse yeniden sorar.
- `X + Y = ` biçiminde **on** toplama sorusu üretir; `X` ve `Y` `n` basamaklı, negatif olmayan tam sayılar. Soruyu `input`'un sorusu olarak yaz.
- Her soruyu sorar. Cevap yanlışsa (ya da sayı değilse) `EEE` yazar ve yeniden sorar; bir soruya toplam üç hak var. Üçünde de yanlışsa doğru cevabı `6 + 6 = 12` biçiminde yazar ve sonraki soruya geçer.
- Sonunda puanı yazar: ilk denemede doğru cevaplanan soru sayısı, `Score: 9` biçiminde.

Programı başlangıç kodundaki düzene göre yaz: `get_level` seviyeyi alıp döndürür, `generate_integer(level)` `level` basamaklı rastgele bir tam sayı döndürür (1 için 0–9, 2 için 10–99, 3 için 100–999; başka seviyede `ValueError` fırlatır). Sayıları her soru için **önce `X` sonra `Y`** diye üret: denetim rastgele üreteci her durumda aynı tohumla başlatıyor, sıra aynıysa senin programın da aynı soruları sorar. (CS50'de dosyanın adı `professor.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `1`, `7`, `6`, `9`, `6`, `9`, `11`, `1`, `12`, `4`, `9` → çıktı `Score: 10`
- Girdi `1`, `cat`, `7`, `6`, `9`, `6`, `9`, `11`, `1`, `12`, `4`, `9` → çıktı `EEE`, `Score: 9`
- Girdi `1`, `cat`, `8`, `9`, `6`, `9`, `6`, `9`, `11`, `1`, `12`, `4`, `9` → çıktı `EEE`, `EEE`, `EEE`, `5 + 2 = 7`, `Score: 9`
- Girdi `-1`, `4`, `2`, `94`, `161`, `137`, `108`, `145`, `107`, `117`, `21`, `141`, `82` → çıktı `Score: 10`
- Girdi `3`, `751`, `1043`, `1095`, `450`, `288`, `1173`, `1315`, `1043`, `959`, `1117` → çıktı `Score: 10`
