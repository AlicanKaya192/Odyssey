Okul not sisteminin giriş akışı için küçük bir tehdit modeli. Parçalar:
öğrenci (dış varlık), giriş isteği (veri akışı, güven sınırını geçiyor),
web uygulaması (süreç), kullanıcı tablosu ve kayıt dosyası (veri
depoları).

| Parça | Harf | Ne olabilir? | Cevap |
|---|---|---|---|
| Öğrenci | S | Başkasının parolasıyla giriş | MFA, deneme sınırı |
| Öğrenci | R | "Ben girmedim" demek | Giriş kaydı: zaman, kaynak, sonuç |
| Giriş isteği | T | Yolda parolanın değiştirilmesi | Yalnızca HTTPS |
| Giriş isteği | I | Yolda parolanın okunması | Yalnızca HTTPS |
| Giriş isteği | D | Çok sayıda istekle sayfanın kilitlenmesi | Kaynak başına hız sınırı |
| Web uygulaması | S | Uygulamanın kendini başka hizmet gibi tanıtması | Hizmetler arası kimlik doğrulama |
| Web uygulaması | T | Oturum verisinin değiştirilmesi | İmzalı oturum jetonu |
| Web uygulaması | I | Hata mesajında kullanıcının var olup olmadığını söylemek | Tek tip hata mesajı |
| Web uygulaması | E | Öğrencinin öğretmen sayfasını kullanması | Sunucuda rol denetimi |
| Kullanıcı tablosu | T | Parola özetlerinin değiştirilmesi | Uygulama kullanıcısına en az yetki |
| Kullanıcı tablosu | I | Tablonun sızması | Tuzlu ve yavaş özet |
| Kayıt dosyası | R | Kayıtların silinmesiyle izlerin yok edilmesi | Kayıtları başka bir sisteme kopyalamak |
| Kayıt dosyası | I | Kayıtlarda parola görünmesi | Parolayı asla kayda yazmamak |

## Bu tablodan çıkanlar

- Aynı önlem birkaç satırı kapatabilir (HTTPS hem T hem I).
- Bazı satırlar başka bölümlere bağlanır: parola saklama, yetkilendirme,
  hata mesajları. Tehdit modeli, yapılacak işlerin haritasıdır.
- Her satırın bir sahibi ve tarihi olursa tablo bir iş listesine dönüşür.
- Satırların bir kısmı puanlanıp kabul de edilebilir; önemli olan
  kararın yazılı olması.
