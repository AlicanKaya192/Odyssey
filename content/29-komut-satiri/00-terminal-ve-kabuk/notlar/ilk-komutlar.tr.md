Bu bölümün komutları, bir bakışta.

## Komutlar

| Komut | Ne yapar |
|---|---|
| `pwd` | Bulunduğun klasörün tam yolunu yazar. |
| `ls` | Bulunduğun klasördekileri listeler; klasörlerin sonunda `/`. |
| `ls -a` | Gizli dosyalarla birlikte listeler (`./`, `../`, `.bashrc`). |
| `ls notes` | `notes` klasörünün içini, oraya gitmeden listeler. |
| `echo Merhaba` | Metni ekrana yazar. |
| `echo "a    b"` | Tırnak içindeki boşlukları korur. |
| `history` | Bu oturumda yazdığın komutlar, numaralı. |
| `clear` | Ekranı temizler (kısayolu `Ctrl+L`). |

## Bir komut satırının düzeni

```text
ls  -a  notes
│   │   └── argüman: neyin üzerinde çalışacak
│   └────── seçenek: nasıl çalışacak (tireyle başlar)
└────────── komut: hangi program
```

## Tuşlar

| Tuş | Ne yapar |
|---|---|
| Yukarı ok | Önceki komutu getirir |
| `Ctrl+C` | Çalışan komutu durdurur |
| `Tab` | Adı tamamlar (Odyssey terminalinde yok) |

## Sık hatalar

| Gördüğün | Sebebi | Ne yaparsın |
|---|---|---|
| `bash: Ls: command not found` | Büyük harf ya da yazım hatası | `ls` diye küçük harfle yaz |
| `bash: ls-a: command not found` | Komutla seçenek arasında boşluk yok | `ls -a` |
| `ls: cannot access 'x': No such file or directory` | Öyle bir dosya ya da klasör yok | `ls` ile adına bak |
| Boşluklar kayboldu | Metin tırnaksız | `echo "metin"` |
