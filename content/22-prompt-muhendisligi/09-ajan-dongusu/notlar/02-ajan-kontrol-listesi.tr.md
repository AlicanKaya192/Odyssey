Bir ajanı çalıştırmadan önce:

| Soru | Cevap yoksa ne olur? |
|---|---|
| Adımların sırası gerçekten girdiye göre değişiyor mu? | Zincir yeterken ajan kurulur; daha pahalı ve daha zor test edilir |
| Adım sınırı kaç? | Takılan ajan sonsuza kadar döner |
| Token bütçesi kaç? | Uzun geçmiş her turda yeniden ödenir |
| Hangi araçlar izin listesinde? | Model istenmeyen bir işi çağırabilir |
| Geri alınamaz işler onaylı mı? | Ajan bir iptali ya da ödemeyi kendisi yapar |
| Sınır dolunca iş nereye gider? | Müşteri cevapsız kalır |

**Döngüde her turda:**

1. Modeli çağır; giren token'ı ize yaz.
2. Araç çağrısı yoksa cevabı al ve doğrula (uzunluk, vaat, dayanak).
3. Her araç çağrısı için: tekrar mı? izin listesinde mi? argümanlar
   doğru mu? onay gerekiyor mu?
4. Sonucu ya da hatayı `tool` mesajı olarak geçmişe ekle.
5. Adım sınırını ve token bütçesini denetle.

**Sık hatalar:**

- **Durmayı modele bırakmak.** Model "bitti" demeyebilir; program
  durdurur.
- **Aynı çağrıyı tekrar tekrar çalıştırmak.** Hem araç hem token harcanır.
- **Döngünün düzgün bitmesini başarı saymak.** Cevap yarım olabilir;
  değerlendirme kümesiyle ölç.
- **İz tutmamak.** Yanlış bir cevabın hangi turda başladığı bulunamaz.
