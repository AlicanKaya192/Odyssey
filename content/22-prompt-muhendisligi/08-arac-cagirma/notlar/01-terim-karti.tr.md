| Terim | Anlamı |
|---|---|
| **Araç** (tool) | Programın modele sunduğu fonksiyon: sipariş getirmek, tutar hesaplamak |
| **Araç şeması** | Modele giden kısım: aracın adı, açıklaması, argümanları |
| **Araç çağrısı** (tool call) | Modelin cevap yerine döndürdüğü istek: hangi araç, hangi argümanlar |
| **Araç sonucu** | Programın aracı çalıştırıp `tool` mesajıyla modele verdiği sonuç |
| **İzin listesi** (allow-list) | Programın çalıştırmayı kabul ettiği araçların listesi |
| **Onay** | Geri alınamaz bir işi çalıştırmadan önce müşterinin ya da çalışanın onayı |
| **Dayanak denetimi** | Son cevaptaki bilgilerin araç sonucuyla aynı olup olmadığına bakmak |

**Akılda tut:**

- Model aracı çalıştırmaz; çağrıyı program doğrular ve çalıştırır.
- Derste beş örnek çağrıdan biri sipariş bilgisi döndürdü; ikisi hata
  sonucu, bilinmeyen araç reddedildi, iptal onay bekledi.
- Bir soru araç kullanınca iki çağrı tuttu; ikinci çağrı soruyu, araç
  çağrısını ve sonucunu birlikte taşır.
- Araç sonucunda olmayan bir tarih yazan cevap dayanak denetiminde
  yakalandı.
