Kahvaltının 7:00–8:00, öğle yemeğinin 12:00–13:00, akşam yemeğinin 18:00–19:00 arasında yendiği bir ülkede olduğunu düşün. Kullanıcıdan saati isteyen ve kahvaltı, öğle ya da akşam yemeği vaktiyse `breakfast time`, `lunch time` ya da `dinner time` yazan bir program yaz. Yemek vakti değilse **hiçbir şey yazma**. Girdi 24 saatlik `#:##` ya da `##:##` biçiminde; aralıkların uçları dahil (7:00 de 8:00 de kahvaltı).

Programı başlangıç kodundaki düzene göre yaz: `convert(time)` `"7:30"` gibi bir metni saate, `float` olarak çevirsin (`7.5`). Dosyanın sonundaki `if __name__ == "__main__":` satırı `main`'i yalnızca dosya doğrudan çalıştırılınca çağırır; neden gerektiğini 5. haftada birim testlerinde göreceğiz. (CS50'de dosyanın adı `meal.py`.)

İpucu (CS50'den): `hours, minutes = time.split(":")`; bir saatte 60 dakika var.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `7:00` → çıktı `breakfast time`
- Girdi `7:30` → çıktı `breakfast time`
- Girdi `12:42` → çıktı `lunch time`
- Girdi `18:32` → çıktı `dinner time`
- Girdi `11:11` → çıktı (boş)
- Girdi `8:00` → çıktı `breakfast time`
- Girdi `19:00` → çıktı `dinner time`
