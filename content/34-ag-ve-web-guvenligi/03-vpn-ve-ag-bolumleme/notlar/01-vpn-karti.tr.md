## VPN bir bakışta

| Soru | Cevap |
|---|---|
| Ne kurar? | İki nokta arasında şifreli tünel |
| Nasıl? | İç paket şifrelenip dış pakete konur |
| Yolu izleyen ne görür? | Yalnızca dış paket: kaynak, VPN geçidi, boyut, zaman |
| Uzaktan erişim | Bir bilgisayar kurum ağına bağlanır |
| Siteden siteye | İki ağ birbirine bağlanır |
| Bölünmüş tünel | Yalnızca kurum trafiği tünelden geçer |

## Korur / korumaz

| Korur | Korumaz |
|---|---|
| Ortak Wi-Fi'de dinleme | Bilgisayardaki zararlı yazılım |
| Yerel ağda araya girme | Oltalama sayfasına girilen parola |
| İç sunucuları internete açmadan kullanma | Geçitten sonraki yol |
| | Ziyaret edilen sitenin açıkları |
| | Anonimlik (VPN sağlayıcısı görür) |

## Kurallar

- VPN'e bağlanan cihaz **iç ağın parçası** olur; cihaz ve kişi sıkı
  denetlenir (MFA, güncel cihaz).
- VPN'den gelen herkese iç ağın tamamı açılmaz; bölümleme yine geçerli.
- Yönetim portları (SSH, uzak masaüstü) internete değil, VPN'e ya da
  yönetim ağına açılır.
- VPN geçidinin kendisi internete açık bir sunucudur: güncel tutulur ve
  izlenir.

## Terimler

- **VPN geçidi** (gateway): tünelin kurum tarafındaki ucu.
- **Tünel**: dış paketlerin içinde şifreli iç paketlerin taşındığı yol.
- **Bölünmüş tünel** (split tunneling): yalnızca seçili trafiğin tünelden
  geçmesi; tersi **tam tünel** (full tunnel).
