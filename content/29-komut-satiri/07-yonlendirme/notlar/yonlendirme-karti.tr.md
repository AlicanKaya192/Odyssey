Bütün yönlendirmeler, bir bakışta.

## Akışlar

| Numara | Adı | Normalde |
|---|---|---|
| 0 | stdin (standart girdi) | Klavye |
| 1 | stdout (standart çıktı) | Ekran |
| 2 | stderr (standart hata) | Ekran |

## Yazımlar

| Yazım | Ne yapar |
|---|---|
| `komut > f` | stdout'u f'ye yazar (f baştan yazılır) |
| `komut >> f` | stdout'u f'nin sonuna ekler |
| `komut 2> f` | stderr'i f'ye yazar |
| `komut 2>> f` | stderr'i f'nin sonuna ekler |
| `komut > f 2>&1` | İkisini de f'ye |
| `komut &> f` | Aynısı, kısa yazım (bash) |
| `komut > out.txt 2> err.txt` | Çıktı ve hata ayrı dosyalara |
| `komut > /dev/null` | Çıktıyı yok et |
| `komut 2> /dev/null` | Hataları yok et |
| `komut < f` | Girdiyi f'den oku |
| `komut < in.txt > out.txt` | Dosyadan oku, dosyaya yaz |
| `> f` | f'yi boşalt (ya da boş oluştur) |

## Hatırla

- Boşluk serbest: `> f` ile `>f` aynı. Ama `2>` ayrılmaz: `2 > f` yazarsan `2`
  komutun argümanı olur.
- `2>&1` yönlendirmelerin **sonuna**: `> f 2>&1`.
- Okuduğun dosyaya aynı komutta `>` ile yazma.
