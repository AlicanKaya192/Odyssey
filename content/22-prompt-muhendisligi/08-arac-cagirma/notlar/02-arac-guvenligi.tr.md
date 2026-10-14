Bir aracı modele açmadan önce şu tabloyu doldur:

| Soru | Örnek: `get_order` | Örnek: `cancel_order` |
|---|---|---|
| Ne yapıyor? | Siparişin durumunu okur | Siparişi iptal eder |
| Geri alınabilir mi? | Okuma, bir şey değiştirmez | Hayır |
| Onay gerekir mi? | Hayır | Evet: müşteri ya da çalışan |
| Argümanların kalıbı | `ORD-` + 5 rakam | `ORD-` + 5 rakam |
| Kimin verisine erişir? | Yalnızca sohbetteki müşterinin siparişi | Aynı |
| Hata nasıl döner? | `{"error": ...}` | `{"error": ...}` ya da `{"pending": ...}` |

**Program tarafında kurallar:**

1. Araçları bir izin listesinde tut; modelin verdiği adı başka bir yolla
   çalıştırma.
2. Argümanları kalıba göre doğrula; müşteri metni argümana taşınabilir.
3. Bir aracın erişebildiği veriyi sınırla: başka müşterinin siparişi
   gelmemeli (sohbetteki müşterinin kimliğini program bilir, model değil).
4. Geri alınamaz işlerde onay bekle; onayı model değil, kişi verir.
5. Hataları yapılı sonuç olarak modele geri ver; program çökmesin.
6. Her araç çağrısını argümanları ve sonucuyla kaydet.

**Sık hatalar:**

- **Modelin istediği her çağrıyı çalıştırmak.** Araç çağrısı bir istektir.
- **Açıklamayı özensiz yazmak.** Model hangi aracı seçeceğine çoğu zaman
  açıklamaya bakarak karar verir.
- **Aracın sonucunu cevapla karşılaştırmamak.** Model sonuçta olmayan bir
  bilgi yazabilir.
- **Bir araçla fazla iş yaptırmak.** "Herhangi bir SQL çalıştır" gibi
  genel araçlar saldırı yüzeyini büyütür; dar araçlar yaz.
