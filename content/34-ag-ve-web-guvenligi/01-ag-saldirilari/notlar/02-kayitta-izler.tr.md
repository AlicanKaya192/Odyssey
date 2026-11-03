Saldırıların çoğu kayıtlarda iz bırakır. Savunan taraf için önemli olan,
hangi izin neyi gösterdiğini bilmektir. Aşağıdaki eşikler örnektir; her
ağın "normali" farklıdır ve eşik o normale göre seçilir.

## Ne görürsen ne düşünürsün?

| Kayıttaki iz | Olası anlamı |
|---|---|
| Yönlendiricinin MAC adresi birden değişti | ARP sahteciliği |
| Dışarıdan gelen paketin kaynağı iç ağ adresi | Sahte kaynak adresi |
| Çok sayıda SYN, neredeyse hiç ACK yok | SYN seli |
| Tek kaynaktan kısa sürede çok sayıda farklı port | Port tarama |
| Tek kaynaktan çok sayıda giriş denemesi | Parola deneme saldırısı |
| Aynı isteğin aynı imzayla iki kez gelmesi | Yeniden oynatma |
| Hiç sorulmamış sorulara gelen büyük cevaplar | Yansıtma saldırısının kurbanı olmak |

## İz bulunca

- **Önce doğrula.** Yeni bir yönlendirici kurulduysa MAC'in değişmesi
  normaldir; bir yedekleme işi de çok sayıda bağlantı açabilir.
- **Kaydet ve sakla.** Zamanı, kaynağı, hedefi yaz; olay müdahalesinde
  (Olay Müdahalesi bölümü) bu kayıtlar gerekir.
- **Süz ya da sınırla.** Kaynağı geçici olarak engellemek ya da hızını
  düşürmek. Sahte adres kullanan bir saldırıda kaynağı engellemek masum
  bir adresi cezalandırabilir; dikkatli ol.
- **Kapat.** Taramada açık bulunan ama kullanılmayan servisi kapat.

## Yapılmayacaklar

- Saldırganın adresine "karşı saldırı" yapmak: adres sahte olabilir ve
  çoğu yerde yasa dışıdır.
- Yalnızca adres engelleyip içeriği şifrelememek: dinleme ve MitM yine
  mümkün.
- Tek bir eşiğe güvenmek: saldırgan eşiğin hemen altında kalabilir
  (yavaş tarama). Birden çok iz birlikte değerlendirilir.
