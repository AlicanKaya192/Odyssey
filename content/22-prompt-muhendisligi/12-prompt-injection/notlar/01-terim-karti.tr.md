| Terim | Anlamı |
|---|---|
| **Prompt injection** | Verideki bir talimatla modelin davranışını değiştirme saldırısı |
| **Doğrudan saldırı** | Talimatı kullanıcının kendisinin yazması |
| **Dolaylı saldırı** | Talimatın belge, web sayfası ya da araç sonucu gibi bir verinin içinde gelmesi |
| **Girdi dedektörü** | Gelen metinde saldırı kalıbı arayan katman |
| **İz** (canary) | Sistem mesajına konan, başka hiçbir yerde geçmeyen kelime; cevapta görünürse sızıntı var |
| **Dışarı veri kaçırma** (exfiltration) | Verinin bir bağlantı ya da görsel adresiyle başka bir sunucuya gönderilmesi |
| **En az yetki** | Asistanın yalnızca işinin gerektirdiği araçlara sahip olması |

**Akılda tut:**

- Derste dedektörün kesinliği 0,8, duyarlılığı 0,57 çıktı: "1gnore",
  başka dildeki saldırı ve "yöneticiyim" iddiası kaçtı; masum bir mesaj
  yanlış alarm verdi.
- Çıktı denetimi sistem mesajı sızıntısını ve izin listesinde olmayan
  iki alan adına giden bağlantıyı yakaladı; biri görsel bağlantısıydı.
- Bu saldırının bilinen kesin bir çözümü yok; savunma katmanlıdır ve
  ölçülür.
