Bir Linux bilgisayarının kökünde gördüğün klasörler ve ne işe yaradıkları.
Hepsini ezberlemen gerekmiyor; nerede ne aranacağını bilmek yeter.

| Klasör | İçinde ne var | Sen ne yaparsın |
|---|---|---|
| `/` | Kök; her şeyin başı | Bakarsın |
| `/home` | Kullanıcıların ev klasörleri | Kendi klasöründe çalışırsın |
| `/home/ada` (`~`) | Senin dosyaların, ayarların | Her şeyi |
| `/etc` | Sistemin ayar dosyaları (`hostname`, `passwd`) | Okursun; değiştirmek yönetici işi |
| `/tmp` | Geçici dosyalar | Deneme dosyası koyabilirsin; kalıcı değil |
| `/usr` | Kurulu programlar ve kütüphaneler | Bakarsın |
| `/bin`, `/usr/bin` | Komutların kendisi (`ls`, `cat`, `grep`) | Çalıştırırsın |
| `/var` | Değişen veriler; `/var/log` altında kayıtlar | Kayıtları okursun |
| `/root` | Yöneticinin (root) ev klasörü | Giremezsin |

## Windows'ta karşılıkları

| Linux | Windows'ta benzeri |
|---|---|
| `/home/ada` | `C:\Users\ada` |
| `/usr/bin` | `C:\Program Files` |
| `/etc` | Kayıt defteri ve `C:\Windows` altındaki ayarlar |
| `/tmp` | `C:\Users\ada\AppData\Local\Temp` |

## Git Bash'te

Git Bash'in `/` klasörü Git'in kurulduğu klasördür (`C:\Program Files\Git`);
Windows disklerin `/c`, `/d` diye görünür. Ev klasörün `/c/Users/adın`.
