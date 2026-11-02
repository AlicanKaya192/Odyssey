Çıkış kodları ve onlara göre karar vermenin bütün yolları.

## Sık görülen kodlar

| Kod | Anlamı |
|---|---|
| 0 | Başarılı |
| 1 | Genel hata; grep'te "bulunamadı" |
| 2 | Yanlış kullanım; ls ve grep'te "dosya yok" |
| 126 | Bulundu ama çalıştırılamadı (izin) |
| 127 | Komut bulunamadı |
| 130 | Ctrl+C ile durduruldu |

## Okumak ve kullanmak

| Yazım | Ne yapar |
|---|---|
| `echo $?` | Son komutun kodu |
| `code=$?` | Kodu saklar (hemen sonra) |
| `exit 3` | Betiği 3 koduyla bitirir |
| `true` / `false` | Her zaman 0 / her zaman 1 |

## Zincirler

| Yazım | b ne zaman çalışır |
|---|---|
| `a && b` | a başarılıysa |
| <code>a &#124;&#124; b</code> | a başarısızsa |
| `a ; b` | Her durumda |
| `! a && b` | a başarısızsa |
| <code>a &amp;&amp; b &#124;&#124; c</code> | b, a başarılıysa; c, a ya da b düşerse |

## Koşul olarak komut

```bash
if grep -q ERROR app.log; then
  echo "errors found"
fi
```

`if`, `while` ve `&&`, komutun çıktısına değil **koduna** bakar.

## Hatırla

- `$?` her komuttan sonra yeniden yazılır.
- Borunun kodu sondaki komutundur.
- `a && b || c` bir `if`/`else` gibi görünür ama değildir: b düşerse c de
  çalışır. Önemli kararlarda `if` yaz.
