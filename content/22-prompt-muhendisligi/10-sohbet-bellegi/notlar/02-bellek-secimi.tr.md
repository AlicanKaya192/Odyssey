Hangi yolu ne zaman kullanırsın?

| Yol | Token | Unutur mu? | Dikkat |
|---|---|---|---|
| Bütün geçmiş | Mesaj sayısıyla hızla büyür | Hayır | Pencereye sığmayabilir |
| Son N mesaj | Sabit kalır | Evet, eski bilgileri | En basit yol |
| Özet + son N | Az, ama özet çağrısı da var | Ayrıntıları düşürebilir | Özet de doğrulanmalı |
| Bilgi belleği + son N | Az | Bellekteki bilgileri unutmaz | Kişisel veri; süzgeç ve silme |

**Bilgi belleği kurarken:**

1. Hangi bilgilerin gerektiğini yaz: ad, sipariş numarası, seçilen ürün.
   Gerekmeyeni tutma.
2. Bilgiyi kodla (düzenli ifade) ya da modelle (JSON) çıkar; ikisinde de
   doğrula.
3. Saklamadan önce süz: parola, kart numarası, kimlik numarası, sağlık
   bilgisi girmez.
4. Belleği sistem mesajına kısa bir satır olarak ekle.
5. Belleği kullanıcıya bağla; görüntüleme ve silme yolu sun; kayıtlara
   ömür ver.

**Sık hatalar:**

- **Her şeyi saklamak.** Bellek bir müşteri kaydıdır; gereğinden fazlası
  hem risk hem token.
- **Özete körü körüne güvenmek.** Derste özet sipariş numarasını düşürdü.
- **Bir kullanıcının belleğini başka bir sohbette kullanmak.** En ciddi
  gizlilik hatası.
- **Çıkarılan bilgiyi doğrulamamak.** Yanlış bir sipariş numarası
  bellekte kalırsa her çağrıda modele gider.
