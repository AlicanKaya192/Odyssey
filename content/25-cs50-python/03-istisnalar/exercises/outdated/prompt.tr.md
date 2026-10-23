ABD'de tarihler genellikle ay-gün-yıl sırasıyla yazılır (`MM/DD/YYYY`). Bu biçim sıralanamaz (yıl en sonda) ve belirsizdir: Harvard 8 Eylül 1636'da kuruldu, ama `9/8/1636` 9 Ağustos 1636 diye de okunabilir. Bilgisayarlar ise ISO 8601'i kullanır: yıl-ay-gün (`YYYY-MM-DD`), yıl dört, ay ve gün iki basamakla, gerekirse başına sıfır konarak.

Kullanıcıdan ay-gün-yıl sırasıyla, `9/8/1636` ya da `September 8, 1636` gibi bir tarih isteyen bir program yaz; ay adı başlangıç kodundaki `months` listesinden biri. Aynı tarihi `YYYY-MM-DD` biçiminde yaz. Girdi iki biçimden birine uygun geçerli bir tarih değilse **yeniden sor**. Her ayın en fazla 31 gün çektiğini varsay; 28, 29, 30 gün denetimine gerek yok. (CS50'de dosyanın adı `outdated.py`.)

İpucu: `months.index("September")` `8` verir (listede olmayan ad `ValueError`). f-string'de `{month:02}` sayıyı başına sıfır koyarak iki basamakla yazar.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `9/8/1636` → çıktı `1636-09-08`
- Girdi `September 8, 1636` → çıktı `1636-09-08`
- Girdi `23/6/1912`, `6/23/1912` → çıktı `1912-06-23`
- Girdi `December 80, 1980`, `12/25/1980` → çıktı `1980-12-25`
- Girdi `September 8 1636`, `1/1/2000` → çıktı `2000-01-01`
- Girdi `  10/9/1701 ` → çıktı `1701-10-09`
- Girdi `Octobr 9, 1701`, `October 9, 1701` → çıktı `1701-10-09`
