`less` gerçek bir Linux, macOS ya da Git Bash terminalinde uzun dosyaları
okumak için kullanılır. Odyssey'nin terminalinde yok; burada `head`, `tail`
ve `cat -n` var.

```text
$ less logs/server.log
```

## Tuşlar

| Tuş | Ne yapar |
|---|---|
| Boşluk ya da `Page Down` | Bir sayfa ileri |
| `b` ya da `Page Up` | Bir sayfa geri |
| Aşağı / yukarı ok | Bir satır |
| `g` | Dosyanın başına |
| `G` | Dosyanın sonuna |
| `/kelime` ve Enter | İleriye doğru ara |
| `n` / `N` | Sonraki / önceki eşleşme |
| `q` | Çık |

## Bilmekte yarar var

- `less` dosyayı değiştirmez; yalnızca okursun.
- `man ls` gibi kılavuz sayfaları da `less` içinde açılır; aynı tuşlar orada
  da geçerli.
- `less +F dosya`, `tail -f` gibi sonu izler; `Ctrl+C` ile normal görünüme
  dönülür.
- Takılırsan `q`. Ekranda `:` görüyorsan `less` hâlâ açıktır.
