Bu dersin terminali bir benzetici: dosyaları ve komutları kendi içinde
taklit ediyor, gerçek program çalıştırmıyor. Gerçek bir terminale geçince
karşına çıkacak, burada denenemeyen şeyler.

## Süreçleri yönetmek

- `ps aux | grep python`: çalışan Python süreçlerini ve PID'lerini bulur.
- `kill 4321`: 4321 numaralı sürece "kapan" der. Kapanmazsa `kill -9 4321`
  zorla kapatır (kaydedilmemiş iş kaybolur).
- Ctrl+C önde çalışan komutu durdurur. Bir komut "takıldı" gibi görünüyorsa
  ilk denenecek şey budur.
- `python train.py &` uzun bir işi arka plana atar; `jobs` listeler, `fg`
  öne getirir. Terminal kapanınca da sürsün istiyorsan `nohup` ya da `tmux`.

## Paket yöneticileri

| Sistem | Komut |
|---|---|
| Ubuntu, Debian | `sudo apt update`, `sudo apt install ad` |
| Fedora | `sudo dnf install ad` |
| macOS | `brew install ad` |
| Windows | `winget install ad` |

Paket yöneticisi programı, bağımlılıklarıyla birlikte kurar ve PATH'e koyar.
Python paketleri ayrıca `pip` ile kurulur (Python patikasında anlatıldı).

## Yardım bulmak

- `man komut`: komutun kılavuzu. Ok tuşlarıyla gezilir, `/kelime` arar, `q`
  çıkar.
- `komut --help`: kısa özet; çoğu programda var.
- Bir hata mesajını olduğu gibi aramak çoğu zaman en hızlı yoldur.

## Uzak sunucular

`ssh kullanıcı@adres` başka bir bilgisayarda (bir bulut sunucusunda, bir
okul makinesinde) komut satırı açar. Bağlandıktan sonra bu patikadaki her şey
orada da aynı çalışır: `ls`, `cd`, `grep`, izinler, betikler. Makine öğrenmesi
modelleri çoğu zaman böyle, ekranı olmayan sunucularda eğitilir.

## Windows'ta gerçek Linux

- **Git Bash**: Git ile gelir; bu patikadaki komutların çoğu çalışır, ama
  izinler ve süreçler Windows'unkidir.
- **WSL**: Windows içinde gerçek bir Linux (Ubuntu gibi) çalıştırır. Linux
  sunucularında olacağın gibi çalışmak için en yakın yol.
