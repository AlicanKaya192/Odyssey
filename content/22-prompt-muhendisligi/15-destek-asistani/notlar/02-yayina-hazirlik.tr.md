Bir LLM asistanını müşterilere açmadan önce kontrol listesi:

**Ölçüm**

- [ ] Gerçek mesajlardan kurulmuş, her kategoriden yeterince örnek içeren
  bir değerlendirme kümesi var; geliştirme ve test olarak ayrılmış.
- [ ] Saldırı mesajları ve onlara benzeyen masum mesajlar da kümede.
- [ ] Her sonuç türü (gönder, engelle, devret, yedek) için beklenen sonuç
  yazılı.
- [ ] Son sürüm test kümesinde bir kez ölçüldü ve günlüğe yazıldı.

**Güvenlik**

- [ ] Asistanın yalnızca işinin gerektirdiği araçları var; geri alınamaz
  işler bir insanın onayıyla.
- [ ] Sistem mesajında gizli bilgi yok.
- [ ] Çıktı denetimi tarihleri ve sayıları veriye dayandırıyor; vaat ve
  yapılamayan iş iddiası yakalanıyor; bağlantılar izin listesinden.
- [ ] Müşterinin verisi önbellekte başka birine verilmiyor.

**Dayanıklılık ve maliyet**

- [ ] Geçici hatalar sınırlı ve jitter'lı beklemeyle yeniden deneniyor;
  kalıcı hatalar denenmiyor.
- [ ] Toplam bekleme için süre sınırı ve yedek cevap var.
- [ ] `max_tokens` beklenen cevaba göre; mesaj başına token ölçüldü.
- [ ] Günlük bir harcama sınırı var.

**İşletme**

- [ ] Devredilen ve engellenen mesajlar kaydediliyor; bir insan bakıyor.
- [ ] Hata oranları izleniyor (geçici ve kalıcı ayrı).
- [ ] Prompt'un her sürümü saklanıyor; hangi sürümün ne zaman açıldığı
  biliniyor ve eskisine dönülebiliyor.
- [ ] Müşteri bir yapay zekâ asistanıyla konuştuğunu biliyor ve bir
  insana ulaşabiliyor.
