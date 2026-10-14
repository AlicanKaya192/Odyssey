| Terim | Anlamı |
|---|---|
| **Entegrasyon** (integration) | Herkesin değişikliğini ortak koda katmak, birleştirmek. |
| **Sürekli entegrasyon** (CI) | Sık ve küçük birleştirmek; her birleştirmede kodun temiz bir makinede kendiliğinden kurulup test edilmesi. |
| **Sürekli teslim** (continuous delivery) | Testi geçen her değişikliğin yayına hazır pakete dönüşmesi; yayını insan başlatır. |
| **Sürekli dağıtım** (continuous deployment) | Testi geçen her değişikliğin kendiliğinden kullanıcıya ulaşması. |
| **Hat** (pipeline) | Kodun yolculuğundaki aşamaların sıralı listesi: kur, denetle, test et, paketle, yayınla. |
| **Aşama** (stage) | Hattın bir adımı; düşerse hat orada durur. |
| **Hızlı düşmek** (fail fast) | Sorunu erken ve ucuz yerde yakalamak; hızlı aşamalar öne konur. |
| **Yeşil / kırmızı** (green / red build) | Hattın geçtiği / düştüğü çalıştırma. |
| **CI servisi** | Hattı çalıştıran hizmet; bu patikada GitHub Actions. |
| **İş akışı** (workflow) | Hattı tarif eden YAML dosyası, `.github/workflows/` içinde. |
| **Tetikleyici** (trigger) | İş akışını başlatan olay, örneğin `push`. |
| **İş** (job) | Aynı makinede çalışan adımlar grubu. |
| **Adım** (step) | Tek bir komut (`run:`) ya da hazır bir eylem (`uses:`). |
| **Eylem** (action) | Başkasının yazdığı hazır adım; `actions/checkout@v4` gibi, `@` sonrası sürümü. |
| **Çalıştırıcı** (runner) | İşi çalıştıran, her seferinde sıfırdan açılan temiz makine. |

İş akışının iskeleti üç soruya cevap verir:

- **Ne zaman?** `on:`
- **Nerede?** `jobs:` → `runs-on:`
- **Ne?** `steps:`
