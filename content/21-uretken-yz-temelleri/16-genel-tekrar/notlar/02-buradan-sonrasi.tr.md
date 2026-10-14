**Sıradaki modül:** Prompt Mühendisliği ve LLM Uygulamaları. Bu modülde
kurduğun istemci, token sayımı, RAG, doğrulama ve değerlendirme orada da
kullanılacak; odak, modelle konuşmanın kendisi: net talimat, örnekli
prompt, yapılı çıktı, araç çağırma, ajan döngüsü, bellek ve prompt
injection'a karşı savunma.

**Gerçek araçlara geçerken:**

- Bu modüldeki modeller NumPy ile, küçük veriyle ve tek bilgisayarda
  kuruldu; fikirleri göstermek için. Gerçek resim ve dil modelleri derin
  öğrenme kütüphaneleriyle, çok büyük veriyle ve güçlü donanımla eğitilir.
- Gerçek bir sohbet API'sine geçtiğinde bu modülün kalıpları aynen geçerli:
  mesaj listesi, bitiş nedeni, token sayımı (o modelin kendi
  parçalayıcısıyla), maliyet kaydı, doğrulama.
- Vektör aramada TF-IDF yerine bir gömme modeli ve büyük derlemlerde bir
  vektör veritabanı kullanılır; ölçme yöntemi (key@k, recall@k, MRR) aynı
  kalır.
- İnce ayar ve LoRA için hazır kütüphaneler var; ama unutmayı ve ödülü
  kandırmayı ölçmek yine senin işin.

**Pratik öneriler:**

1. Kendi belgelerinden 30–50 soruluk bir değerlendirme kümesi kur;
   cevabı belgelerde olmayan sorular da ekle.
2. Önce aramayı ölç, sonra cevabı.
3. Bir değişiklik yaptığında aynı kümeyle yeniden ölç; küçük farklara
   yeniden örneklemeyle bak.
4. Kişisel veriyi maskele, kullanıcıya bir modelle konuştuğunu söyle,
   kişiyi etkileyen kararlarda son sözü insana bırak.
