Asistanın her adımı, nereden geldiği ve ne yakaladığı:

| Adım | Bölüm | Ne yapar? | Durdurursa sonuç |
|---|---|---|---|
| Girdi süzgeci | Prompt Injection ve Savunma | Bilinen saldırı kalıplarını arar | `blocked` |
| Sınıflandırma | Bir Promptun Anatomisi, Yapılı Çıktı ve Doğrulama | Tek kelimelik kategori ister, katı ayrıştırır, bir kez onarır | `handover` |
| İnsana giden kategori | Sistem Mesajı, Rol ve Ton | Garanti gibi incelemesi gereken işleri ayırır | `handover` |
| Sipariş verisi | Araç Çağırma | Mesajdaki sipariş numarasıyla veriyi bulur | — |
| Cevap | Sistem Mesajı, Prompt Şablonları | Kurallı sistem mesajı + veri + müşteri mesajı | — |
| Çıktı denetimi | Araç Çağırma, Prompt Injection ve Savunma | Tarih dayanağı, vaat, yapılamayan iş iddiası | `handover` |
| Yeniden deneme | Hatalar, Yeniden Deneme ve Maliyet | Geçici hatada yeniden dener, token ve hata sayar | `fallback` |
| Ölçüm | Promptları Değerlendirmek, Promptu Sistemli İyileştirmek | Senaryo kümesi, beklenen sonuç, tek değişiklik | — |

**Akılda tut:**

- Onarımsız sürüm 10 senaryonun 9'unda beklenen sonucu verdi; tek hata
  cümleyle cevaplanan kategori yüzünden gereksiz devirdi.
- Bir kez onarım 10/10 yaptı; bedeli 143 giren + 16 çıkan token.
- "Yöneticiyim" saldırısını girdi süzgeci kaçırdı, çıktı denetimi "iptal
  ettim" iddiasını yakaladı.
- Asistanın iptal ya da iade aracı yok: en az yetki.
