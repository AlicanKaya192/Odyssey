## Saldırı, katman, savunma

| Saldırı | Katman | Neyi bozar? | Savunma |
|---|---|---|---|
| Dinleme | Her katman | Gizlilik | Şifreleme (TLS) |
| Ortadaki adam | Her katman | Gizlilik, bütünlük | Şifreleme + sertifika denetimi |
| ARP sahteciliği | Bağlantı | Gizlilik, bütünlük | Anahtarda denetim, tespit, TLS |
| Sahte kaynak adresi | Ağ | Kimlik doğruluğu | Giriş ve çıkış süzmesi |
| SYN seli | Taşıma | Erişilebilirlik | SYN çerezi, zaman aşımı, hız sınırı |
| DDoS | Hepsi | Erişilebilirlik | Kapasite, yukarı akış süzmesi |
| Port tarama | Taşıma | (Keşif) | Kapalı port, kayıttan tespit |
| Yeniden oynatma | Uygulama | Bütünlük | Nonce, zaman damgası |

## Terimler

- **Dinleme** (sniffing): yoldaki trafiği okumak.
- **Ortadaki adam** (MitM): iki tarafın arasına girip mesajları okumak,
  değiştirmek.
- **ARP**: IP adresinin MAC adresini soran yerel ağ protokolü; cevabı
  doğrulamaz.
- **Yansıtma / büyütme**: kurbanın adresiyle soru sorup cevapları ona
  yağdırmak; cevap sorudan büyükse büyütme.
- **Botnet**: sahibinin haberi olmadan ele geçirilmiş cihazlardan oluşan
  ağ.
- **SYN çerezi**: sunucunun ACK gelene kadar yer ayırmaması.
- **Nonce**: yalnızca bir kez kullanılan değer.

## Kurallar

- **IP adresi kimlik kanıtı değildir.** Yetkiyi adrese değil kimlik
  doğrulamaya bağla.
- Şifreleme içeriği saklar, **başlıkları saklamaz**.
- Tarayıcının sertifika uyarısı **geçilmez**.
- Hız sınırı **kaynak başına** tutulur.
