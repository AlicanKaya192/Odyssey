Bir belge soru-cevap sistemini yayına almadan önce:

**Veri ve arama**

- [ ] Belgeler güncel mi, kimin sorumluluğunda?
- [ ] Değerlendirme kümesi gerçek kullanıcı sorularından mı? Cevapsız
      sorular da var mı?
- [ ] Arama ölçüldü mü (recall@k, MRR)? Kaçan sorular okundu mu?

**Cevap**

- [ ] Sistem mesajı kuralları açık mı (yalnızca kaynaklardan, kaynak
      numarası, "bulamadım" cümlesi birebir)?
- [ ] Cevaplar doğrulanıyor mu (kaynak numarası, sayılar, adlar)?
- [ ] Doğrulanamayan cevap kullanıcıya gitmiyor mu?

**Güvenlik ve maliyet**

- [ ] Kişisel veri aramaya, modele ve kayda gitmeden maskeleniyor mu?
- [ ] Soru başına token ve maliyet kaydediliyor mu? Ölçekle çarpıldı mı?
- [ ] Kullanıcıya bir modelle konuştuğu ve hata olabileceği söyleniyor mu?
- [ ] "Bulamadım" durumunda kişi bir insana yönlendiriliyor mu?

**Değişiklikten sonra**

- [ ] Aynı değerlendirme kümesiyle yeniden ölçüldü mü?
- [ ] Küçük farklar için yeniden örnekleme aralığına bakıldı mı?

**Sık hatalar:**

- **Yalnızca doğru sayısına bakmak:** bölümde iki sistem 15'te eşitti; fark
  yanlış cevaplardaydı.
- **Doğrulamayı atlamak:** örnek okuyucu yanlış sayı yazmıyordu ama kayıtlı
  yanlış yanıt bunu sınadı; gerçek model yazabilir.
- **Kayıtta kişisel veri:** maskeleme kayıttan önce yapılmalı.
