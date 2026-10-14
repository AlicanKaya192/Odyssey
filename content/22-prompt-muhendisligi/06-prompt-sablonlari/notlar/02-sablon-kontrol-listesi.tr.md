Python'da üç şablon yolu ve tuzakları:

| Yol | Yer tutucu | Tuzak | Güvenli kullanım |
|---|---|---|---|
| `str.format` | `{ad}` | JSON parantezleri değişken sanılır | JSON'da `{{` ve `}}` |
| `string.Template` | `$ad` | `safe_substitute` eksikleri sessizce bırakır | Yalnızca `substitute` |
| Kendi `render`'ın | `{{ad}}` | Sırayla `replace` değerin içini de doldurur | Tek geçiş (`re.sub`) + değişken denetimi |

**Bir şablonu kullanmadan önce:**

1. Şablondaki değişkenlerin listesini çıkar; verilen değerlerle
   karşılaştır. Eksik ya da kullanılmayan varsa dur.
2. Değerleri tek geçişte yerleştir.
3. Uzun değişkenleri bütçeye sığdır; nereden kestiğine karar ver ve
   kestiğini `...` ile belli et.
4. Şablonun adını ve sürümünü kayda yaz.
5. Yeni bir sürümü değerlendirme kümesiyle eskisine karşı ölç.

**Sık hatalar:**

- **Eksik değişkenle prompt göndermek.** Model `$order_id` gibi bir işareti
  kendince yorumlar.
- **Müşteri metnini şablon gibi işlemek.** Metindeki işaretler doldurulur
  ya da yanlış yere kayar.
- **Uzun metni hep baştan kesmek.** Destek mesajlarında asıl istek çoğu
  zaman sondadır.
- **Şablonu yerinde değiştirmek.** Eski sürüm kaybolursa iki sürüm
  karşılaştırılamaz.
