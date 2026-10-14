| Terim | Anlamı |
|---|---|
| **Ajan** (agent) | Modelin her turda sonraki eylemi seçtiği, programın araçları çalıştırdığı döngü |
| **Tur** (step) | Bir model çağrısı ve ardından çalıştırılan araçlar |
| **Adım sınırı** | Döngünün en fazla kaç tur döneceği |
| **Token bütçesi** | Bir ajan çalışmasının harcayabileceği en fazla token |
| **İz** (trace) | Her turun aracı, argümanı, sonucu ve token'ı |
| **Tekrar yakalama** | Aynı argümanlarla aynı çağrının ikinci kez çalıştırılmaması |

**Akılda tut:**

- Derste soruyu çözen ajan üç turda 246, tekrar eden ajan beş turda 516
  giren token harcadı; tekrar eden ajanı adım sınırı durdurdu.
- Hatadan sonra düzelen ajan doğru araca geçti ama soruyu yarım
  cevapladı: döngünün düzgün bitmesi cevabın tam olduğu anlamına gelmez.
- Her tur geçmişi yeniden gönderir; turun giren token'ı her turda büyür.
- Adımlar sabitse zincir daha öngörülebilir ve ucuzdur.
