| Terim | Anlamı |
|---|---|
| **Difüzyon modeli** | Veriye adım adım gürültü eklemenin tersini öğrenen, saf gürültüden adım adım örnek üreten model |
| **İleri süreç** | Veriye her adımda biraz gürültü eklemek; model gerekmez |
| **Geri süreç** | Ağın gürültü tahminiyle her adımda biraz gürültü çıkarmak |
| **Gürültü takvimi** | Her adımın gürültü payı $\beta_t$; bölümde 0,0001'den 0,1'e doğrusal |
| $\bar\alpha_t$ | $\alpha_1 \cdots \alpha_t$ ($\alpha_t = 1 - \beta_t$); $t$ adım sonunda verinin kalan payı |
| **Tek adımda gürültü** | $x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \varepsilon$ |
| **Adım gömmesi** (time embedding) | Adım numarasının sinüs ve kosinüslerle ağa verilmesi |
| **Gürültü tahmini** $\hat\varepsilon$ | Ağın, noktaya eklenmiş gürültü için tahmini |
| **Kod uzayında difüzyon** (latent diffusion) | Difüzyonu bir VAE'nin küçük kod uzayında çalıştırmak |
| **Koşullu üretim** | Ağa bir etiket ya da metin gömmesi de verip üretimi yönlendirmek |

**Akılda tut:**

- Eğitim tek ağın sıradan bir ortalama kare hata regresyonu: hedef, eklenen
  gürültü.
- Geri adımda, son adım dışında taze gürültü eklenir; eklenmezse örnekler
  kümelerin ortasına toplanır ve çeşitlilik kaybolur.
- Bölümde GAN'ı bozan öğrenme oranında (0,01) bile üç tohumda sekiz küme
  bulundu. Bedeli: bir örnek için ağ 100 kez çalışır, GAN'da bir kez.
