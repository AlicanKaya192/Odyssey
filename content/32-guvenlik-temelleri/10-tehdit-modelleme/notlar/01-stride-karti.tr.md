## STRIDE

| Harf | İngilizce | Türkçe | Bozduğu | Tipik önlem |
|---|---|---|---|---|
| **S** | Spoofing | Kimlik taklidi | Kimlik doğruluğu | Güçlü kimlik doğrulama, MFA |
| **T** | Tampering | Kurcalama | Bütünlük | Yazma yetkisini sınırlamak, özet ve imza, TLS |
| **R** | Repudiation | İnkâr | İnkâr edilemezlik | Değiştirilemeyen kayıtlar, dijital imza |
| **I** | Information disclosure | Bilgi ifşası | Gizlilik | Erişim denetimi, şifreleme, az bilgi veren hata mesajı |
| **D** | Denial of service | Hizmet engelleme | Erişilebilirlik | Hız sınırı, yedeklilik, kaynak kotası |
| **E** | Elevation of privilege | Yetki yükseltme | Yetkilendirme | Sunucuda ve nesne düzeyinde denetim, en az yetki |

## Parça başına STRIDE

| Parça | Sorulacak harfler |
|---|---|
| Dış varlık (external entity) | S, R |
| Süreç (process) | S, T, R, I, D, E |
| Veri deposu (data store) | T, R (kayıt deposuysa), I, D |
| Veri akışı (data flow) | T, I, D |

## Veri akış şeması

- **Dış varlık:** denetiminde olmayan kişi ya da sistem.
- **Süreç:** veriyi işleyen kod.
- **Veri deposu:** verinin durduğu yer.
- **Veri akışı:** parçalar arasında giden veri.
- **Güven sınırı:** güven düzeyinin değiştiği çizgi; sınırı geçen her akış
  ayrıca incelenir.

## Dört soru

1. Ne üzerinde çalışıyoruz?
2. Ne ters gidebilir?
3. Bununla ilgili ne yapacağız?
4. İşi iyi yaptık mı?
