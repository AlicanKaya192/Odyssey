## Bitler

| Harf | İzin | Değer | Klasörde |
|---|---|---|---|
| `r` | Okuma | 4 | İçindekileri listelemek |
| `w` | Yazma | 2 | İçinde dosya açmak, silmek |
| `x` | Çalıştırma | 1 | İçine girmek |

Sınıflar: sahip (`u`), grup (`g`), diğerleri (`o`). Sekizlik izinde ilk
rakam sahibin, ikincisi grubun, üçüncüsü diğerlerinin.

## Sık izinler

| Sekizlik | Ondalık | Dize | Kullanım |
|---|---|---|---|
| `755` | 493 | `rwxr-xr-x` | Program, ortak klasör |
| `750` | 488 | `rwxr-x---` | Grubun kullanacağı program |
| `644` | 420 | `rw-r--r--` | Sıradan dosya |
| `640` | 416 | `rw-r-----` | Grubun okuyacağı dosya |
| `600` | 384 | `rw-------` | Anahtar, parola dosyası |
| `700` | 448 | `rwx------` | Özel klasör |

## Komut satırında

| Komut | Ne yapar? |
|---|---|
| `ls -l dosya` | İzin dizesini, sahibi ve grubu gösterir |
| `chmod 600 dosya` | İzni sekizlikle ayarlar |
| `chmod o-w dosya` | Diğerlerinden yazma iznini kaldırır |
| `chown ada:staff dosya` | Sahibi ve grubu değiştirir |
| `umask` | Geçerli maskeyi gösterir |

## Python kalıpları

- Sınıfın bitleri: sahip `(mode >> 6) & 7`, grup `(mode >> 3) & 7`,
  diğerleri `mode & 7`.
- Herkes yazabiliyor mu: `mode & 0o002`.
- Sahipten başkası bir şey yapabiliyor mu: `mode & 0o077`.
- Umask uygulamak: `base & ~umask`.
- Sekizlik metin: `oct(0o644)` → `'0o644'`; geri çevirmek `int("644", 8)`.

## Akılda tutulacak

- Tek sınıf seçilir: sahip, sahip bitlerine bakar; `077` izinli dosyayı
  sahibi okuyamaz.
- Umask yalnızca kaldırır.
- `777` ve herkesin okuyabildiği anahtar dosyası, denetimde ilk aranan
  iki hatadır.
