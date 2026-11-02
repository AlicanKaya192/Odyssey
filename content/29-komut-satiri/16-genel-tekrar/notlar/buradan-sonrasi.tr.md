Bu patika komut satırının günlük kullanımını kapsadı. Daha ileri gitmek
istersen bakılacak konular.

## İlk iş: gerçek bir terminal

- Windows'ta Git Bash'i aç ya da WSL ile Ubuntu kur; macOS ve Linux'ta Terminal
  zaten var.
- Bu patikadaki alıştırmaları orada, kendi dosyalarınla tekrar et.
- Bir hafta boyunca dosya işlerini (taşıma, arama, sayma) bilerek terminalde
  yap.

## İleri araçlar

| Araç | Ne işe yarar |
|---|---|
| `awk` | Sütunlu metinde hesap: `awk '{s += $3} END {print s}'` |
| `sed` | Metinde bul ve değiştir: `sed 's/eski/yeni/g'` |
| `xargs` | Bir listedeki her öğe için komut: <code>find . -name '*.tmp' &#124; xargs rm</code> |
| `case` | Betikte çok seçenekli karar |
| `read` | Betikte kullanıcıdan girdi almak |
| `tee` | Çıktıyı hem ekrana hem dosyaya |
| `tmux` | Bir terminalde birden çok pencere; bağlantı koparsa iş sürer |
| `ssh`, `scp` | Uzak sunucuda çalışmak, dosya göndermek |
| `cron` | Komutu belirli saatlerde kendiliğinden çalıştırmak |
| `set -euo pipefail` | Betikleri hatada durdurmak |

## Odyssey'de buradan nereye

- **Git ile Sürüm Kontrolü**: komut satırında en çok kullanılan araç.
- **Docker**: komutlar, Dockerfile içindeki `RUN` satırları ve konteynerin
  kabuğu bu patikanın üzerine kurulu.
- **Sistem Tasarımı (CI/CD)**: GitHub Actions adımları birer kabuk komutu;
  çıkış kodları geçti/kaldı kararını verir.
- **Büyük Veri** ve **MLOps**: uzun işler sunucularda, terminalden çalıştırılır.

## Kaynaklar

- `man komut`: her komutun tam kılavuzu, her zaman elinin altında.
- **The Linux Command Line** (William Shotts): ücretsiz okunabilen, baştan sona
  bir kitap.
- **ShellCheck**: betiklerdeki tırnak ve sınama hatalarını yakalayan bir araç;
  düzenleyicilere eklenti olarak da kurulur.
