**Gerçek bir modele geçerken:**

- Bu modüldeki bütün kod gerçek bir sohbet API'siyle de çalışır;
  `ChatClient`'ın yerine o servisin istemcisi gelir. Mesaj listesi, bitiş
  nedeni, token kullanımı ve hata türleri her serviste benzer ama adları ve
  ayrıntıları farklıdır; servisin belgesine bakılır.
- Token'ları o modelin kendi parçalayıcısıyla say; bu modüldeki sayaç
  basitleştirilmiş.
- Araç çağırmanın biçimi servisten servise değişir; doğrulama, onay ve
  dayanak denetimi senin programında kalır.
- Fiyatlar ve sınırlar değişir; harcamayı kendi kaydından izle.

**Odyssey'de buradan nereye?**

- **Üretken Yapay Zekâ Temelleri:** RAG, halüsinasyon ölçümü, ince ayar ve
  LoRA; destek asistanının cevaplarını belgelere dayandırmak için.
- **NLP Temelleri** ve **Gömmeler ve Dil Modelleri:** metin
  sınıflandırma, gömmeler ve dikkat; oyuncak modelin yerine gerçek bir
  sınıflandırıcıyı ölçmek için.
- **FastAPI ile REST API Yazmak:** asistanı bir uç noktaya çevirmek; doğrulama,
  hata yönetimi ve testler.
- **Docker:** asistanı ve API'sini paketlemek.

**Pratik öneriler:**

1. Kendi işinden 50–100 mesajlık bir değerlendirme kümesi kur; saldırı
   mesajlarını ve onlara benzeyen masum mesajları da ekle.
2. Kümenin bir kısmını test olarak ayır ve ona yalnızca en sonda bak.
3. İlk sürümü basit tut; her değişikliği ölç, günlüğe yaz.
4. Asistana yalnızca gereken araçları ver; emin olunamayan her durumu bir
   insana devret.
5. Kullanıcıya bir yapay zekâ asistanıyla konuştuğunu söyle.
