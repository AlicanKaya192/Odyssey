Bir `ls -l` satırı, soldan sağa.

```text
drwxr-xr-x 2 ada ada 4096 Oct  7 10:00 src/
-rw-r--r-- 1 ada ada  292 Oct  7 10:00 report.txt
```

| Sütun | Örnek | Anlamı |
|---|---|---|
| 1. harf | `d` / `-` | Klasör / sıradan dosya |
| 2–10. harfler | `rwxr-xr-x` | İzinler: sahip, grup, diğerleri (üçer harf) |
| Sayı | `2` / `1` | Bağlantı sayısı (klasörde alt klasörlerle artar) |
| Ad | `ada` | Sahip |
| Ad | `ada` | Grup |
| Sayı | `4096` / `292` | Boyut (bayt); `-h` ile `4.0K` |
| Tarih | `Oct  7 10:00` | Son değişiklik; eski dosyalarda saat yerine yıl |
| Ad | `src/` | Adı; bu terminal ve Git Bash klasöre `/` ekler |

## Sık sorulan

- **Klasör neden 4096?** Klasör kaydının disk bloğu. İçindekilerin toplamı
  için başka bir komut (`du -sh klasör`) kullanılır.
- **Boyut 0 olan dosya?** Boş dosya, çoğu zaman `touch` ile açılmış.
- **İki kez `ada` neden?** Biri kullanıcı, biri grup. Linux'ta her
  kullanıcının kendi adıyla bir grubu olur.
- **`total` nedir?** Diskteki toplam blok; dosya sayısı değil.
- **Satır sonundaki `*`?** Çalıştırılabilir dosya (İzinler bölümü).
