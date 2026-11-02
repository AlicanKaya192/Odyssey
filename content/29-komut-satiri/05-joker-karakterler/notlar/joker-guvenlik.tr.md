Jokerler güçlüdür; `rm`, `mv` ve `cp` ile birleşince yanlış bir harf çok
dosyayı etkiler. Şu dört alışkanlık çoğu kazayı önler.

## 1. Önce echo

Asıl komutun başına `echo` koy ve çalıştır:

```bash
echo rm *.tmp
```

Ekranda çalışacak komutun tam hâlini görürsün. Doğruysa `echo`'yu sil ve
yeniden çalıştır (yukarı ok, satırın başı, sil).

## 2. Boşluklara dikkat

| Yazdığın | Anlamı |
|---|---|
| `rm *.tmp` | `.tmp` ile biten dosyalar |
| `rm * .tmp` | **Her şey** ve `.tmp` adlı dosya |
| `rm *tmp` | `tmp` ile biten her şey (`.tmp` de, `notes-tmp` da) |

## 3. Neredesin?

`*` bulunduğun klasöre göre açılır. `rm *.log` yazmadan önce `pwd`. Yolu
kalıba yazmak daha güvenlidir: `rm ~/project/logs/*.log`.

## 4. Kalıbı programa vermek gerekiyorsa tırnakla

`find` gibi komutlar kalıbı kendileri yorumlar. Tırnaksız yazarsan kabuk
önce açar ve programa başka bir şey gider:

```bash
find . -name "*.txt"
```

Bu bölümde gördüğün kural burada da geçerli: tırnak içinde joker açılmaz.
