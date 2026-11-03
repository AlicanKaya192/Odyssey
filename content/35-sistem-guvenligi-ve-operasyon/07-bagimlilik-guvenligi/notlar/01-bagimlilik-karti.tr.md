## Kavramlar

| Kavram | Anlamı |
|---|---|
| Doğrudan bağımlılık | Açıkça kurduğun paket |
| Dolaylı bağımlılık | Paketlerin kendi kullandığı paketler |
| SBOM | Kullanılan bütün paketlerin listesi |
| Sabitleme (pinning) | Sürümü tam yazmak: `paket==1.2.3` |
| Kilit dosyası | Sürüm + dosya özeti; tekrarlanabilir kurulum |
| Güvenlik duyurusu | Hangi sürümlerin etkilendiği, hangisinde düzeltildiği |
| Typosquatting | Popüler pakete benzeyen adla zararlı paket |
| Bağımlılık karışıklığı | İç paket adının açık depoda taklidi |

## requirements.txt yazımları

| Satır | Anlamı | Sabit mi? |
|---|---|---|
| `numpy==2.1.3` | Tam bu sürüm | Evet |
| `pandas>=2.0` | 2.0 ya da daha yenisi | Hayır |
| `flask~=3.0` | 3.x içinde en yenisi | Hayır |
| `flask` | Ne gelirse | Hayır |
| `# yorum` | Yok sayılır | — |

## Python kalıpları

- Paket adını ayırmak: `re.split(r"[<>=!~ ;\[]", line)[0]`.
- Sabit mi: `"==" in line`.
- Dolaylı bağımlılıklar: yığın + `seen` kümesi (döngüye karşı).
- Etkileniyor mu: `version(introduced) <= version(kurulu) < version(fixed)`.
- Benzer ad: `difflib.get_close_matches(ad, populer, n=1, cutoff=0.8)`.
- Dosya özeti: `hashlib.sha256(veri).hexdigest()`.

## Akılda tutulacak

- Paketin açığı senin açığındır; dolaylı olanlar dahil.
- Sabitlenmiş sürüm kendiliğinden güncellenmez; güncelleme düzenli bir
  iştir.
- Özetsiz sabitleme dosyanın değişmediğini kanıtlamaz.
- Her yeni bağımlılık bir insan tarafından gözden geçirilir.
