Bir kapının işe yaraması eşiğin doğru seçilmesine bağlı. Çok gevşek
eşik hiçbir şey yakalamaz; çok sıkı eşik ekibi kapıyı kapatmaya ya da
anlamsız iş yapmaya iter.

**Lint ve biçim: sıfır tolerans**

Bu kapılarda eşik genelde "hiç hata yok". Kural gerçekten yanlışsa kural
kapatılır (bir ayar dosyasında), hata görmezden gelinmez. Var olan büyük
bir projeye ilk kez eklenirken önce yalnızca yeni kodda uygulanabilir.

**Kapsam: makul ve düşmeyen**

- %70–90 arası sık görülür. %100 peşinde koşmak çoğu zaman anlamsız
  testlere yol açar.
- Asıl soru: önemli dallar (hata yolları, sınırlar, para hesabı) test
  ediliyor mu?
- Eşiği bugünkü değerin biraz altına koy ve zamanla yükselt; kapsamın
  düşmesine izin verme ("cırcır", ratchet).

**Kapı kapandığında ne yapılır**

1. Önce mesajı oku: hangi dosya, hangi satır, hangi kural.
2. Aynı komutu kendi bilgisayarında çalıştır, aynı sonucu gör.
3. Düzelt ve yeniden gönder. Kapıyı kapatmak ya da eşiği düşürmek son
   çare ve bilinçli bir karar olmalı.

**Sık yapılan hatalar**

| Hata | Sonuç |
|---|---|
| Hatta biçimlendiriciyi `--check` olmadan çalıştırmak | Dosyalar makinede düzelir ama depoya gitmez; kapı hiç kapanmaz. |
| Lint'i testlerden sonraya koymak | Bir yazım hatası için dakikalarca test beklenir. |
| `assert`'siz test yazıp kapsamı yükseltmek | Kapı geçer ama hiçbir şey denetlenmez. |
| Eşiği her kapanışta düşürmek | Kapı bir süre sonra hiçbir şey ifade etmez. |
