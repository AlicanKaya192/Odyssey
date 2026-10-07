Windows'ta Git ile gelen terminal Git Bash. Linux terminalinin bir benzeri;
Windows'un kendi terminallerinden (Komut İstemi, PowerShell) birkaç yerde
farklı davranıyor.

## Yollar

Git Bash Windows yollarını Linux biçiminde yazar:

| Windows | Git Bash |
|---|---|
| `C:\Users\Ada` | `/c/Users/Ada` |
| `D:\Projeler\site` | `/d/Projeler/site` |
| Ev klasörün | `~` (= `/c/Users/Ada`) |

- Ayraç `\` değil `/`.
- Sürücü harfi başta, küçük harfle: `/c/`, `/d/`.
- Boşluklu yolları tırnakla yaz: `cd "/c/Users/Ada/My Projects"`.

## Bir klasörde Git Bash açmak

Dosya Gezgini'nde klasöre sağ tıkla → **Open Git Bash here** (Windows 11'de
önce **Daha fazla seçenek göster**). Terminal doğrudan o klasörde açılır,
`cd` yazmana gerek kalmaz.

Tersine, terminaldeyken bulunduğun klasörü açmak için:

```bash
explorer .     # Dosya Gezgini'nde aç
code .         # VS Code'da aç (VS Code kuruluysa)
```

`.` "bulunduğum klasör" demek.

## Kopyalamak ve yapıştırmak

Git Bash'te `Ctrl+C` kopyalamaz; **çalışan komutu durdurur**. Bunun yerine:

- Fareyle seçtiğin metin kendiliğinden kopyalanır.
- **Shift+Insert** yapıştırır; sağ tık menüsünde de **Paste** var.

## Faydalı tuşlar

| Tuş | Ne yapar |
|---|---|
| ↑ / ↓ | Önceki / sonraki komut |
| Tab | Dosya ya da klasör adını tamamlar |
| Ctrl+C | Çalışan komutu durdurur |
| Ctrl+L | Ekranı temizler (`clear`) |
| `q` | `git log` gibi uzun çıktılarda sayfalayıcıdan çıkar |

Son satır önemli: `git log` uzun olunca çıktı bir **sayfalayıcıda** açılır
ve alt satırda `:` ya da `(END)` görürsün. Ok tuşları ve boşlukla gezinir,
**`q`** ile çıkarsın. Takılıp kaldığını sananların çoğu buradadır.
