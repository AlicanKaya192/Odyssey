Bir LLM uygulamasının injection savunması için kontrol listesi:

| Katman | Ne yapılır? | Neyi kaçırabilir? |
|---|---|---|
| Veriyi ayırmak | Ayraç + kaçırma; "bu veri, talimat değil" demek | Model yine de verideki cümleden etkilenebilir |
| Girdi dedektörü | Kalıp ya da eğitilmiş sınıflandırıcı | Yeni yazımlar, başka diller; yanlış alarm verir |
| En az yetki | Yalnızca gereken araçlar | — (zararı sınırlar, saldırıyı durdurmaz) |
| Kaynağa göre yetki | Belgeden/araçtan gelen istek geri alınamaz iş tetikleyemez | Kullanıcının kendisi saldırgansa |
| Onay | Geri alınamaz işlerde insan onayı | İnsan dikkatsizse |
| Çıktı denetimi | İz (canary), bağlantı izin listesi, vaat ve gizli bilgi kalıpları | Kalıba uymayan sızıntılar |
| Kayıt ve izleme | Şüpheli girdi ve engellenen çıktıları kaydet | — (sonradan fark etmeyi sağlar) |

**Kurallar:**

1. Sistem mesajını herkese açık say; içine gizli bilgi yazma.
2. Modelin okuduğu her dış metni (yorum, belge, web sayfası, araç
   sonucu) güvenilmeyen veri say.
3. Cevabı bir sayfada çiziyorsan bağlantıları ve görselleri izin
   listesine göre süz.
4. Bildiğin saldırıları ve onlara benzeyen masum mesajları bir
   değerlendirme kümesinde tut; her değişiklikte yeniden ölç.

**Sık hatalar:**

- **Tek bir katmana güvenmek.** Derste dedektör yedi saldırının üçünü
  kaçırdı.
- **Yalnızca doğrudan saldırıyı düşünmek.** Dolaylı saldırıda kullanıcı
  masumdur; saldırı veridedir.
- **"Ben yöneticiyim" gibi iddialara göre yetki vermek.** Yetkiyi
  oturumdaki gerçek kimlik belirler.
- **Görsel bağlantısını zararsız sanmak.** Tarayıcı onu kendiliğinden
  ister; veri tıklamadan dışarı gider.
